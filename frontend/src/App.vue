<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <RouterLink class="brand" to="/dashboard">Sistema de Ventas</RouterLink>

      <nav class="main-nav" aria-label="Navegación principal">
        <RouterLink to="/dashboard">Inicio</RouterLink>
        <RouterLink to="/clientes">Clientes</RouterLink>
        <RouterLink to="/productos">Productos</RouterLink>
        <RouterLink to="/pedidos">Pedidos</RouterLink>
      </nav>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>
