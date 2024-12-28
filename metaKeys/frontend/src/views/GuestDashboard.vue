<template>
  <div class="guest-dashboard">
    <nav :class="{ 'hidden-navbar': isNavbarHidden && scrollY > navHeight }">
      <button class="nav-btn" @click="showSection('component1')">
        <img :src="getImageUrl('key', 'png')" alt="Key" class="nav-icon" />
      </button>
      <button class="nav-btn" @click="showSection('component2')">
        <img :src="getImageUrl('info_icon', 'png')" alt="Info Icon" class="nav-icon" />
      </button>
      <button class="nav-btn" @click="showSection('component3')">
        <img :src="getImageUrl('parking', 'png')" alt="Parking" class="nav-icon" />
      </button>
      <button class="nav-btn" @click="showSection('component4')">
        <img :src="getImageUrl('restaurant', 'png')" alt="Restaurant" class="nav-icon" />
      </button>
      <button class="nav-btn" @click="showSection('component5')">
        <img :src="getImageUrl('bed', 'png')" alt="Bed" class="nav-icon" />
      </button>
    </nav>
    <div v-if="loading" class="spinner-container">
      <div class="spinner-content">
        <h2>Caricamento...</h2>
        <p>Stiamo recuperando i tuoi dati del profilo. Attendere prego...</p>
        <div class="spinner"></div>
      </div>
    </div>
    <div v-else>
      <div class="header">
        <div class="apartment-name">{{ profile.apartment_name }}</div>
        <div class="greeting">Ciao, {{ profile.name }}!</div>
      </div>
      <div class="profile-card" v-if="profile && currentSection === 'component1'">
        <p>
          <strong>Check-In:</strong> {{ formatDate(profile.check_in_date) }} ore:
          {{ formatTime(profile.check_in_time) }}
        </p>
        <p>
          <strong>Check-Out:</strong>
          {{ formatDate(profile.check_out_date) }} ore:
          {{ formatTime(profile.check_out_time) }}
        </p>
      </div>
      <GuestKeysComponent v-if="currentSection === 'component1'" 
                          :profile="profile" 
                          :doorsMessage="doorsMessage" 
                          :errorMessage="errorMessage" 
                          @update-checkin-profile="handleProfileUpdate" 
      />
      <div v-if="currentSection === 'component2'">
        <GuestInfoComponent />
      </div>
      <div v-if="currentSection === 'component3'">
        <GuestParkingInfoComponent />
      </div>
      <div v-if="currentSection === 'component4'">
        <GuestRestaurantsInfoComponent />
      </div>
      <div v-if="currentSection === 'component5'">
        <GuestApartmentRoomInfoComponent />
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from "../common/api.service";
import GuestKeysComponent from "../components/GuestKeysComponent.vue";
import GuestInfoComponent from "../components/GuestInfoComponent.vue";
import GuestParkingInfoComponent from "../components/GuestParkingInfoComponent.vue";
import GuestRestaurantsInfoComponent from "../components/GuestRestaurantsInfoComponent.vue";
import GuestApartmentRoomInfoComponent from "../components/GuestApartmentRoomInfoComponent.vue";

export default {
  name: "GuestDashboard",
  components: {
    GuestKeysComponent,
    GuestInfoComponent,
    GuestParkingInfoComponent,
    GuestRestaurantsInfoComponent,
    GuestApartmentRoomInfoComponent,
  },
  data() {
    return {
      profile: null, // Stato per memorizzare i dati del profilo
      loading: true, // Stato per gestire il caricamento dei dati
      isNavbarHidden: false,
      lastScrollY: window.scrollY,
      scrollY: window.scrollY,
      navHeight: 60, // Adjust based on navbar height
      doorsMessage: "", // Messaggio da mostrare se non ci sono stanze
      errorMessage: "", // Stato per memorizzare il messaggio di errore
      currentSection: "component1", // Stato per gestire la sezione corrente
    };
  },
  methods: {
    getImageUrl(name, ext) {
      return new URL(`../assets/${name}.${ext}`, import.meta.url).href;
    },
    async fetchProfileData() {
      try {
        const response = await ApiService.get("/api/checkin-profiles-guest/");
        if (response.data && response.data.length > 0) {
          this.profile = response.data[0]; // Assumi un solo profilo per l'ospite
          this.setTimers();
        }
      } catch (error) {
        console.error(
          "Errore durante il recupero dei dati del profilo:",
          error
        );
        this.errorMessage = "Errore durante il recupero dei dati del profilo.";
      } finally {
        this.loading = false; // Imposta loading su false dopo il caricamento
      }
    },
    formatTime(time) {
      // Rimuovi gli ultimi tre caratteri dell'ora
      return time ? time.slice(0, -3) : "";
    },
    formatDate(date) {
      // Formatta la data in formato dd/mm/yyyy
      const [year, month, day] = date.split("-");
      return `${day}/${month}/${year}`;
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
    setTimers() {
      const checkInDateTime = new Date(
        `${this.profile.check_in_date}T${this.profile.check_in_time}`
      );
      const checkOutDateTime = new Date(
        `${this.profile.check_out_date}T${this.profile.check_out_time}`
      );

      const now = new Date();

      if (checkInDateTime > now) {
        setTimeout(() => {
          this.$refs.guestKeysComponent.fetchRoomData();
        }, checkInDateTime - now);
      }

      if (checkOutDateTime > now) {
        setTimeout(() => {
          this.$refs.guestKeysComponent.fetchRoomData();
        }, checkOutDateTime - now);
      }
    },
    updateProfile(updatedFields) {
      this.profile = { ...this.profile, ...updatedFields };
    },
    handleProfileUpdate(updatedFields) {
      this.profile = { ...this.profile, ...updatedFields };
      this.$refs.guestKeysComponent.fetchRoomData(); // Richiama fetchRoomData quando i form vengono inviati con successo
    },
    showSection(section) {
      this.currentSection = section;
    },
  },
  created() {
    this.fetchProfileData();
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
.guest-dashboard {
  max-width: 800px;
  margin: 0 auto;
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
  left: 50%;
  transform: translateX(-50%);
}

.hidden-navbar {
  top: -60px; /* Adjust based on navbar height */
}

.nav-btn {
  background-color: transparent;
  border: none;
  color: #007bff;
  cursor: pointer;
  transition: color 0.3s, transform 0.3s;
  margin: 0 10px; /* Aggiungi spazio tra le icone */
  background: none; /* Rimuovi lo sfondo */
  border-radius: 50%; /* Rendi il bottone rotondo */
}

.nav-btn:hover {
  color: #0056b3;
}

.nav-btn:active {
  transform: scale(0.95);
}

.nav-btn:focus {
  outline: none;
  box-shadow: none;
}

.nav-icon {
  width: 24px;
  height: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.greeting {
  font-size: 18px;
  font-weight: bold;
}

.apartment-name {
  font-size: 18px;
  font-weight: bold;
}

.profile-card {
  background-color: #e0f7e9; /* Sfondoverde chiaro */
  border: 1px solid #ccc; /* Bordo */
  display: flex;
  flex-direction: column;
  font-size: 12px;
  margin-bottom: 5px;
  text-align: start; /* Aggiunto text-align: start */
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Altezza del contenitore dello spinner */
}

.spinner-content {
  text-align: center;
  text-align: left; /* Aggiunto text-align: left */
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #09f;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.info-card {
  background-color: white;
  color: black;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  width: calc(33.333% - 20px);
  font-size: 14px;
  text-align: start; /* Aggiunto text-align: start */
  text-align: left; /* Aggiunto text-align: left */
}

</style>
