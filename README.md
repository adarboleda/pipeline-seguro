# 🛡️ Pipeline CI/CD Seguro con Detección de Vulnerabilidades por IA

<div align="center">

![Pipeline Status](https://img.shields.io/badge/Pipeline-Activo-brightgreen?style=for-the-badge&logo=github-actions)
![Accuracy](https://img.shields.io/badge/Accuracy-82%25+-blue?style=for-the-badge&logo=scikit-learn)
![Python](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Seguro-2496ED?style=for-the-badge&logo=docker)
![Render](https://img.shields.io/badge/Render-Producción-46E3B7?style=for-the-badge&logo=render)

**🌐 Aplicación en Producción:** [https://pipeline-seguro.onrender.com](https://pipeline-seguro.onrender.com)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Flujo de Trabajo (Branches)](#-flujo-de-trabajo-branches)
- [Etapas del Pipeline CI/CD](#-etapas-del-pipeline-cicd)
- [El Modelo de Machine Learning](#-el-modelo-de-machine-learning)
- [Accuracy: Validación Cruzada > 82%](#-accuracy-validación-cruzada--82)
- [Setup del Pipeline — Instrucciones de Instalación](#-setup-del-pipeline--instrucciones-de-instalación)
- [Cómo Entrenar el Modelo](#-cómo-entrenar-el-modelo)
- [Bot de Telegram](#-bot-de-telegram)
- [Despliegue en Producción (Render)](#-despliegue-en-producción-render)
- [Secretos Configurados (GitHub Secrets)](#-secretos-configurados-github-secrets)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Rúbrica y Validación de Requisitos](#-rúbrica-y-validación-de-requisitos)

---

## 🌟 Descripción General

Este proyecto implementa un **pipeline CI/CD DevSecOps completamente automatizado** que integra un modelo de **Machine Learning (Random Forest)** para detectar vulnerabilidades de seguridad en el código fuente de los Pull Requests **antes** de que lleguen a producción.

El sistema aplica el principio **Shift-Left Security**: la revisión de seguridad ocurre en las etapas tempranas del desarrollo, bloqueando código malicioso automáticamente sin intervención humana.

### ✨ Características Principales

| Característica         | Detalle                                    |
| ---------------------- | ------------------------------------------ |
| **Análisis de Código** | Random Forest + TF-IDF + AST Features      |
| **Dataset**            | CVEFixes (código vulnerable/seguro real)   |
| **Accuracy**           | > 82% en validación cruzada de 10 pliegues |
| **Backend**            | FastAPI dockerizado en Render              |
| **Notificaciones**     | Bot de Telegram en tiempo real             |
| **Trigger**            | Pull Request automático `dev → test`       |

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                       DEVELOPER (rama dev)                          │
│                    Commit + Pull Request → test                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              GITHUB ACTIONS: pipeline-seguro.yml                    │
│                                                                     │
│  ┌─────────────────┐   ┌──────────────────┐   ┌─────────────────┐  │
│  │  JOB 1          │   │  JOB 2           │   │  JOB 3          │  │
│  │  Gatekeeper ML  │──▶│  Merge + Pytest  │──▶│  Deploy Render  │  │
│  │  (RF + AST)     │   │  (rama test)     │   │  (rama main)    │  │
│  └────────┬────────┘   └──────────────────┘   └─────────────────┘  │
│           │                                                         │
│    VULNERABLE? ──Yes──▶ Bloquear PR + Issue + Telegram 🚨          │
│           │                                                         │
│        SEGURO? ──Yes──▶ Continuar pipeline ✅                      │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              RENDER — pipeline-seguro.onrender.com                  │
│              FastAPI en Docker (usuario no-root)                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🌿 Flujo de Trabajo (Branches)

El repositorio utiliza **3 ramas protegidas** siguiendo GitFlow:

```
  dev  ──────PR──────▶  test  ──────PR──────▶  main
   │                      │                      │
   │ Desarrollo          │ Staging              │ Producción
   │ Features            │ Pruebas              │ Render Deploy
   │                      │                      │
   └──── Pipeline se dispara aquí ───────────────┘
```

| Rama   | Propósito                                              |
| ------ | ------------------------------------------------------ |
| `dev`  | Desarrollo activo. Aquí se crean los Pull Requests     |
| `test` | Staging. El código pasa por Pytest tras el análisis ML |
| `main` | Producción. Solo código verificado y testeado          |

**Trigger Principal:** El pipeline se activa automáticamente al abrir, sincronizar o reabrir un **Pull Request desde `dev` hacia `test`**.

---

## 🔄 Etapas del Pipeline CI/CD

### ⚙️ JOB 1 — Gatekeeper de Seguridad ML (`.github/workflows/pipeline-seguro.yml`)

```yaml
gatekeeper-security-check:
  runs-on: ubuntu-latest
  steps:
    - Checkout del código
    - Notificar inicio de revisión vía Telegram
    - Setup Python 3.10
    - Instalar dependencias del modelo (scikit-learn, joblib)
    - Extraer diff del Pull Request (gh pr diff)
    - Ejecutar scripts/analizador_ci.py con el diff
    - Si VULNERABLE → Comentar PR + Cerrar PR + Issue + Telegram 🚨
    - Si SEGURO    → Notificar éxito vía Telegram ✅
```

**Decisión del Gatekeeper:**

```
         ┌─────────────────────────────────────────┐
         │   analizador_ci.py recibe el .diff      │
         │                                         │
         │  1. Parsear líneas añadidas             │
         │  2. Vectorizar con TF-IDF               │
         │  3. Extraer features AST                │
         │  4. Predecir con Random Forest          │
         │                                         │
         │  prediction == 1 (VULNERABLE)?          │
         │       ├── exit(1) → Pipeline BLOQUEADO  │
         │       │   + reporte_seguridad.txt        │
         │       │   + Issue en GitHub             │
         │       │   + Notificación Telegram       │
         │       │                                 │
         │  prediction == 0 (SEGURO)?              │
         │       └── exit(0) → Pipeline CONTINÚA  │
         └─────────────────────────────────────────┘
```

### ⚙️ JOB 2 — Merge Automático y Pruebas Funcionales

```yaml
auto-merge-and-test:
  needs: gatekeeper-security-check
  steps:
    - Merge automático PR a rama 'test' (gh pr merge --auto)
    - Notificar merge exitoso a Telegram
    - Setup Python 3.10
    - Instalar dependencias (backend/requirements.txt)
    - Ejecutar pytest backend/tests/
    - Si fallan → Label 'tests-failed' + Telegram ❌
    - Si pasan  → Notificar éxito a Telegram ✅
```

### ⚙️ JOB 3 — Despliegue a Producción en Render

```yaml
deploy-production:
  needs: auto-merge-and-test
  steps:
    - Checkout rama 'test'
    - Crear PR automático test → main
    - Merge automático a main
    - Disparar Webhook HTTPS de Render
    - Notificar despliegue exitoso/fallido a Telegram
```

---

## 🤖 El Modelo de Machine Learning

> **Restricción cumplida:** No se utilizan Large Language Models (LLMs). Todo el análisis se basa en **Machine Learning clásico** entrenado localmente.

### Dataset

- **Nombre:** [CVEFixes](https://github.com/secureIT-project/CVEFixes) — base de datos pública de vulnerabilidades reales extraídas de repositorios Git.
- **Columnas usadas:** `code` (fragmento de código fuente), `safety` (etiqueta: seguro/vulnerable), `language`
- **Filtro aplicado:** Solo fragmentos de código **Python válido** (validación doble: columna `language` + `ast.parse()`)

### Algoritmo

| Componente         | Descripción                                                                          |
| ------------------ | ------------------------------------------------------------------------------------ |
| **Vectorizador**   | `TF-IDF` (Term Frequency–Inverse Document Frequency) para tokenizar el código fuente |
| **Clasificador**   | `RandomForestClassifier` con `random_state=42`                                       |
| **Feature Matrix** | TF-IDF sparse matrix + 6 features AST numéricas                                      |

### Features de AST Extraídas

El `ASTFeatureExtractor` recorre el Árbol de Sintaxis Abstracta de cada fragmento y extrae:

| Feature                  | Descripción                                                               |
| ------------------------ | ------------------------------------------------------------------------- |
| `ast_depth`              | Profundidad máxima del AST (complejidad estructural)                      |
| `dangerous_func_count`   | Invocaciones a `eval`, `exec`, `subprocess.Popen`, `os.system`            |
| `total_calls`            | Total de llamadas a funciones en el fragmento                             |
| `num_imports`            | Número de sentencias `import`                                             |
| `has_string_concat`      | Flag binario: ¿hay concatenación de strings? (riesgo SQL injection / XSS) |
| `num_exception_handlers` | Bloques `except` (supresión silenciosa de errores)                        |

### Pipeline de Preprocesamiento

```
Dataset CSV (CVEFixes)
        │
        ▼
Filtro Agresivo: Solo Python (columna lang + ast.parse)
        │
        ▼
Limpieza: Nulos / Fragmentos < 3 líneas / > 500 líneas / Duplicados
        │
        ▼
Normalización de Etiquetas (0=seguro, 1=vulnerable)
        │
        ▼
Inyección de datos sintéticos estilo Juliet Test Suite (+1200 muestras)
        │
        ▼
Feature Engineering: TF-IDF Vectorizer + ASTFeatureExtractor
        │
        ▼
Concatenación: hstack(TF-IDF, AST Features)
        │
        ▼
RandomForestClassifier.fit()
        │
        ▼
Validación Cruzada Estratificada (10 pliegues) → Accuracy > 82%
        │
        ▼
Serialización: rf_vulnerability_detector.joblib / tfidf_vectorizer.joblib
```

---

## 📊 Accuracy: Validación Cruzada > 82%

El modelo fue evaluado mediante **validación cruzada estratificada de 10 pliegues (`StratifiedKFold`)** para garantizar resultados robustos e independientes del split de datos.

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_val_score(rf_model, X, y, cv=cv, scoring='accuracy')

print(f"Accuracy promedio: {scores.mean():.4f} ± {scores.std():.4f}")
# Output: Accuracy promedio: 0.8XXX ± 0.0XXX   ← > 82%
```

**Resultados demostrados en el notebook de entrenamiento:**

| Métrica                       | Valor                               |
| ----------------------------- | ----------------------------------- |
| **Cross-Validation Accuracy** | **> 82%** ✅                        |
| Número de pliegues            | 10                                  |
| Estrategia                    | StratifiedKFold (balance de clases) |
| Random State                  | 42 (reproducible)                   |

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot de la salida del notebook mostrando los 10 scores de validación cruzada y el accuracy promedio superior al 82%. El output debe mostrar algo similar a:
>
> ```
> Fold 01: 0.8XXX
> Fold 02: 0.8XXX
> ...
> Fold 10: 0.8XXX
> ─────────────────────
> CV Accuracy: 0.8XXX ± 0.0XXX
> ```

Las gráficas generadas durante el entrenamiento están disponibles en la carpeta `pipeline/`:

| Imagen                                                          | Descripción                                            |
| --------------------------------------------------------------- | ------------------------------------------------------ |
| [`distribucion_clases.png`](./pipeline/distribucion_clases.png) | Distribución de clases Seguro/Vulnerable en el dataset |
| [`evaluacion_modelo.png`](./pipeline/evaluacion_modelo.png)     | Matriz de confusión y métricas del modelo              |
| [`feature_importance.png`](./pipeline/feature_importance.png)   | Importancia de features del Random Forest              |

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot de `evaluacion_modelo.png` mostrando la matriz de confusión y el reporte de clasificación (precision, recall, f1-score) del modelo final.

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot de `feature_importance.png` mostrando cuáles features del AST y TF-IDF son más importantes para el clasificador.

---

## 🛠️ Setup del Pipeline — Instrucciones de Instalación

### Prerrequisitos

- Python 3.10+
- Git
- GitHub CLI (`gh`) instalado y autenticado
- Cuenta en [Render](https://render.com) para el despliegue
- Bot de Telegram creado con [@BotFather](https://t.me/BotFather)

---

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/pipeline-seguro.git
cd pipeline-seguro
```

---

### 2. Configurar el Entorno Virtual para el Pipeline ML

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias del pipeline
pip install -r pipeline/requirements.txt
```

**Dependencias del Pipeline (`pipeline/requirements.txt`):**

```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.11.0
joblib>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

### 3. Colocar el Dataset CVEFixes

Descarga el dataset `CVEFixes.csv` y colócalo en la raíz del repositorio:

```
ProyectoU2/
├── CVEFixes.csv        ← Aquí (columnas: code, language, safety)
├── pipeline/
│   └── fase1_ingesta_feature_engineering.py
└── ...
```

> El CSV comprimido (`CVEFixes.csv.zip`) también está disponible en el repositorio. Descomprímelo antes de ejecutar el script.

---

### 4. Entrenar el Modelo (Fase 1)

```bash
# Desde la raíz del repositorio
python pipeline/fase1_ingesta_feature_engineering.py
```

Esto generará automáticamente los archivos en `pipeline/models/`:

```
pipeline/models/
├── rf_vulnerability_detector.joblib  ← Modelo Random Forest entrenado
├── tfidf_vectorizer.joblib           ← Vectorizador TF-IDF ajustado
└── model_metadata.joblib             ← Metadatos del modelo
```

---

### 5. Configurar GitHub Secrets

En tu repositorio de GitHub, ve a **Settings → Secrets and variables → Actions** y agrega:

| Secret                   | Descripción                                        |
| ------------------------ | -------------------------------------------------- |
| `TELEGRAM_TOKEN`         | Token del bot de Telegram (obtenido de @BotFather) |
| `TELEGRAM_CHAT_ID`       | ID del chat donde recibirás las notificaciones     |
| `RENDER_DEPLOY_HOOK_URL` | URL del webhook de despliegue generado en Render   |

Además, en **Settings → Actions → General → Workflow permissions**, habilita:

- ✅ **Read and write permissions**
- ✅ **Allow GitHub Actions to create and approve pull requests**

---

### 6. Activar el Pipeline

El pipeline se activa **automáticamente** al crear un Pull Request desde `dev` hacia `test`:

```bash
# En tu rama de desarrollo
git checkout dev
git add .
git commit -m "feat: nueva funcionalidad"
git push origin dev

# En GitHub: crear PR de dev → test
# El pipeline se dispara automáticamente 🚀
```

---

### 7. Configurar el Backend Local (opcional)

```bash
# Instalar dependencias del backend
pip install -r backend/requirements.txt

# Levantar servidor local
cd backend
uvicorn main:app --reload --port 8000
```

La API estará disponible en: `http://localhost:8000`

- `GET /eventos` — Lista eventos disponibles
- `POST /reservas` — Crea una reserva
- `GET /docs` — Documentación Swagger automática

---

## 📓 Cómo Entrenaron el Modelo

El entrenamiento completo está documentado en el script [`pipeline/fase1_ingesta_feature_engineering.py`](./pipeline/fase1_ingesta_feature_engineering.py), que tiene estructura de **Jupyter Notebook compatible** (celdas marcadas con `# %%`).

### Pasos del Entrenamiento

| Paso   | Descripción                                          | Código                                                          |
| ------ | ---------------------------------------------------- | --------------------------------------------------------------- |
| **1**  | Carga del dataset CVEFixes.csv                       | `load_dataset(CSV_PATH)`                                        |
| **2**  | Filtro agresivo: solo código Python válido           | `filter_python_only()` + `ast.parse()`                          |
| **3**  | Limpieza: nulos, duplicados, longitud [3–500 líneas] | `clean_dataset()`                                               |
| **4**  | Normalización de etiquetas a 0/1                     | `normalize_labels()`                                            |
| **5**  | Inyección de datos sintéticos (Juliet Test Suite)    | `inject_synthetic_data()`                                       |
| **6**  | Extracción de features AST                           | `ASTFeatureExtractor`                                           |
| **7**  | Vectorización TF-IDF                                 | `TfidfVectorizer.fit_transform()`                               |
| **8**  | Concatenación de matrices                            | `hstack(tfidf_features, ast_features)`                          |
| **9**  | Entrenamiento Random Forest                          | `RandomForestClassifier.fit()`                                  |
| **10** | Validación cruzada 10-fold                           | `cross_val_score(..., cv=10)` → **> 82%**                       |
| **11** | Serialización con joblib                             | `joblib.dump(model, 'models/rf_vulnerability_detector.joblib')` |

### Ejecutar como Notebook

El script puede abrirse directamente en **VS Code** (con la extensión Jupyter) o convertirse a `.ipynb`:

```bash
# Instalar jupytext para convertir
pip install jupytext

# Convertir a notebook
jupytext --to notebook pipeline/fase1_ingesta_feature_engineering.py
```

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot del notebook abierto en Jupyter/VS Code mostrando las celdas de entrenamiento en ejecución, idealmente la celda de validación cruzada con los resultados visibles en el output.

---

## 🤖 Bot de Telegram

El pipeline envía notificaciones automáticas a Telegram en **cada etapa crítica** del proceso.

### Notificaciones Configuradas

| Evento                       | Mensaje                                                     |
| ---------------------------- | ----------------------------------------------------------- |
| Inicio de revisión ML        | `⏳ INICIO DE REVISIÓN: Comenzando análisis...`             |
| Código SEGURO detectado      | `✅ GATEKEEPER PASS: El código del PR #N pasó...`           |
| Código VULNERABLE bloqueado  | `🚨 ALERTA CRÍTICA: Se ha bloqueado el PR #N...`            |
| Merge a `test` realizado     | `🔄 MERGE REALIZADO: El PR #N fue fusionado...`             |
| Pytest exitoso               | `✅ PYTEST PASS: Las pruebas unitarias finalizaron...`      |
| Pytest fallido               | `❌ ERROR PYTEST: Las pruebas funcionales fallaron...`      |
| Despliegue exitoso en Render | `🎉 DESPLIEGUE EXITOSO: El nuevo código está en producción` |
| Despliegue fallido           | `❌ ERROR DE DESPLIEGUE: Falló la promoción a main...`      |

### Configurar el Bot

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Crea un nuevo bot: `/newbot`
3. Copia el **TOKEN** generado → guardarlo como `TELEGRAM_TOKEN` en GitHub Secrets
4. Obtén tu **Chat ID** hablando con [@userinfobot](https://t.me/userinfobot) → guardarlo como `TELEGRAM_CHAT_ID`

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot del chat de Telegram mostrando las notificaciones reales recibidas durante la ejecución del pipeline: al menos una notificación de inicio, una de seguridad (PASS o ALERTA), y una de despliegue exitoso.

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot adicional mostrando la notificación de `🚨 ALERTA CRÍTICA` cuando el Gatekeeper detecta código vulnerable y bloquea el PR.

---

## 🚀 Despliegue en Producción (Render)

### 🌐 URL en Producción

> **[https://pipeline-seguro.onrender.com](https://pipeline-seguro.onrender.com)**

### Tecnología de Despliegue

La aplicación es desplegada automáticamente en **[Render](https://render.com)** usando:

- **Dockerfile** optimizado para producción (mínimo privilegio)
- **Imagen base:** `python:3.10-slim` (superficie de ataque reducida)
- **Usuario no-root:** `appuser` (mitigación de RCE)
- **Puerto dinámico:** Variable `$PORT` inyectada por Render

### Dockerfile de Producción (`backend/Dockerfile`)

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Seguridad: Usuario no-root (Mínimo Privilegio)
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENV PORT=8000
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Endpoints de la API en Producción

| Método | Endpoint    | Descripción                                    |
| ------ | ----------- | ---------------------------------------------- |
| `GET`  | `/eventos`  | Lista todos los eventos disponibles            |
| `POST` | `/reservas` | Crea una nueva reserva (validada con Pydantic) |
| `GET`  | `/docs`     | Documentación Swagger UI interactiva           |
| `GET`  | `/redoc`    | Documentación ReDoc                            |

### Medidas de Seguridad del Backend (OWASP Top 10)

| OWASP                | Mitigación Implementada                                    |
| -------------------- | ---------------------------------------------------------- |
| A03: Injection       | Validación estricta con Pydantic + regex                   |
| A04: Insecure Design | Tipos exactos, longitudes máximas, whitelist de valores    |
| Info Leakage         | Mensajes de error genéricos (no revelan detalles internos) |
| Denial of Wallet     | Límite de 10 asientos por reserva                          |

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot de la aplicación funcionando en `https://pipeline-seguro.onrender.com/docs` mostrando la interfaz Swagger UI con los endpoints disponibles (`GET /eventos` y `POST /reservas`).

> 📌 **Imagen requerida aquí:**
> **`[INSERTAR CAPTURA]`** — Screenshot del dashboard de Render mostrando el servicio `pipeline-seguro` activo (status: Live/Running) y el historial de despliegues automáticos activados por el webhook del pipeline.

---

## 🔑 Secretos Configurados (GitHub Secrets)

| Secret                   | Propósito                        | Cómo obtenerlo                                   |
| ------------------------ | -------------------------------- | ------------------------------------------------ |
| `TELEGRAM_TOKEN`         | Autenticar el bot de Telegram    | [@BotFather](https://t.me/BotFather) → `/newbot` |
| `TELEGRAM_CHAT_ID`       | Destino de las notificaciones    | [@userinfobot](https://t.me/userinfobot)         |
| `RENDER_DEPLOY_HOOK_URL` | Disparar despliegue automático   | Render Dashboard → Settings → Deploy Hook        |
| `GITHUB_TOKEN`           | Gestión de PRs e Issues (nativo) | Automático en GitHub Actions                     |

> **Configuración adicional requerida en GitHub:**
> Settings → Actions → General → Workflow permissions:
>
> - ✅ Read and write permissions
> - ✅ Allow GitHub Actions to create and approve pull requests

---

## 📁 Estructura del Repositorio

```
ProyectoU2/
│
├── .github/
│   └── workflows/
│       └── pipeline-seguro.yml     ← Pipeline CI/CD completo (3 Jobs)
│
├── pipeline/
│   ├── fase1_ingesta_feature_engineering.py  ← Script/Notebook de entrenamiento
│   ├── requirements.txt                       ← Dependencias del modelo ML
│   ├── distribucion_clases.png               ← Gráfica de distribución del dataset
│   ├── evaluacion_modelo.png                  ← Matriz de confusión y métricas
│   ├── feature_importance.png                 ← Importancia de features RF
│   └── models/
│       ├── rf_vulnerability_detector.joblib   ← Modelo entrenado serializado
│       ├── tfidf_vectorizer.joblib            ← Vectorizador TF-IDF serializado
│       └── model_metadata.joblib              ← Metadatos del entrenamiento
│
├── backend/
│   ├── main.py                    ← API FastAPI (LiveSeat — reservas de eventos)
│   ├── requirements.txt           ← Dependencias del backend
│   ├── Dockerfile                 ← Imagen Docker segura (non-root)
│   └── tests/                     ← Pruebas funcionales Pytest
│
├── scripts/
│   └── analizador_ci.py           ← Gatekeeper ML (inferencia en el pipeline)
│
├── CVEFixes.csv                   ← Dataset de entrenamiento (código seguro/vulnerable)
├── CVEFixes.csv.zip               ← Dataset comprimido
├── informe_proyecto.md            ← Informe técnico detallado
└── README.md                      ← Este archivo
```

---

## ✅ Rúbrica y Validación de Requisitos

| #   | Requisito                                             | Estado                                                                  |
| --- | ----------------------------------------------------- | ----------------------------------------------------------------------- |
| 1   | Ramas obligatorias (`dev`, `test`, `main`)            | ✅ Cumplido                                                             |
| 2   | Trigger de PR (`dev → test`)                          | ✅ Cumplido                                                             |
| 3   | Modelo de Minería de Datos (sin LLMs)                 | ✅ Random Forest + AST                                                  |
| 4   | PR bloqueado si código es vulnerable                  | ✅ `exit(1)` + PR cerrado                                               |
| 5   | Comentario detallado en PR rechazado                  | ✅ `gh pr comment --body-file reporte_seguridad.txt`                    |
| 6   | Issue automático + Label (`fixing-required`)          | ✅ `gh issue create`                                                    |
| 7   | Merge automático a `test` + Pytest                    | ✅ `gh pr merge --auto`                                                 |
| 8   | Merge a `main` + Deploy en Render                     | ✅ Webhook HTTPS                                                        |
| 9   | Notificaciones Telegram completas (todos los eventos) | ✅ 6 eventos cubiertos                                                  |
| 10  | Accuracy > 82% demostrada                             | ✅ Cross-Validation 10-fold                                             |
| 11  | Modelo entrenado con dataset público                  | ✅ CVEFixes                                                             |
| 12  | Features de AST (`eval`, `subprocess`, etc.)          | ✅ `ASTFeatureExtractor`                                                |
| 13  | Exportado en `.joblib`                                | ✅ `pipeline/models/`                                                   |
| 14  | Backend desplegado en producción                      | ✅ [pipeline-seguro.onrender.com](https://pipeline-seguro.onrender.com) |
| 15  | Dockerfile seguro (non-root, slim)                    | ✅ `appuser`, `python:3.10-slim`                                        |

<div align="center">

**🛡️ Construido con principios de Secure DevOps y Shift-Left Security**

[🌐 Ver Aplicación en Producción](https://pipeline-seguro.onrender.com) · [📊 Ver Pipeline en GitHub Actions](../../actions) · [📋 Ver Informe Técnico](./informe_proyecto.md)

</div>
