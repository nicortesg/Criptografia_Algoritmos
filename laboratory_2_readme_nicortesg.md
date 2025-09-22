# Laboratory 2 — Components and Connectors

**Nombre:** \<Nicolás Cortés Gutiérrez>

**Curso:** Arquitectura de software

---

## 1. Resumen

Este repositorio contiene la implementación del laboratorio 2 (Components and Connectors). Incluye 4 componentes: dos bases de datos (MongoDB y MySQL) y dos servicios (GraphQL con FastAPI y REST con Flask). El README documenta la arquitectura, cómo desplegarla con Docker Compose, cómo probar los flujos y qué entregar.

---

## 2. Vista Component-and-Connector
<img width="1384" height="144" alt="image" src="https://github.com/user-attachments/assets/a43a37f3-26e0-4245-9e8d-61d8e2cad0da" />
**component-1**: MongoDB. Almacena la colección `items` utilizada por component-2.
<img width="1903" height="703" alt="image" src="https://github.com/user-attachments/assets/9b882279-9449-4995-bd3f-53d6fb665514" />
**component-2**: FastAPI + Strawberry GraphQL (servicio GraphQL en `/graphql`, puerto `8000`). Conecta a MongoDB mediante `motor`.
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/7a6d62aa-f7bb-490e-8c26-0fc8ee1f3680" />
**component-3**: MySQL (imagen `mysql:8`). Base de datos relacional que almacena la tabla `items` usada por component-4.
<img width="1119" height="180" alt="image" src="https://github.com/user-attachments/assets/33783ff4-0405-4b94-92d2-548d3bfc096b" />
**component-4**: Flask REST API (endpoints `/items`, puerto `8001`). Conecta a MySQL usando `mysql-connector-python`.

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
