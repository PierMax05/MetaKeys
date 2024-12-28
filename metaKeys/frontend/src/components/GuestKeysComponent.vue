<template>
  <div>
    <div v-if="errorMessage" class="alert alert-danger mt-2">
      {{ errorMessage }}
    </div>
    <transition name="fade">
      <div class="doors-list" v-if="room || localDoorsMessage">
        <p v-if="room" class="room-name"><strong>{{ room.name }}</strong></p>
        <div v-if="room">
          <div class="rooms-container">
            <div class="room-item">
              <div class="doors-container">
                <div v-for="door in room.doors || []" :key="door.id" class="door-item" :class="{ opened: door.opened, selected: selectedDoor === door.id }" @click="selectDoor(door.id, $event)">
                  <div class="door-content">
                    <h4 class="door-name">{{ door.name }}</h4>
                    <div v-if="!door.opened" :class="{ 'instructions-container': true, 'scrollable': selectedDoor === door.id }">
                      <strong>Istruzioni:</strong>
                      <p>{{ door.instructions }}</p>
                    </div>
                    <p v-if="door.opened" class="opened-text">APERTO!</p>
                    <p v-if="door.access_type === 'codice'" class="code-container"><strong>Codice di Accesso:</strong> {{ door.access_code }}</p>
                    <div v-if="door.access_type === 'shelly' && !door.opened" class="cpc-container">
                      <label :for="'cpc-input-' + door.id"><strong>CPC:</strong></label>
                      <input :id="'cpc-input-' + door.id" type="text" v-model="door.cpcInput" class="form-control"/>
                      <button @click="checkCPC(door)" class="btn btn-success cpc-button">Apri</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else v-html="localDoorsMessage"></div>
      </div>
    </transition>
    <div v-if="loading" class="spinner-container">
      <div class="spinner-content">
        <h2>Caricamento...</h2>
        <div class="spinner"></div>
      </div>
    </div>
    <div
      v-if="
        profile && profile.require_billing_info == true &&
        profile.got_billing_info == false
      "
    >
      <h3>Informazioni di Fatturazione</h3>
      <BillingInfoForm
        v-if="profile"
        :checkinProfile="profile"
        :visible="profile.require_billing_info && !profile.got_billing_info"
        @update-checkin-profile="updateProfile"
      />
    </div>
    <div
      v-if="
        profile && (profile.require_registration_form == true ||
          profile.require_document_photo == true) &&
        profile.got_registration_form == false
      "
    >
      <h3>Informazioni sugli Ospiti</h3>
      <GuestForm
        :checkinProfile="profile"
        @update-checkin-profile="updateProfile"
      />
    </div>
    <div v-if="fixedErrorMessage" class="fixed-error-card">
      {{ fixedErrorMessage }}
    </div>
  </div>
</template>

<script>
import GuestForm from "./GuestForm.vue";
import BillingInfoForm from "./BillingInfoForm.vue";
import ApiService from "../common/api.service";

export default {
  name: "GuestKeysComponent",
  components: {
    GuestForm,
    BillingInfoForm,
  },
  props: {
    profile: Object,
    doorsMessage: String,
    errorMessage: String,
  },
  data() {
    return {
      room: null, // Stato per memorizzare i dati della stanza
      fixedErrorMessage: "", // Stato per il messaggio di errore fisso
      loading: true, // Stato per gestire il caricamento dei dati
      selectedDoor: null, // Stato per la porta selezionata
      localDoorsMessage: this.doorsMessage, // Stato locale per il messaggio delle porte
    };
  },
  methods: {
    formatTime(time) {
      // Rimuovi gli ultimi tre caratteri dell'ora
      return time ? time.slice(0, -3) : "";
    },
    formatDate(date) {
      // Formatta la data in formato dd/mm/yyyy
      const [year, month, day] = date.split("-");
      return `${day}/${month}/${year}`;
    },
    sortedDoors(doors) {
      return doors ? doors.slice().sort((a, b) => a.priority - b.priority) : [];
    },
    updateProfile(updatedFields) {
      this.$emit("update-checkin-profile", updatedFields);
    },
    async fetchRoomData() {
      try {
        const response = await ApiService.get("/api/guest-room/");
        if (response.data.detail) {
          this.localDoorsMessage = response.data.detail;
        } else {
          this.room = response.data[0]; // Aggiorna lo stato della stanza
          this.room.doors = this.sortedDoors(this.room.doors); // Ordina le porte dopo aver ottenuto i dati
          this.selectedDoor = this.room.doors[0].id; // Seleziona automaticamente la prima porta
          this.$nextTick(() => {
            const firstCardElement = this.$el.querySelector('.door-item');
            if (firstCardElement) {
              firstCardElement.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
            }
          });
        }
      } catch (error) {
        console.error(
          "Errore durante il recupero dei dati della stanza:",
          error
        );
        this.errorMessage = "Errore durante il recupero dei dati della stanza.";
      } finally {
        this.loading = false; // Imposta loading su false dopo il caricamento
      }
    },
    async checkCPC(door) {
      try {
        const response = await ApiService.post("/api/check-cpc/", {
          door_id: door.id,
          cpc: door.cpcInput,
        });
        console.log(response.data.detail);
        this.fixedErrorMessage = ""; // Resetta il messaggio di errore fisso se il CPC è corretto

        // Mostra "APERTO!" e cambia lo stile della card
        door.opened = true;
        setTimeout(() => {
          door.opened = false;
        }, 5000);
      } catch (error) {
        console.error("Errore durante il controllo del CPC:", error);
        this.fixedErrorMessage = "ATTENZIONE! CPC errato."; // Imposta il messaggio di errore fisso
      }
    },
    selectDoor(doorId, event) {
      this.selectedDoor = doorId;
      const cardElement = event.target.closest('.door-item');
      cardElement.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
    },
  },
  created() {
    this.fetchRoomData();
  },
};
</script>

