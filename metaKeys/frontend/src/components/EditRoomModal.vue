<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h3>Modifica Camera</h3>
      <form @submit.prevent="submitForm" class="edit-room-form">
        <div class="form-group">
          <label for="name">Nome</label>
          <input
            id="name"
            v-model="localRoom.name"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label>Porte</label>
          <div class="doors-selection">
            <div v-for="door in doors" :key="door.id" class="form-check">
              <input
                type="checkbox"
                :id="'door-' + door.id"
                :value="door.id"
                v-model="localRoom.doors"
                class="form-check-input"
              />
              <label :for="'door-' + door.id" class="form-check-label">{{ door.name }}</label>
            </div>
          </div>
        </div>
        <div v-if="errorMessage" class="error-card">{{ errorMessage }}</div>
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
  name: "EditRoomModal",
  props: {
    room: {
      type: Object,
      required: true,
    },
    apartment: {
      type: Object,
      required: true,
    },
    doors: {
      type: Array,
      required: true,
    },
  },
  setup(props, { emit }) {
    const store = useStore();
    const localRoom = ref({ ...props.room, apartment: props.apartment?.id });
    const originalRoom = ref({ ...props.room, apartment: props.apartment?.id });
    const errorMessage = ref("");

    const submitForm = async () => {
      if (
        JSON.stringify(localRoom.value) === JSON.stringify(originalRoom.value)
      ) {
        errorMessage.value = "Nessuna modifica apportata.";
        showTemporaryMessage("errorMessage");
        return;
      }
      errorMessage.value = "";
      try {
        await store.dispatch('updateRoom', localRoom.value);
        emit("roomUpdated");
        closeModal();
      } catch (error) {
        errorMessage.value = "Errore nella modifica della camera.";
        showTemporaryMessage("errorMessage");
        console.error("Errore nella modifica della camera:", error);
      }
    };

    const deleteRoom = async () => {
      try {
        await store.dispatch('deleteRoom', localRoom.value.id);
        emit("roomDeleted");
        closeModal();
      } catch (error) {
        errorMessage.value = "Errore nella cancellazione della camera.";
        showTemporaryMessage("errorMessage");
        console.error("Errore nella cancellazione della camera:", error);
      }
    };

    const confirmDelete = async () => {
      if (confirm("Sei sicuro di voler cancellare questa camera?")) {
        try {
          await deleteRoom();
        } catch (error) {
          console.error("Errore nella cancellazione della camera:", error);
        }
      }
    };

    const closeModal = () => {
      emit("closeEM");
    };

    const showTemporaryMessage = (field) => {
      setTimeout(() => {
        if (field === "errorMessage") {
          errorMessage.value = "";
        }
      }, 3000);
    };

    watch(
      () => props.room,
      (newVal) => {
        localRoom.value = { ...newVal, apartment: props.apartment?.id };
        originalRoom.value = { ...newVal, apartment: props.apartment?.id };
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
      localRoom,
      originalRoom,
      errorMessage,
      submitForm,
      deleteRoom,
      closeModal,
      showTemporaryMessage,
      confirmDelete,
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
.edit-room-form {
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

.doors-selection {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.form-check {
  margin-bottom: 10px;
}
</style>
