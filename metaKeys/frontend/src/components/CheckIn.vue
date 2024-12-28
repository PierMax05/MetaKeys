<template>
  <div class="check-in-container">
    <div class="search-container">
      <div class="name-inputs">
        <input
          type="text"
          v-model="searchFirstName"
          placeholder="Cerca per nome"
          class="search-input"
        />
        <input
          type="text"
          v-model="searchLastName"
          placeholder="Cerca per cognome"
          class="search-input"
        />
      </div>
      <div class="search-buttons">
        <input
          type="date"
          v-model="searchDate"
          placeholder="Cerca per data di check-in"
          class="search-input"
        />
        <button class="search-btn" @click="searchProfiles">Cerca</button>
        <button class="reset-btn" @click="resetSearch">Reset</button>
      </div>
    </div>
    <div class="action-container mb-2">
      <div class="today-card" v-if="isToday">Oggi</div>
      <button class="open-modal-btn" @click="showModal = true">
        Nuovo Accesso
      </button>
    </div>
    <ModalComponent v-if="showModal" :isOpen="showModal" @close="showModal = false">
      <template #header>
        <h3>Nuovo Accesso</h3>
      </template>
      <template #body>
        <GuestsRegistrationComponent
          @submit-registration="handleRegistrationSubmit"
          @close="showModal = false"
          @success="handleSuccess"
        />
      </template>
    </ModalComponent>
    <div v-if="!isSearching" class="profile-cards">
      <div v-for="profile in profiles" :key="profile.id" class="profile-card">
        <div>
          <h3>{{ getApartmentName(profile.apartment) }}</h3>
          <h4>{{ profile.room_name }}</h4>
          <h6>{{ profile.name }} {{ profile.surname }}</h6>
          <p>
            check-in: {{ profile.check_in_date }} /
            {{ formatTime(profile.check_in_time) }}
          </p>
          <p>
            check-out: {{ profile.check_out_date }} /
            {{ formatTime(profile.check_out_time) }}
          </p>
          <p>Numero Ospiti {{ profile.guest_number }}</p>
          <div class="card">
            <h6 class="mt-2">CREDENZIALI</h6>
            <p>user: {{ profile.username }}</p>
            <p>pass: {{ profile.psw }}</p>
          </div>
        </div>
        <button class="edit-btn" @click.stop="openEditModal(profile)">
          Edita
        </button>
      </div>
    </div>
    <div v-if="isSearching" class="profile-cards">
      <div
        v-for="profile in searchResults"
        :key="profile.id"
        class="profile-card"
      >
        <div>
          <h3>{{ getApartmentName(profile.apartment) }}</h3>
          <h6>{{ profile.name }} {{ profile.surname }}</h6>
          <p>
            check-in: {{ profile.check_in_date }} /
            {{ formatTime(profile.check_in_time) }}
          </p>
          <p>
            check-out: {{ profile.check_out_date }} /
            {{ formatTime(profile.check_out_time) }}
          </p>
          <p>Numero Ospiti {{ profile.guest_number }}</p>
          <div class="card">
            <h6 class="mt-2">CREDENZIALI</h6>
            <p>user: {{ profile.username }}</p>
            <p>pass: {{ profile.psw }}</p>
          </div>
        </div>
        <button class="edit-btn" @click.stop="openEditModal(profile)">
          Edita
        </button>
      </div>
    </div>
    <ModalComponent v-if="showEditModal" :isOpen="showEditModal" @close="showEditModal = false">
      <template #header>
        <h3>Modifica Check-in</h3>
      </template>
      <template #body>
        <EditProfile
          :profile="selectedProfile"
          @submit-edit="handleEditSubmit"
          @delete-profile="handleDeleteProfile"
          @success="handleSuccess"
          @close="showEditModal = false"
        />
      </template>
    </ModalComponent>
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import ApiService from "../common/api.service.js";
import GuestsRegistrationComponent from "./GuestsRegistrationComponent.vue";
import ModalComponent from "./Modal.vue";
import EditProfile from "./EditProfile.vue";

const showModal = ref(false);
const showEditModal = ref(false);
const searchFirstName = ref("");
const searchLastName = ref("");
const searchDate = ref("");
const profiles = ref([]);
const searchResults = ref([]);
const isSearching = ref(false);
const apartments = ref([]);
const selectedProfile = ref(null);
const error = ref(null);
const successMessage = ref("");
const selectedDay = ref(null);

const isToday = computed(() => {
  const today = new Date().toISOString().split("T")[0];
  return selectedDay.value === today;
});

const fetchProfiles = async () => {
  searchResults.value = [];
  isSearching.value = false;
  selectedDay.value = new Date().toISOString().split("T")[0];
  try {
    const response = await ApiService.get("/api/checkin-profiles/");
    profiles.value = response.data.currents;
  } catch (error) {
    console.error("Errore durante il recupero dei profili di check-in:", error);
  }
};

