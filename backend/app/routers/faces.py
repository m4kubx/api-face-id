from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
from typing import List, Optional
import json

from app.core.database import get_db, FaceEmbedding
from app.core.deps import get_current_user, get_current_tenant
from app.services.face_engine import face_engine
from app.services.storage import save_upload, delete_file

router = APIRouter(prefix="/faces", tags=["faces"])


class FaceResponse(BaseModel):
    id: str
    user_id: str
    image_url: str
    created_at: str


@router.post("/register")
async def register_face(
    user_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    tenant: dict = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filepath = await save_upload(file, tenant["tenant_id"])

    try:
        embedding = face_engine.extract_embedding(filepath)
    except Exception as e:
        delete_file(filepath)
        raise HTTPException(status_code=400, detail=str(e))

    face = FaceEmbedding(
        tenant_id=tenant["tenant_id"],
        user_id=user_id,
        image_path=filepath,
        embedding=json.dumps(embedding),
        model_name="ArcFace"
    )
    db.add(face)
    await db.commit()
    await db.refresh(face)

    return {
        "id": str(face.id),
        "user_id": user_id,
        "message": "Face registered successfully"
    }


@router.get("/list", response_model=List[FaceResponse])
async def list_faces(
    current_user: dict = Depends(get_current_user),
    tenant: dict = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FaceEmbedding).where(FaceEmbedding.tenant_id == tenant["tenant_id"])
    )
    faces = result.scalars().all()

    return [
        FaceResponse(
            id=str(face.id),
            user_id=str(face.user_id),
            image_url=f"/uploads/{tenant['tenant_id']}/{face.image_path.split('/')[-1]}",
            created_at=face.created_at.isoformat()
        )
        for face in faces
    ]


@router.delete("/{face_id}")
async def delete_face(
    face_id: str,
    current_user: dict = Depends(get_current_user),
    tenant: dict = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FaceEmbedding).where(
            FaceEmbedding.id == face_id,
            FaceEmbedding.tenant_id == tenant["tenant_id"]
        )
    )
    face = result.scalar_one_or_none()

    if not face:
        raise HTTPException(status_code=404, detail="Face not found")

    delete_file(face.image_path)
    await db.delete(face)
    await db.commit()

    return {"message": "Face deleted successfully"}
