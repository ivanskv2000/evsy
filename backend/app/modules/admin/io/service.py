from enum import Enum

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.events.models import Event
from app.modules.fields.models import Field
from app.modules.tags.crud import get_or_create_tags
from app.modules.tags.models import Tag
from app.shared.models import EventField, EventTag

from .schemas import ExportBundle, ExportEvent, ExportField, ExportTag, ImportBundle


class ImportSource(str, Enum):
    json = "json"
    csv = "csv"


class ExportTarget(str, Enum):
    json = "json"
    csv = "csv"
    markdown = "markdown"
    zip = "zip"


def export_bundle(db: Session) -> ExportBundle:
    tags = db.query(Tag).all()
    fields = db.query(Field).all()
    events = db.query(Event).all()

    return ExportBundle(
        tags=[ExportTag(id=tag.id, description=tag.description) for tag in tags],
        fields=[
            ExportField(
                name=field.name,
                description=field.description,
                field_type=field.field_type,
                example=field.example,
            )
            for field in fields
        ],
        events=[
            ExportEvent(
                name=event.name,
                description=event.description,
                links=event.links,
                tags=[tag.id for tag in event.tags],
                fields=[field.name for field in event.fields],
            )
            for event in events
        ],
    )


def export_to(target: ExportTarget, db: Session) -> ExportBundle | str:
    if target == ExportTarget.json:
        return export_bundle(db)

    elif target == ExportTarget.csv:
        raise HTTPException(status_code=501, detail="CSV export is not implemented yet")

    elif target == ExportTarget.markdown:
        raise HTTPException(
            status_code=501, detail="Markdown export is not implemented yet"
        )

    elif target == ExportTarget.zip:
        raise HTTPException(status_code=501, detail="ZIP export is not implemented yet")

    else:
        raise HTTPException(status_code=400, detail=f"Unknown export source: {target}")


def assert_db_empty(db: Session):
    if db.query(Event).first() or db.query(Field).first() or db.query(Tag).first():
        raise HTTPException(
            status_code=405, detail="Import is only allowed on empty database"
        )


def import_bundle(bundle: ImportBundle, db: Session):
    assert_db_empty(db)

    # Create fields and build name → model map
    field_map = {}
    for field_data in bundle.fields:
        field = Field(
            name=field_data.name,
            description=field_data.description,
            field_type=field_data.field_type,
            example=field_data.example,
        )
        db.add(field)
        db.flush()  # Ensures ID is available before linking
        field_map[field.name] = field

    all_tag_ids = {tag.id for tag in bundle.tags}
    for event in bundle.events:
        all_tag_ids.update(event.tags)

    _ = get_or_create_tags(db, list(all_tag_ids))
    db.flush()

    for event_data in bundle.events:
        event = Event(
            name=event_data.name,
            description=event_data.description,
            links=event_data.links or [],
        )
        db.add(event)
        db.flush()

        for tag_id in event_data.tags:
            db.add(EventTag(event_id=event.id, tag_id=tag_id))

        for field_name in event_data.fields:
            if field_name not in field_map:
                raise HTTPException(
                    status_code=400, detail=f"Unknown field name: {field_name}"
                )
            db.add(EventField(event_id=event.id, field_id=field_map[field_name].id))

    db.commit()


def import_from(source: ImportSource, data: any, db: Session):
    if source == ImportSource.json:
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="Expected JSON object")
        bundle = ImportBundle(**data)
        import_bundle(bundle, db)

    elif source == ImportSource.csv:
        raise HTTPException(status_code=501, detail="CSV import is not implemented yet")

    else:
        raise HTTPException(status_code=400, detail=f"Unknown import source: {source}")
