<template>
  <div class="login-container">
    <h1>metaKeys</h1>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
  <div v-if="loading" class="spinner-container">
    <div class="spinner"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ApiService from '../common/api.service';
import { useRouter } from 'vue-router';

const emit = defineEmits(['login-success']);
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const router = useRouter();

const login = async () => {
  try {
    loading.value = true;
    // Rimuovi i token precedenti
    document.cookie = 'accessToken=; Max-Age=0; path=/;';
    localStorage.removeItem('accessToken');

    const response = await ApiService.post('/api/auth/login/', {
      username: username.value,
      password: password.value,
    });
    const accessToken = response.data.key;
    const isSecure = process.env.NODE_ENV === 'production';
    document.cookie = `accessToken=${accessToken}; path=/; ${isSecure ? 'secure; HttpOnly' : ''}`;
    localStorage.setItem('accessToken', accessToken);
    ApiService.setHeader(accessToken); // Passa il token di accesso per impostare l'header
    const userResponse = await ApiService.get('/api/user_information/');
    const userType = userResponse.data.profile_type;
    emit('login-success'); // Emit event on successful login
    setTimeout(() => {
      if (userType === 'owner') {
        router.push('/owners');
      } else {
        router.push('/guest');
      }
    }, 0); // Esegui il routing dopo il montaggio della pagina
  } catch (err) {
    error.value = 'Invalid username or password';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  margin-top: 10%;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .login-container {
    margin-top: 10%;
    padding: 15px;
  }

  button {
    padding: 8px;
  }
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #1a252f;
}

.error {
  color: red;
  margin-top: 10px;
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
