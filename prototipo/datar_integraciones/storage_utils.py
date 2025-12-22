"""
Utilidades para guardar archivos generados por los agentes en Google Cloud Storage.

Diseño:
- El bucket se toma de la variable de entorno `MEDIA_BUCKET_NAME`.
- Opcionalmente se puede definir `MEDIA_PUBLIC_BASE_URL` para personalizar la URL base
  pública (por ejemplo, detrás de un CDN). Si no se define, se usa:
  https://storage.googleapis.com/<bucket>/<ruta_objeto>

Estas funciones están pensadas para usarse desde los agentes `Gente_*` que generan
archivos `.wav` y `.png` (Pasto, Sonora, Intuitiva, Bosque). En caso de cualquier
error al subir a Storage, los agentes deben capturar la excepción y devolver al
menos la ruta local del archivo para no romper la experiencia.
"""

import os
from typing import Optional

from google.cloud import storage

MEDIA_BUCKET_ENV = "MEDIA_BUCKET_NAME"
MEDIA_BASE_URL_ENV = "MEDIA_PUBLIC_BASE_URL"


def _get_bucket_name() -> str:
    bucket_name = os.getenv(MEDIA_BUCKET_ENV)
    if not bucket_name:
        raise RuntimeError(
            f"La variable de entorno {MEDIA_BUCKET_ENV} no está configurada. "
            "Configura el bucket de Cloud Storage donde se guardarán los medios."
        )
    return bucket_name


def _get_public_base_url(bucket_name: Optional[str] = None) -> str:
    """
    Devuelve la URL base pública para los objetos del bucket.

    Si `MEDIA_PUBLIC_BASE_URL` está definida, se usa tal cual (recortando `/` final).
    En caso contrario, se usa el dominio estándar de Cloud Storage.
    """
    base = os.getenv(MEDIA_BASE_URL_ENV)
    if base:
        return base.rstrip("/")

    bucket_name = bucket_name or _get_bucket_name()
    return f"https://storage.googleapis.com/{bucket_name}"


def upload_file_to_gcs(
    local_path: str, destination_path: str, content_type: Optional[str] = None
) -> str:
    """
    Sube un archivo existente en disco a Cloud Storage y devuelve la URL pública.

    Args:
        local_path: Ruta local del archivo a subir.
        destination_path: Ruta destino dentro del bucket (por ejemplo,
            "gente_sonora/audio/composicion_2025...wav").
        content_type: MIME type opcional (por ejemplo "audio/wav" o "image/png").

    Returns:
        URL HTTP que apunta al objeto en Cloud Storage.
    """
    bucket_name = _get_bucket_name()

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_path)

    if content_type:
        blob.content_type = content_type

    blob.upload_from_filename(local_path)

    # Las políticas de acceso (público/privado) se controlan a nivel de bucket/IAM.
    base_url = _get_public_base_url(bucket_name)
    return f"{base_url}/{destination_path.lstrip('/')}"


def upload_bytes_to_gcs(
    data: bytes,
    destination_path: str,
    content_type: Optional[str] = None,
) -> str:
    """
    Sube datos en memoria (bytes) a Cloud Storage y devuelve la URL pública.

    Útil para casos donde no se necesita escribir a disco primero.
    """
    bucket_name = _get_bucket_name()

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_path)

    if content_type:
        blob.content_type = content_type

    blob.upload_from_string(data)

    base_url = _get_public_base_url(bucket_name)
    return f"{base_url}/{destination_path.lstrip('/')}"


