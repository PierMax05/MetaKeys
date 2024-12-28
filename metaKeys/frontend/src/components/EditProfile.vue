<template>
  <div>
    <!-- Form per modificare il profilo -->
    <form @submit.prevent="submitEdit" class="register-guest-form">
      <div class="form-group">
        <label for="name">Nome:</label>
        <input
          type="text"
          v-model="localProfile.name"
          id="name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="surname">Cognome:</label>
        <input
          type="text"
          v-model="localProfile.surname"
          id="surname"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="apartment">Struttura:</label>
        <select v-model="localProfile.apartment" id="apartment" class="form-control" required @change="fetchRooms">
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
        <select v-model="localProfile.room" id="room" class="form-control" required>
          <option
            v-for="room in rooms"
            :key="room.id"
            :value="room.id"
          >
            {{ room.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="check_in_date">Data Check-In:</label>
        <input
          type="date"
          v-model="localProfile.check_in_date"
          id="check_in_date"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check_in_time">Ora Check-In:</label>
        <input
          type="time"
          v-model="localProfile.check_in_time"
          id="check_in_time"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check_out_date">Data Check-Out:</label>
        <input
          type="date"
          v-model="localProfile.check_out_date"
          id="check_out_date"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="check_out_time">Ora Check-Out:</label>
        <input
          type="time"
          v-model="localProfile.check_out_time"
          id="check_out_time"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="guest_number">Numero Ospiti:</label>
        <input
          type="number"
          v-model="localProfile.guest_number"
          id="guest_number"
          class="form-control"
          required
        />
      </div>
      <div class="form-switch" v-if="localProfile.username">
        <input
          type="checkbox"
          id="require_registration_form"
          v-model="localProfile.require_registration_form"
          class="form-check-input"
        />
        <label class="form-check-label" for="require_registration_form">
          Richiedi Form Registrazione
        </label>
      </div>
      <div class="form-switch" v-if="localProfile.username">
        <input
          type="checkbox"
          id="require_document_photo"
          v-model="localProfile.require_document_photo"
          class="form-check-input"
        />
        <label class="form-check-label" for="require_document_photo">
          Richiedi Foto Documenti
        </label>
      </div>
      <div class="form-switch" v-if="localProfile.username">
        <input
          type="checkbox"
          id="require_billing_info"
          v-model="localProfile.require_billing_info"
          class="form-check-input"
        />
        <label class="form-check-label" for="require_billing_info">
          Richiedi Informazioni Fatturazione
        </label>
      </div>
      <div class="button-group mt-3">
        <div>
          <button type="button" @click="cancelEdit" class="btn btn-secondary">
            Annulla
          </button>
        </div>
        <div>
          <button
            type="button"
            @click="confirmDeleteProfile"
            class="btn btn-danger me-3"
          >
            Cancella
          </button>
          <button type="submit" class="btn btn-primary submit-button">
            Salva
          </button>
        </div>
      </div>
    </form>
    <div v-if="message" class="message">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { ref, watch, defineComponent, onMounted } from 'vue';
import { useStore } from 'vuex';
import ApiService from "../common/api.service"; // Importa ApiService

export default defineComponent({
  props: {
    profile: Object,
  },
  setup(props, { emit }) {
    const store = useStore();
    const localProfile = ref({ ...props.profile });
    const message = ref("");
    const rooms = ref([]);

    watch(() => props.profile, (newProfile) => {
      localProfile.value = { ...newProfile };
    });

    const close = () => {
      emit("close");
    };

    const submitEdit = async () => {
      try {
        await ApiService.patch(
          `/api/register/checkin/${localProfile.value.id}/`,
          localProfile.value
        );
        emit("close");
        emit("submit-edit", localProfile.value);
        emit("success", "Modifiche salvate con successo!");
      } catch (error) {
        console.error("Errore durante l'invio delle modifiche:", error);
        alert("Errore durante l'invio delle modifiche.");
      }
    };

    const confirmDeleteProfile = () => {
      if (
        confirm(
          "Sei sicuro di voler cancellare questo profilo? Tutti i dati sugli ospiti verranno cancellati."
        )
      ) {
        deleteProfile();
      }
    };

    const deleteProfile = async () => {
      try {
        await ApiService.delete(
          `/api/register/checkin/${localProfile.value.id}/`
        );
        emit("close");
        emit("delete-profile", localProfile.value.id);
        emit("success", "Profilo cancellato con successo!");
      } catch (error) {
        console.error("Errore durante la cancellazione del profilo:", error);
        alert("Errore durante la cancellazione del profilo.");
      }
    };

    const cancelEdit = () => {
      emit("close");
    };

    const fetchRooms = async () => {
      if (localProfile.value.apartment) {
        await store.dispatch('fetchRooms', localProfile.value.apartment);
        rooms.value = store.getters.getRoomsByApartment(localProfile.value.apartment);
      } else {
        rooms.value = [];
      }
    };

    watch(() => localProfile.value.apartment, (newApartmentId) => {
      fetchRooms();
    });

    onMounted(() => {
      store.dispatch('fetchApartments');
      fetchRooms();
    });

    return {
      localProfile,
      message,
      close,
      submitEdit,
      confirmDeleteProfile,
      deleteProfile,
      cancelEdit,
      rooms,
      apartments: store.state.apartments.apartments,
      fetchRooms,
    };
  },
});
</script>

<style scoped>
.register-guest-form {
  padding: 5%;
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
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.form-switch {
  justify-content: space-between;
  display: flex;
  align-items: center;
  gap: 10px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  justify-content: space-between;
}

.btn {
  font-size: 16px;
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

.btn-danger {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .register-guest-form {
    padding: 15px;
  }

  .form-control {
    font-size: 14px;
  }

  .btn {
    font-size: 14px;
  }
}
</style>
