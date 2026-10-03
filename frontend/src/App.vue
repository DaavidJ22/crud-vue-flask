<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-header__inner">
        <RouterLink class="brand" to="/dashboard">
          <span class="brand__mark" aria-hidden="true">SV</span>
          <span>Sistema de Ventas</span>
        </RouterLink>

        <nav class="main-nav" aria-label="Navegación principal">
          <RouterLink to="/dashboard">Inicio</RouterLink>
          <RouterLink to="/clientes">Clientes</RouterLink>
          <RouterLink to="/productos">Productos</RouterLink>
          <RouterLink to="/pedidos">Pedidos</RouterLink>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>
