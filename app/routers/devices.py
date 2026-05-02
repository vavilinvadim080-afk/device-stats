from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DeviceReading
from app.schemas import DeviceDataIn, DeviceDataOut

router = APIRouter(prefix="/devices", tags=["Устройства"])


@router.post(
    "/{device_id}/data",
    response_model=DeviceDataOut,
    status_code=status.HTTP_201_CREATED,
    summary="Принять данные с устройства",
)
def post_device_data(
    device_id: str,
    data: DeviceDataIn,
    db: Session = Depends(get_db),
):
    reading = DeviceReading(
        device_id=device_id,
        x=data.x,
        y=data.y,
        z=data.z,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading
