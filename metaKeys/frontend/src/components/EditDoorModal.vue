<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h3>Modifica Porta</h3>
      <form @submit.prevent="submitForm" class="edit-door-form">
        <div class="form-group">
          <label for="name">Nome</label>
          <input
            id="name"
            v-model="localDoor.name"
            class="form-control"
            required
            maxlength="40"
          />
          <small class="form-text text-muted">
            Il nome della porta deve essere al massimo di 40 caratteri.
          </small>
        </div>
        <div class="form-group">
          <label for="access_type">Tipo di Accesso</label>
          <select id="access_type" v-model="localDoor.access_type" class="form-control" required>
            <option value="shelly">Shelly</option>
            <option value="codice">Codice</option>
            <option value="solo istruzioni">Solo Istruzioni</option>
          </select>
        </div>
        <div class="form-group" v-if="localDoor.access_type === 'shelly'">
          <label for="id_device">ID Dispositivo</label>
          <input
            id="id_device"
            v-model="localDoor.id_device"
            class="form-control"
            required
          />
          <small class="form-text text-muted">
            Inserisci l'ID del dispositivo Shelly.
          </small>
        </div>
        <div class="form-group" v-if="localDoor.access_type === 'shelly'">
          <label for="CPC">CPC</label>
          <input
            id="CPC"
            v-model="localDoor.check_position_code"
            class="form-control"
            required
          />
          <small class="form-text text-muted">
            Il CPC è un codice che serve per far in modo che l'ospite non possa aprire la porta se non si trova davanti ad essa. Il CPC va affisso vicino alla porta.
          </small>
        </div>
        <div class="form-group" v-if="localDoor.access_type === 'shelly'">
          <label for="channel_device">Canale Dispositivo</label>
          <input
            id="channel_device"
            type="number"
            v-model.number="localDoor.channel_device"
            class="form-control"
            required
          />
          <small class="form-text text-muted">
            Inserisci il canale del dispositivo Shelly.
          </small>
        </div>
        <div class="form-group" v-if="localDoor.access_type === 'codice'">
          <label for="access_code">Codice di Accesso</label>
          <input
            id="access_code"
            v-model="localDoor.access_code"
            class="form-control"
            maxlength="20"
            required
          />
          <small class="form-text text-muted">
            Inserisci il codice per il tastierino o per la cassettina delle chiavi che verrà mostrato all'ospite.
          </small>
        </div>
        <div class="form-group">
          <label for="priority">Priorità</label>
          <input
            id="priority"
            type="number"
            v-model.number="localDoor.priority"
            class="form-control"
            required
          />
          <small class="form-text text-muted">
            La priorità serve a ordinare le porte in base a quelle che l'ospite incontrerà prima. Più basso è il numero, prima verrà mostrata la porta. Porte appartenenti alla stessa camera che hanno lo stesso numero vengono disposte in modo casuale.
          </small>
        </div>
        <div class="form-group">
          <label for="description">Descrizione</label>
          <textarea
            id="description"
            v-model="localDoor.description"
            class="form-control"
            rows="3"
            maxlength="200"
            @input="checkMaxLength('description', 200)"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="instructions">Istruzioni</label>
          <textarea
            id="instructions"
            v-model="localDoor.instructions"
            class="form-control"
            rows="5"
            maxlength="5000"
            @input="checkMaxLength('instructions', 5000)"
          ></textarea>
        </div>
        <div v-if="errorMessage" class="error-card">{{ errorMessage }}</div>
        <div v-if="maxLengthMessage" class="error-card">
          {{ maxLengthMessage }}
        </div>
        <div class="button-group">
          <button type="button" class="btn btn-secondary" @click="closeModal">
            Annulla
          </button>
          <div class="right-buttons">
            <button type="button" class="btn btn-danger" @click="confirmDelete">
              Cancella
            </button>
            <button type="submit" class="btn btn-success">Salva</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch, defineComponent, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: "EditDoorModal",
  props: {
    door: {
      type: Object,
      required: true,
    },
    apartmentId: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const store = useStore();
    const localDoor = ref({ ...props.door, apartment: props.apartmentId, channel_device: props.door.channel_device || 0 });
    const originalDoor = ref({ ...props.door, apartment: props.apartmentId, channel_device: props.door.channel_device || 0 });
    const errorMessage = ref("");
    const maxLengthMessage = ref("");

    const submitForm = async () => {
      if (
        JSON.stringify(localDoor.value) === JSON.stringify(originalDoor.value)
      ) {
        errorMessage.value = "Nessuna modifica apportata.";
        showTemporaryMessage("errorMessage");
        return;
      }
      errorMessage.value = "";
      try {
        await store.dispatch('updateDoor', localDoor.value);
        emit("doorUpdated");
        closeModal();
      } catch (error) {
        errorMessage.value = "Errore nella modifica della porta.";
        showTemporaryMessage("errorMessage");
        console.error("Errore nella modifica della porta:", error);
      }
    };

    const confirmDelete = async () => {
      if (confirm("Sei sicuro di voler cancellare questa porta?")) {
        try {
          await deleteDoor();
        } catch (error) {
          console.error("Errore nella cancellazione della porta:", error);
        }
      }
    };

    const deleteDoor = async () => {
      try {
        await store.dispatch('deleteDoor', localDoor.value.id);
        emit("doorDeleted");
        closeModal();
      } catch (error) {
        errorMessage.value = "Errore nella cancellazione della porta.";
        showTemporaryMessage("errorMessage");
        console.error("Errore nella cancellazione della porta:", error);
      }
    };

    const closeModal = () => {
      emit("closeEM");
    };

    const checkMaxLength = (field, maxLength) => {
      if (localDoor.value[field].length >= maxLength) {
        maxLengthMessage.value = `Hai raggiunto il limite massimo di ${maxLength} caratteri.`;
        showTemporaryMessage("maxLengthMessage");
      }
    };

    const showTemporaryMessage = (field) => {
      setTimeout(() => {
        if (field === "errorMessage") {
          errorMessage.value = "";
        } else if (field === "maxLengthMessage") {
          maxLengthMessage.value = "";
        }
      }, 3000);
    };

    watch(
      () => props.door,
      (newVal) => {
        localDoor.value = { ...newVal, apartment: props.apartmentId };
        originalDoor.value = { ...newVal, apartment: props.apartmentId };
      },
      { deep: true }
    );

    onMounted(() => {
      document.body.style.overflow = 'hidden';
    });

    onUnmounted(() => {
      document.body.style.overflow = '';
    });

    return {
      localDoor,
      originalDoor,
      errorMessage,
      maxLengthMessage,
      submitForm,
      deleteDoor,
      confirmDelete,
      closeModal,
      checkMaxLength,
      showTemporaryMessage,
    };
  },
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow-y: auto;
}

.modal-content {
  background-color: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .modal-content {
    width: 100%;
    height: 100%;
  }

  .form-control {
    font-size: 14px;
  }

  .btn {
    font-size: 14px;
  }
}
.edit-door-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex-grow: 1;
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

.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.right-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

.btn-success {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
}

.btn-danger {
  background-color: #dc3545;
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

.btn-success:hover {
  background-color: #218838;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.error-card {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
