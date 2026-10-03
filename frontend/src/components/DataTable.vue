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
  border: 1px solid var(--color-border);
  border-radius: 0.65rem;
  box-shadow: 0 4px 12px rgb(15 23 42 / 4%);
}

.data-table {
  width: 100%;
  min-width: 680px;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.9rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  color: #475569;
  background: #f8fafc;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.045em;
  text-transform: uppercase;
  white-space: nowrap;
}

.data-table tbody tr {
  transition: background-color 0.15s ease;
}

.data-table tbody tr:nth-child(even) {
  background: #fbfdff;
}

.data-table tbody tr:hover {
  background: #eff6ff;
}

.data-table tbody tr:last-child td {
  border-bottom: 0;
}

.data-table__actions {
  white-space: nowrap;
}

.data-table__empty {
  padding: 2rem 1rem !important;
  color: var(--color-muted);
  text-align: center;
}
</style>
