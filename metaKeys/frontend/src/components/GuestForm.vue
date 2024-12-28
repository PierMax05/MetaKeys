<template>
  <transition name="slide-up">
    <div v-if="visible" class="guest-form">
      <form
        v-for="(guest, index) in guests"
        :key="index"
        @submit.prevent="submitForm(index)"
      >
        <h3>Ospite {{ index + 1 }}</h3>
        <hr />
        <div v-if="checkinProfile.require_registration_form">
          <div
            :class="['form-group', { 'has-error': errors[index]?.first_name }]"
          >
            <label for="first_name">Nome</label>
            <input
              type="text"
              v-model="guest.first_name"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.first_name"
              class="form-text text-danger"
            >
              {{ errors[index].first_name }}
            </small>
          </div>
          <div
            :class="['form-group', { 'has-error': errors[index]?.last_name }]"
          >
            <label for="last_name">Cognome</label>
            <input
              type="text"
              v-model="guest.last_name"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.last_name"
              class="form-text text-danger"
            >
              {{ errors[index].last_name }}
            </small>
          </div>
          <div
            :class="['form-group', { 'has-error': errors[index]?.citizenship }]"
          >
            <label for="citizenship">Cittadinanza</label>
            <input
              type="text"
              v-model="guest.citizenship"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.citizenship"
              class="form-text text-danger"
            >
              {{ errors[index].citizenship }}
            </small>
          </div>
          <div
            :class="[
              'form-group',
              { 'has-error': errors[index]?.place_of_birth },
            ]"
          >
            <label for="place_of_birth">Luogo di Nascita</label>
            <input
              type="text"
              v-model="guest.place_of_birth"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.place_of_birth"
              class="form-text text-danger"
            >
              {{ errors[index].place_of_birth }}
            </small>
          </div>
          <div
            :class="[
              'form-group',
              { 'has-error': errors[index]?.date_of_birth },
            ]"
          >
            <label for="date_of_birth">Data di Nascita</label>
            <input
              type="date"
              v-model="guest.date_of_birth"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.date_of_birth"
              class="form-text text-danger"
            >
              {{ errors[index].date_of_birth }}
            </small>
          </div>
          <div :class="['form-group', { 'has-error': errors[index]?.gender }]">
            <label for="gender">Genere</label>
            <select v-model="guest.gender" class="form-control">
              <option value="F">Femmina</option>
              <option value="M">Maschio</option>
            </select>
            <small v-if="errors[index]?.gender" class="form-text text-danger">
              {{ errors[index].gender }}
            </small>
          </div>
          <div
            v-if="index === 0"
            :class="[
              'form-group',
              { 'has-error': errors[index]?.place_of_issue },
            ]"
          >
            <label for="place_of_issue">Luogo di Emissione</label>
            <input
              type="text"
              v-model="guest.place_of_issue"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.place_of_issue"
              class="form-text text-danger"
            >
              {{ errors[index].place_of_issue }}
            </small>
          </div>
          <div
            :class="[
              'form-group',
              { 'has-error': errors[index]?.document_type },
            ]"
          >
            <label for="document_type">Tipo di Documento</label>
            <select v-model="guest.document_type" class="form-control" required>
              <option value="passport">Passaporto</option>
              <option value="identity card">Carta d'Identità</option>
            </select>
            <small
              v-if="errors[index]?.document_type"
              class="form-text text-danger"
            >
              {{ errors[index].document_type }}
            </small>
          </div>
          <div
            v-if="index === 0"
            :class="[
              'form-group',
              { 'has-error': errors[index]?.document_number },
            ]"
          >
            <label for="document_number">Numero di Documento</label>
            <input
              type="text"
              v-model="guest.document_number"
              class="form-control"
              required
            />
            <small
              v-if="errors[index]?.document_number"
              class="form-text text-danger"
            >
              {{ errors[index].document_number }}
            </small>
          </div>
        </div>

        <div class="form-group" v-if="checkinProfile.require_document_photo">
          <label for="document_photo">
            <span v-if="guest.document_type !== 'passport'">Foto Documento Fronte</span>
            <span v-else>Foto Documento</span>
          </label>
          <input
            type="file"
            accept="image/*,.pdf"
            @change="handleFileUpload($event, index)"
            class="form-control"
            required
          />
          <small class="form-text text-muted">
            Formati accettati: JPEG, PNG, BMP, GIF, PDF
          </small>
          <br />
          <small
            v-if="errors[index]?.document_photo"
            class="form-text text-danger"
          >
            {{ errors[index].document_photo }}
          </small>
        </div>
        <div
          v-if="guest.document_type !== 'passport'"
          :class="[
            'form-group',
            { 'has-error': errors[index]?.document_photo_back },
          ]"
        >
          <label for="document_photo_back">Foto Retro Documento</label>
          <input
            type="file"
            accept="image/*,.pdf"
            @change="handleFileUploadBack($event, index)"
            class="form-control"
          />
          <small class="form-text text-muted">
            Formati accettati: JPEG, PNG, BMP, GIF, PDF
          </small>
          <br />
          <small
            v-if="errors[index]?.document_photo_back"
            class="form-text text-danger"
          >
            {{ errors[index].document_photo_back }}
          </small>
        </div>
      </form>
      <button @click="submitAllForms" class="btn btn-primary mt-4">
        Invia Tutti
      </button>
      <div v-if="loading" class="spinner-container">
        <div class="spinner"></div>
      </div>
      <div v-if="successMessage" class="alert alert-success mt-4">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-4">
        {{ errorMessage }}
      </div>
      <div v-if="errorMessages.length" class="alert alert-danger fixed-bottom">
        {{ errorMessages.join(" ") }}
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, watch, toRefs } from 'vue';
import ApiService from "../common/api.service";

