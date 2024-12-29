import ApiService from '../../common/api.service';

const state = {
  apartments: [],
  rooms: {},
  doors: {},
  isApartmentsFetched: false,
  fetchedRooms: {},
  hasShellyDevices: false,
  doorStatus: [],
  connectionIssues: false,
};

const actions = {
  async fetchApartments({ commit, state }) {
    if (state.isApartmentsFetched) return;
    try {
      const { data } = await ApiService.get("/api/apartments/");  
      commit('SET_APARTMENTS', data);
      commit('SET_APARTMENTS_FETCHED', true);
      commit('CHECK_HAS_SHELLY_DEVICES'); // Controlla se ci sono dispositivi Shelly
    } catch (error) {
      console.error(error);
    }
  },
  async fetchRooms({ commit, state }, apartmentId) {
    if (state.fetchedRooms[apartmentId]) return;
    try {
      const { data } = await ApiService.get(`/api/rooms/?apartment=${apartmentId}`);
      commit('SET_ROOMS', { apartmentId, rooms: data });
      commit('SET_ROOMS_FETCHED', apartmentId);
    } catch (error) {
      console.error(error);
    }
  },
  async fetchDoors({ commit }, apartmentId) {
    try {
      const { data } = await ApiService.get(`/api/doors/?apartment=${apartmentId}`);
      commit('SET_DOORS', { apartmentId, doors: data });
    } catch (error) {
      console.error(error);
    }
  },
  async createDoor({ commit, dispatch }, door) {
    try {
      const { data } = await ApiService.post("/api/doors/", door);
      commit('ADD_DOOR', data);
      await dispatch('checkDoorStatus'); // Richiama checkDoorStatus dopo la creazione
    } catch (error) {
      console.error(error);
    }
  },
  async updateDoor({ commit, dispatch }, door) {
    try {
      const { data } = await ApiService.put(`/api/doors/${door.id}/`, door);
      commit('UPDATE_DOOR', data);
      await dispatch('checkDoorStatus'); // Richiama checkDoorStatus dopo l'aggiornamento
    } catch (error) {
      console.error(error);
    }
  },
  async deleteDoor({ commit, dispatch }, doorId) {
    try {
      await ApiService.delete(`/api/doors/${doorId}/`);
      commit('DELETE_DOOR', doorId);
      await dispatch('checkDoorStatus'); // Richiama checkDoorStatus dopo la cancellazione
    } catch (error) {
      console.error(error);
    }
  },
  async createRoom({ commit }, room) {
    try {
      const { data } = await ApiService.post("/api/rooms/", room);
      commit('ADD_ROOM', data);
    } catch (error) {
      console.error(error);
    }
  },
  async updateRoom({ commit }, room) {
    try {
      const { data } = await ApiService.put(`/api/rooms/${room.id}/`, room);
      commit('UPDATE_ROOM', data);
    } catch (error) {
      console.error(error);
    }
  },
  async deleteRoom({ commit }, roomId) {
    try {
      await ApiService.delete(`/api/rooms/${roomId}/`);
      commit('DELETE_ROOM', roomId);
    } catch (error) {
      console.error(error);
    }
  },
  async updateApartment({ commit, dispatch }, apartment) {
    try {
      const { data } = await ApiService.put(`/api/apartments/${apartment.id}/`, apartment);
      commit('UPDATE_APARTMENT', data);
      commit('CHECK_HAS_SHELLY_DEVICES'); // Controlla se ci sono dispositivi Shelly dopo l'aggiornamento
      await dispatch('checkDoorStatus'); // Richiama checkDoorStatus dopo l'aggiornamento
    } catch (error) {
      console.error(error);
    }
  },
  async deleteApartment({ commit, dispatch }, apartmentId) {
    try {
      await ApiService.delete(`/api/apartments/${apartmentId}/`);
      commit('DELETE_APARTMENT', apartmentId);
      commit('CHECK_HAS_SHELLY_DEVICES'); // Controlla se ci sono dispositivi Shelly dopo la cancellazione
      await dispatch('checkDoorStatus'); // Richiama checkDoorStatus dopo la cancellazione
    } catch (error) {
      console.error(error);
    }
  },
  async checkDoorStatus({ commit }) {
    try {
      const { data } = await ApiService.get('/api/check-doors-status/');
      const connectionIssues = data.some(status => !status.status.isok || !status.status.connected);
      commit('SET_DOOR_STATUS', data);
      commit('SET_CONNECTION_ISSUES', connectionIssues);
    } catch (error) {
      console.error('Errore durante il controllo dello stato delle porte:', error);
    }
  },
};

