<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  placeholder: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

function updateValue(event) {
  const value = event.target.value
  const normalizedValue = props.type === 'number' && value !== '' ? Number(value) : value
  emit('update:modelValue', normalizedValue)
}
</script>

<template>
  <label class="field">
    <span class="field__label">{{ label }}</span>
    <input
      class="field__input"
      :class="{ 'field__input--error': error }"
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      @input="updateValue"
    />
    <span v-if="error" class="field__error">{{ error }}</span>
  </label>
</template>

<style scoped>
.field {
  display: grid;
  gap: 0.4rem;
}

.field__label {
  color: #374151;
  font-weight: 600;
}

.field__input {
  width: 100%;
  padding: 0.65rem 0.75rem;
  color: #111827;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 0.4rem;
  outline: none;
}

.field__input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgb(37 99 235 / 15%);
}

.field__input--error {
  border-color: #dc2626;
}

.field__error {
  color: #b91c1c;
  font-size: 0.875rem;
}
</style>
