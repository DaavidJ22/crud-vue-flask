<script setup>
import { onMounted, reactive, ref } from 'vue'

import { clientesApi } from '../api/clientes'
import { pedidosApi } from '../api/pedidos'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const pedidos = ref([])
const clientes = ref([])
const productos = ref([])
const error = ref('')
const guardando = ref(false)
const editandoEstado = ref(false)
const idEditando = ref(null)
const estadoEditando = ref('pendiente')

const form = reactive({
  cliente_id: '',
  producto_id: '',
  cantidad: 1,
})

const estados = ['pendiente', 'pagado', 'enviado', 'cancelado']

const columnas = [
  { key: 'id', label: 'ID' },
  { key: 'clienteNombre', label: 'Cliente' },
  { key: 'productoNombre', label: 'Producto' },
  { key: 'cantidad', label: 'Cantidad' },
  { key: 'estado', label: 'Estado' },
  { key: 'totalFormato', label: 'Total' },
]

function formatearMoneda(value) {
  const amount = Number(value)
  return `Q${Number.isFinite(amount) ? amount.toFixed(2) : '0.00'}`
}

function normalizarPedidos(data) {
  return data.map((pedido) => ({
    ...pedido,
    clienteNombre: pedido.cliente?.nombre || '',
    productoNombre: pedido.producto?.nombre || '',
    totalFormato: formatearMoneda(pedido.total),
  }))
}

async function cargarPedidos() {
  const response = await pedidosApi.listar()
  pedidos.value = normalizarPedidos(response.data)
}

async function cargarClientes() {
  const response = await clientesApi.listar()
  clientes.value = response.data
}

async function cargarProductos() {
  const response = await productosApi.listar()
  productos.value = response.data
}

async function cargarInicial() {
  error.value = ''

  try {
    await Promise.all([cargarPedidos(), cargarClientes(), cargarProductos()])
  } catch (requestError) {
    error.value = requestError.message
  }
}

function limpiar() {
  form.cliente_id = ''
  form.producto_id = ''
  form.cantidad = 1
}

async function guardar() {
  if (!form.cliente_id) {
    error.value = 'El cliente es obligatorio'
    return
  }

  if (!form.producto_id) {
    error.value = 'El producto es obligatorio'
    return
  }

  if (form.cantidad === '' || form.cantidad === null) {
    error.value = 'La cantidad es obligatoria'
    return
  }

  const cantidad = Number(form.cantidad)

  if (!Number.isInteger(cantidad) || cantidad <= 0) {
    error.value = 'La cantidad debe ser mayor que cero'
    return
  }

  guardando.value = true
  error.value = ''

  try {
    await pedidosApi.crear({
      cliente_id: Number(form.cliente_id),
      producto_id: Number(form.producto_id),
      cantidad,
    })
    limpiar()
    await Promise.all([cargarPedidos(), cargarProductos()])
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    guardando.value = false
  }
}

function editarEstado(pedido) {
  editandoEstado.value = true
  idEditando.value = pedido.id
  estadoEditando.value = pedido.estado
  error.value = ''
}

function cancelarEstado() {
  editandoEstado.value = false
  idEditando.value = null
  estadoEditando.value = 'pendiente'
}

async function guardarEstado(pedido) {
  guardando.value = true
  error.value = ''

  try {
    await pedidosApi.actualizar(pedido.id, { estado: estadoEditando.value })
    cancelarEstado()
    await cargarPedidos()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    guardando.value = false
  }
}

async function eliminar(pedido) {
  if (!window.confirm(`¿Eliminar pedido #${pedido.id}?`)) {
    return
  }

  error.value = ''

  try {
    await pedidosApi.eliminar(pedido.id)

    if (idEditando.value === pedido.id) {
      cancelarEstado()
    }

    await cargarPedidos()
  } catch (requestError) {
    error.value = requestError.message
  }
}

onMounted(cargarInicial)
</script>

<template>
  <section class="pedidos-page">
    <header class="page-header">
      <div>
        <h1>Pedidos</h1>
        <p>Crea pedidos, consulta sus totales y actualiza su estado.</p>
      </div>
    </header>

    <AlertMessage :message="error" />

    <form class="pedido-form" @submit.prevent="guardar">
      <h2>Nuevo pedido</h2>

      <div class="form-grid">
        <label class="select-field">
          <span>Cliente</span>
          <select v-model.number="form.cliente_id" required>
            <option disabled value="">Selecciona un cliente</option>
            <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
              {{ cliente.nombre }}
            </option>
          </select>
        </label>

        <label class="select-field">
          <span>Producto</span>
          <select v-model.number="form.producto_id" required>
            <option disabled value="">Selecciona un producto</option>
            <option v-for="producto in productos" :key="producto.id" :value="producto.id">
              {{ producto.nombre }} — {{ formatearMoneda(producto.precio) }} — Stock:
              {{ producto.stock }}
            </option>
          </select>
        </label>

        <BaseInput v-model="form.cantidad" label="Cantidad" type="number" placeholder="1" />
      </div>

      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ guardando ? 'Guardando...' : 'Crear' }}
        </BaseButton>
      </div>
    </form>

    <section class="pedidos-list">
      <h2>Pedidos registrados</h2>

      <DataTable :rows="pedidos" :columns="columnas">
        <template #actions="{ row }">
          <div
            v-if="editandoEstado && idEditando === row.id"
            class="estado-actions estado-actions--editing"
          >
            <select v-model="estadoEditando" aria-label="Estado del pedido">
              <option v-for="estado in estados" :key="estado" :value="estado">
                {{ estado }}
              </option>
            </select>
            <BaseButton :disabled="guardando" @click="guardarEstado(row)">Guardar</BaseButton>
            <BaseButton variant="secondary" :disabled="guardando" @click="cancelarEstado">
              Cancelar
            </BaseButton>
          </div>

          <div v-else class="estado-actions">
            <BaseButton variant="secondary" @click="editarEstado(row)"> Cambiar estado </BaseButton>
            <BaseButton variant="danger" :disabled="guardando" @click="eliminar(row)">
              Eliminar
            </BaseButton>
          </div>
        </template>
      </DataTable>
    </section>
  </section>
</template>

<style scoped>
.pedidos-page {
  display: grid;
  gap: 1.5rem;
}

.page-header h1,
.pedido-form h2,
.pedidos-list h2 {
  margin: 0;
  color: #111827;
}

.page-header p {
  margin: 0.4rem 0 0;
  color: #6b7280;
}

.pedido-form,
.pedidos-list {
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

.select-field {
  display: grid;
  gap: 0.4rem;
  color: #374151;
  font-weight: 600;
}

.select-field select,
.estado-actions select {
  min-width: 10rem;
  padding: 0.65rem 0.75rem;
  color: #111827;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 0.4rem;
}

.form-actions,
.estado-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.estado-actions {
  align-items: center;
}

.estado-actions :deep(.button) {
  padding: 0.4rem 0.7rem;
  font-size: 0.875rem;
}

.estado-actions--editing {
  min-width: 24rem;
}

@media (max-width: 800px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .estado-actions--editing {
    min-width: 0;
  }
}
</style>
