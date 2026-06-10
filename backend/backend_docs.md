# Documentación del Backend (LiveSeat API)

## 📌 Arquitectura y Diseño (Clean Architecture)
Este proyecto ha sido refactorizado para utilizar los principios de **Clean Architecture**, dividiendo responsabilidades en capas claras y mejorando la mantenibilidad, escalabilidad y la **seguridad**.

### Estructura de Directorios:
- **`app/main.py`**: El punto de entrada principal (Entrypoint). Aquí inicializamos FastAPI e incluimos nuestros *routers* de forma modular.
- **`app/models/`**: Contiene los modelos de dominio. Estos modelos representan las estructuras de datos de negocio puras (y el esquema en base de datos interna).
- **`app/schemas/`**: Pydantic models encargados de la validación, transformación y **sanitización** estricta de las entradas (requests) y salidas (responses) de la API. Mitiga problemas como Inyecciones y XSS.
- **`app/services/`**: Concentra toda la **lógica de negocio**. (Ej. Reglas para reservar un asiento o crear un evento). Así desacoplamos la lógica del transporte HTTP.
- **`app/api/endpoints/`**: Aquí van exclusivamente los Controladores (Routers) de FastAPI, cuya única labor es recibir HTTP Requests, llamar a los Servicios y retornar las Responses HTTP.
- **`app/db/`**: Lógica de almacenamiento. Por ahora simula una base de datos en memoria (Diccionario).

---

## 🔒 Mecanismos de Seguridad
1. **Validación Exhaustiva (Pydantic):** Restricciones de tipos (`int`, `str`, `EmailStr`), límites (`min_length`, `max_length`), y Expresiones Regulares (`pattern`) evitan cargas (payloads) maliciosos, SQLi, DoS lógicos, etc.
2. **Sanitización XSS (Bleach):** Se implementó sanitización con la librería `bleach` en los esquemas de creación (como el nombre del evento) para remover etiquetas y atributos HTML maliciosos, frustrando intentos de Cross-Site Scripting (XSS).
3. **Mínimo Privilegio (Docker):** El contenedor de la app no ejecuta como `root`, previniendo toma de control del servidor en caso de ejecución remota de código (RCE).
4. **Manejo Correcto de Errores:** Errores 404 estandarizados que evitan *Fugas de Información* (Information Leakage).

---

## 📡 Endpoints de la API

### 1. Gestión de Eventos
- **`GET /eventos/`**
  - **Descripción:** Lista todos los eventos disponibles.
  - **Respuesta:**
    ```json
    [
      {
        "id": 1,
        "nombre": "Concierto Rock Clasico",
        "asientos_disponibles": 100
      }
    ]
    ```

- **`POST /eventos/`**
  - **Descripción:** Crea un evento nuevo asegurando la limpieza del input (Sanitización XSS activa).
  - **Body de Ejemplo:**
    ```json
    {
      "nombre": "Festival de Verano",
      "asientos_disponibles": 500
    }
    ```

### 2. Gestión de Reservas
- **`POST /reservas/`**
  - **Descripción:** Crea una reserva descontando el inventario disponible y validando la lógica del negocio.
  - **Body de Ejemplo:**
    ```json
    {
      "evento_id": 1,
      "email_usuario": "usuario@ejemplo.com",
      "cantidad_asientos": 2,
      "metodo_pago": "tarjeta"
    }
    ```
  - **Respuesta:**
    ```json
    {
      "mensaje": "Reserva confirmada exitosamente",
      "detalles": {
        "evento_id": 1,
        "asientos_reservados": 2,
        "reserva_id": 1
      }
    }
    ```

- **`GET /reservas/`**
  - **Descripción:** Lista todas las reservas realizadas.
