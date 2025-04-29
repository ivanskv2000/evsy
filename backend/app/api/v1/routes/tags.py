from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post(
    "/",
    response_model=schemas.TagOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tag",
    description="Create a tag manually. Typically, tags are created automatically when creating or updating an event.",
    responses={
        201: {"description": "Tag created successfully"},
    },
)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.create_tag(db=db, tag=tag)
    return db_tag


@router.get(
    "/",
    response_model=list[schemas.TagOut],
    summary="List all tags",
    description="Return a paginated list of all tags available in the system.",
    responses={
        200: {"description": "List of tags returned"},
    },
)
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.get_tags(db=db, skip=skip, limit=limit)
    return tags


@router.get(
    "/{tag_id}",
    response_model=schemas.TagOut,
    summary="Get tag by ID",
    description="Return a single tag by its unique identifier.",
    responses={
        200: {"description": "Tag found"},
        404: {"description": "Tag not found"},
    },
)
def get_event(tag_id: str, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.put(
    "/{tag_id}",
    response_model=schemas.TagOut,
    summary="Update a tag",
    description="Update the description of an existing tag.",
    responses={
        200: {"description": "Tag updated"},
        404: {"description": "Tag not found"},
    },
)
def update_tag(tag_id: str, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.update_tag(db=db, tag_id=tag_id, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.delete(
    "/{tag_id}",
    response_model=schemas.TagOut,
    summary="Delete a tag",
    description="Delete a tag by its ID. This will remove the tag from all related events.",
    responses={
        200: {"description": "Tag deleted"},
        404: {"description": "Tag not found"},
    },
)
def delete_tag(tag_id: str, db: Session = Depends(get_db)):
    db_tag = crud.delete_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag
