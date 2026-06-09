# Informe Técnico: Desarrollo e Implementación de un Pipeline CI/CD Seguro con IA para Detección de Vulnerabilidades

## 1. Objetivo del Proyecto
Diseñar, implementar y demostrar un pipeline CI/CD completamente automatizado y seguro que integra un modelo de inteligencia artificial basado en Minería de Datos (Machine Learning clásico). El modelo clasifica el código fuente de los Pull Requests como **Seguro** o **Vulnerable**, bloqueando código malicioso y permitiendo que solo código verificado alcance la etapa de producción en Render.

Todo el proceso cumple estrictamente con los principios de **Secure DevOps** y **Shift-Left Security**.

---

## 2. Flujo de Trabajo (Branches y Triggers)
El repositorio Git cuenta con tres ramas fundamentales:
- **`dev`**: Rama de desarrollo donde se integran las nuevas características.
- **`test`**: Rama de staging y ejecución de pruebas funcionales (Pytest).
- **`main`**: Rama de producción (despliegue a Render).

**Trigger Principal:**
El pipeline se dispara automáticamente en GitHub Actions cada vez que se crea o actualiza un **Pull Request (PR) desde `dev` hacia `test`**.

---

## 3. Modelo de Minería de Datos (Machine Learning)
Se cumplió de forma estricta la restricción de **no utilizar Large Language Models (LLM)**. Todo el análisis de seguridad se fundamenta en un modelo de Minería de Datos Tradicional entrenado localmente.

### Detalles del Entrenamiento
- **Dataset:** Se utilizó el dataset público **CVEFixes** (código vulnerable y seguro extraído de repositorios públicos).
- **Algoritmo:** **Random Forest Classifier** apoyado en un **TF-IDF Vectorizer** (NLP clásico para tokenización).
- **Extracción de Features:** El script de entrenamiento (Notebook `fase1_ingesta_feature_engiennering.ipynb`) y el Gatekeeper (`analizador_ci.py`) extraen un mix de features NLP y AST (Abstract Syntax Tree):
  1. Conteo de tokens (TF-IDF).
  2. Complejidad y profundidad del código (AST Depth).
  3. Llamadas a funciones peligrosas (`eval`, `exec`, `subprocess`, `os.system`).
  4. Concatenación insegura de strings.
- **Resultados de Accuracy:** El modelo alcanzó una precisión (Cross-Validation Accuracy) superior al **82%** (demostrada en el reporte de Fase 1 del proyecto).
- **Archivos Entregados:** `.joblib` exportados y presentes en el repositorio (`model_metadata.joblib`, `rf_vulnerability_detector.joblib`, `tfidf_vectorizer.joblib`).

---

## 4. Etapas del Pipeline CI/CD

### Etapa 1: Revisión de Seguridad (Gatekeeper ML)
1. Extrae el `diff` (solo las líneas modificadas y añadidas) del Pull Request mediante GitHub CLI.
2. Extrae los nombres de los archivos modificados.
3. Ejecuta `scripts/analizador_ci.py` pasándole el `diff`.
4. El script carga los modelos `.joblib`, extrae el AST y los features TF-IDF (ofuscando palabras clave para evitar auto-falsos positivos).
5. **Si es VULNERABLE:**
   - Termina con `exit 1` bloqueando el pipeline.
   - Crea un comentario automático en el PR con el reporte de probabilidad y archivos afectados.
   - Envía notificación urgente por Telegram.
   - Crea un Issue automático vinculando el PR fallido.
   - Etiqueta el PR como rechazado.
6. **Si es SEGURO:** Continúa hacia la Etapa 2.

### Etapa 2: Merge Automático y Pruebas
1. Se utiliza `gh pr merge --auto --merge` para fusionar el código seguro en `test`.
2. Se instalan dependencias usando `backend/requirements.txt`.
3. Se ejecutan las pruebas funcionales de la API (FastAPI) usando `Pytest`.
4. **Si las pruebas fallan:** Etiqueta el PR con `tests-failed` y envía un mensaje de error a Telegram.
5. **Si pasan:** Envía un mensaje de éxito a Telegram.

### Etapa 3: Despliegue en Producción
1. Al pasar todas las pruebas, se crea automáticamente un PR desde `test` hacia `main` y se fusiona automáticamente (promoción de código).
2. Se dispara un Webhook HTTPS hacia **Render**.
3. Render descarga la rama `main`, detecta la carpeta `backend/` y el archivo `Dockerfile`, reconstruye la imagen basada en `python:3.10-slim` (con usuario no root), y levanta el contenedor.
4. Se envía una notificación final de Telegram confirmando el despliegue exitoso.

---

## 5. Secretos Configurados (GitHub Secrets)
Para lograr la completa automatización, se utilizaron los siguientes Secrets en GitHub Actions:
- `TELEGRAM_TOKEN`: Token del bot de Telegram creado mediante BotFather.
- `TELEGRAM_CHAT_ID`: ID del chat del desarrollador o del equipo para recibir las notificaciones.
- `RENDER_DEPLOY_HOOK_URL`: URL del webhook generado en el Dashboard de Render para activar despliegues automáticos.
- `GITHUB_TOKEN` (Nativo): Permiso elevado habilitado en Settings (`Workflow permissions: Read and write permissions + Allow GitHub Actions to create and approve PRs`) para la auto-gestión de Issues y PRs.

---

## 6. Validación de Rúbrica y Requisitos

✅ **1. Ramas obligatorias (dev, test, main):** Cumplido.
✅ **2. Trigger de PR (dev -> test):** Cumplido.
✅ **3. Etapa 1 - Modelo de Minería de Datos:** Cumplido. No usa LLMs (se usa Random Forest + AST).
✅ **4. Etapa 1 - PR bloqueado si es vulnerable:** Cumplido (exit code 1).
✅ **5. Etapa 1 - Comentario detallado en PR:** Cumplido (`gh pr comment --body-file reporte_seguridad.txt`).
✅ **6. Etapa 1 - Issue automática/Etiqueta (fixing-required):** Cumplido (`gh issue create`).
✅ **7. Etapa 2 - Merge automático a test + Pytest:** Cumplido (`gh pr merge`).
✅ **8. Etapa 3 - Merge a main y Despliegue en Render:** Cumplido (Webhook a Render, backend Dockerizado con privilegios mínimos).
✅ **9. Notificaciones de Telegram completas:** Cumplido *(Se actualizaron todas en el último commit para cumplir la rúbrica al 100%)*:
  - *Inicio de revisión de seguridad* ✅
  - *Resultado de la clasificación* ✅
  - *Merge a test realizado* ✅
  - *Resultado de pruebas (Pytest exitoso o fallido)* ✅
  - *Despliegue exitoso o fallido* ✅
  - *Rechazo por vulnerabilidad con detalles* ✅
✅ **10. Requisitos del Modelo:** Cumplido. Entrenado localmente, dataset público (CVEFixes), features de AST (eval, subprocess), >82% accuracy, exportado en `.joblib`.

### Detalles de la entrega:
- **Repositorio:** Configurado completamente.
- **Bot de Telegram:** Funcionando con todos los eventos.
- **Aplicación Desplegada:** `pipeline-seguro.onrender.com`.
- **Dockerfile Seguro:** Mínimo privilegio, usuario `appuser`, `python-slim`.

**Todo cumple al 100% con los lineamientos del proyecto.**
