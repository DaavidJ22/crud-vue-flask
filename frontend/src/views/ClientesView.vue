<script setup>
import { onMounted, reactive, ref } from 'vue'

import { clientesApi } from '../api/clientes'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const clientes = ref([])
const error = ref('')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const formulario = reactive({
  nombre: '',
  correo: '',
  telefono: '',
})

const columnas = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'correo', label: 'Correo' },
  { key: 'telefono', label: 'Teléfono' },
]

function limpiar() {
  formulario.nombre = ''
  formulario.correo = ''
  formulario.telefono = ''
}

function cancelar() {
  editando.value = false
  idEditando.value = null
  error.value = ''
  limpiar()
}

async function cargar() {
  error.value = ''

  try {
    const response = await clientesApi.listar()
    clientes.value = response.data
  } catch (requestError) {
    error.value = requestError.message
  }
}

async function guardar() {
  const nombre = formulario.nombre.trim()
  const correo = formulario.correo.trim().toLowerCase()
  const telefono = formulario.telefono.trim()

  if (!nombre) {
    error.value = 'El nombre es obligatorio'
    return
  }

  if (!correo) {
    error.value = 'El correo es obligatorio'
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) {
    error.value = 'El correo no tiene un formato válido'
    return
  }

  guardando.value = true
  error.value = ''

  const cliente = { nombre, correo, telefono }

  try {
    if (editando.value) {
      await clientesApi.actualizar(idEditando.value, cliente)
    } else {
      await clientesApi.crear(cliente)
    }

    cancelar()
    await cargar()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    guardando.value = false
  }
}

function editar(cliente) {
  editando.value = true
  idEditando.value = cliente.id
  error.value = ''
  formulario.nombre = cliente.nombre
  formulario.correo = cliente.correo
  formulario.telefono = cliente.telefono || ''
}

async function eliminar(cliente) {
  if (!window.confirm(`¿Eliminar a ${cliente.nombre}?`)) {
    return
  }

  error.value = ''

  try {
    await clientesApi.eliminar(cliente.id)

    if (idEditando.value === cliente.id) {
      cancelar()
    }

    await cargar()
  } catch (requestError) {
    error.value = requestError.message
  }
}

onMounted(cargar)
</script>

<template>
  <section class="clientes-page">
    <header class="page-header">
      <div>
        <h1>Clientes</h1>
        <p>Registra y administra la información de tus clientes.</p>
      </div>
    </header>

    <AlertMessage :message="error" />

    <form class="cliente-form" @submit.prevent="guardar">
      <h2>{{ editando ? 'Editar cliente' : 'Nuevo cliente' }}</h2>

      <div class="form-grid">
        <BaseInput v-model="formulario.nombre" label="Nombre" placeholder="Nombre completo" />
        <BaseInput
          v-model="formulario.correo"
          label="Correo"
          type="email"
          placeholder="cliente@correo.com"
        />
        <BaseInput v-model="formulario.telefono" label="Teléfono" placeholder="Teléfono opcional" />
      </div>

      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ guardando ? 'Guardando...' : editando ? 'Actualizar' : 'Crear' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="cancelar"> Cancelar </BaseButton>
      </div>
    </form>

    <section class="clientes-list">
      <h2>Clientes registrados</h2>

      <DataTable :rows="clientes" :columns="columnas">
        <template #actions="{ row }">
          <div class="table-actions">
            <BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton>
            <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
          </div>
        </template>
      </DataTable>
    </section>
  </section>
</template>

<style scoped>
.clientes-page {
  display: grid;
  gap: 1.5rem;
}

.page-header h1,
.cliente-form h2,
.clientes-list h2 {
  margin: 0;
  color: #111827;
}

.page-header p {
  margin: 0.4rem 0 0;
  color: #6b7280;
}

.cliente-form,
.clientes-list {
  display: grid;
  gap: 1rem;
  padding: 1.5rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  box-shadow: 0 6px 18px rgb(15 23 42 / 6%);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.form-actions,
.table-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.table-actions :deep(.button) {
  padding: 0.4rem 0.7rem;
  font-size: 0.875rem;
}

@media (max-width: 800px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
