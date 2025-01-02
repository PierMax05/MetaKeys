<template>
  <div>
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal-create-apartment">
        <button class="close-button" @click="closeModal">&times;</button>
        <div class="create-aparment">
          <CreateApartmentModal @close="closeModal" @apartment-created="addApartmentToList" />
        </div>
      </div>
    </div>
    <div v-if="isUpdateModalOpen" class="modal-overlay">
      <div class="modal-update-apartment">
        <button class="close-button" @click="closeUpdateModal">&times;</button>
        <UpdateApartment
          :apartment="selectedApartment"
          @close="closeUpdateModal"
          @update-apartment="updateSelectedApartment"
          @delete-apartment="removeApartment"
        />
      </div>
    </div>
    <div v-if="selectedApartment" class="apartment-detail">
      <ApartmentDetail
        v-if="selectedApartment"
        :apartmentId="selectedApartment.id"
        @close="deselectApartment"
        @edit="openUpdateModal"
        @update-apartment="updateSelectedApartment"
        @delete-apartment="removeApartment"
      />
    </div>
    <div v-else class="apartments-list">
      <div class="header">
        <div class="left-buttons">
          <button v-if="hasShellyDevices" class="btn btn-shelly" @click="$emit('showShellyStatus')">
            <span>Shelly</span>
          </button>
        </div>
        <button class="btn btn-primary" @click="openModal">Crea Struttura</button>
      </div>
      <div class="cards-container">
        <div
          class="card"
          v-for="apartment in apartments"
          :key="apartment.id"
          @click="selectApartment(apartment)"
        >
          <h3>{{ apartment.name }}</h3>
          <p>{{ apartment.address }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import CreateApartmentModal from "./CreateApartment.vue";
import UpdateApartment from "./UpdateApartment.vue";
import ApartmentDetail from "./ApartmentDetail.vue";
import CreateDoorComponent from "./CreateDoorComponent.vue";
import CreateRoomComponent from "./CreateRoomComponent.vue";

export default {
  name: "ApartmentsList",
  components: {
    CreateApartmentModal,
    UpdateApartment,
    ApartmentDetail,
    CreateDoorComponent, // Aggiungi il nuovo componente qui
    CreateRoomComponent, // Aggiungi il nuovo componente qui
  },
  setup(props, { emit }) {
    const store = useStore();
    const apartments = computed(() => store.state.apartments.apartments);
    const hasShellyDevices = computed(() => store.getters.hasShellyDevices);
    const isModalOpen = ref(false);
    const isUpdateModalOpen = ref(false);
    const selectedApartment = ref(null);

    const fetchApartments = async () => {
      await store.dispatch('fetchApartments');
    };

    const openModal = () => {
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
      fetchApartments(); // Ricarica la lista degli appartamenti dopo la creazione
    };

    const openUpdateModal = () => {
      isUpdateModalOpen.value = true;
    };

    const closeUpdateModal = () => {
      fetchApartments(); // Ricarica la lista degli appartamenti dopo l'aggiornamento
      isUpdateModalOpen.value = false;
    };

    const selectApartment = (apartment) => {
      selectedApartment.value = apartment;
    };

    const deselectApartment = () => {
      selectedApartment.value = null;
    };

    const updateSelectedApartment = (updatedApartment) => {
      selectedApartment.value = updatedApartment;
      store.commit('SET_APARTMENTS', store.state.apartments.apartments.map(apartment => apartment.id === updatedApartment.id ? updatedApartment : apartment));
    };

    const removeApartment = (apartmentId) => {
      store.commit('SET_APARTMENTS', store.state.apartments.apartments.filter(apartment => apartment.id !== apartmentId));
      closeUpdateModal();
      deselectApartment();
    };

    const addApartmentToList = (newApartment) => {
      store.commit('SET_APARTMENTS', [...store.state.apartments.apartments, newApartment]);
    };

    onMounted(() => {
      fetchApartments();
    });

    return {
      apartments,
      hasShellyDevices,
      isModalOpen,
      isUpdateModalOpen,
      selectedApartment,
      openModal,
      closeModal,
      openUpdateModal,
      closeUpdateModal,
      selectApartment,
      deselectApartment,
      updateSelectedApartment,
      removeApartment,
      addApartmentToList,
    };
  },
};
</script>

<style scoped>
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

.modal-create-apartment,
.modal-update-apartment {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  z-index: 1000;
  width: 100%;
  max-width: 800px;
}

.btn-primary {
  background-color: #28a745;
  color: white;
}

.btn-primary:hover {
  background-color: #218838;
}

.btn-shelly {
  background-color: #007bff;
  color: white;
}

.btn-shelly:hover {
  background-color: #0056b3;
}

.create-aparment {
  margin-top: 20px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  background-color: transparent;
  color: #000;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.apartments-list,
.apartment-detail {
  padding: 20px;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  padding: 20px;
  gap: 20px;
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 20px;
  width: calc(33.333% - 20px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .card {
    width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .card {
    width: 100%;
  }
}

.card h3 {
  margin-top: 0;
}

.card p {
  margin: 5px 0;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.left-buttons {
  display: flex;
  gap: 10px;
}
</style>
