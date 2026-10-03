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
  gap: 0.45rem;
}

.field__label {
  color: #334155;
  font-size: 0.9rem;
  font-weight: 600;
}

.field__input {
  width: 100%;
  min-height: 2.75rem;
  padding: 0.7rem 0.8rem;
  color: var(--color-heading);
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.field__input::placeholder {
  color: #94a3b8;
}

.field__input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 15%);
}

.field__input--error {
  border-color: #dc2626;
}

.field__error {
  color: #b91c1c;
  font-size: 0.825rem;
}
</style>