const searchProfiles = async () => {
  if (!searchFirstName.value && !searchLastName.value && !searchDate.value) {
    isSearching.value = false;
    fetchProfiles();
    return;
  }
  resetProfiles();
  selectedDay.value = searchDate.value;
  const params = new URLSearchParams();
  if (searchFirstName.value) params.append("name", searchFirstName.value);
  if (searchLastName.value) params.append("surname", searchLastName.value);
  if (searchDate.value) params.append("check_in_date", searchDate.value);
  try {
    const response = await ApiService.get(`/api/checkin-profiles/?${params.toString()}`);
    searchResults.value = response.data.search_results;
    isSearching.value = true;
  } catch (error) {
    console.error("Errore durante la ricerca dei profili di check-in:", error);
  }
};

const fetchApartments = async () => {
  try {
    const response = await ApiService.get("/api/apartments/");
    apartments.value = response.data;
  } catch (error) {
    console.error("Errore nel recupero degli appartamenti:", error);
  }
};

const getApartmentName = (apartmentId) => {
  const apartment = apartments.value.find(apartment => apartment.id === apartmentId);
  return apartment ? apartment.name : "N/A";
};

const formatTime = (dateTime) => {
  return dateTime.slice(0, 5);
};

const resetSearch = () => {
  searchFirstName.value = "";
  searchLastName.value = "";
  searchDate.value = "";
  fetchProfiles();
};

const resetProfiles = () => {
  profiles.value = [];
};

const openEditModal = (profile) => {
  selectedProfile.value = profile;
  showEditModal.value = true;
};

const handleEditSubmit = (updatedProfile) => {
  if (!isSearching.value) {
    const index = profiles.value.findIndex(profile => profile.id === updatedProfile.id);
    if (index !== -1) {
      profiles.value.splice(index, 1, updatedProfile);
    }
  } else {
    const index = searchResults.value.findIndex(profile => profile.id === updatedProfile.id);
    if (index !== -1) {
      searchResults.value.splice(index, 1, updatedProfile);
    }
  }
  showEditModal.value = false;
};

const handleDeleteProfile = (profileId) => {
  if (!isSearching.value) {
    profiles.value = profiles.value.filter(profile => profile.id !== profileId);
  } else {
    searchResults.value = searchResults.value.filter(profile => profile.id !== profileId);
  }
  showEditModal.value = false;
};

const handleRegistrationSubmit = (newProfile) => {
  profiles.value.push(newProfile);
  searchDate.value = newProfile.check_in_date;
  searchProfiles();
  showModal.value = false;
};

const handleSuccess = (message) => {
  successMessage.value = message;
  setTimeout(() => {
    successMessage.value = "";
  }, 3000);
};

onMounted(() => {
  fetchApartments();
  fetchProfiles();
});
</script>

<style scoped>
.check-in-container {
  padding: 20px;
}

.search-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.name-inputs {
  display: flex;
  width: 100%;
  gap: 5px;
  flex: 1;
}


.search-input {
  border-radius: 4px;
  border: 1px solid #ccc;
  flex: 1;
}

.search-buttons {
  display: flex;
  gap: 10px;
}

.search-btn,
.reset-btn {
  padding: 3px 20px;
  border-radius: 4px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.search-btn:hover,
.reset-btn:hover {
  background-color: #0056b3;
}

.reset-btn {
  background-color: #6c757d;
}

.reset-btn:hover {
  background-color: #5a6268;
}

.open-modal-btn {
  padding: 3px 15px;
  border-radius: 4px;
  background-color: #28a745;
  border: none;
  color: white;
  cursor: pointer;
  white-space: nowrap;
  margin-left: auto;
}

.open-modal-btn:hover {
  background-color: #218838;
}

.profile-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.profile-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex: 1 1 calc(33.333% - 20px);
  box-sizing: border-box;
  min-width: 250px;
  border: 1px solid #ccc;
  position: relative;
}

.profile-card h3 {
  margin-top: 0;
}

.profile-card p {
  margin: 5px 0;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #c3e6cb;
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
}

@media (max-width: 768px) {
  .profile-card {
    flex: 1 1 calc(50% - 20px);
  }
  .search-container {
    flex-direction: column;
  }
  .name-inputs {
    flex-direction: row;
    width: 100%;
  }
  .search-buttons {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .profile-card {
    flex: 1 1 100%;
  }
  .search-container {
    flex-direction: column;
  }
  .name-inputs {
    flex-direction: row;
  }
  .search-buttons {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    width: 100%;
  }
}

@media (min-width: 769px) {
  .search-container {
    flex-wrap: nowrap;
  }
  .search-buttons {
    margin-top: 0;
  }
}

.action-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.today-card {
  background-color: #cce5ff;
  color: #004085;
  padding: 3px 15px;
  border-radius: 4px;
  border: 1px solid #b8daff;
}

.edit-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 3px 10px;
  border-radius: 4px;
  border: none;
  background-color: #ffc107;
  color: white;
  cursor: pointer;
}

.edit-btn:hover {
  background-color: #c69500;
}
</style>
