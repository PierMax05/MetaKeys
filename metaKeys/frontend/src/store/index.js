import { createStore } from 'vuex';
import infos from './modules/infos';
import apartments from './modules/apartments';

export default createStore({
  modules: {
    infos,
    apartments,
  },
});
