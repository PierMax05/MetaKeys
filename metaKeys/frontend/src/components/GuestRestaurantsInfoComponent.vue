<template>
  <div class="guest-restaurants-info">
    <div v-if="loading" class="spinner-container">
      <div class="spinner-content">
        <h2>Caricamento...</h2>
        <div class="spinner"></div>
      </div>
    </div>
    <div v-else>
      <div v-if="restaurantsInfos.length">
        <div class="info-type">
          <h5>Ristoranti Consigliati</h5>
        </div>
        <div class="info-cards">
          <div class="info-cards-container">
            <div v-for="(info, index) in restaurantsInfos" :key="info.id" 
                 :class="['info-card', { 'active': activeCard === info.id, 'first-card': index === 0, 'last-card': index === restaurantsInfos.length - 1, 'scrollable': activeCard === info.id }]"
                 @click="setActiveCard(info.id, $event)">
              <div :class="['card-content', { 'scrollable': activeCard === info.id }]">
                <h4>{{ info.title }}</h4>
                <p>{{ info.info }}</p>
              </div>
              <div v-if="info.google_link && info.google_link.trim() !== ''">
                <br>
                <div class="card-footer">
                  <a :href="info.google_link" target="_blank">Apri in Mappe</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>Nessuna informazione sui ristoranti disponibile.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'GuestRestaurantsInfoComponent',
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
    restaurantsInfos() {
      return this.infos.filter(info => info.type === 'restaurants');
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
.guest-restaurants-info {
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
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: white;
  color: black;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  width: 300px; /* Modificato width */
  font-size: 14px;
  text-align: start; /* Aggiunto text-align: start */
  transition: transform 0.3s ease, box-shadow 0.3s ease, z-index 0.3s ease; /* Aggiunto z-index */
  margin: 50px 0; /* Aumentato margine sopra e sotto */
  white-space: normal; /* Permetti al testo di andare a capo */
  height: 250px; /* Altezza ridotta */
  overflow: hidden; /* Evita che il testo esca fuori dalle card non selezionate */
  position: relative; /* Aggiunto per il posizionamento del footer */
  z-index: 1; /* Aggiunto per la sovrapposizione */
}

.card-content {
  overflow-y: hidden; /* Disabilita lo scroll verticale per il contenuto */
  flex-grow: 1; /* Permetti al contenuto di crescere */
}

.card-content.scrollable {
  overflow-y: auto; /* Permetti lo scroll verticale solo quando attivo */
}

.info-card.scrollable {
  overflow-y: auto; /* Permetti lo scroll verticale solo quando attivo */
}

.info-card.active {
  transform: scale(1.2); /* Aumentato scale */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Aumentato box-shadow */
  overflow-y: auto; /* Permetti lo scroll verticale */
  z-index: 10; /* Porta la card attiva in primo piano */
}

.info-card.first-card.active {
  transform-origin: left center;
}

.info-card.last-card.active {
  transform-origin: right center;
}

.info-card .card-footer {
  position: absolute; /* Fissa il footer in basso */
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: white; /* Aggiunto per migliorare la visibilità */
  padding-top: 10px;
  text-align: center;
}

.info-card .card-footer a {
  color: #1a237e;
  text-decoration: none;
  font-weight: bold;
}

.info-card .card-footer a:hover {
  text-decoration: underline;
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
