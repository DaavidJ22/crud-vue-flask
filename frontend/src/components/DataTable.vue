<script setup>
defineProps({
  rows: {
    type: Array,
    default: () => [],
  },
  columns: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key" scope="col">
            {{ column.label }}
          </th>
          <th scope="col">Acciones</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(row, index) in rows" :key="row.id ?? index">
          <td v-for="column in columns" :key="column.key">
            {{ row[column.key] }}
          </td>
          <td class="data-table__actions">
            <slot name="actions" :row="row" />
          </td>
        </tr>

        <tr v-if="rows.length === 0">
          <td class="data-table__empty" :colspan="columns.length + 1">No hay registros.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0.6rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.data-table th {
  color: #374151;
  background: #f9fafb;
  font-size: 0.875rem;
}

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

.data-table__actions {
  white-space: nowrap;
}

.data-table__empty {
  color: #6b7280;
  text-align: center;
}
</style>
