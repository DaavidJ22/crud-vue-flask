<script setup>
defineProps({
  message: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'error',
  },
})
</script>

<template>
  <div v-if="message" :class="['alert', `alert--${type}`]" role="alert">
    {{ message }}
  </div>
</template>

<style scoped>
.alert {
  padding: 0.8rem 1rem;
  border: 1px solid transparent;
  border-radius: 0.4rem;
}

.alert--error {
  color: #991b1b;
  background: #fef2f2;
  border-color: #fecaca;
}

.alert--success {
  color: #166534;
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.alert--warning {
  color: #92400e;
  background: #fffbeb;
  border-color: #fde68a;
}
</style>
