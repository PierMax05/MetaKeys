<template>
  <div class="checkin-search">
    <form @submit.prevent="searchCheckInProfiles" class="search-form">
      <label for="start_date" class="start-date">Dal</label>
      <input type="date" v-model="startDate" required class="search-input" />
      <label for="end_date" class="end-date">Al</label>
      <input type="date" v-model="endDate" required class="search-input" />
      <button type="submit" class="btn search-btn">Cerca</button>
    </form>
    <div v-if="checkInProfiles.length" class="profile-cards">
      <div
        v-for="(profile, index) in checkInProfiles"
        :key="profile.id"
        class="card profile-card"
        @click="openModal(index)"
      >
        <h6>{{ profile.apartment_name }}</h6>
        <h6>{{ profile.name }} {{ profile.surname }}</h6>
      </div>
    </div>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <button
            @click="prevProfile"
            :disabled="currentIndex === 0"
            class="btn nav-btn"
          >
            Indietro
          </button>
          <button
            @click="nextProfile"
            :disabled="currentIndex === checkInProfiles.length - 1"
            class="btn nav-btn"
          >
            Avanti
          </button>
        </div>
        <div class="modal-body">
          <div class="card stay-details-card">
            <h5>{{ currentProfile.apartment_name }}</h5>
            <p>{{ currentProfile.name }} {{ currentProfile.surname }}</p>
            <p>
              Dal {{ formatDate(currentProfile.check_in_date) }} Al
              {{ formatDate(currentProfile.check_out_date) }}
            </p>
            <p>Ospiti: {{ currentProfile.guest_number }}</p>
          </div>
          <h4>Ospiti</h4>
          <div v-if="currentProfile.guests && currentProfile.guests.length">
            <table class="guests-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Cognome</th>
                  <th>Data di Nascita</th>
                  <th>Età</th>
                  <th>Cittadinanza</th>
                  <th>Luogo di Nascita</th>
                  <th>Genere</th>
                  <th>Tipo Documento</th>
                  <th>Luogo di Rilascio</th>
                  <th>Numero Documento</th>
                  <th>Azioni</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(guest, index) in currentProfile.guests"
                  :key="guest.id"
                >
                  <td>{{ guest.first_name }}</td>
                  <td>{{ guest.last_name }}</td>
                  <td>{{ formatDate(guest.date_of_birth) }}</td>
                  <td>{{ calculateAge(guest.date_of_birth) }}</td>
                  <td>{{ guest.citizenship }}</td>
                  <td>{{ guest.place_of_birth }}</td>
                  <td>{{ guest.gender }}</td>
                  <td>{{ guest.document_type }}</td>
                  <td>{{ guest.place_of_issue }}</td>
                  <td>{{ guest.document_number }}</td>
                  <td>
                    <button @click="openGuestModal(index)" class="btn btn-link">
                      <img
                        :src="getImageUrl('id-card.png')"
                        alt="ID Card Icon"
                        class="icon"
                      />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div
              v-for="(guest, index) in currentProfile.guests"
              :key="guest.id"
              class="guest-card"
            >
              <p>Nome: {{ guest.first_name }}</p>
              <p>Cognome: {{ guest.last_name }}</p>
              <p>Data di Nascita: {{ formatDate(guest.date_of_birth) }}</p>
              <p>Età: {{ calculateAge(guest.date_of_birth) }}</p>
              <p>Cittadinanza: {{ guest.citizenship }}</p>
              <p>Luogo di Nascita: {{ guest.place_of_birth }}</p>
              <p>Genere: {{ guest.gender }}</p>
              <p>Tipo Documento: {{ guest.document_type }}</p>
              <p>Luogo di Rilascio: {{ guest.place_of_issue }}</p>
              <p>Numero Documento: {{ guest.document_number }}</p>
              <button @click="openGuestModal(index)" class="btn">
                <img
                  :src="getImageUrl('id-card.png')"
                  alt="ID Card Icon"
                  class="icon"
                />
              </button>
            </div>
          </div>
          <div v-else class="card no-data-card">
            <p>Ancora Nessun ospite registrato.</p>
          </div>
          <h4 class="m-4">Informazioni di Fatturazione</h4>
          <div
            v-if="
              currentProfile.billing_info && currentProfile.billing_info.length
            "
          >
            <table class="billing-table">
              <thead>
                <tr>
                  <th>Tipo Persona</th>
                  <th>Nome</th>
                  <th>Cognome</th>
                  <th>Nome Azienda</th>
                  <th>Partita IVA</th>
                  <th>Codice Fiscale</th>
                  <th>Indirizzo</th>
                  <th>Città</th>
                  <th>CAP</th>
                  <th>Paese</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="info in currentProfile.billing_info" :key="info.id">
                  <td>{{ info.person_type }}</td>
                  <td>{{ info.first_name }}</td>
                  <td>{{ info.last_name }}</td>
                  <td>{{ info.company_name }}</td>
                  <td>{{ info.vat_number }}</td>
                  <td>{{ info.tax_code }}</td>
                  <td>{{ info.address }}</td>
                  <td>{{ info.city }}</td>
                  <td>{{ info.postal_code }}</td>
                  <td>{{ info.country }}</td>
                  <td>{{ info.email }}</td>
                </tr>
              </tbody>
            </table>
            <div
              v-for="info in currentProfile.billing_info"
              :key="info.id"
              class="billing-card"
            >
              <p>Tipo Persona: {{ info.person_type }}</p>
              <p>Nome: {{ info.first_name }}</p>
              <p>Cognome: {{ info.last_name }}</p>
              <p>Nome Azienda: {{ info.company_name }}</p>
              <p>Partita IVA: {{ info.vat_number }}</p>
              <p>Codice Fiscale: {{ info.tax_code }}</p>
              <p>Indirizzo: {{ info.address }}</p>
              <p>Città: {{ info.city }}</p>
              <p>CAP: {{ info.postal_code }}</p>
              <p>Paese: {{ info.country }}</p>
              <p>Email: {{ info.email }}</p>
            </div>
          </div>
          <div v-else class="card no-data-card">
            <p>Ancora Nessuna informazione di fatturazione disponibile.</p>
          </div>
        </div>
        <div v-if="showGuestModal" class="modal">
          <div class="modal-content">
            <div class="modal-header">
              <button
                @click="prevGuest"
                :disabled="currentGuestIndex === 0"
                class="btn nav-btn"
              >
                Indietro
              </button>
              <button
                @click="nextGuest"
                :disabled="
                  currentGuestIndex === currentProfile.guests.length - 1
                "
                class="btn nav-btn"
              >
                Avanti
              </button>
              <button @click="closeGuestModal" class="btn close-btn">
                Chiudi
              </button>
            </div>
            <div class="modal-body">
              <div class="card-container">
                <form
                  class="card document-details-card"
                  @submit.prevent="updateGuestDetails"
                  ref="documentDetailsCard"
                >
                  <h3>Dettagli Documento</h3>
                  <label>
                    Nome:
                    <input type="text" v-model="currentGuest.first_name" />
                  </label>
                  <label>
                    Cognome:
                    <input type="text" v-model="currentGuest.last_name" />
                  </label>
                  <label>
                    Data di Nascita:
                    <input type="date" v-model="currentGuest.date_of_birth" />
                  </label>
                  <label>
                    Cittadinanza:
                    <input type="text" v-model="currentGuest.citizenship" />
                  </label>
                  <label>
                    Luogo di Nascita:
                    <input type="text" v-model="currentGuest.place_of_birth" />
                  </label>
                  <label>
                    Sesso:
                    <input type="text" v-model="currentGuest.gender" />
                  </label>
                  <label>
                    Tipo Documento:
                    <input type="text" v-model="currentGuest.document_type" />
                  </label>
                  <label>
                    Numero Documento:
                    <input type="text" v-model="currentGuest.document_number" />
                  </label>
                  <label>
                    Luogo di Rilascio:
                    <input type="text" v-model="currentGuest.place_of_issue" />
                  </label>
                  <button type="submit" class="btn mb-2">Salva</button>
                </form>
                <div class="card document-photo-card">
                  <div v-if="currentGuest.document_photo">
                    <div class="photo-buttons">
                      <button v-if="!showBackPhoto && currentGuest.document_photo_back" @click="showBackPhoto = true" class="btn">
                        Retro
                      </button>
                      <button v-if="showBackPhoto && currentGuest.document_photo_back" @click="showBackPhoto = false" class="btn">
                        Fronte
                      </button>
                    </div>
                    <img
                      v-if="!showBackPhoto"
                      :src="getProtectedMediaUrl(currentGuest.document_photo)"
                      alt="Foto Documento"
                      class="document-photo"
                      ref="documentPhotoCardImg"
                    />
                    <img
                      v-if="showBackPhoto && currentGuest.document_photo_back"
                      :src="getProtectedMediaUrl(currentGuest.document_photo_back)"
                      alt="Foto Documento Retro"
                      class="document-photo"
                      ref="documentPhotoCardImg"
                    />
                    <div v-else class="pdf-container" ref="pdfContainer"></div>
                  </div>
                  <div v-else>
                    <p>Nessuna foto disponibile.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="btn close-btn">Chiudi</button>
        </div>
      </div>
    </div>
    <div
      v-if="notification.message"
      :class="['notification', notification.type]"
    >
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';

