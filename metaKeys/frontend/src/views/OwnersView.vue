<template>
  <div class="owners-view">
    <nav :class="{ 'hidden-navbar': isNavbarHidden && scrollY > navHeight }">
      <div class="nav-buttons">
        <button class="btn" @click="showComponent('createApartment')">
          <span v-if="isSmallScreen"
            ><img class="icon" :src="getImageUrl('apartment', 'png')"
          /></span>
          <span v-else>Strutture</span>
        </button>
        <button class="btn" @click="showComponent('checkIn')">
          <span v-if="isSmallScreen"
            ><img class="icon" :src="getImageUrl('access', 'png')"
          /></span>
          <span v-else>Accessi</span>
        </button>
        <button class="btn" @click="showComponent('checkInSearch')">
          <span v-if="isSmallScreen"
            ><img class="icon" :src="getImageUrl('bed', 'png')"
          /></span>
          <span v-else>Soggiorni</span>
        </button>
        <button class="btn" @click="showComponent('info')">
          <span v-if="isSmallScreen"
            ><img class="icon" :src="getImageUrl('info_icon', 'png')"
          /></span>
          <span v-else>Informazioni</span>
        </button>
      </div>
    </nav>
    <div v-if="connectionIssues" class="alert alert-warning">
      ATTENZIONE! Ci sono dei dispositivi Shelly che non sono in funzione. 
      Controllare il server URI, la chiave di autenticazione, l'ID del dispositivo forniti e la connessione dei dispositivi.
    </div>
    <div v-if="activeComponent === 'checkIn'">
      <CheckIn />
    </div>
    <div v-if="activeComponent === 'createApartment'">
      <ApartmentsList @showShellyStatus="openShellyModal" :hasShellyDevices="hasShellyDevices" />
    </div>
    <div v-if="activeComponent === 'checkInSearch'">
      <CheckInSearch />
    </div>
    <div v-if="activeComponent === 'info'">
      <InfoList />
    </div>
    <div v-if="isShellyModalOpen" class="modal-overlay">
      <div class="modal-content">
        <button class="close-button" @click="closeShellyModal">&times;</button>
        <ShellyStatus :doorStatus="doorStatus" />
      </div>
    </div>
  </div>
</template>

<script>
import ApartmentsList from "../components/ApartmentsList.vue";
import CheckIn from "../components/CheckIn.vue";
import CheckInSearch from "../components/CheckInSearch.vue";
import InfoList from "../components/InfoList.vue";
import ShellyStatus from "../components/ShellyStatus.vue";
import ApiService from '../common/api.service';

export default {
  name: "OwnersView",
  components: {
    CheckIn,
    ApartmentsList,
    CheckInSearch,
    InfoList,
    ShellyStatus,
  },
  data() {
    return {
      activeComponent: "createApartment",
      isSmallScreen: window.innerWidth <= 768,
      isNavbarHidden: false,
      lastScrollY: window.scrollY,
      scrollY: window.scrollY,
      navHeight: 60, // Adjust based on navbar height
      doorStatus: [],
      isShellyModalOpen: false,
      connectionIssues: false,
      hasShellyDevices: false,
    };
  },

  methods: {
    getImageUrl(name, ext) {
      return new URL(`../assets/${name}.${ext}`, import.meta.url).href;
    },
    showComponent(component) {
      this.activeComponent = component;
    },
    checkScreenSize() {
      this.isSmallScreen = window.innerWidth <= 768;
    },
    handleScroll() {
      this.scrollY = window.scrollY;
      if (this.scrollY < this.lastScrollY) {
        this.isNavbarHidden = false;
      } else if (this.scrollY > this.navHeight) {
        this.isNavbarHidden = true;
      }
      this.lastScrollY = this.scrollY;
    },
    async checkDoorStatus() {
      try {
        const response = await ApiService.get('/api/check-doors-status/');
        this.doorStatus = response.data;
        this.connectionIssues = this.doorStatus.some(status => !status.status.isok || !status.status.connected);
        this.hasShellyDevices = this.doorStatus.length > 0;
      } catch (error) {
        console.error('Errore durante il controllo dello stato delle porte:', error);
      }
    },
    openShellyModal() {
      this.isShellyModalOpen = true;
    },
    closeShellyModal() {
      this.isShellyModalOpen = false;
    },
  },
  async mounted() {
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize);
    window.addEventListener("scroll", this.handleScroll);
    await this.checkDoorStatus();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.checkScreenSize);
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
.owners-view {
  margin-top: 50px; /* Adjust based on the combined height of the fixed navbars */
}

nav {
  display: flex;
  justify-content: center;
  padding: 5px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  transition: top 0.3s;
  position: fixed;
  width: 100%;
  top: 50px; /* Adjust based on the height of the fixed navbar in App.vue */
  z-index: 999;
}

.hidden-navbar {
  top: -60px; /* Adjust based on navbar height */
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  background-color: transparent;
  color: #007bff;
  border: none;
  cursor: pointer;
  transition: color 0.3s, transform 0.3s;
  display: flex;
  align-items: center;
}

.btn:hover {
  color: #0056b3;
}

.btn:active {
  transform: scale(0.95);
}

.btn:focus {
  outline: none;
  box-shadow: none;
}

.icon {
  width: 32px; /* Ingrandisci le icone */
  height: 32px; /* Ingrandisci le icone */
}

@media (max-width: 768px) {
  .btn {
    background-color: transparent;
    color: #007bff;
    border: none;
  }

  .btn:hover {
    background-color: transparent;
    color: #0056b3;
  }

  .btn:focus {
    box-shadow: none;
  }
}

.status-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px 0;
  background-color: #f9f9f9;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  height: 100%;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.alert {
  padding: 15px;
  background-color: #f9c74f;
  color: black;
  margin-bottom: 20px;
  border-radius: 5px;
  text-align: center;
}
</style>