const mutations = {
  SET_APARTMENTS(state, apartments) {
    state.apartments = apartments;
  },
  SET_ROOMS(state, { apartmentId, rooms }) {
    state.rooms = { ...state.rooms, [apartmentId]: rooms };
  },
  SET_DOORS(state, { apartmentId, doors }) {
    state.doors = { ...state.doors, [apartmentId]: doors };
  },
  ADD_DOOR(state, door) {
    if (!state.doors[door.apartment]) {
      state.doors[door.apartment] = [];
    }
    state.doors[door.apartment].push(door);
  },
  ADD_ROOM(state, room) {
    if (!state.rooms[room.apartment]) {
      state.rooms[room.apartment] = [];
    }
    state.rooms[room.apartment].push(room);
  },
  UPDATE_DOOR(state, updatedDoor) {
    const doors = state.doors[updatedDoor.apartment] || [];
    const index = doors.findIndex(door => door.id === updatedDoor.id);
    if (index !== -1) {
      doors.splice(index, 1, updatedDoor);
    }
  },
  UPDATE_ROOM(state, updatedRoom) {
    const rooms = state.rooms[updatedRoom.apartment] || [];
    const index = rooms.findIndex(room => room.id === updatedRoom.id);
    if (index !== -1) {
      rooms.splice(index, 1, updatedRoom);
    }
  },
  DELETE_DOOR(state, doorId) {
    for (const apartmentId in state.doors) {
      state.doors[apartmentId] = state.doors[apartmentId].filter(door => door.id !== doorId);
    }
  },
  DELETE_ROOM(state, roomId) {
    for (const apartmentId in state.rooms) {
      state.rooms[apartmentId] = state.rooms[apartmentId].filter(room => room.id !== roomId);
    }
  },
  SET_APARTMENTS_FETCHED(state, status) {
    state.isApartmentsFetched = status;
  },
  SET_ROOMS_FETCHED(state, apartmentId) {
    state.fetchedRooms = { ...state.fetchedRooms, [apartmentId]: true };
  },
  UPDATE_APARTMENT(state, updatedApartment) {
    const index = state.apartments.findIndex(apartment => apartment.id === updatedApartment.id);
    if (index !== -1) {
      state.apartments.splice(index, 1, updatedApartment);
    }
  },
  DELETE_APARTMENT(state, apartmentId) {
    state.apartments = state.apartments.filter(apartment => apartment.id !== apartmentId);
  },
  SET_HAS_SHELLY_DEVICES(state, status) {
    state.hasShellyDevices = status;
  },
  CHECK_HAS_SHELLY_DEVICES(state) {
    state.hasShellyDevices = state.apartments.some(apartment => apartment.shelly);
  },
  SET_DOOR_STATUS(state, status) {
    state.doorStatus = status;
  },
  SET_CONNECTION_ISSUES(state, status) {
    state.connectionIssues = status;
  },
};

const getters = {
  getRoomsByApartment: (state) => (apartmentId) => {
    return state.rooms[apartmentId] || [];
  },
  hasShellyDevices: (state) => {
    return state.hasShellyDevices;
  },
  doorStatus: (state) => {
    return state.doorStatus;
  },
  connectionIssues: (state) => {
    return state.connectionIssues;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
