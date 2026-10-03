<script setup>
import { onMounted, reactive, ref } from 'vue'

import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const productos = ref([])
const error = ref('')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const formulario = reactive({
  nombre: '',
  descripcion: '',
  precio: 0,
  stock: 0,
  activo: true,
})

const columnas = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'precio', label: 'Precio' },
  { key: 'stock', label: 'Stock' },
  { key: 'activoTexto', label: 'Activo' },
]

function limpiar() {
  formulario.nombre = ''
  formulario.descripcion = ''
  formulario.precio = 0
  formulario.stock = 0
  formulario.activo = true
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
    const response = await productosApi.listar()
    productos.value = response.data.map((producto) => ({
      ...producto,
      activoTexto: producto.activo ? 'Sí' : 'No',
    }))
  } catch (requestError) {
    error.value = requestError.message
  }
}

async function guardar() {
  const nombre = formulario.nombre.trim()

  if (!nombre) {
    error.value = 'El nombre es obligatorio'
    return
  }

  if (formulario.precio === '' || formulario.precio === null) {
    error.value = 'El precio es obligatorio'
    return
  }

  if (formulario.stock === '' || formulario.stock === null) {
    error.value = 'El stock es obligatorio'
    return
  }

  const precio = Number(formulario.precio)
  const stock = Number(formulario.stock)

  if (!Number.isFinite(precio)) {
    error.value = 'El precio debe ser un número válido'
    return
  }

  if (!Number.isInteger(stock)) {
    error.value = 'El stock debe ser un número entero'
    return
  }

  if (precio < 0) {
    error.value = 'El precio no puede ser negativo'
    return
  }

  if (stock < 0) {
    error.value = 'El stock no puede ser negativo'
    return
  }

  guardando.value = true
  error.value = ''

  const producto = {
    nombre,
    descripcion: formulario.descripcion.trim(),
    precio,
    stock,
    activo: formulario.activo,
  }

  try {
    if (editando.value) {
      await productosApi.actualizar(idEditando.value, producto)
    } else {
      await productosApi.crear(producto)
    }

    cancelar()
    await cargar()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    guardando.value = false
  }
}

function editar(producto) {
  editando.value = true
  idEditando.value = producto.id
  error.value = ''
  formulario.nombre = producto.nombre
  formulario.descripcion = producto.descripcion || ''
  formulario.precio = producto.precio
  formulario.stock = producto.stock
  formulario.activo = producto.activo
}

async function eliminar(producto) {
  if (!window.confirm(`¿Eliminar producto ${producto.nombre}?`)) {
    return
  }

  error.value = ''

  try {
    await productosApi.eliminar(producto.id)

    if (idEditando.value === producto.id) {
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
  <section class="productos-page">
    <header class="page-header">
      <div>
        <h1>Productos</h1>
        <p>Registra y administra los productos disponibles.</p>
      </div>
    </header>

    <AlertMessage :message="error" />

    <form class="producto-form" @submit.prevent="guardar">
      <h2>{{ editando ? 'Editar producto' : 'Nuevo producto' }}</h2>

      <div class="form-grid">
        <BaseInput v-model="formulario.nombre" label="Nombre" placeholder="Nombre del producto" />
        <BaseInput
          v-model="formulario.descripcion"
          label="Descripción"
          placeholder="Descripción opcional"
        />
        <BaseInput v-model="formulario.precio" label="Precio" type="number" placeholder="0.00" />
        <BaseInput v-model="formulario.stock" label="Stock" type="number" placeholder="0" />

        <label class="checkbox-field">
          <input v-model="formulario.activo" type="checkbox" />
          <span>Producto activo</span>
        </label>
      </div>

      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ guardando ? 'Guardando...' : editando ? 'Actualizar' : 'Crear' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="cancelar"> Cancelar </BaseButton>
      </div>
    </form>

    <section class="productos-list">
      <h2>Productos registrados</h2>

      <DataTable :rows="productos" :columns="columnas">
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
.productos-page {
  display: grid;
  gap: 1.5rem;
}

.page-header h1,
.producto-form h2,
.productos-list h2 {
  margin: 0;
  color: #111827;
}

.page-header p {
  margin: 0.4rem 0 0;
  color: #6b7280;
}

.producto-form,
.productos-list {
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.checkbox-field {
  display: flex;
  align-items: center;
  align-self: end;
  gap: 0.55rem;
  min-height: 2.7rem;
  color: #374151;
  font-weight: 600;
}

.checkbox-field input {
  width: 1rem;
  height: 1rem;
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
