import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; // Importa lo store Vuex
import ApiService from './common/api.service';

ApiService.init('http://localhost:8000'); // Sostituisci con il tuo baseURL
const accessToken = localStorage.getItem('accessToken');
if (accessToken) {
  ApiService.setHeader(accessToken);
}

const app = createApp(App).use(router).use(store); // Crea l'istanza dell'app

// codice per abilitare HMR
if (import.meta.hot) {
  import.meta.hot.accept();
  import.meta.hot.dispose(() => {
    app.unmount(); // Smonta l'app precedente
  });
}

app.mount('#app'); // Monta l'app
