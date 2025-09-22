# Laboratory 2 — Components and Connectors

**Nombre:** \<Nicolás Cortés Gutiérrez>

**Curso:** Arquitectura de software

---

## 1. Resumen

Este repositorio contiene la implementación del laboratorio 2 (Components and Connectors). Incluye 4 componentes: dos bases de datos (MongoDB y MySQL) y dos servicios (GraphQL con FastAPI y REST con Flask). El README documenta la arquitectura, cómo desplegarla con Docker Compose, cómo probar los flujos y qué entregar.

---

## 2. Vista Component-and-Connector
![alt text](image.png)
- **component-1**: MongoDB. Almacena la colección `items` utilizada por component-2.
- **component-2**: FastAPI + Strawberry GraphQL (servicio GraphQL en `/graphql`, puerto `8000`). Conecta a MongoDB mediante `motor`.
- **component-3**: MySQL (imagen `mysql:8`). Base de datos relacional que almacena la tabla `items` usada por component-4.
- **component-4**: Flask REST API (endpoints `/items`, puerto `8001`). Conecta a MySQL usando `mysql-connector-python`.

---

## 3. Conectores identificados

- **TCP/DB connectors**:
  - `component-2 -> component-1`: URI `mongodb://component-1:27017` (driver `motor`).
  - `component-4 -> component-3`: host `component-3`, puerto `3306` (driver `mysql-connector-python`).
- **HTTP connectors**:
  - Cliente (curl / navegador) -> `component-2`: HTTP GraphQL en `http://localhost:8000/graphql`.
  - Cliente (curl / Postman) -> `component-4`: HTTP REST en `http://localhost:8001/items`.
- **Conectores internos**: bibliotecas/drivers que traducen llamadas de la app a operaciones de persistencia.

---

## 4. Estructura de archivos (resumen)

```
c&c/
├─ component-2/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ db.py
│  │  ├─ main.py
│  │  └─ schema.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ component-4/
│  ├─ app/
│  │  └─ app.py
│  ├─ requirements.txt
│  └─ Dockerfile
└─ docker-compose.yml
```

---

## 5. Requisitos previos

- Docker Desktop con integración WSL2 (si trabajas en Windows + WSL).
- WSL2 (o un Linux con Docker instalado).
- `docker` y `docker compose` disponibles en la terminal.

---

## 6. Comandos para ejecutar (desde la carpeta raíz `c&c`)

1. Levantar todo (construir imágenes):

```bash
docker compose up --build
# o en background:
docker compose up --build -d
```

2. Verificar contenedores:

```bash
docker compose ps
```

3. Ver logs de un servicio (ejemplo MySQL):

```bash
docker compose logs -f component-3
```

4. Parar y eliminar recursos:

```bash
docker compose down
```

---

## 7. Flow 1 — MySQL + component-4 (REST)

### 7.1 Crear la tabla `items` en MySQL

Puedes hacerlo de forma interactiva o en una sola línea.

**Interactivo**:

```bash
# entrar al shell del contenedor MySQL
docker exec -it component-3 sh
# dentro del contenedor
mysql -u root -p
# contraseña: 123
USE db;
CREATE TABLE IF NOT EXISTS items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT
);
SELECT * FROM items;
EXIT;
```

**No interactivo (una sola línea)**:

```bash
docker exec -i component-3 mysql -u root -p123 -e "USE db; CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT);"
```

### 7.2 Probar el endpoint REST (component-4)

Insertar un item:

```bash
curl -X POST http://localhost:8001/items \
  -H "Content-Type: application/json" \
  -d '{"name": "SwArch", "description": "2025-I"}'
```

Obtener items:

```bash
curl http://localhost:8001/items
```

Verificar en MySQL:

```bash
docker exec -i component-3 mysql -u root -p123 -e "USE db; SELECT * FROM items;"
```

---

## 8. Flow 2 — MongoDB + component-2 (GraphQL)

### 8.1 Insertar usando GraphQL (recomendada)

**Mutación (curl)**:

```bash
curl -s -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { addItem(name: \"SwArch\", description: \"2025-I\") { id name description } }"}'
```

**Consulta (curl)**:

```bash
curl -s -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"query { items { id name description } }"}'
```

O usa la interfaz web: `http://localhost:8000/graphql`.

### 8.2 Ver directamente en Mongo

```bash
docker exec -it component-1 mongosh --eval 'use db; db.items.find().pretty()'
```

---

## 9. Troubleshooting (problemas comunes)

- ``\*\* no encontrado\*\*: en WSL usa `docker compose` (plugin) y asegúrate de activar WSL Integration en Docker Desktop.
- ``\*\* a la DB al arrancar\*\*: `depends_on` no espera a que la DB esté lista. Espera unos segundos o añade `healthcheck` en `docker-compose.yml`.
- **Permisos docker**: si `docker` requiere sudo, añade tu usuario al grupo `docker` (`sudo usermod -aG docker $USER`) y reconéctate.
- **Puerto en uso**: ajusta los mapeos de puertos en `docker-compose.yml` si aparecen errores de bind.

---

## 10. Entrega — formato y pasos (GitHub)

1. Crea la rama `laboratory_2`:

```bash
git checkout -b laboratory_2
```

2. Crea la carpeta del usuario (reemplaza `<TU_UNAL_USERNAME>`):

```
mkdir -p laboratories/laboratory_2/<TU_UNAL_USERNAME>
```

3. Mueve o copia este README.md dentro de esa carpeta (o crea un README con el mismo contenido).
4. Añade, commitea y pushea:

```bash
git add laboratories/laboratory_2/<TU_UNAL_USERNAME>/README.md
git commit -m "Laboratory 2 - deliverable"
git push origin laboratory_2
```

---

## 11. Archivos a incluir en la entrega

- `docker-compose.yml`
- `component-2/` (app, Dockerfile, requirements.txt)
- `component-4/` (app, Dockerfile, requirements.txt)
- `README.md` (este archivo)

---

## 12. Notas finales

- Reemplaza el campo **Nombre** y `<TU_UNAL_USERNAME>` antes de commitear.
- Si quieres, incluye capturas de pantalla (logs, GraphQL con datos) en la carpeta de la entrega.

---

Si necesitas que adapte el README (por ejemplo, traducir, añadir diagrama, capturas o instrucciones para Windows), dime qué quieres cambiar y lo actualizo.

