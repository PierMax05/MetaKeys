<template>
  <div class="create-room-modal">
    <h2>Crea Camera</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Nome</label>
        <input
          id="name"
          v-model="room.name"
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
              v-model="room.doors"
              class="form-check-input"
            />
            <label :for="'door-' + door.id" class="form-check-label">{{ door.name }}</label>
          </div>
        </div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="closeModal">Chiudi</button>
        <div class="action-buttons">
          <button type="submit" class="btn btn-primary">Crea</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, defineComponent } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: "CreateRoomComponent",
  props: {
    apartmentId: {
      type: Number,
      required: true,
    },
    doors: {
      type: Array,
      required: true,
    },
  },
  setup(props, { emit }) {
    const store = useStore();
    const room = ref({
      name: '',
      apartment: props.apartmentId,
      doors: [],
    });

    const submitForm = async () => {
      try {
        await store.dispatch('createRoom', room.value);
        emit('roomCreated');
        closeModal();
      } catch (error) {
        console.error(error);
      }
    };

    const closeModal = () => {
      emit("closeCM");
    };

    return {
      room,
      submitForm,
      closeModal,
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

.create-room-modal {
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

.form-check {
  margin-bottom: 10px;
}

.doors-selection {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}
</style>
