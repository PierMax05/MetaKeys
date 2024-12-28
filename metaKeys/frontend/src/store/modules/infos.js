import ApiService from '../../common/api.service';

const state = {
  infos: [],
  isFetched: false,
  selectedInfo: null,
};

const getters = {
  filteredInfos: (state) => (apartmentId) => {
    return state.infos.filter(info => info.apartment === apartmentId);
  },
};

const actions = {
  async fetchInfos({ commit, state }) {
    if (state.isFetched) return;
    try {
      const { data } = await ApiService.get(`/api/apartment-info/`);
      commit('SET_INFOS', data);
      commit('SET_FETCHED', true);
    } catch (error) {
      console.error(error);
    }
  },
  async createInfo({ commit }, info) {
    try {
      const { data } = await ApiService.post(`/api/apartment-info/`, info);
      commit('ADD_INFO', data);
    } catch (error) {
      console.error(error);
    }
  },
  async updateInfo({ commit }, info) {
    try {
      const { data } = await ApiService.put(`/api/apartment-info/${info.id}/`, info);
      commit('UPDATE_INFO', data);
    } catch (error) {
      console.error(error);
    }
  },
  async deleteInfo({ commit }, infoId) {
    try {
      await ApiService.delete(`/api/apartment-info/${infoId}/`);
      commit('REMOVE_INFO', infoId);
    } catch (error) {
      console.error(error);
    }
  },
  selectInfo({ commit }, info) {
    commit('SET_SELECTED_INFO', info);
  },
  deselectInfo({ commit }) {
    commit('SET_SELECTED_INFO', null);
  },
};

const mutations = {
  SET_INFOS(state, infos) {
    state.infos = infos;
  },
  SET_FETCHED(state, status) {
    state.isFetched = status;
  },
  ADD_INFO(state, info) {
    state.infos.push(info);
  },
  UPDATE_INFO(state, updatedInfo) {
    const index = state.infos.findIndex(info => info.id === updatedInfo.id);
    if (index !== -1) {
      state.infos.splice(index, 1, updatedInfo);
    }
  },
  REMOVE_INFO(state, infoId) {
    state.infos = state.infos.filter(info => info.id !== infoId);
  },
  SET_SELECTED_INFO(state, info) {
    state.selectedInfo = info;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
