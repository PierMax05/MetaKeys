<template>
  <div id="app">
    <nav class="navbar fixed-navbar" v-if="$route.name !== 'Login'">
      <div class="logo-container">
        <span class="logo">metaKeys</span>
      </div>
      <a href="#" @click.prevent="logout" class="logout-link">Logout</a>
    </nav>
    <div v-if="loading" class="spinner-container">
      <div class="spinner"></div>
    </div>
    <div class="router" v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from './common/api.service';

const router = useRouter();
const isAuthenticated = ref(false);
const loading = ref(true);

onMounted(() => {
  const accessToken = localStorage.getItem('accessToken');
  if (!accessToken) {
    router.push('/login');
  } else {
    ApiService.setHeader(accessToken);
    isAuthenticated.value = true;
  }
  loading.value = false;
});

const logout = async () => {
  try {
    await ApiService.post('/api/auth/logout/', {}, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const isSecure = process.env.NODE_ENV === 'production';
    document.cookie = `accessToken=; Max-Age=0; path=/; ${isSecure ? 'secure; HttpOnly' : ''}`;
    localStorage.removeItem('accessToken');
    router.push('/login');
    window.location.reload(); // Refresh della pagina
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
</script>

<style>
#app {
  text-align: center;
}

.navbar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #333;
  color: white;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.5em;
  font-weight: bold;
}

.logout-link {
  color: white;
  text-decoration: none;
  margin-left: auto;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}

.router {
  margin-top: 100px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>