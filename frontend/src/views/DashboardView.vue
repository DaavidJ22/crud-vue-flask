<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="dashboard">
    <header class="dashboard-hero">
      <span class="dashboard-hero__eyebrow">Panel principal</span>
      <h1>Sistema de Ventas</h1>
      <p>Administra clientes, productos y pedidos desde un solo lugar.</p>
    </header>

    <div class="dashboard-grid" aria-label="Módulos del sistema">
      <RouterLink class="module-card module-card--clients" to="/clientes">
        <span class="module-card__number" aria-hidden="true">01</span>
        <div>
          <h2>Clientes</h2>
          <p>Registra y consulta la información de tus clientes.</p>
        </div>
        <span class="module-card__link">Ir a clientes <span aria-hidden="true">→</span></span>
      </RouterLink>

      <RouterLink class="module-card module-card--products" to="/productos">
        <span class="module-card__number" aria-hidden="true">02</span>
        <div>
          <h2>Productos</h2>
          <p>Administra precios, existencias y disponibilidad.</p>
        </div>
        <span class="module-card__link">Ir a productos <span aria-hidden="true">→</span></span>
      </RouterLink>

      <RouterLink class="module-card module-card--orders" to="/pedidos">
        <span class="module-card__number" aria-hidden="true">03</span>
        <div>
          <h2>Pedidos</h2>
          <p>Crea pedidos y da seguimiento a su estado.</p>
        </div>
        <span class="module-card__link">Ir a pedidos <span aria-hidden="true">→</span></span>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.dashboard {
  display: grid;
  gap: 1.5rem;
}

.dashboard-hero {
  position: relative;
  overflow: hidden;
  padding: clamp(2rem, 6vw, 4rem);
  color: #ffffff;
  background:
    radial-gradient(circle at 88% 15%, rgb(96 165 250 / 45%), transparent 28%),
    linear-gradient(135deg, #0f172a, #1e3a8a);
  border: 1px solid rgb(147 197 253 / 18%);
  border-radius: 1rem;
  box-shadow: 0 20px 45px rgb(15 23 42 / 18%);
}

.dashboard-hero__eyebrow {
  display: inline-block;
  margin-bottom: 1rem;
  padding: 0.3rem 0.65rem;
  color: #bfdbfe;
  background: rgb(255 255 255 / 10%);
  border: 1px solid rgb(255 255 255 / 14%);
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.dashboard-hero h1 {
  max-width: 700px;
  margin: 0;
  font-size: clamp(2.3rem, 7vw, 4.5rem);
  letter-spacing: -0.045em;
  line-height: 1.05;
}

.dashboard-hero p {
  max-width: 620px;
  margin: 1.25rem 0 0;
  color: #dbeafe;
  font-size: clamp(1rem, 2vw, 1.2rem);
  line-height: 1.7;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.module-card {
  display: flex;
  min-height: 235px;
  padding: 1.5rem;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-top: 4px solid var(--card-accent);
  border-radius: 0.8rem;
  box-shadow: var(--shadow-card);
  flex-direction: column;
  justify-content: space-between;
  transition:
    transform 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.module-card:hover {
  border-color: var(--card-accent);
  box-shadow: 0 18px 36px rgb(15 23 42 / 12%);
  transform: translateY(-4px);
}

.module-card--clients {
  --card-accent: #2563eb;
}

.module-card--products {
  --card-accent: #0f766e;
}

.module-card--orders {
  --card-accent: #7c3aed;
}

.module-card__number {
  color: var(--card-accent);
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.module-card h2 {
  margin: 0 0 0.5rem;
  color: var(--color-heading);
  font-size: 1.35rem;
}

.module-card p {
  margin: 0;
  color: var(--color-muted);
  line-height: 1.6;
}

.module-card__link {
  color: var(--card-accent);
  font-size: 0.9rem;
  font-weight: 700;
}

@media (max-width: 800px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .module-card {
    min-height: 190px;
  }
}
</style>
