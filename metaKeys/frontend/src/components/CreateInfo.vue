<template>
  <div>
    <button class="close-button" @click="$emit('close')">&times;</button>
    <h2>Crea Informazione</h2>
    <form @submit.prevent="createInfo">
      <div class="form-group">
        <label for="title">Titolo</label>
        <input type="text" v-model="form.title" :maxlength="maxTitleChars" @input="updateTitleCharCount" required />
        <p class="char-counter">{{ remainingTitleChars }} caratteri rimanenti</p>
      </div>
      <div class="form-group">
        <label for="type">Tipo</label>
        <select v-model="form.type" required @change="handleTypeChange">
          <option value="general">Generale</option>
          <option value="parking_info">Informazioni Parcheggio</option>
          <option value="restaurants">Ristoranti</option>
          <option value="nearby">Nei Paraggi</option>
          <option value="places_to_visit">Cosa Visitare</option>
          <option value="apartment_info">Informazioni Appartamento</option>
          <option value="room_info">Informazioni Camera</option>
        </select>
      </div>
      <div class="form-group">
        <label for="apartment">Struttura</label>
        <select v-model="form.apartment" required @change="fetchRooms">
          <option v-for="apartment in apartments" :key="apartment.id" :value="apartment.id">
            {{ apartment.name }}
          </option>
        </select>
      </div>
      <div class="form-group" v-if="form.type === 'room_info'">
        <label for="room">Camera</label>
        <select v-model="form.room" :disabled="!form.apartment" required>
          <option v-for="room in rooms" :key="room.id" :value="room.id">
            {{ room.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="info">Informazione</label>
        <textarea v-model="form.info" :maxlength="maxInfoChars" @input="updateInfoCharCount" required></textarea>
        <p class="char-counter">{{ remainingInfoChars }} caratteri rimanenti</p>
      </div>
      <div class="form-group" v-if="form.type !== 'general' && form.type !== 'apartment_info' && form.type !== 'room_info'">
        <label for="google_link">Link Google</label>
        <input type="url" v-model="form.google_link" />
        <small class="form-text text-muted">Copia e incolla il link della posizione di Google Maps.</small>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
      <button type="submit" class="btn btn-primary">Crea</button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';

export default {
  name: "CreateInfo",
  setup(_, { emit }) {
    const store = useStore();
    const form = ref({
      title: "",
      type: "general",
      info: "",
      google_link: "",
      apartment: null,
      room: null,
    });

    const maxTitleChars = 255;
    const maxInfoChars = 5000;
    const remainingTitleChars = ref(maxTitleChars);
    const remainingInfoChars = ref(maxInfoChars);
    const errorMessage = ref("");

    const updateTitleCharCount = () => {
      remainingTitleChars.value = maxTitleChars - form.value.title.length;
    };

    const updateInfoCharCount = () => {
      remainingInfoChars.value = maxInfoChars - form.value.info.length;
    };

    const apartments = computed(() => store.state.apartments.apartments);
    const rooms = computed(() => store.state.apartments.rooms[form.value.apartment] || []);

    const fetchRooms = async () => {
      if (form.value.apartment && !store.state.apartments.fetchedRooms[form.value.apartment]) {
        try {
          await store.dispatch('fetchRooms', form.value.apartment);
        } catch (error) {
          console.error("Errore nel recupero delle camere:", error);
        }
      }
    };

    onMounted(() => {
      store.dispatch('fetchApartments');
    });

    const handleTypeChange = () => {
      if (form.value.type !== 'room_info') {
        form.value.room = null;
      }
    };

    const validateGoogleLink = (link) => {
      return link.startsWith("https://maps.app.goo.gl/");
    };

    const createInfo = async () => {
      if (form.value.google_link && !validateGoogleLink(form.value.google_link)) {
        errorMessage.value = "Il link deve essere un link di Google Maps'.";
        return;
      }
      try {
        await store.dispatch('createInfo', form.value);
        emit("close");
      } catch (error) {
        if (error.response && error.response.data) {
          errorMessage.value = error.response.data[0];
        } else {
          console.error("Errore nella creazione dell'informazione:", error);
        }
      }
    };

    return {
      form,
      maxTitleChars,
      maxInfoChars,
      remainingTitleChars,
      remainingInfoChars,
      errorMessage,
      updateTitleCharCount,
      updateInfoCharCount,
      apartments,
      rooms,
      handleTypeChange,
      fetchRooms,
      createInfo,
    };
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-weight: bold;
}

input,
textarea,
select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.char-counter {
  text-align: right;
  font-size: 12px;
  color: #6c757d;
}

.error-message {
  color: red;
  font-size: 12px;
}

.btn-primary {
  background-color: #28a745;
  color: white;
}

.btn-primary:hover {
  background-color: #218838;
}

.modal-create-info {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  padding: 20px;
  overflow-y: auto;
  z-index: 1000;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  background-color: transparent;
  color: #000;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
</style>
