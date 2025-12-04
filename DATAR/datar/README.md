## DATAR – Despliegue privado en Cloud Run con bucket de medios y `adk deploy cloud_run`

Este README describe el flujo de **despliegue en Cloud Run (privado)** usando `adk deploy cloud_run` desde código fuente, y cómo se integran:
- El **bucket de medios** en Cloud Storage (para `.wav` y `.png` generados por los agentes `Gente_*`).
- Los **secretos** (especialmente `OPENROUTER_API_KEY`).
- La **autenticación** con tokens de identidad para acceder al servicio privado.

La estructura ya cumple con la guía oficial de ADK para Cloud Run en Python:  
`https://google.github.io/adk-docs/deploy/cloud-run/`

---

### 1. Variables de entorno locales

Desde el directorio `DATAR/`:

```bash
cd /Users/manglerojo/Desarollo/DATAR/integracion-1/DATAR

export GOOGLE_CLOUD_PROJECT="TU_PROYECTO"
export GOOGLE_CLOUD_LOCATION="southamerica-east1"

# Nombre de bucket único (ajusta el sufijo para tu entorno)
export MEDIA_BUCKET_NAME="datar-integraciones-media-dev"
```

En `DATAR/.env` define al menos:

```env
OPENROUTER_API_KEY=tu_clave_de_openrouter
GOOGLE_CLOUD_PROJECT=tu-proyecto-gcp
GOOGLE_CLOUD_LOCATION=southamerica-east1
```

Los agentes suben archivos a rutas como:
- `gente_sonora/audio/...`
- `gente_pasto/audio/...`
- `gente_bosque/cartografias/...`
- `gente_intuitiva/imagenes/...`

---

### 2. Crear y configurar el bucket de medios en Cloud Storage

```bash
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Crear bucket regional
gcloud storage buckets create gs://$MEDIA_BUCKET_NAME \
  --project=$GOOGLE_CLOUD_PROJECT \
  --location=$GOOGLE_CLOUD_LOCATION \
  --uniform-bucket-level-access

# Permitir lectura pública de objetos (para Discord / web‑app)
gcloud storage buckets add-iam-policy-binding gs://$MEDIA_BUCKET_NAME \
  --member=allUsers \
  --role=roles/storage.objectViewer
```

Así las URLs del tipo  
`https://storage.googleapis.com/$MEDIA_BUCKET_NAME/...`  
son legibles por navegador, Discord, etc.

Más adelante puedes quitar el acceso público y usar **URLs firmadas** desde tu backend, sin cambiar el contrato de los agentes (siguen devolviendo una URL HTTP).

---

### 3. Secretos en Secret Manager

Solo guardamos como secreto lo sensible: **`OPENROUTER_API_KEY`**.

**Primero, carga la variable desde tu `.env`:**

```bash
cd /Users/manglerojo/Desarollo/DATAR/integracion-1/DATAR

# Cargar OPENROUTER_API_KEY desde .env
export OPENROUTER_API_KEY=$(grep OPENROUTER_API_KEY .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")

# Verificar que se cargó (no debe estar vacío)
if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "ERROR: OPENROUTER_API_KEY no está definida en .env"
  exit 1
fi

echo "✓ OPENROUTER_API_KEY cargada (longitud: ${#OPENROUTER_API_KEY} caracteres)"
```

**Luego, crear o actualizar el secreto:**

```bash
# Crear el secreto (si no existe) o agregar una nueva versión (si ya existe)
echo -n "$OPENROUTER_API_KEY" | gcloud secrets create OPENROUTER_API_KEY \
  --project=$GOOGLE_CLOUD_PROJECT \
  --data-file=- 2>/dev/null || \
echo -n "$OPENROUTER_API_KEY" | gcloud secrets versions add OPENROUTER_API_KEY \
  --project=$GOOGLE_CLOUD_PROJECT \
  --data-file=-
```

Dar permisos a la service account por defecto de Cloud Run:

```bash
PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \
  --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding OPENROUTER_API_KEY \
  --project=$GOOGLE_CLOUD_PROJECT \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

El resto de valores (`MEDIA_BUCKET_NAME`, etc.) se mantienen como **variables de entorno normales**.

---

### 4. Despliegue privado con `adk deploy cloud_run` desde código fuente

Requisitos de estructura (ya cumplidos):
- `datar/agent.py` define el objeto `app`.
- `datar/__init__.py` importa `agent`.
- `datar/requirements.txt` contiene las dependencias (incluye `google-adk`, `google-cloud-storage`, etc.).

Desde `DATAR/`:

```bash
cd /Users/manglerojo/Desarollo/DATAR/integracion-1/DATAR

