import os
import uuid
import aiofiles
from fastapi import UploadFile
from app.core.config import get_settings

settings = get_settings()


async def save_upload(file: UploadFile, tenant_id: str) -> str:
    tenant_dir = os.path.join(settings.UPLOAD_DIR, tenant_id)
    os.makedirs(tenant_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{file_ext}"
    filepath = os.path.join(tenant_dir, filename)

    async with aiofiles.open(filepath, 'wb') as f:
        content = await file.read()
        await f.write(content)

    return filepath


def delete_file(filepath: str) -> bool:
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception:
        return False


def get_file_url(filepath: str, tenant_id: str) -> str:
    filename = os.path.basename(filepath)
    return f"/uploads/{tenant_id}/{filename}"
