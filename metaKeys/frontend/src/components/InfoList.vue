<template>
  <div>
    <!-- Spinner per il caricamento degli appartamenti -->
    <div v-if="isLoadingApartments" class="spinner-overlay">
      <div class="spinner"></div>
    </div>
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal-create-info">
        <button class="close-button" @click="closeModal">&times;</button>
        <div class="create-info">
          <CreateInfoModal @close="closeModal" />
        </div>
      </div>
    </div>
    <div v-if="isUpdateModalOpen" class="modal-overlay">
      <div class="modal-update-info">
        <button class="close-button" @click="closeUpdateModal">&times;</button>
        <UpdateInfo
          :info="selectedInfo"
          @close="closeUpdateModal"
          @update-info="updateSelectedInfo"
        />
      </div>
    </div>
    <div v-if="selectedInfo" class="info-detail">
      <InfoDetail
        :info="selectedInfo"
        @close="deselectInfo"
        @edit="openUpdateModal"
        @update-info="updateSelectedInfo"
        @delete-info="removeInfo"
      />
    </div>
    <div v-else class="info-list">
      <div class="info-list-header">
        <div class="form-group">
          <select v-model="selectedApartment" @change="fetchInfosAndRooms">
            <option v-for="apartment in apartments" :key="apartment.id" :value="apartment.id">
              {{ apartment.name }}
            </option>
          </select>
        </div>
        <button class="btn btn-primary" @click="openModal">Aggiungi</button>
      </div>
      <div v-for="(infos, type) in groupedInfos" :key="type">
        <h2 class="type-header" @click="toggleType(type)">{{ typeTranslations[type] }}</h2>
        <div v-if="isTypeOpen(type)" class="dropdown-content">
          <div v-if="type === 'room_info'">
            <div v-for="(roomInfos, roomId) in infos" :key="roomId">
              <h4 class="room-name" @click="toggleRoom(roomId)">{{ roomNames[roomId] }}</h4>
              <transition name="slide">
                <div v-if="isRoomOpen(roomId)" class="cards-container">
                  <div
                    class="card"
                    v-for="info in roomInfos"
                    :key="info.id"
                    @click="selectInfo(info)"
                  >
                    <h3>{{ info.title }}</h3>
                  </div>
                </div>
              </transition>
            </div>
          </div>
          <div v-else class="cards-container">
            <div
              class="card"
              v-for="info in infos"
              :key="info.id"
              @click="selectInfo(info)"
            >
              <h3>{{ info.title }}</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from 'vuex';
import CreateInfoModal from "./CreateInfo.vue";
import UpdateInfo from "./UpdateInfo.vue";
import InfoDetail from "./InfoDetail.vue";

const typeTranslations = {
  general: 'Generale',
  parking_info: 'Informazioni Parcheggio',
  restaurants: 'Ristoranti',
  nearby: 'Nei Paraggi',
  places_to_visit: 'Cosa Visitare',
  apartment_info: 'Informazioni Appartamento',
  room_info: 'Informazioni Camera'
};