import apiService from '../common/api.service';

const startDate = ref(new Date().toISOString().slice(0, 10));
const endDate = ref(new Date().toISOString().slice(0, 10));
const checkInProfiles = ref([]);
const showModal = ref(false);
const currentIndex = ref(0);
const showGuestModal = ref(false);
const currentGuestIndex = ref(0);
const notification = ref({
  message: "",
  type: "",
});
const showBackPhoto = ref(false);

const currentProfile = computed(() => checkInProfiles.value[currentIndex.value] || {});
const currentGuest = computed(() => currentProfile.value.guests[currentGuestIndex.value] || {});

const searchCheckInProfiles = async () => {
  const params = new URLSearchParams();
  params.append("start_date", startDate.value);
  params.append("end_date", endDate.value);
  try {
    const response = await apiService.get(`/api/owner-checkin-details/?${params.toString()}`);
    checkInProfiles.value = response.data;
  } catch (error) {
    console.error(error);
  }
};


const openModal = (index) => {
  currentIndex.value = index;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const prevProfile = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    showBackPhoto.value = false;
  }
};

const nextProfile = () => {
  if (currentIndex.value < checkInProfiles.value.length - 1) {
    currentIndex.value++;
    showBackPhoto.value = false;
  }
};

const openGuestModal = (index) => {
  currentGuestIndex.value = index;
  showGuestModal.value = true;
};

