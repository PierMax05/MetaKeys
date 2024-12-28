<template>
  <div class="guest-apartment-room-info">
    <div v-if="loading" class="spinner-container">
      <div class="spinner-content">
        <h2>Caricamento...</h2>
        <div class="spinner"></div>
      </div>
    </div>
    <div v-else>
      <div v-if="apartmentInfos.length">
        <div class="info-type">
          <h5>Informazioni sull'Appartamento</h5>
        </div>
        <div class="info-cards">
          <div class="info-cards-container">
            <div v-for="(info, index) in apartmentInfos" :key="info.id" 
                 :class="['info-card', { 'active': activeCard === info.id, 'first-card': index === 0, 'last-card': index === apartmentInfos.length - 1, 'scrollable': activeCard === info.id }]"
                 @click="setActiveCard(info.id, $event)">
              <h4>{{ info.title }}</h4>
              <p>{{ info.info }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-if="roomInfos.length">
        <div class="info-type">
          <h5>Informazioni sulla Stanza</h5>
        </div>
        <div class="info-cards">
          <div class="info-cards-container">
            <div v-for="(info, index) in roomInfos" :key="info.id" 
                 :class="['info-card', { 'active': activeCard === info.id, 'first-card': index === 0, 'last-card': index === roomInfos.length - 1, 'scrollable': activeCard === info.id }]"
                 @click="setActiveCard(info.id, $event)">
              <h4>{{ info.title }}</h4>
              <p>{{ info.info }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!apartmentInfos.length && !roomInfos.length">
        <p>Nessuna informazione disponibile.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'GuestApartmentRoomInfoComponent',
  data() {
    return {
      loading: true,
      activeCard: null,
    };
  },
  computed: {
    ...mapState({
      infos: state => state.infos.infos,
    }),
    apartmentInfos() {
      return this.infos.filter(info => info.type === 'apartment_info');
    },
    roomInfos() {
      return this.infos.filter(info => info.type === 'room_info');
    },
  },
  methods: {
    ...mapActions(['fetchInfos']),
    setActiveCard(cardId, event) {
      this.activeCard = this.activeCard === cardId ? null : cardId;
      if (this.activeCard) {
        const cardElement = event.target.closest('.info-card');
        cardElement.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
      }
    },
  },
  async created() {
    await this.fetchInfos();
    this.loading = false;
  },
};
</script>

<style scoped>
.guest-apartment-room-info {
  padding: 20px;
}

.info-type {
  background-color: #1a237e; /* Blu scuro */
  color: white;
  padding: 5px;
  margin-top: 10px;
  cursor: pointer;
  font-size: 14px; /* Testo più piccolo */
}

.info-cards {
  overflow-x: auto; /* Aggiunto overflow-x: auto */
  white-space: nowrap; /* Aggiunto white-space: nowrap */
  padding-bottom: 10px; /* Aggiunto padding-bottom */
}

.info-cards-container {
  display: inline-flex; /* Aggiunto display: inline-flex */
  gap: 20px;
}

.info-card {
  background-color: white;
  color: black;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  width: 300px; /* Modificato width */
  font-size: 14px;
  text-align: start; /* Aggiunto text-align: start */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin: 50px 0; /* Aumentato margine sopra e sotto */
  height: 250px; /* Altezza ridotta */
  white-space: normal; /* Permetti al testo di andare a capo */
  overflow: hidden; /* Evita che il testo esca fuori dalle card non selezionate */
}

.info-card.scrollable {
  overflow-y: auto; /* Permetti lo scroll verticale solo quando attivo */
}

.info-card.active {
  transform: scale(1.2); /* Aumentato scale */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Aumentato box-shadow */
  overflow-y: auto; /* Permetti lo scroll verticale */
}

.info-card.first-card.active {
  transform-origin: left center;
}

.info-card.last-card.active {
  transform-origin: right center;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.spinner-content {
  text-align: center;
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

@media (max-width: 768px) {
  .info-card {
    width: 250px; /* Modificato width */
    margin: 40px 0; /* Elimina margine laterale */
  }
}

@media (max-width: 480px) {
  .info-card {
    width: 200px; /* Modificato width */
    margin: 40px 0; /* Elimina margine laterale */
  }
}
</style>