export default {
  name: "InfoList",
  components: {
    CreateInfoModal,
    UpdateInfo,
    InfoDetail,
  },
  setup() {
    const store = useStore();
    const apartments = computed(() => store.state.apartments.apartments);
    const selectedApartment = ref(apartments.value.length > 0 ? apartments.value[0].id : null);
    const isModalOpen = ref(false);
    const isUpdateModalOpen = ref(false);
    const isLoadingApartments = ref(false);
    let isRemoving = ref(false);
    const rooms = ref([]);
    const roomNames = ref({});
    const isRoomsFetched = ref(false);
    const openTypes = ref([]);
    const openRooms = ref([]);

    const fetchInfos = async () => {
      if (selectedApartment.value && !store.state.infos.isFetched) {
        await store.dispatch('fetchInfos', selectedApartment.value);
      }
    };

    const fetchRooms = async () => {
      if (selectedApartment.value && !store.state.apartments.fetchedRooms[selectedApartment.value]) {
        try {
          await store.dispatch('fetchRooms', selectedApartment.value);
          rooms.value = store.getters.getRoomsByApartment(selectedApartment.value);
          roomNames.value = rooms.value.reduce((acc, room) => {
            acc[room.id] = room.name;
            return acc;
          }, {});
          isRoomsFetched.value = true;
        } catch (error) {
          console.error("Errore nel recupero delle camere:", error);
        }
      } else {
        rooms.value = store.getters.getRoomsByApartment(selectedApartment.value);
        roomNames.value = rooms.value.reduce((acc, room) => {
          acc[room.id] = room.name;
          return acc;
        }, {});
        isRoomsFetched.value = true;
      }
    };

    const fetchInfosAndRooms = async () => {
      await fetchInfos();
      await fetchRooms();
    };

    const fetchApartments = async () => {
      isLoadingApartments.value = true;
      await store.dispatch('fetchApartments');
      isLoadingApartments.value = false;
      if (apartments.value.length > 0 && !selectedApartment.value) {
        selectedApartment.value = apartments.value[0].id;
        fetchInfosAndRooms();
      }
    };

    const openModal = () => {
      isModalOpen.value = true;
    };

    const closeModal = async () => {
      isModalOpen.value = false;
      await store.dispatch('fetchInfos', selectedApartment.value);
    };

    const openUpdateModal = () => {
      isUpdateModalOpen.value = true;
    };

    const closeUpdateModal = () => {
      isUpdateModalOpen.value = false;
    };

    const selectInfo = (info) => {
      store.dispatch('selectInfo', info);
    };

    const deselectInfo = () => {
      store.dispatch('deselectInfo');
    };

    const updateSelectedInfo = async (updatedInfo) => {
      await store.dispatch('updateInfo', updatedInfo);
      store.dispatch('selectInfo', updatedInfo);
    };

    const removeInfo = async (infoId) => {
      if (isRemoving.value) return;
      isRemoving.value = true;
      try {
        await store.dispatch('deleteInfo', infoId);
        deselectInfo();
      } catch (error) {
        console.error("Errore nell'eliminazione dell'informazione:", error);
      } finally {
        isRemoving.value = false;
      }
    };

    const filteredInfos = computed(() => {
      if (selectedApartment.value) {
        return store.getters.filteredInfos(selectedApartment.value);
      }
      return [];
    });

    const groupedInfos = computed(() => {
      const groups = {};
      filteredInfos.value.forEach(info => {
        if (info.type === 'room_info') {
          if (!groups[info.type]) {
            groups[info.type] = {};
          }
          if (!groups[info.type][info.room]) {
            groups[info.type][info.room] = [];
          }
          groups[info.type][info.room].push(info);
        } else {
          if (!groups[info.type]) {
            groups[info.type] = [];
          }
          groups[info.type].push(info);
        }
      });
      return groups;
    });

    const selectedInfo = computed(() => store.state.infos.selectedInfo);

    const toggleType = (type) => {
      if (openTypes.value.includes(type)) {
        openTypes.value = openTypes.value.filter(t => t !== type);
      } else {
        openTypes.value.push(type);
      }
    };

    const isTypeOpen = (type) => {
      return openTypes.value.includes(type);
    };

    const toggleRoom = (roomId) => {
      if (openRooms.value.includes(roomId)) {
        openRooms.value = openRooms.value.filter(r => r !== roomId);
      } else {
        openRooms.value.push(roomId);
      }
    };

    const isRoomOpen = (roomId) => {
      return openRooms.value.includes(roomId);
    };

    onMounted(() => {
      fetchApartments();
      fetchInfosAndRooms();
    });

    watch(selectedApartment, (newApartment) => {
      if (newApartment) {
        fetchInfosAndRooms();
      }
    });

    return {
      selectedApartment,
      isModalOpen,
      isUpdateModalOpen,
      selectedInfo,
      apartments,
      openModal,
      closeModal,
      openUpdateModal,
      closeUpdateModal,
      selectInfo,
      deselectInfo,
      updateSelectedInfo,
      removeInfo,
      filteredInfos,
      groupedInfos,
      isLoadingApartments,
      typeTranslations,
      roomNames,
      toggleType,
      isTypeOpen,
      toggleRoom,
      isRoomOpen,
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

.modal-create-info,
.modal-update-info {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  padding: 20px;
  overflow-y: auto;
  z-index: 1000;
}

.btn-primary {
  background-color: #28a745;
  color: white;
}

.btn-primary:hover {
  background-color: #218838;
}

.create-info {
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

.info-list,
.info-detail {
  padding: 20px;
  font-size: 1em;
}

.info-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 1em;
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
  font-size: 1em;
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
  font-size: 1.125em;
}

.card p {
  margin: 5px 0;
  font-size: 1em;
}

/* Spinner styles */
.spinner-overlay {
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

.spinner {
  border: 8px solid rgba(0, 0, 0, 0.1);
  border-top: 8px solid #000;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.type-header {
  background-color: #0056b3;
  color: white;
  padding: 10px;
  cursor: pointer;
  border: 1px solid #dee2e6;
  margin-bottom: 0;
  font-size: 1em;
}

.room-name {
  font-size: 0.875em;
  cursor: pointer;
  padding: 5px;
  border: 1px solid #dee2e6;
  margin-bottom: 0;
}

.dropdown-content {
  border: 1px solid #dee2e6;
  border-top: none;
  padding: 10px;
  margin-bottom: 10px;
  overflow: hidden;
  transition: height 1s ease-in-out;
}

.slide-enter-active {
  transition: height 1s ease-in-out;
}

.slide-enter, .slide-leave-to {
  height: 0;
}
</style>
