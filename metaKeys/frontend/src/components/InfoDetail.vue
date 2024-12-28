<template>
  <div v-if="info">
    <h2>{{ info.title }}</h2>
    <p><strong>Tipo:</strong> {{ info.type }}</p>
    <p><strong>Informazione:</strong> {{ info.info }}</p>
    <p v-if="info.google_link"><strong>Link Google:</strong> <a :href="info.google_link" target="_blank">{{ info.google_link }}</a></p>
    <div class="button-group">
      <button class="btn btn-secondary" @click="$emit('close')">Chiudi</button>
      <div class="right-buttons">
        <button class="btn btn-primary" @click="$emit('edit')">Modifica</button>
        <button class="btn btn-danger" @click="deleteInfo">Elimina</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex';
import { computed } from 'vue';

export default {
  name: "InfoDetail",
  setup(_, { emit }) {
    const store = useStore();
    const info = computed(() => store.state.infos.selectedInfo);

    const deleteInfo = async () => {
      if (store.state.infos.deletedInfoIds.has(info.value.id)) return;
      try {
        await store.dispatch('deleteInfo', info.value.id);
        emit("delete-info", info.value.id);
      } catch (error) {
        console.error("Errore nell'eliminazione dell'informazione:", error);
      }
    };

    return {
      info,
      deleteInfo,
    };
  },
};
</script>

<style scoped>
.btn {
  margin: 5px;
  font-size: 1em;
}

.btn-primary {
  background-color: #0056b3;
  color: white;
}

.btn-primary:hover {
  background-color: #004085;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.button-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.right-buttons {
  display: flex;
}

h2 {
  font-size: 1.75em;
}

p {
  font-size: 1em;
}
</style>
