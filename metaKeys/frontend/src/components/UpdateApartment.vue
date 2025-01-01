<template>
  <div class="update-apartment-modal">
    <h2>Aggiorna Struttura</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Nome</label>
        <input
          id="name"
          v-model="localApartment.name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="address">Indirizzo</label>
        <input
          id="address"
          v-model="localApartment.address"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="google_maps_link">Link Google Maps</label>
        <input
          id="google_maps_link"
          v-model="localApartment.google_maps_link"
          @input="validateGoogleLink"
          class="form-control"
        />
        <div class="form-text text-muted">
          Cerca la posizione su Google Maps e copia il link qui.
        </div>
        <div v-if="googleLinkError" class="text-danger">{{ googleLinkError }}</div>
      </div>
      <div class="shelly-form">
        <h5>Shelly</h5>
        <div class="form-switch">
          <label for="shelly">Usa dispositivi Shelly</label>
          <input
            type="checkbox"
            id="shelly"
            v-model="localApartment.shelly"
            class="form-check-input"
            @change="handleShellyChange"
          />
        </div>
        <div v-if="localApartment.shelly">
          <div class="form-group">
            <label for="server_uri">URI del Server</label>
            <input
              id="server_uri"
              v-model="localApartment.server_uri"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label for="auth_key">Chiave di Autenticazione</label>
            <input
              id="auth_key"
              v-model="localApartment.auth_key"
              class="form-control"
              required
            />
          </div>
        </div>
      </div>
      <p class="text-muted">
        Seleziona le informazioni che desideri richiedere all'ospite. Sarà possibile
        modificarle durante la creazione di un soggiorno.
      </p>
      <div class="form-switch">
        <label for="get_guest_info">informazioni ospite</label>
        <input
          type="checkbox"
          id="get_guest_info"
          v-model="localApartment.get_guest_info"
          class="form-check-input"
        />
      </div>
      <div class="form-switch">
        <label for="get_document_photo">foto documento</label>
        <input
          type="checkbox"
          id="get_document_photo"
          v-model="localApartment.get_document_photo"
          class="form-check-input"
        />
      </div>
      <div class="form-switch">
        <label for="get_billing_info">informazioni di fatturazione</label>
        <input
          type="checkbox"
          id="get_billing_info"
          v-model="localApartment.get_billing_info"
          class="form-check-input"
        />
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="$emit('close')">Chiudi</button>
        <div class="action-buttons">
          <button type="submit" class="btn btn-primary">Aggiorna</button>
          <button type="button" class="btn btn-danger" @click="confirmDelete">Cancella</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, watch, defineComponent, toRefs, computed } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: "UpdateApartment",
  props: {
    apartmentId: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const store = useStore();
    const apartment = computed(() => store.state.apartments.apartments.find(a => a.id === props.apartmentId));
    const localApartment = ref({...apartment.value});
    const originalApartment = ref({...apartment.value});
    const googleLinkError = ref(null);

    const handleShellyChange = () => {
      if (!localApartment.value.shelly) {
        localApartment.value.server_uri = "";
        localApartment.value.auth_key = "";
      }
    };

    const validateGoogleLink = () => {
      const pattern = /^https:\/\/maps\.app\.goo\.gl\//;
      googleLinkError.value = pattern.test(localApartment.value.google_maps_link)
        ? null
        : "Il link deve essere un link di Google Maps.";
    };

    const submitForm = async () => {
      if (JSON.stringify(localApartment.value) === JSON.stringify(originalApartment.value)) {
        emit("close");
        emit("no-changes");
        return;
      }
      try {
        const response = await store.dispatch('updateApartment', localApartment.value);
        if (response && response.data) {
          emit("update-apartment", response.data);
        }
      } catch (error) {
        console.error(error);
      }
      emit("close");
    };

    const deleteApartment = async () => {
      try {
        emit("delete-apartment", localApartment.value.id);
      } catch (error) {
        console.error(error);
      }
    };

    const confirmDelete = () => {
      if (confirm("Sei sicuro di voler cancellare questo appartamento?")) {
        deleteApartment();
      }
    };

    watch(
      apartment,
      (newVal) => {
        localApartment.value = { ...newVal };
        originalApartment.value = { ...newVal };
      },
      { deep: true }
    );

    return {
      localApartment,
      googleLinkError,
      handleShellyChange,
      validateGoogleLink,
      submitForm,
      confirmDelete,
    };
  },
});
</script>

<style scoped>
.btn {
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.update-apartment-modal {
  position: relative;
  padding: 20px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.shelly-form {
  padding: 5%;
  border: 1px solid #ccc;
  margin-top: 20px;
}
.form-switch {
  display: flex;
  justify-content: space-between;
  padding-left: 0px;
}
</style>