<style scoped>
.message-card {
  background-color: white;
  border: 1px solid black; /* Aggiungi un bordo visibile */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.doors-list {
  background-color: white;
  border-radius: 8px; /* Angoli arrotondati */
  transition: all 0.3s ease; /* Aggiungi una transizione */
}

.rooms-container {
  display: flex;
  overflow-x: auto; /* Abilita lo scrolling orizzontale */
}

.doors-container {
  display: flex;
  flex-wrap: nowrap; /* Impedisce il wrapping delle card */
  overflow-x: auto; /* Abilita lo scrolling orizzontale */
  padding-inline: 50px; /* Spazio laterale */
}

.doors-list ul {
  list-style-type: none;
  padding: 0;
}

.doors-list li {
  background-color: white;
  margin-bottom: 10px;
}

.room-item {
  display: flex;
  flex-direction: column;
  margin-right: 10px; /* Spazio tra le card */
}

.room-name {
  text-align: left;
}

.door-item {
  background-color: white;
  color: black;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px;
  width: 300px; /* Larghezza delle card impostata al 90% dello schermo */
  font-size: 14px;
  text-align: start; /* Aggiunto text-align: start */
  transition: transform 0.3s ease, box-shadow 0.3s ease, z-index 0.3s ease;
  margin: 60px 0; /* Margine sopra e sotto */
  height: 500px; /* Altezza delle card impostata all'80% dello schermo */
  white-space: normal; /* Permetti al testo di andare a capo */
  overflow: hidden; /* Evita che il testo esca fuori dalle card non selezionate */
  position: relative; /* Aggiunto per posizionare il cpc-container */
}

.door-item.scrollable {
  overflow-y: auto; /* Permetti lo scroll verticale solo quando attivo */
}

.door-item.selected {
  transform: scale(1.2); /* Aumentato scale */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Aumentato box-shadow */
  overflow-y: auto; /* Permetti lo scroll verticale */
  z-index: 1; /* Porta la card selezionata sopra le altre */
}

.door-content {
  display: flex;
  flex-direction: column;
  text-align: left;
  height: 100%; /* Altezza completa per il contenuto */
}

.door-name {
  font-size: 12px; /* Rimpicciolisci il testo del nome della porta */
}

.instructions-container {
  border: 1px solid #ccc; /* Aggiungi un bordo */
  padding: 10px;
  max-height: calc(100% - 80px); /* Altezza massima per evitare sovrapposizione con cpc-container */
  overflow: hidden; /* Evita che il testo esca fuori dalle card non selezionate */
  text-overflow: ellipsis; /* Aggiungi ellissi per il testo che esce fuori */
}

.instructions-container.scrollable {
  overflow-y: auto; /* Abilita lo scroll verticale solo per la card selezionata */
}

.opened-text {
  color: green;
  font-size: 24px;
  font-weight: bold;
}

.cpc-container,
.code-container {
  border-top: 1px solid #ccc; /* Aggiunto un bordo sopra */
  display: flex;
  align-items: center;
  position: absolute; /* Posiziona il cpc-container in basso */
  bottom: 10px; /* Distanza dal fondo della card */
  left: 10px; /* Distanza dal lato sinistro della card */
  right: 10px; /* Distanza dal lato destro della card */
  font-size: 12px; /* Rimpicciolisci il contenuto */
}

.cpc-button {
  border-radius: 50%;
  margin-left: 10px;
  padding: 10px 10px;
  font-size: 12px; /* Rimpicciolisci il contenuto */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

.fixed-error-card {
  position: fixed;
  bottom: 10%;
  left: 10%;
  right: 10%;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 10px;
  text-align: center;
  z-index: 1000;
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

@media (max-width: 600px) {
  .door-item {
    height: 50vh; /* Altezza delle card impostata al 50% dello schermo per schermi piccoli */
    width: 70vw; /* Larghezza delle card impostata al 70% dello schermo per schermi piccoli */
  }
}
</style>
