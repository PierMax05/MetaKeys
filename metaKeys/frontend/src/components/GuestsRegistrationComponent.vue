<template>
  <div class="register-guest-container">
    <form @submit.prevent="registerCheckInProfile" class="register-guest-form">
      <div class="form-group">
        <label for="name">Nome:</label>
        <input type="text" v-model="form.name" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="surname">Cognome:</label>
        <input
          type="text"
          v-model="form.surname"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="source">Fonte:</label>
        <input
          type="text"
          v-model="form.source"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="guest_number">Numero Ospiti:</label>
        <input
          type="number"
          v-model="form.guest_number"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check-in-date">Data del check-in:</label>
        <input
          type="date"
          v-model="form.check_in_date"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check-out-date">Data del check-out:</label>
        <input
          type="date"
          v-model="form.check_out_date"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check-in-time">Ora del check-in:</label>
        <input
          type="time"
          v-model="form.check_in_time"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check-out-time">Ora del check-out:</label>
        <input
          type="time"
          v-model="form.check_out_time"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <div class="password-input-group">
          <input
            type="text"
            v-model="form.password"
            class="form-control"
            required
          />
          <button
            type="button"
            @click="generatePassword"
            class="btn btn-secondary"
          >
            Genera
          </button>
        </div>
      </div>
      <div class="form-group">
        <label for="apartment">Struttura:</label>
        <select v-model="form.apartment" class="form-control" required @change="fetchRooms">
          <option value="" disabled selected>Seleziona una struttura</option>
          <option
            v-for="apartment in apartments"
            :key="apartment.id"
            :value="apartment.id"
          >
            {{ apartment.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="room">Camera:</label>
        <select v-model="form.room" class="form-control" required>
          <option value="" disabled selected>Seleziona una camera</option>
          <option
            v-for="room in rooms"
            :key="room.id"
            :value="room.id"
          >
            {{ room.name }}
          </option>
        </select>
      </div>
      <div class="form-switch">
        <input
          type="checkbox"
          id="require_registration_form"
          v-model="form.require_registration_form"
          class="form-check-input"
        />
        <label class="form-check-label" for="require_registration_form">
          Richiedi Form Registrazione
        </label>
      </div>
      <div class="form-switch">
        <input
          type="checkbox"
          id="require_document_photo"
          v-model="form.require_document_photo"
          class="form-check-input"
        />
        <label class="form-check-label" for="require_document_photo">
          Richiedi Foto Documenti
        </label>
      </div>
      <div class="form-switch">
        <input
          type="checkbox"
          id="require_billing_info"
          v-model="form.require_billing_info"
          class="form-check-input"
        />
        <label class="form-check-label" for="require_billing_info">
          Richiedi Informazioni Fatturazione
        </label>
      </div>
      <div class="button-group">
        <button type="submit" class="btn btn-primary submit-button">
          Registra
        </button>
        <button
          type="button"
          @click="cancelRegistration"
          class="btn btn-secondary"
        >
          Annulla
        </button>
      </div>
    </form>
    <div v-if="message" class="message">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { ref, defineComponent, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import ApiService from '../common/api.service';

export default defineComponent({
  name: "GuestsRegistrationComponent",
  setup(_, { emit }) {
    const store = useStore();
    const form = ref({
      name: "",
      surname: "",
      source: "",
      guest_number: "",
      check_in_date: "",
      check_out_date: "",
      check_in_time: "",
      check_out_time: "",
      password: "",
      apartment: "",
      room: "",
      require_registration_form: false,
      require_document_photo: false,
      require_billing_info: false,
    });

    const apartments = ref([]);
    const rooms = ref([]);
    const message = ref("");

    const registerCheckInProfile = async () => {
      try {
        const response = await ApiService.post("/api/register/checkin/", form.value);
        emit("submit-registration", response.data);
        emit("close");
        emit("success", "Check-in registrato con successo!");
        resetForm();
      } catch (error) {
        console.error("Errore nella registrazione del check-in:", error);
        alert("Errore nella registrazione del check-in.");
      }
    };

    const resetForm = () => {
      form.value = {
        name: "",
        surname: "",
        source: "",
        guest_number: "",
        check_in_date: "",
        check_out_date: "",
        check_in_time: "",
        check_out_time: "",
        password: "",
        apartment: "",
        room: "",
        require_registration_form: true,
        require_document_photo: true,
        require_billing_info: true,
      };
    };

    const generatePassword = () => {
      const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789";
      let password = "";
      for (let i = 0; i < 8; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      form.value.password = password;
    };

    const cancelRegistration = () => {
      emit("close");
    };

    const fetchRooms = async () => {
      if (form.value.apartment) {
        await store.dispatch('fetchRooms', form.value.apartment);
        rooms.value = store.getters.getRoomsByApartment(form.value.apartment);
        const selectedApartment = store.state.apartments.apartments.find(a => a.id === form.value.apartment);
        if (selectedApartment) {
          form.value.require_registration_form = selectedApartment.get_guest_info;
          form.value.require_document_photo = selectedApartment.get_document_photo;
          form.value.require_billing_info = selectedApartment.get_billing_info;
        }
      } else {
        rooms.value = [];
      }
    };

    watch(() => form.value.apartment, (newApartmentId) => {
      fetchRooms();
    });

    onMounted(() => {
      store.dispatch('fetchApartments');
    });

    return {
      form,
      apartments: store.state.apartments.apartments,
      rooms,
      message,
      registerCheckInProfile,
      generatePassword,
      cancelRegistration,
      fetchRooms,
    };
  },
});
</script>

<style scoped>
.register-guest-container {
  padding: 5%;
  max-width: 100%;
  margin: 0 auto;
}

.register-guest-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.register-guest-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-control {
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.password-input-group {
  display: flex;
  gap: 10px;
}

.password-input-group .form-control {
  flex: 1;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  cursor: pointer;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .form-control {
    font-size: 14px;
  }
}

.form-switch {
  display: flex;
  justify-content: space-between; /* Distribuisce lo spazio tra gli elementi figli */
  gap: 10px; /* Aggiunge un margine tra gli elementi */
}
</style>
