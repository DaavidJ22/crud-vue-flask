<script setup>
defineProps({
  type: {
    type: String,
    default: 'button',
  },
  variant: {
    type: String,
    default: 'primary',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <button :type="type" :class="['button', `button--${variant}`]" :disabled="disabled">
    <slot />
  </button>
</template>

<style scoped>
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1rem;
  color: #ffffff;
  font-weight: 600;
  border: 0;
  border-radius: 0.4rem;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    opacity 0.2s ease;
}

.button--primary {
  background: #2563eb;
}

.button--secondary {
  background: #4b5563;
}

.button--danger {
  background: #dc2626;
}

.button:hover:not(:disabled) {
  filter: brightness(0.92);
}

.button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}
</style>
