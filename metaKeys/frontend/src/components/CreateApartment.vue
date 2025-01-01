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
      <div class="form-group">
        <label for="google_maps_link">Link Google Maps</label>
        <input
          id="google_maps_link"
          v-model="apartment.google_maps_link"
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
      <p class="text-muted">
        Seleziona le informazioni che desideri richiedere all'ospite. Sarà possibile
        modificarle durante la creazione di un soggiorno.
      </p>
      <div class="form-switch">
        <label for="get_guest_info">Richiedi informazioni ospite</label>
        <input
          type="checkbox"
          id="get_guest_info"
          v-model="apartment.get_guest_info"
          class="form-check-input"
        />
      </div>
      <div class="form-switch">
        <label for="get_document_photo">Richiedi foto documento</label>
        <input
          type="checkbox"
          id="get_document_photo"
          v-model="apartment.get_document_photo"
          class="form-check-input"
        />
      </div>
      <div class="form-switch">
        <label for="get_billing_info">Richiedi informazioni di fatturazione</label>
        <input
          type="checkbox"
          id="get_billing_info"
          v-model="apartment.get_billing_info"
          class="form-check-input"
        />
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
      google_maps_link: "",
      get_guest_info: false,
      get_document_photo: false,
      get_billing_info: false,
    });
    const urlError = ref(null);
    const googleLinkError = ref(null);
    const { emit } = getCurrentInstance();

    const validateUrl = () => {
      const pattern =
        /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
      urlError.value = pattern.test(apartment.value.server_uri)
        ? null
        : "URL non valido";
    };

    const validateGoogleLink = () => {
      const pattern = /^https:\/\/maps\.app\.goo\.gl\//;
      googleLinkError.value = pattern.test(apartment.value.google_maps_link)
        ? null
        : "Il link deve essere un link di Google Maps.";
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
        apartment.value.google_maps_link = "";
        apartment.value.get_guest_info = false;
        apartment.value.get_document_photo = false;
        apartment.value.get_billing_info = false;
        emit("apartment-created", response.data); // Emissione evento per aggiornare la lista degli appartamenti
        emit("close"); // Emissione evento per chiudere il modal
      } catch (error) {
        console.error(error);
      }
    };

    return {
      apartment,
      urlError,
      googleLinkError,
      validateUrl,
      validateGoogleLink,
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