export default {
  props: {
    checkinProfile: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit }) {
    const guests = ref([]);
    const loading = ref(false);
    const successMessage = ref("");
    const errorMessage = ref("");
    const visible = ref(true);
    const errorMessages = ref([]);
    const errors = ref([]);

    watch(
      () => props.checkinProfile,
      (newProfile) => {
        if (newProfile) {
          guests.value = Array(newProfile.guest_number)
            .fill()
            .map((_, index) => ({
              checkin_profile: newProfile.id,
              citizenship: "",
              place_of_birth: "",
              last_name:
                index === 0 && newProfile.require_registration_form
                  ? newProfile.surname
                  : "",
              first_name:
                index === 0 && newProfile.require_registration_form
                  ? newProfile.name
                  : "",
              date_of_birth: "",
              gender: "",
              place_of_issue: "",
              document_type: "identity card", // Imposta il tipo di documento di default
              document_number: "",
              document_photo: null,
              document_photo_back: null,
            }));
          errors.value = Array(newProfile.guest_number).fill({});
        }
      },
      { immediate: true }
    );

    const handleFileUpload = (event, index) => {
      guests.value[index].document_photo = event.target.files[0];
    };

    const handleFileUploadBack = (event, index) => {
      guests.value[index].document_photo_back = event.target.files[0];
    };

    const validateFile = (file) => {
      const allowedImageExtensions = ["jpg", "jpeg", "png", "bmp", "gif"];
      const allowedFileTypes = [
        "image/jpeg",
        "image/png",
        "image/bmp",
        "image/gif",
        "application/pdf",
      ];
      const fileType = file.type;
      const fileExtension = file.name.split(".").pop().toLowerCase();
      return (
        file &&
        allowedFileTypes.includes(fileType) &&
        (allowedImageExtensions.includes(fileExtension) ||
          fileExtension === "pdf")
      );
    };

    const validateForm = (guest, index) => {
      const formErrors = {};
      if (props.checkinProfile.require_registration_form) {
        if (!guest.first_name) formErrors.first_name = "Il nome è obbligatorio.";
        if (!guest.last_name) formErrors.last_name = "Il cognome è obbligatorio.";
        if (!guest.citizenship)
          formErrors.citizenship = "La cittadinanza è obbligatoria.";
        if (!guest.place_of_birth)
          formErrors.place_of_birth = "Il luogo di nascita è obbligatorio.";
        if (!guest.date_of_birth)
          formErrors.date_of_birth = "La data di nascita è obbligatoria.";
        if (!guest.gender) formErrors.gender = "Il genere è obbligatorio.";
        if (!guest.place_of_issue && index === 0)
          formErrors.place_of_issue = "Il luogo di emissione è obbligatorio.";
        if (!guest.document_type && index === 0)
          formErrors.document_type = "Il tipo di documento è obbligatorio.";
        if (!guest.document_number && index === 0)
          formErrors.document_number = "Il numero di documento è obbligatorio.";
      }
      if (
        props.checkinProfile.require_document_photo &&
        !validateFile(guest.document_photo)
      ) {
        formErrors.document_photo =
          "La foto del documento è obbligatoria e deve essere in un formato supportato.";
      }
      if (
        guest.document_type !== 'passport' &&
        props.checkinProfile.require_document_photo &&
        !validateFile(guest.document_photo_back)
      ) {
        formErrors.document_photo_back =
          "La foto del retro del documento è obbligatoria e deve essere in un formato supportato.";
      }
      errors.value[index] = formErrors;
      return Object.keys(formErrors).length === 0;
    };

    const submitForm = async (index) => {
      const guest = guests.value[index];
      if (!validateForm(guest, index)) {
        return;
      }

      const formData = new FormData();
      if (!props.checkinProfile.require_registration_form) {
        guest.first_name = props.checkinProfile.name;
        guest.last_name = props.checkinProfile.surname;
      }
      for (const key in guest) {
        if (guest[key] !== null) {
          formData.append(key, guest[key]);
        }
      }

      try {
        loading.value = true;
        const response = await ApiService.post(
          "/api/guests-registration/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        successMessage.value = "Form inviato con successo!";
        errorMessage.value = "";
        if (response.status === 200 || response.status === 201) {
          emit("update-checkin-profile", { got_registration_form: true });
          visible.value = false;
        }
      } catch (error) {
        console.error("Errore durante l'invio del form:", error);
        errorMessage.value = "Errore durante l'invio del form. Riprova.";
        successMessage.value = "";
      } finally {
        loading.value = false;
      }
    };

    const submitAllForms = async () => {
      errorMessages.value = [];
      let allValid = true;
      for (let i = 0; i < guests.value.length; i++) {
        if (!validateForm(guests.value[i], i)) {
          allValid = false;
        }
      }
      if (!allValid) {
        errorMessages.value.push(
          "Per favore, correggi gli errori nei campi evidenziati."
        );
        setTimeout(() => {
          errorMessages.value = [];
        }, 3000);
        return;
      }
      for (let i = 0; i < guests.value.length; i++) {
        await submitForm(i);
      }
    };

    return {
      ...toRefs(props),
      guests,
      loading,
      successMessage,
      errorMessage,
      visible,
      errorMessages,
      errors,
      handleFileUpload,
      handleFileUploadBack,
      validateFile,
      validateForm,
      submitForm,
      submitAllForms,
    };
  },
};
</script>

<style scoped>
.guest-form {
  max-width: 1000px;
  margin: 5% auto;
  border: 1px solid #ddd;
  padding: 5%;
  border-radius: 10px;
  background-color: #f9f9f9;
}
.form-check-inline {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-check-inline .form-check-input {
  margin-right: 10px;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Altezza del contenitore dello spinner */
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
  .guest-form {
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
