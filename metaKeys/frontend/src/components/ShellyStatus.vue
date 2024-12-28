<template>
  <div class="shelly-status">
    <h3>Stato dispositivi shelly</h3>
    <div v-if="doorStatus.length">
      <div
        v-for="status in doorStatus"
        :key="status.door_id"
        :class="['status-card', getStatusClass(status)]"
      >
        <p>{{ status.door_name }} in {{ status.apartment_name }}</p>
        <p>Stato: {{ status.status.isok ? 'OK' : 'Non OK' }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShellyStatus",
  props: {
    doorStatus: {
      type: Array,
      required: true,
    },
  },
  methods: {
    getStatusClass(status) {
      if (status.status.isok) {
        return 'status-ok-connected';
      } else {
        return 'status-not-ok';
      }
    },
  },
};
</script>

<style scoped>
.shelly-status {
  padding-inline: 120px;
  display: flex;
  flex-direction: column;
}

.status-card {
  border: 1px solid #ddd;
  margin-top: 5px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.status-ok-connected {
  background-color: #28a745; /* Bright green */
  border-color: #28a745;
  color: white; /* White text */
}

.status-not-ok {
  background-color: #dc3545; /* Bright red */
  border-color: #dc3545;
  color: white; /* White text */
}

@media (max-width: 768px) {
  .shelly-status {
    padding-inline: 0;
    
  }
}
</style>
