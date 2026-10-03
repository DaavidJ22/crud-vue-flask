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
  min-height: 2.55rem;
  padding: 0.65rem 1.05rem;
  color: #ffffff;
  font-weight: 600;
  border: 1px solid transparent;
  border-radius: 0.5rem;
  box-shadow: 0 2px 5px rgb(15 23 42 / 12%);
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease,
    transform 0.2s ease;
}

.button--primary {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.button--secondary {
  background: #475569;
  border-color: #475569;
}

.button--danger {
  background: #dc2626;
  border-color: #dc2626;
}

.button:hover:not(:disabled) {
  box-shadow: 0 6px 14px rgb(15 23 42 / 18%);
  filter: brightness(0.94);
  transform: translateY(-1px);
}

.button:active:not(:disabled) {
  box-shadow: 0 2px 5px rgb(15 23 42 / 12%);
  transform: translateY(0);
}

.button:disabled {
  cursor: not-allowed;
  box-shadow: none;
  filter: grayscale(0.25);
  opacity: 0.5;
}
</style>
