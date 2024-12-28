<template>
  <transition name="slide-up">
    <div v-if="visible" class="billing-info-form">
      <form @submit.prevent="submitForm">
        <!-- Campo per il tipo di persona -->
        <div :class="['form-group', { 'has-error': errors.person_type }]">
          <label for="person_type">Tipo di Persona</label>
          <select v-model="form.person_type" class="form-control">
            <option value="individual">Persona Fisica</option>
            <option value="company">Azienda</option>
          </select>
          <small v-if="errors.person_type" class="form-text text-danger">
            {{ errors.person_type }}
          </small>
        </div>
        <!-- Campi per persona fisica -->
        <div
          v-if="form.person_type === 'individual'"
          :class="['form-group', { 'has-error': errors.first_name }]"
        >
          <label for="first_name">Nome</label>
          <input type="text" v-model="form.first_name" class="form-control" />
          <small v-if="errors.first_name" class="form-text text-danger">
            {{ errors.first_name }}
          </small>
        </div>
        <div
          v-if="form.person_type === 'individual'"
          :class="['form-group', { 'has-error': errors.last_name }]"
        >
          <label for="last_name">Cognome</label>
          <input type="text" v-model="form.last_name" class="form-control" />
          <small v-if="errors.last_name" class="form-text text-danger">
            {{ errors.last_name }}
          </small>
        </div>
        <!-- Campi per azienda -->
        <div
          v-if="form.person_type === 'company'"
          :class="['form-group', { 'has-error': errors.company_name }]"
        >
          <label for="company_name">Nome Azienda</label>
          <input type="text" v-model="form.company_name" class="form-control" />
          <small v-if="errors.company_name" class="form-text text-danger">
            {{ errors.company_name }}
          </small>
        </div>
        <div
          v-if="form.person_type === 'company'"
          :class="['form-group', { 'has-error': errors.vat_number }]"
        >
          <label for="vat_number">Partita IVA</label>
          <input type="text" v-model="form.vat_number" class="form-control" />
          <small v-if="errors.vat_number" class="form-text text-danger">
            {{ errors.vat_number }}
          </small>
        </div>
        <!-- Campi comuni -->
        <div
          v-if="form.person_type === 'individual'"
          :class="['form-group', { 'has-error': errors.tax_code }]"
        >
          <label for="tax_code">Codice Fiscale</label>
          <input type="text" v-model="form.tax_code" class="form-control" />
          <small v-if="errors.tax_code" class="form-text text-danger">
            {{ errors.tax_code }}
          </small>
        </div>
        <div :class="['form-group', { 'has-error': errors.address }]">
          <label for="address">Indirizzo</label>
          <input type="text" v-model="form.address" class="form-control" />
          <small v-if="errors.address" class="form-text text-danger">
            {{ errors.address }}
          </small>
        </div>
        <div :class="['form-group', { 'has-error': errors.city }]">
          <label for="city">Città</label>
          <input type="text" v-model="form.city" class="form-control" />
          <small v-if="errors.city" class="form-text text-danger">
            {{ errors.city }}
          </small>
        </div>
        <div :class="['form-group', { 'has-error': errors.postal_code }]">
          <label for="postal_code">Codice Postale</label>
          <input type="text" v-model="form.postal_code" class="form-control" />
          <small v-if="errors.postal_code" class="form-text text-danger">
            {{ errors.postal_code }}
          </small>
        </div>
        <div :class="['form-group', { 'has-error': errors.country }]">
          <label for="country">Paese</label>
          <input type="text" v-model="form.country" class="form-control" />
          <small v-if="errors.country" class="form-text text-danger">
            {{ errors.country }}
          </small>
        </div>
        <div :class="['form-group', { 'has-error': errors.email }]">
          <label for="email">Email</label>
          <input type="email" v-model="form.email" class="form-control" />
          <small v-if="errors.email" class="form-text text-danger">
            {{ errors.email }}
          </small>
        </div>
        <!-- Pulsante di invio -->
        <button type="submit" class="btn btn-primary mt-4" :disabled="loading">
          Invia
        </button>
      </form>
      <!-- Spinner di caricamento -->
      <div v-if="loading" class="spinner-container">
        {{ errorMessage }}
      </div>
      <div v-if="errorMessages.length" class="alert alert-danger fixed-bottom">
        {{ errorMessages.join(" ") }}
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, reactive, toRefs, watch } from 'vue';
import ApiService from "../common/api.service.js";

