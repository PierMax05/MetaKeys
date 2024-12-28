<template>
  <div class="create-door-modal">
    <h2>Crea Porta</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Nome</label>
        <input
          id="name"
          v-model="door.name"
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
        <select id="access_type" v-model="door.access_type" class="form-control" required>
          <option value="shelly">Shelly</option>
          <option value="codice">Codice</option>
          <option value="solo istruzioni">Solo Istruzioni</option>
        </select>
      </div>
      <div class="form-group" v-if="door.access_type === 'shelly'">
        <label for="id_device">ID Dispositivo</label>
        <input
          id="id_device"
          v-model="door.id_device"
          class="form-control"
          required
        />
        <small class="form-text text-muted">
          Inserisci l'ID del dispositivo Shelly.
        </small>
      </div>
      <div class="form-group" v-if="door.access_type === 'shelly'">
        <label for="CPC">CPC</label>
        <input
          id="CPC"
          v-model="door.check_position_code"
          class="form-control"
          required
        />
        <small class="form-text text-muted">
          Il CPC è un codice che serve per far in modo che l'ospite non possa aprire la porta se non si trova davanti ad essa. Il CPC va affisso vicino alla porta.
        </small>
      </div>
      <div class="form-group" v-if="door.access_type === 'shelly'">
        <label for="channel_device">Canale Dispositivo</label>
        <input
          id="channel_device"
          type="number"
          v-model.number="door.channel_device"
          class="form-control"
          required
        />
        <small class="form-text text-muted">
          Inserisci il canale del dispositivo Shelly.
        </small>
      </div>
      <div class="form-group" v-if="door.access_type === 'codice'">
        <label for="access_code">Codice di Accesso</label>
        <input
          id="access_code"
          v-model="door.access_code"
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
          v-model.number="door.priority"
          class="form-control"
          required
        />
        <small class="form-text text-muted">
          La priorità serve a ordinare le porte in base a quelle che l'ospite incontrerà prima. Più basso è il numero, prima verrà mostrata la porta. Porte appartenenti alla stessa stanza che hanno lo stesso numero vengono disposte in modo casuale.
        </small>
      </div>
      <div class="form-group">
        <label for="description">Descrizione</label>
        <textarea
          id="description"
          v-model="door.description"
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
          v-model="door.instructions"
          class="form-control"
          rows="5"
          maxlength="5000"
          @input="checkMaxLength('instructions', 5000)"
        ></textarea>
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
  name: "CreateDoorComponent",
  props: {
    apartmentId: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const store = useStore();
    const door = ref({
      name: "",
      id_device: "",
      check_position_code: "",
      access_code: "",
      priority: null,
      apartment: props.apartmentId,
      description: "",
      instructions: "",
      access_type: "solo istruzioni",
      rooms: [],
      channel_device: 0,
    });
    const errorMessage = ref("");
    const maxLengthMessage = ref("");

    const submitForm = async () => {
      errorMessage.value = "";
      try {
        await store.dispatch('createDoor', door.value);
        emit("doorCreated");
        closeModal();
      } catch (error) {
        errorMessage.value = "Errore nella creazione della porta.";
        showTemporaryMessage("errorMessage");
        console.error("Errore nella creazione della porta:", error);
      }
    };

    const checkMaxLength = (field, maxLength) => {
      if (door.value[field].length >= maxLength) {
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

    const closeModal = () => {
      emit("closeCM");
    };

    return {
      door,
      errorMessage,
      maxLengthMessage,
      submitForm,
      checkMaxLength,
      showTemporaryMessage,
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

.create-door-modal {
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
</style>
