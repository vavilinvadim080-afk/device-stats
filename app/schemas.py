from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceDataIn(BaseModel):
    x: float
    y: float
    z: float


class DeviceDataOut(BaseModel):
    id: int
    device_id: str
    x: float
    y: float
    z: float
    timestamp: datetime

    model_config = {"from_attributes": True}


class AxisStats(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float


class DeviceAnalytics(BaseModel):
    device_id: str
    period_from: Optional[datetime] = None
    period_to: Optional[datetime] = None
    x: AxisStats
    y: AxisStats
    z: AxisStats
