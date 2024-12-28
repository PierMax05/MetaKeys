<template>
  <div class="modal-overlay" @click.self="close">
    <div class="base-modal">
      <div class="modal-content">
        <header class="modal-header">
          <slot name="header"></slot>
        </header>
        <section class="modal-body">
          <slot name="body"></slot>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, watch } from 'vue';

export default defineComponent({
  name: "ModalComponent",
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['close'],
  setup(props, { emit }) {
    const close = () => {
      emit("close");
    };

    watch(
      () => props.isOpen,
      (newVal) => {
        if (newVal) {
          document.body.classList.add("no-scroll");
        } else {
          document.body.classList.remove("no-scroll");
        }
      }
    );

    return {
      close,
    };
  },
});
</script>

<style scoped>
.base-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.modal-content {
  background: white;
  width: 90%;
  max-width: 800px;
  max-height: 90%;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
}

.modal-header,
.modal-footer {
  flex-shrink: 0;
  padding: 10px;
  background: #f1f1f1;
  border-bottom: 1px solid #ddd;
}

.modal-body {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
}

/* Media query per schermi piccoli */
@media (max-width: 768px) {
  .modal-content {
    width: 100%;
    height: 100%;
    max-width: none;
    max-height: none;
    border-radius: 0;
  }
}

/* Classe per disabilitare lo scrolling */
.no-scroll {
  overflow: hidden;
}
</style>