export APP_NAME="datar_integraciones"
export AGENT_PATH="datar"  # subdirectorio donde está agent.py

adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=datar-integraciones \
  --app_name=$APP_NAME \
  --with_ui \
  $AGENT_PATH
```

**⚠️ IMPORTANTE**: Durante el despliegue, `adk` puede preguntar:

```
Allow unauthenticated invocations to [datar-integraciones] (y/N)?
```

**Responde `N` (No)** para mantener el servicio **privado** y requerir autenticación con tokens de identidad.

Este comando:
- Construye una imagen a partir del código fuente + `requirements.txt`.
- Despliega un servicio de Cloud Run **privado** (requiere autenticación).
- Expone la **UI de ADK** (`--with_ui`) para pruebas internas (también requiere autenticación).

Al final verás una URL como:

```text
https://datar-integraciones-xxxxx-uc.a.run.app
```

Guárdala como `APP_URL`.

---

### 5. Configuración de entorno en el servicio de Cloud Run

1. **Permisos de Storage para la service account de Cloud Run**:

```bash
PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \
  --format="value(projectNumber)")
CLOUDRUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud storage buckets add-iam-policy-binding gs://$MEDIA_BUCKET_NAME \
  --member="serviceAccount:${CLOUDRUN_SA}" \
  --role=roles/storage.objectAdmin
```

2. **Conectar el secreto `OPENROUTER_API_KEY` al servicio**:

```bash
gcloud run services update datar-integraciones \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --update-secrets=OPENROUTER_API_KEY=OPENROUTER_API_KEY:latest
```

3. **Configurar variables de entorno en el servicio**:

```bash
gcloud run services update datar-integraciones \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --set-env-vars="MEDIA_BUCKET_NAME=$MEDIA_BUCKET_NAME,GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION"
```

Opcional:

```bash
--set-env-vars="MEDIA_PUBLIC_BASE_URL=https://storage.googleapis.com/$MEDIA_BUCKET_NAME"
```

si quieres fijar explícitamente la base URL pública usada por los helpers.

---

### 6. Probar el servicio privado con `curl` + token de identidad

El servicio es privado: solo responde a peticiones con un **token de identidad** válido.

```bash
export APP_URL="https://datar-integraciones-xxxxx.a.run.app"  # URL real
export TOKEN=$(gcloud auth print-identity-token)

# Listar apps
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$APP_URL/list-apps"

# Ejecutar el agente (ejemplo simple)
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "$APP_URL/run" \
  -d '{
    "app_name": "datar_integraciones",
    "user_id": "test_user",
    "session_id": "test_session",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Quiero que Gente_Pasto me genere un paisaje sonoro corto"
      }]
    },
    "streaming": false
  }'
```

La respuesta incluirá:
- Texto generado por DATAR (por ejemplo, a través de Gente_Pasto/Sonora/Bosque/Intuitiva).
- Rutas locales y **URLs HTTP de Cloud Storage** (`https://storage.googleapis.com/$MEDIA_BUCKET_NAME/...`) para `.wav` y `.png`.

Esas URLs se pueden usar directamente en:
- `<audio src="...">` o `<img src="...">` en una web‑app.
- Mensajes y adjuntos de un bot de Discord.

---

### 7. Esquema de integración con backend (para Discord / web‑app)

Manteniendo Cloud Run **privado**, el patrón recomendado es:

- Un **backend propio** (otro Cloud Run, GKE, etc.) con su propia service account:
  - Tiene rol `roles/run.invoker` sobre el servicio `datar-integraciones`.
  - Obtiene un **identity token** con audiencia `aud = APP_URL`.
  - Llama a `POST $APP_URL/run` (o `/run_sse`) con:
    - `Authorization: Bearer <TOKEN>`.
- Ese backend expone sus propios endpoints a:
  - Un **bot de Discord** (solo ve el backend, no GCP directamente).
  - Una **web‑app** (frontend) que habla con el backend.

Flujo típico:
1. Discord o la web‑app hacen una petición a tu backend (por ejemplo `/datar/gente-pasto`).
2. El backend construye el `new_message` para la app DATAR y llama a Cloud Run con token de identidad.
3. Recibe del agente:
   - Texto.
   - URLs de Cloud Storage (.wav/.png).
4. El backend devuelve eso al bot o al frontend, que ahora puede:
   - Mostrar imágenes con `<img>`.
   - Reproducir audio con `<audio>`.
   - Compartir directamente las URLs en Discord.

Con estos pasos tienes el flujo completo para:
- Ejecutar **DATAR** en Cloud Run de forma **privada**.
- Guardar y servir los medios desde **Cloud Storage**.
- Integrarte con bots de Discord y web‑apps a través de un backend propio.


