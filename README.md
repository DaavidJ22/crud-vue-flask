# CRUD Vue 3 + Axios + Flask

Aplicación web de ventas para administrar clientes, productos y pedidos. El frontend está construido con Vue 3, Vue Router y Axios, mientras que el backend utiliza Flask, Flask-SQLAlchemy, Flask-Migrate y una base de datos SQLite.

## Funcionalidades

- CRUD de clientes.
- CRUD de productos.
- Creación, consulta, actualización de estado y eliminación de pedidos.
- Validaciones en frontend y backend.
- Control de existencias al crear pedidos.
- Estados de pedido: `pendiente`, `pagado`, `enviado` y `cancelado`.
- Navegación SPA sin recargar la página.
- Componentes reutilizables para botones, campos, tablas y alertas.
- Diseño responsivo para escritorio y pantallas pequeñas.

## Estructura del proyecto

```text
crud-vue-flask/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models.py
│   │   ├── extensions.py
│   │   ├── errors.py
│   │   └── __init__.py
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env.example
│   └── package.json
└── README.md
```

## Arquitectura

- **Flask** expone una API REST para clientes, productos y pedidos.
- **SQLAlchemy** define los modelos, las claves foráneas y sus relaciones.
- **Flask-Migrate** administra los cambios del esquema de la base de datos.
- **Vue 3** implementa la interfaz de usuario como una aplicación de una sola página.
- **Axios** comunica el frontend con la API y centraliza el manejo de errores HTTP.
- **Vue Router** gestiona la navegación entre el dashboard y las vistas CRUD.
- `frontend/src/components/` contiene piezas visuales genéricas y reutilizables.
- `frontend/src/views/` contiene las páginas completas de la aplicación.
- `frontend/src/api/` contiene el cliente HTTP y los módulos de acceso a cada recurso.

## Modelos

### Cliente

- `id`
- `nombre`
- `correo`
- `telefono`

### Producto

- `id`
- `nombre`
- `descripcion`
- `precio`
- `stock`
- `activo`

### Pedido

- `id`
- `cantidad`
- `estado`
- `cliente`
- `producto`

Un cliente puede tener varios pedidos. Un producto también puede aparecer en varios pedidos. Cada pedido pertenece a un cliente y a un producto.

## Endpoints principales

### Clientes

```text
GET    /api/clientes
POST   /api/clientes
GET    /api/clientes/<id>
PUT    /api/clientes/<id>
DELETE /api/clientes/<id>
```

### Productos

```text
GET    /api/productos
POST   /api/productos
GET    /api/productos/<id>
PUT    /api/productos/<id>
DELETE /api/productos/<id>
```

### Pedidos

```text
GET    /api/pedidos
POST   /api/pedidos
GET    /api/pedidos/<id>
PUT    /api/pedidos/<id>
DELETE /api/pedidos/<id>
```

El backend también ofrece `GET /health` para comprobar el estado de la aplicación.

## Requisitos

- Python 3.11 o superior.
- Node.js LTS.
- npm.

## Instalación del backend

Desde la raíz del proyecto, ejecuta en PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Revisa las variables de `.env` y luego aplica las migraciones e inicia Flask:

```powershell
flask --app run.py db upgrade
flask --app run.py run --debug
```

## Instalación del frontend

En otra terminal, desde la raíz del proyecto:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

La variable `VITE_API_URL` define la URL base utilizada por Axios.

## URLs

- Backend: `http://localhost:5000`
- Frontend: `http://localhost:5173`

## Pruebas

Para ejecutar las pruebas del backend:

```powershell
cd backend
pytest
```

Actualmente existen 13 pruebas automatizadas para las API de clientes y productos. Las 13 pruebas pasan correctamente.

Para revisar el frontend:

```powershell
cd frontend
npm run lint
npm run build
```

## Seguridad y configuración

- Los archivos `.env` contienen configuración local y no se suben al repositorio.
- Los archivos `.env.example` documentan las variables necesarias sin incluir secretos reales.
- CORS acepta solicitudes únicamente desde el origen configurado en `FRONTEND_ORIGIN`.
- El backend vuelve a validar los datos aunque el frontend ya haya realizado validaciones.
- Los entornos virtuales, `node_modules`, bases locales y archivos generados están excluidos mediante `.gitignore`.

## Capturas de pantalla

- Dashboard: pendiente de agregar.
- Clientes: pendiente de agregar.
- Productos: pendiente de agregar.
- Pedidos: pendiente de agregar.

## Autor

Jeason Marcos