export default {
  props: {
    checkinProfile: {
      type: Object,
      required: true,
    },
    visible: {
      type: Boolean,
      required: true,
    },
  },
  setup(props, { emit }) {
    const form = reactive({
      checkin_profile: props.checkinProfile.id,
      person_type: "individual",
      first_name: props.checkinProfile.name,
      last_name: props.checkinProfile.surname,
      company_name: "",
      vat_number: "",
      tax_code: "",
      address: "",
      city: "",
      postal_code: "",
      country: "",
      email: "",
    });

    const loading = ref(false);
    const successMessage = ref("");
    const errorMessage = ref("");
    const errorMessages = ref([]);
    const errors = reactive({});

    watch(() => props.checkinProfile, (newProfile) => {
      form.checkin_profile = newProfile.id;
      form.first_name = newProfile.name;
      form.last_name = newProfile.surname;
    });

    const validateForm = () => {
      const errors = {};
      if (!form.person_type)
        errors.person_type = "Il tipo di persona è obbligatorio.";
      if (form.person_type === "individual") {
        if (!form.first_name)
          errors.first_name = "Il nome è obbligatorio.";
        if (!form.last_name)
          errors.last_name = "Il cognome è obbligatorio.";
      }
      if (form.person_type === "company") {
        if (!form.company_name)
          errors.company_name = "Il nome dell'azienda è obbligatorio.";
        if (!form.vat_number)
          errors.vat_number = "La partita IVA è obbligatoria.";
      }
      if (!form.tax_code)
        errors.tax_code = "Il codice fiscale è obbligatorio.";
      if (!form.address) errors.address = "L'indirizzo è obbligatorio.";
      if (!form.city) errors.city = "La città è obbligatoria.";
      if (!form.postal_code)
        errors.postal_code = "Il codice postale è obbligatorio.";
      if (!form.country) errors.country = "Il paese è obbligatorio.";
      if (!form.email) errors.email = "L'email è obbligatoria.";
      Object.assign(errors, errors);
      return Object.keys(errors).length === 0;
    };

    const submitForm = async () => {
      if (!validateForm()) {
        errorMessages.value.push(
          "Per favore, correggi gli errori nei campi evidenziati."
        );
        setTimeout(() => {
          errorMessages.value = [];
        }, 3000);
        return;
      }

      loading.value = true;
      try {
        await ApiService.post("/api/billing-info/", form);
        successMessage.value =
          "Informazioni di fatturazione inviate con successo!";
        errorMessage.value = "";
        emit("update-checkin-profile", { got_billing_info: true });
      } catch (error) {
        console.error("Errore durante l'invio del form:", error);
        errorMessage.value = "Errore durante l'invio del form. Riprova.";
        successMessage.value = "";
      } finally {
        loading.value = false;
      }
    };

    return {
      ...toRefs(form),
      loading,
      form,
      successMessage,
      errorMessage,
      errorMessages,
      errors,
      validateForm,
      submitForm,
    };
  },
};
</script>

<style scoped>
.billing-info-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.form-group {
  margin-bottom: 15px;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #09f;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .billing-info-form {
    padding: 15px;
  }

  .form-group {
    margin-bottom: 10px;
  }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.5s ease;
}
.slide-up-enter, .slide-up-leave-to /* .slide-up-leave-active in <2.1.8 */ {
  transform: translateY(0);
  opacity: 1;
}
.slide-up-leave-active {
  transform: translateY(-100%);
  opacity: 0;
}

.alert.fixed-bottom {
  position: fixed;
  bottom: 20px;
  width: auto;
  max-width: 90%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1050;
  margin: 0;
  border-radius: 10px;
}

.has-error input,
.has-error select {
  border-color: #dc3545;
}

.has-error .form-text {
  color: #dc3545;
}
</style>
