<template>
  <div class="apartment-detail">
    <button class="close-button" @click="$emit('close')">&larr;</button>
    <div class="details">
      <h2>{{ apartment.name }}</h2>
      <div class="button-group">
        <button class="action-button" :class="{ selected: selectedButton === 'apartment' }" @click="selectButton('apartment')">Struttura</button>
        <div class="divider"></div>
        <button class="action-button" :class="{ selected: selectedButton === 'doors' }" @click="selectButton('doors'); openDoorsModal()">Porte</button>
        <div class="divider"></div>
        <button class="action-button" :class="{ selected: selectedButton === 'rooms' }" @click="selectButton('rooms')">Camere</button>
      </div>
      <div class="apartment" v-if="selectedButton === 'apartment'">
        <div class="apartment-header">
          <h3>Struttura</h3>
          <button class="btn btn-primary" @click="openUpdateModal">Modifica Struttura</button>
        </div>
        <div v-if="isUpdateModalOpen">
          <UpdateApartment
            :apartmentId="apartment.id"
            @close="closeUpdateModal"
            @update-apartment="handleUpdate"
            @delete-apartment="handleDelete"
          />
        </div>
        <div v-else>
          <p><strong>Nome:</strong> {{ apartment.name }}</p>
          <p><strong>Indirizzo:</strong> {{ apartment.address }}</p>
          <p v-if="apartment.server_uri"><strong>URI del Server:</strong> {{ apartment.server_uri }}</p>
          <div class="auth-key-container" v-if="apartment.auth_key">
            <p><strong>Chiave di Autenticazione:</strong></p>
            <div class="auth-key">{{ apartment.auth_key }}</div>
          </div>
        </div>
      </div>
      <div class="doors" v-if="selectedButton === 'doors'">
        <div class="apartment-header">
          <h3>Porte</h3>
          <button class="btn btn-primary" @click="openCreateModal">Crea Porta</button>
        </div>
        <div v-if="isCreateModalOpen">
          <CreateDoorComponent
            :apartmentId="apartment.id"
            @closeCM="closeCreateModal"
            @doorCreated="handleDoorCreated"
          />
        </div>
        <div v-else-if="isEditDoorModalOpen">
          <EditDoorModal
            :door="selectedDoor"
            :apartmentId="apartment.id"
            @closeEM="closeEditDoorModal"
            @doorUpdated="handleDoorUpdated"
            @doorDeleted="handleDoorDeleted"
          />
        </div>
        <div v-else>
          <div class="rooms-grid" v-if="doors.length">
            <div class="room-card" v-for="door in doors" :key="door.id" @click="openEditDoorModal(door)">
              <h4>{{ door.name }}</h4>
            </div>
          </div>
          <p v-else>Non ci sono porte per l'appartamento selezionato.</p>
      </div>
        </div>
      <div class="rooms" v-if="selectedButton === 'rooms'">
        <div class="apartment-header">
          <h3>Camere</h3>
          <button class="btn btn-primary" @click="openCreateRoomModal">Crea Camera</button>
        </div>
        <div v-if="isCreateRoomModalOpen">
          <CreateRoomComponent
            :doors="doors"
            :apartmentId="apartment.id"
            @closeCM="closeCreateRoomModal"
            @roomCreated="handleRoomCreated"
          />
        </div>
        <div v-else-if="isEditRoomModalOpen">
          <EditRoomModal
            :room="selectedRoom"
            :apartment="apartment"
            :doors="doors"
            @closeEM="closeEditRoomModal"
            @roomUpdated="handleRoomUpdated"
            @roomDeleted="handleRoomDeleted"
          />
        </div>
        <div v-else>
          <div class="rooms-grid" v-if="rooms.length">
            <div class="room-card" v-for="room in rooms" :key="room.id" @click="openEditRoomModal(room)">
              <h4>{{ room.name }}</h4>
            </div>
          </div>
          <p v-else>Non ci sono camere per l'appartamento selezionato.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import ApiService from "../common/api.service.js";
import CreateDoorComponent from "./CreateDoorComponent.vue";
import EditDoorModal from "./EditDoorModal.vue";
import CreateRoomComponent from "./CreateRoomComponent.vue";
import EditRoomModal from "./EditRoomModal.vue";
import UpdateApartment from "./UpdateApartment.vue";

