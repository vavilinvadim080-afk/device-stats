import statistics
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DeviceReading
from app.schemas import AxisStats, DeviceAnalytics

router = APIRouter(prefix="/devices", tags=["Аналитика"])


def compute_stats(values: list) -> AxisStats:
    return AxisStats(
        min=min(values),
        max=max(values),
        count=len(values),
        sum=round(sum(values), 6),
        median=statistics.median(values),
    )


@router.get(
    "/{device_id}/analytics",
    response_model=DeviceAnalytics,
    summary="Аналитика по устройству",
)
def get_device_analytics(
    device_id: str,
    from_ts: Optional[datetime] = Query(None, description="начало периода (ISO)"),
    to_ts: Optional[datetime] = Query(None, description="конец периода (ISO)"),
    db: Session = Depends(get_db),
):
    query = db.query(DeviceReading).filter(DeviceReading.device_id == device_id)

    if from_ts:
        query = query.filter(DeviceReading.timestamp >= from_ts)
    if to_ts:
        query = query.filter(DeviceReading.timestamp <= to_ts)

    readings = query.all()

    if not readings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"данные для устройства '{device_id}' не найдены",
        )

    x_values = [r.x for r in readings]
    y_values = [r.y for r in readings]
    z_values = [r.z for r in readings]

    return DeviceAnalytics(
        device_id=device_id,
        period_from=from_ts,
        period_to=to_ts,
        x=compute_stats(x_values),
        y=compute_stats(y_values),
        z=compute_stats(z_values),
    )
