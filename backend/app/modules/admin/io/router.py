from fastapi import APIRouter

router = APIRouter(prefix="/io", tags=["Admin I/O"])


@router.post("/import")
def import_data():
    pass


@router.get("/export")
def export_data():
    pass
