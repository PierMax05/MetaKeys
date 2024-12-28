import ApiService from '../../common/api.service';

const state = {
  apartments: [],
  rooms: {},
  doors: {},
  isApartmentsFetched: false,
  fetchedRooms: {},
};

const actions = {
  async fetchApartments({ commit, state }) {
    if (state.isApartmentsFetched) return;
    try {
      const { data } = await ApiService.get("/api/apartments/");  
      commit('SET_APARTMENTS', data);
      commit('SET_APARTMENTS_FETCHED', true);
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
  async createDoor({ commit }, door) {
    try {
      const { data } = await ApiService.post("/api/doors/", door);
      commit('ADD_DOOR', data);
    } catch (error) {
      console.error(error);
    }
  },
  async updateDoor({ commit }, door) {
    try {
      const { data } = await ApiService.put(`/api/doors/${door.id}/`, door);
      commit('UPDATE_DOOR', data);
    } catch (error) {
      console.error(error);
    }
  },
  async deleteDoor({ commit }, doorId) {
    try {
      await ApiService.delete(`/api/doors/${doorId}/`);
      commit('DELETE_DOOR', doorId);
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
  async updateApartment({ commit }, apartment) {
    try {
      const { data } = await ApiService.put(`/api/apartments/${apartment.id}/`, apartment);
      commit('UPDATE_APARTMENT', data);
    } catch (error) {
      console.error(error);
    }
  },
  async deleteApartment({ commit }, apartmentId) {
    try {
      await ApiService.delete(`/api/apartments/${apartmentId}/`);
      commit('DELETE_APARTMENT', apartmentId);
    } catch (error) {
      console.error(error);
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
};

const getters = {
  getRoomsByApartment: (state) => (apartmentId) => {
    return state.rooms[apartmentId] || [];
  }
};

export default {
  state,
  actions,
  mutations,
  getters,
};
