import yaml
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.token import get_current_user
from app.modules.events import crud as event_crud
from app.modules.events.schemas import EventCreate, EventOut
from app.modules.events.service import generate_json_schema_for_event
from app.modules.fields.crud import get_fields_by_ids
from app.modules.tags.crud import get_or_create_tags

router = APIRouter(
    prefix="/events", tags=["events"], dependencies=[Depends(get_current_user)]
)


@router.post(
    "/",
    response_model=EventOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
    description=(
        "Create a new analytics event. "
        "Tags that do not exist will be created automatically. "
        "Fields must be pre-created before assigning."
    ),
    responses={
        201: {"description": "Event created successfully"},
        400: {"description": "One or more fields do not exist"},
    },
)
def create_event_route(event: EventCreate, db: Session = Depends(get_db)):
    db_fields = get_fields_by_ids(db, event.fields)

    if len(db_fields) != len(event.fields):
        raise HTTPException(status_code=400, detail="One or more fields do not exist.")

    get_or_create_tags(db, event.tags)
    db_event = event_crud.create_event(db=db, event=event)
    return db_event


@router.get(
    "/{event_id}",
    response_model=EventOut,
    response_model_exclude_none=True,
    summary="Get event by ID",
    description="Return a single event by its ID. Includes tags and fields.",
    responses={
        200: {"description": "Event found"},
        404: {"description": "Event not found"},
    },
)
def get_event_route(event_id: int, db: Session = Depends(get_db)):
    db_event = event_crud.get_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get(
    "/",
    response_model=list[EventOut],
    response_model_by_alias=False,
    summary="List all events",
    description="Return a paginated list of all events with their tags and fields.",
    responses={200: {"description": "List of events returned"}},
)
def list_events_route(db: Session = Depends(get_db)):
    return event_crud.get_events(db=db)


@router.put(
    "/{event_id}",
    response_model=EventOut,
    summary="Update an existing event",
    description=(
        "Update an existing analytics event. "
        "New tags will be created if they do not exist. "
        "All field IDs must already exist in the system."
    ),
    responses={
        200: {"description": "Event updated"},
        400: {"description": "One or more fields do not exist"},
        404: {"description": "Event not found"},
    },
)
def update_event_route(
    event_id: int, event: EventCreate, db: Session = Depends(get_db)
):
    db_fields = get_fields_by_ids(db, event.fields)

    if len(db_fields) != len(event.fields):
        raise HTTPException(status_code=400, detail="One or more fields do not exist.")

    get_or_create_tags(db, event.tags)
    db_event = event_crud.update_event(db=db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.delete(
    "/{event_id}",
    response_model=EventOut,
    summary="Delete an event",
    description="Delete an analytics event by ID.",
    responses={
        200: {"description": "Event deleted"},
        404: {"description": "Event not found"},
    },
)
def delete_event_route(event_id: int, db: Session = Depends(get_db)):
    db_event = event_crud.delete_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get(
    "/{event_id}/schema.json",
    response_class=JSONResponse,
    summary="Export event as JSON Schema",
    description="Generate a JSON Schema for the event's data structure. Useful for validation and documentation.",
    responses={
        200: {"description": "JSON Schema generated successfully"},
        404: {"description": "Event not found"}
    }
)
def get_event_json_schema(
    event_id: int,
    include_descriptions: bool = Query(True, description="Include field descriptions in schema"),
    include_examples: bool = Query(True, description="Include field examples in schema"),
    additional_properties: bool = Query(True, description="Allow additional properties in schema"),
    db: Session = Depends(get_db),
):
    db_event = event_crud.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    event = EventOut.model_validate(db_event)
    schema = generate_json_schema_for_event(
        event,
        include_descriptions=include_descriptions,
        include_examples=include_examples,
        additional_properties=additional_properties,
    )
    return schema


@router.get(
    "/{event_id}/schema.yaml",
    summary="Export event as YAML Schema",
    description="Generate a YAML Schema for the event's data structure. Same as JSON but in YAML format.",
    responses={
        200: {"description": "YAML Schema generated successfully"},
        404: {"description": "Event not found"}
    }
)
def get_event_yaml_schema(
    event_id: int,
    include_descriptions: bool = Query(True, description="Include field descriptions in schema"),
    include_examples: bool = Query(True, description="Include field examples in schema"),
    additional_properties: bool = Query(True, description="Allow additional properties in schema"),
    db: Session = Depends(get_db),
):
    db_event = event_crud.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    event = EventOut.model_validate(db_event)
    schema = generate_json_schema_for_event(
        event,
        include_descriptions=include_descriptions,
        include_examples=include_examples,
        additional_properties=additional_properties,
    )
    yaml_data = yaml.dump(schema, sort_keys=False)
    return Response(content=yaml_data, media_type="application/x-yaml")
