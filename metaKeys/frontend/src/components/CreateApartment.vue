<template>
  <div>
    <h3>Crea Alloggio</h3>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Nome</label>
        <input
          id="name"
          v-model="apartment.name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="address">Indirizzo</label>
        <input
          id="address"
          v-model="apartment.address"
          class="form-control"
          required
        />
      </div>
      <div class="shelly-form">
        <h5>Shelly</h5>
        <div class="form-switch">
          <label for="shelly">Usa dispositivi Shelly</label>
          <input
            type="checkbox"
            id="shelly"
            v-model="apartment.shelly"
            class="form-check-input"
            @change="handleShellyChange"
          />
        </div>
        <div v-if="apartment.shelly">
          <div class="form-group">
            <label for="server_uri">URI del Server</label>
            <input
              id="server_uri"
              v-model="apartment.server_uri"
              @input="validateUrl"
              class="form-control"
              required
            />
            <div v-if="urlError" class="text-danger">{{ urlError }}</div>
          </div>
          <div class="form-group">
            <label for="auth_key">Chiave di Autenticazione</label>
            <input
              id="auth_key"
              v-model="apartment.auth_key"
              class="form-control"
              required
            />
            <div class="form-text text-muted">
              La chiave di autenticazione è un codice segreto che il server utilizza
              per verificare la tua identità.
            </div>
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary mt-4">Crea</button>
    </form>
  </div>
</template>

<script>
import { ref, getCurrentInstance } from 'vue';
import { useStore } from 'vuex';
import ApiService from "../common/api.service.js";

export default {
  name: "CreateApartment",
  setup() {
    const store = useStore();
    const apartment = ref({
      name: "",
      server_uri: "",
      auth_key: "",
      address: "",
      shelly: false,
    });
    const urlError = ref(null);
    const { emit } = getCurrentInstance();

    const validateUrl = () => {
      const pattern =
        /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
      urlError.value = pattern.test(apartment.value.server_uri)
        ? null
        : "URL non valido";
    };

    const handleShellyChange = () => {
      if (!apartment.value.shelly) {
        apartment.value.server_uri = "";
        apartment.value.auth_key = "";
      }
    };

    const submitForm = async () => {
      try {
        const response = await ApiService.post("/api/apartments/", apartment.value);
        apartment.value.name = "";
        apartment.value.server_uri = "";
        apartment.value.auth_key = "";
        apartment.value.address = "";
        apartment.value.shelly = false;
        emit("apartment-created", response.data); // Emissione evento per aggiornare la lista degli appartamenti
        emit("close"); // Emissione evento per chiudere il modal
      } catch (error) {
        console.error(error);
      }
    };

    return {
      apartment,
      urlError,
      validateUrl,
      handleShellyChange,
      submitForm,
    };
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 15px;
}

.text-danger {
  color: red;
}
.shelly-form {
  padding: 5%;
  border: 1px solid #ccc;
}
.form-switch {
  display: flex;
  justify-content: space-between;
  padding-left: 0px;
}

</style>
