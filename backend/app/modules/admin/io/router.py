from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from .schemas import ExportBundle
from .service import ExportTarget, ImportSource, export_to, import_from

router = APIRouter(prefix="/io", tags=["io"])


@router.get(
    "/export",
    response_model=ExportBundle,
    status_code=status.HTTP_200_OK,
    summary="Export all data",
    description=(
        "Export all tags, fields, and events as a single bundle. "
        "Supports JSON (default), with future support for CSV, Markdown and zip."
    ),
    responses={
        200: {"description": "Export completed successfully"},
        400: {"description": "Invalid export format"},
        501: {"description": "Export format not implemented"},
    },
)
def export_data(
    db: Session = Depends(get_db),
    target: ExportTarget = Query(
        ExportTarget.json, description="Export format (default: json)"
    ),
):
    return export_to(target, db)


@router.post(
    "/import",
    status_code=status.HTTP_201_CREATED,
    summary="Import data from JSON (or future formats)",
    description=(
        "Import tags, fields, and events. "
        "Only works on an empty database. Supports `source=json` (default). "
        "`csv` and `sheets` are reserved for future use."
    ),
    responses={
        201: {"description": "Import completed successfully"},
        400: {"description": "Invalid input or unsupported source"},
        405: {"description": "Import not allowed on non-empty database"},
        501: {"description": "Import method not implemented"},
    },
)
async def import_data(
    request: Request,
    db: Session = Depends(get_db),
    source: ImportSource = Query(
        ImportSource.json, description="Import source format (default: json)"
    ),
):
    data = await request.json()
    import_from(source, data, db)
    return {"status": "ok"}
