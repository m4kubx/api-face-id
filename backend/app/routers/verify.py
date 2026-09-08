from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from app.core.database import get_db, FaceEmbedding
from app.core.deps import get_current_user, get_current_tenant
from app.core.config import get_settings
from app.services.face_engine import face_engine
from app.services.storage import save_upload

router = APIRouter(prefix="/verify", tags=["verify"])
settings = get_settings()


@router.post("/identify")
async def identify_face(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    tenant: dict = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filepath = await save_upload(file, tenant["tenant_id"])

    try:
        result = await db.execute(
            select(FaceEmbedding).where(FaceEmbedding.tenant_id == tenant["tenant_id"])
        )
        faces = result.scalars().all()

        if not faces:
            return {"identified": False, "user_id": None, "confidence": 0}

        db_embeddings = [
            {"user_id": str(face.user_id), "embedding": json.loads(face.embedding)}
            for face in faces
        ]

        match = face_engine.find_face(filepath, db_embeddings, settings.VERIFICATION_THRESHOLD)

        return {
            "identified": match["match"],
            "user_id": match["user_id"],
            "confidence": match["confidence"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare")
async def compare_faces(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    tenant: dict = Depends(get_current_tenant)
):
    if not file1.content_type.startswith("image/") or not file2.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Files must be images")

    path1 = await save_upload(file1, tenant["tenant_id"])
    path2 = await save_upload(file2, tenant["tenant_id"])

    try:
        result = face_engine.verify_faces(path1, path2, settings.VERIFICATION_THRESHOLD)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze")
async def analyze_face(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    tenant: dict = Depends(get_current_tenant)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filepath = await save_upload(file, tenant["tenant_id"])

    try:
        result = face_engine.analyze_face(filepath)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
