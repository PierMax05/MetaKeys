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
      <div class="shelly-form">
        <h5>Shelly</h5>
        <p>Completa il form seguente se utilizzi dei dispositivi shelly per controllare le porte</p>
        <div class="form-group">
          <label for="server_uri">URI del Server</label>
          <input
            id="server_uri"
            v-model="localApartment.server_uri"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="auth_key">Chiave di Autenticazione</label>
          <input
            id="auth_key"
            v-model="localApartment.auth_key"
            class="form-control"
          />
        </div>
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
    const localApartment = ref({ ...apartment.value });

    const submitForm = async () => {
      try {
        await store.dispatch('updateApartment', localApartment.value);
        emit("update-apartment", localApartment.value);
        emit("close");
      } catch (error) {
        console.error(error);
      }
    };

    const deleteApartment = async () => {
      try {
        await store.dispatch('deleteApartment', localApartment.value.id);
        emit("delete-apartment", localApartment.value.id);
        emit("close");
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
      },
      { deep: true }
    );

    return {
      localApartment,
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
</style>