export default {
  name: "ApartmentDetail",
  components: {
    CreateDoorComponent,
    EditDoorModal,
    CreateRoomComponent,
    EditRoomModal,
    UpdateApartment,
  },
  props: {
    apartmentId: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const store = useStore();
    const apartment = computed(() => store.state.apartments.apartments.find(a => a.id === props.apartmentId));
    const rooms = computed(() => store.state.apartments.rooms[props.apartmentId] || []);
    const isDoorsModalOpen = ref(false);
    const isCreateModalOpen = ref(false);
    const isEditDoorModalOpen = ref(false);
    const isCreateRoomModalOpen = ref(false);
    const isEditRoomModalOpen = ref(false);
    const isUpdateModalOpen = ref(false);
    const doors = ref([]);
    const selectedButton = ref('apartment');
    const selectedDoor = ref(null);
    const selectedRoom = ref(null);

    const fetchDoors = async () => {
      try {
        const response = await ApiService.get(`/api/doors/?apartment=${apartment.value.id}`);
        doors.value = response.data;
      } catch (error) {
        console.error("Errore nel recupero delle porte:", error);
      }
    };

    const fetchRooms = async () => {
      await store.dispatch('fetchRooms', props.apartmentId);
    };

    const openDoorsModal = () => {
      isDoorsModalOpen.value = true;
      fetchDoors();
    };

    const closeDoorsModal = () => {
      isDoorsModalOpen.value = false;
    };

    const openCreateModal = () => {
      isCreateModalOpen.value = true;
    };

    const closeCreateModal = () => {
      isCreateModalOpen.value = false;
    };

    const openEditDoorModal = (door) => {
      selectedDoor.value = door;
      isEditDoorModalOpen.value = true;
    };

    const closeEditDoorModal = () => {
      isEditDoorModalOpen.value = false;
    };

    const openCreateRoomModal = () => {
      fetchDoors();
      isCreateRoomModalOpen.value = true;
    };

    const closeCreateRoomModal = () => {
      isCreateRoomModalOpen.value = false;
    };

    const openEditRoomModal = (room) => {
      fetchDoors();
      selectedRoom.value = room;
      isEditRoomModalOpen.value = true;
    };

    const closeEditRoomModal = () => {
      isEditRoomModalOpen.value = false;
    };

    const openUpdateModal = () => {
      isUpdateModalOpen.value = true;
    };

    const closeUpdateModal = () => {
      isUpdateModalOpen.value = false;
    };

    const handleDoorCreated = () => {
      closeCreateModal();
      openDoorsModal();
    };

    const handleDoorUpdated = () => {
      closeEditDoorModal();
      openDoorsModal();
    };

    const handleDoorDeleted = () => {
      closeEditDoorModal();
      openDoorsModal();
    };

    const handleRoomCreated = () => {
      closeCreateRoomModal();
      fetchRooms();
    };

    const handleRoomUpdated = () => {
      closeEditRoomModal();
      fetchRooms();
    };

    const handleRoomDeleted = () => {
      closeEditRoomModal();
      fetchRooms();
    };

    const handleUpdate = (updatedApartment) => {
      emit("update-apartment", updatedApartment);
      closeUpdateModal();
      apartment.value.name = updatedApartment.name;
      apartment.value.address = updatedApartment.address;
      apartment.value.server_uri = updatedApartment.server_uri;
      apartment.value.auth_key = updatedApartment.auth_key;
    };

    const handleDelete = (apartmentId) => {
      emit("delete-apartment", apartmentId);
      closeUpdateModal();
    };

    const selectButton = (button) => {
      selectedButton.value = button;
      closeAllModals();
    };

    const closeAllModals = () => {
      isCreateModalOpen.value = false;
      isEditDoorModalOpen.value = false;
      isCreateRoomModalOpen.value = false;
      isEditRoomModalOpen.value = false;
      isUpdateModalOpen.value = false;
    };

    onMounted(() => {
      fetchRooms();
    });

    return {
      apartment,
      rooms,
      isDoorsModalOpen,
      isCreateModalOpen,
      isEditDoorModalOpen,
      isCreateRoomModalOpen,
      isEditRoomModalOpen,
      isUpdateModalOpen,
      doors,
      selectedDoor,
      selectedRoom,
      openDoorsModal,
      closeDoorsModal,
      openCreateModal,
      closeCreateModal,
      openEditDoorModal,
      closeEditDoorModal,
      openCreateRoomModal,
      closeCreateRoomModal,
      openEditRoomModal,
      closeEditRoomModal,
      openUpdateModal,
      closeUpdateModal,
      handleDoorCreated,
      handleDoorUpdated,
      handleDoorDeleted,
      handleRoomCreated,
      handleRoomUpdated,
      handleRoomDeleted,
      handleUpdate,
      handleDelete,
      selectedButton,
      selectButton,
      closeAllModals,
    };
  },
};
</script>

<style scoped>
.apartment-detail {
  margin: auto;
  background-color: #fff;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: transparent;
  color: #000;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.button-group {
  display: flex;
  align-items: center;
  justify-content: center; /* Centra i bottoni */
  margin-top: 10px;
}

.action-button {
  background-color: transparent; /* Imposta il fondo trasparente */
  color: #007bff;
  border: none;
  cursor: pointer;
  padding: 10px;
  font-size: 16px;
  transition: transform 0.3s ease; /* Aggiungi transizione per l'effetto di ingrandimento */
  text-decoration: none; /* Rimuovi la sottolineatura */
}

.action-button:hover {
  text-decoration: none; /* Rimuovi la sottolineatura anche al passaggio del mouse */
}

.action-button.selected {
  background-color: transparent; /* Rimuovi lo sfondo per il bottone selezionato */
  color: #007bff; /* Mantieni il colore del testo */
  transform: scale(1.25); /* Ingrandisci il bottone selezionato */
  font-weight: bold; /* Rendi il testo in grassetto per il bottone selezionato */
}

.divider {
  width: 1px;
  height: 20px;
  background-color: #ccc;
  margin: 0 10px;
}

.rooms-header,
.apartment-header,
.doors-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  width: 100%;
  height: 100%;
  max-width: none;
  position: relative;
  overflow-y: auto;
}

.close-modal-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  color: #000;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.btn-primary {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

.btn-primary:hover {
  background-color: #218838;
}

.rooms-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.room-card {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  flex: 1 1 calc(33.333% - 20px);
  box-sizing: border-box;
  text-align: center;
}

.room-card h4 {
  margin: 0;
  font-size: 18px;
  color: #343a40;
}

@media (max-width: 768px) {
  .room-card {
    flex: 1 1 calc(50% - 20px);
  }
}

@media (max-width: 576px) {
  .room-card {
    flex: 1 1 100%;
  }
}

.auth-key-container {
  display: flex;
  flex-direction: column;
}

.auth-key {
  border: 1px solid #dee2e6;
  padding: 5px;
  word-break: break-all;
}
</style>
