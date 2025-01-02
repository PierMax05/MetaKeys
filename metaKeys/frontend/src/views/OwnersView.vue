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
    <div v-if="connectionIssues && showConnectionIssues" class="alert alert-warning fixed-bottom">
      ATTENZIONE! Ci sono dei dispositivi Shelly che non sono in funzione. 
      Controllare il server URI, la chiave di autenticazione, l'ID e la connessione dei dispositivi.
      <div class="button-group">
        <button class="btn" @click="handleClose">Chiudi</button>
      </div>
    </div>
    <div v-if="activeComponent === 'checkIn'">
      <CheckIn />
    </div>
    <div v-if="activeComponent === 'createApartment'">
      <ApartmentsList @showShellyStatus="openShellyModalAndFetchStatus" />
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
import { useStore } from 'vuex';
import { computed, ref } from 'vue';

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
      isShellyModalOpen: false,
      showConnectionIssues: true,
    };
  },
  setup() {
    const store = useStore();
    const hasShellyDevices = computed(() => store.getters.hasShellyDevices);
    const doorStatus = computed(() => store.getters.doorStatus);
    const connectionIssues = computed(() => store.getters.connectionIssues);
    return { hasShellyDevices, doorStatus, connectionIssues, store };
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
    openShellyModal() {
      this.isShellyModalOpen = true;
    },
    closeShellyModal() {
      this.isShellyModalOpen = false;
    },
    handleClose() {
      this.showConnectionIssues = false;
    },
    async fetchShellyStatus() {
      if (this.hasShellyDevices) {
        await this.store.dispatch('checkDoorStatus');
      }
    },
    async openShellyModalAndFetchStatus() {
      await this.fetchShellyStatus();
      this.openShellyModal();
    },
  },
  async mounted() {
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize);
    window.addEventListener("scroll", this.handleScroll);
    await this.fetchShellyStatus();
    await this.store.dispatch('checkDoorStatus'); // Chiama checkDoorStatus appena si entra sulla pagina
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

.alert {
  padding: 15px;
  background-color: #f9c74f;
  color: black;
  margin-bottom: 20px;
  border-radius: 5px;
  text-align: start;
  position: absolute;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  font-size: 20px;
  background-color: transparent;
  color: #000;
  border: none;
}

.fixed-bottom {
  position: fixed;
  bottom: 0;
  width: 100%;
  z-index: 1000;
}
</style>
