from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.material import Material, MaterialStatus
from app.models.card import Card
from app.schemas.material import MaterialResponse
from app.services.parser import extract_pdf_text

router = APIRouter(prefix="/api/materials", tags=["materials"])

MAX_SIZE = 20 * 1024 * 1024


@router.post("/", response_model=MaterialResponse)
async def upload_material(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    filename = file.filename or "unknown"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf":
        file_type = "pdf"
        raw = await file.read()
        if len(raw) > MAX_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="文件超过20MB")
        content = extract_pdf_text(raw)
    elif ext == "md":
        file_type = "md"
        raw = await file.read()
        if len(raw) > MAX_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="文件超过20MB")
        content = raw.decode("utf-8")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持PDF和Markdown格式")

    title = filename.rsplit(".", 1)[0]
    material = Material(user_id=user.id, title=title, content=content, file_type=file_type)
    db.add(material)
    await db.commit()
    await db.refresh(material)
    return MaterialResponse(id=material.id, title=material.title, file_type=material.file_type,
                            status=material.status.value, card_count=0, created_at=material.created_at)


@router.get("/", response_model=list[MaterialResponse])
async def list_materials(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = (
        select(
            Material,
            func.count(Card.id).label("card_count"),
        )
        .outerjoin(Card, Card.material_id == Material.id)
        .where(Material.user_id == user.id)
        .group_by(Material.id)
        .order_by(Material.created_at.desc())
    )
    result = await db.execute(query)
    rows = result.all()
    return [
        MaterialResponse(
            id=m.id, title=m.title, file_type=m.file_type,
            status=m.status.value, card_count=card_count, created_at=m.created_at,
        )
        for m, card_count in rows
    ]


@router.delete("/{material_id}", status_code=204)
async def delete_material(
    material_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Material).where(Material.id == material_id, Material.user_id == user.id)
    )
    material = result.scalar_one_or_none()
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资料不存在")
    await db.delete(material)
    await db.commit()
