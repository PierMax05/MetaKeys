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
        <p>Completa il form seguente se utilizzi dei dispositivi shelly per controllare le porte</p>
        <div class="form-group">
          <label for="server_uri">URI del Server</label>
          <input
            id="server_uri"
            v-model="apartment.server_uri"
            @input="validateUrl"
            class="form-control"
          />
          <div v-if="urlError" class="text-danger">{{ urlError }}</div>
        </div>
        <div class="form-group">
          <label for="auth_key">Chiave di Autenticazione</label>
          <input
            id="auth_key"
            v-model="apartment.auth_key"
            class="form-control"
          />
          <div class="form-text text-muted">
            La chiave di autenticazione è un codice segreto che il server utilizza
            per verificare la tua identità.
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary mt-4">Crea</button>
    </form>
  </div>
</template>

<script>
import { ref, getCurrentInstance } from 'vue';
import ApiService from "../common/api.service.js";

export default {
  name: "CreateApartment",
  setup() {
    const apartment = ref({
      name: "",
      server_uri: "",
      auth_key: "",
      address: "",
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

    const submitForm = async () => {
      try {
        const response = await ApiService.post("/api/apartments/", apartment.value);
        apartment.value.name = "";
        apartment.value.server_uri = "";
        apartment.value.auth_key = "";
        apartment.value.address = "";
        emit("close"); // Emissione evento per chiudere il modal
        emit("apartment-created", response.data); // Emissione evento per aggiornare la lista degli appartamenti
      } catch (error) {
        console.error(error);
      }
    };

    return {
      apartment,
      urlError,
      validateUrl,
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
  margin-top: 20px;
  padding: 5%;
  border: 1px solid #ccc;
}
</style>