const closeGuestModal = () => {
  showGuestModal.value = false;
};

const prevGuest = () => {
  if (currentGuestIndex.value > 0) {
    currentGuestIndex.value--;
    showBackPhoto.value = false;
  }
};

const nextGuest = () => {
  if (currentGuestIndex.value < currentProfile.value.guests.length - 1) {
    currentGuestIndex.value++;
    showBackPhoto.value = false;
  }
};

const calculateAge = (dateOfBirth) => {
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDifference = today.getMonth() - birthDate.getMonth();
  if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
};

const formatDate = (date) => {
  const [year, month, day] = date.split("-");
  return `${day}/${month}/${year}`;
};

const updateGuestDetails = async () => {
  const formData = new FormData();
  for (const key in currentGuest.value) {
    if (Object.prototype.hasOwnProperty.call(currentGuest.value, key) && key !== "id") {
      if (key === "document_photo" || key === "document_photo_back") {
        if (currentGuest.value[key] instanceof File) {
          formData.append(key, currentGuest.value[key]);
        }
      } else {
        formData.append(key, currentGuest.value[key]);
      }
    }
  }
  try {
    await apiService.put(`/api/guests-registration/${currentGuest.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    showNotification("Dettagli aggiornati con successo", "success");
  } catch (error) {
    console.error(error);
    showNotification("Errore durante l'aggiornamento dei dettagli", "error");
    }
  };

const showNotification = (message, type) => {
  notification.value.message = message;
  notification.value.type = type;
  setTimeout(() => {
    notification.value.message = "";
    notification.value.type = "";
  }, 5000);
};

const setDocumentPhotoHeight = () => {
  nextTick(() => {
    const detailsCard = document.querySelector('.document-details-card');
    const photoCardImg = document.querySelector('.document-photo-card img');
    if (detailsCard && photoCardImg) {
      photoCardImg.style.maxHeight = `${detailsCard.clientHeight}px`;
    }
  });
};

const getProtectedMediaUrl = (path) => {
  return `${path}`;
};

const getImageUrl = (name) => {
  const url = new URL(`../assets/${name}`, import.meta.url).href;
  return url;
};
watch(showGuestModal, (newVal) => {
  if (newVal) {
    setDocumentPhotoHeight();
  }
});

onMounted(() => {
  window.addEventListener("resize", setDocumentPhotoHeight);
  searchCheckInProfiles();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", setDocumentPhotoHeight);
});
</script>

<style scoped>
.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  padding: 10px;
}

.search-input {
  border-radius: 4px;
  border: 1px solid #ccc;
  flex: 1;
  min-width: 200px;
}

.start-date,
.end-date {
  border: 1px solid #ccc;
  padding: 5px 10px;
}

.btn {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}

.btn:active {
  transform: scale(0.95);
}

.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5);
}

.profile-cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.profile-card {
  background-color: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  min-width: 250px;
  border: 1px solid #ccc;
  cursor: pointer;
}

.profile-card h3 {
  margin-top: 0;
}

.details-btn {
  margin-top: 10px;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 0;
  border: 1px solid #888;
  width: 100%;
  height: 100%;
  border-radius: 0;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
}

.close-btn {
  background-color: #dc3545;
}

.close-btn:hover {
  background-color: #c82333;
}

.guests-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.guests-table th,
.guests-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.guests-table th {
  background-color: #f2f2f2;
  text-align: left;
}

.billing-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.billing-table th,
.billing-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.billing-table th {
  background-color: #f2f2f2;
  text-align: left;
}

.no-data-card {
  background-color: #5a6a7b;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #0056b3;
  margin-top: 20px;
  text-align: center;
  color: white;
}

.stay-details-card {
  background-color: white;
  padding: 5px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #ccc;
  margin-bottom: 10px;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.document-photo-card,
.document-details-card {
  flex: 1;
  justify-content: center;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #ccc;
  padding: 0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0;
}

.document-photo-card {
  position: relative;
}

.photo-buttons {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.document-photo-card img {
  width: auto;
  max-height: 100%;
  object-fit: contain;
}

.icon {
  width: 24px;
  height: 24px;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
  }

  .profile-cards {
    padding: 10px;
  }

  .profile-card {
    min-width: 100%;
  }

  .modal-content {
    width: 100%;
    height: 100%;
    margin: auto;
  }

  .card-container {
    flex-direction: column;
  }

  .guests-table,
  .billing-table {
    display: none;
  }

  .guest-card,
  .billing-card {
    display: block;
    background-color: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid #ccc;
    margin-bottom: 10px;
  }

  .document-photo-card {
    order: -1; /* Sposta il div con la foto del documento sopra il form */
  }
}

@media (min-width: 769px) {
  .guest-card,
  .billing-card {
    display: none;
  }

  .guests-table,
  .billing-table {
    display: table;
  }
}

@media (max-width: 480px) {
  .search-input {
    min-width: 100%;
  }

  .btn {
    width: 100%;
  }

  .guests-table,
  .billing-table {
    font-size: 12px;
  }
}

.document-details-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.document-details-card label {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  width: 100%;
}

.document-details-card input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.document-photo-container {
  margin-top: 10px;
  width: 100%;
  text-align: center;
}

.document-photo {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.notification {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 4px;
  color: white;
  text-align: center;
  z-index: 1000;
  opacity: 0.9;
}

.notification.success {
  background-color: #28a745;
}

.notification.error {
  background-color: #dc3545;
}

.pdf-container {
  width: 100%;
  height: auto;
  text-align: center;
}

.btn-link {
  background: none; /* Rimuovi lo sfondo */
}
</style>
