from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.tags import crud as tag_crud
from app.modules.tags.schemas import TagCreate, TagOut
from app.modules.auth.token import get_current_user

router = APIRouter(prefix="/tags", tags=["tags"], dependencies=[Depends(get_current_user)])


@router.post(
    "/",
    response_model=TagOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tag",
    description="Create a tag manually. Typically, tags are created automatically when creating or updating an event.",
)
def create_tag_route(tag: TagCreate, db: Session = Depends(get_db)):
    return tag_crud.create_tag(db=db, tag=tag)


@router.get(
    "/",
    response_model=list[TagOut],
    summary="List all tags",
    description="Return a paginated list of all tags available in the system.",
)
def list_tags_route(db: Session = Depends(get_db)):
    return tag_crud.get_tags(db=db)


@router.get(
    "/{tag_id}",
    response_model=TagOut,
    summary="Get tag by ID",
    description="Return a single tag by its unique identifier.",
    responses={404: {"description": "Tag not found"}},
)
def get_tag_route(tag_id: str, db: Session = Depends(get_db)):
    db_tag = tag_crud.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.put(
    "/{tag_id}",
    response_model=TagOut,
    summary="Update a tag",
    description="Update the description of an existing tag.",
    responses={404: {"description": "Tag not found"}},
)
def update_tag_route(tag_id: str, tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = tag_crud.update_tag(db=db, tag_id=tag_id, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.delete(
    "/{tag_id}",
    response_model=TagOut,
    summary="Delete a tag",
    description="Delete a tag by its ID. This will remove the tag from all related events.",
    responses={404: {"description": "Tag not found"}},
)
def delete_tag_route(tag_id: str, db: Session = Depends(get_db)):
    db_tag = tag_crud.delete_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag
