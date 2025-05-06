from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class VehicleSchema(BaseModel):
    model: str
    plate: str
    year: int


class VehicleCheckUploadSchema(BaseModel):
    vehicles: List[VehicleSchema]


class VehiclesUploadResponse(BaseModel):
    id: str
    valid_until: datetime


class ProcessVehiclesInfoSchema(BaseModel):
    requester_email: EmailStr
    file_identification: str
    description: str


class ProcessVehiclesInfoResponse(BaseModel):
    id: str
    requester_email: EmailStr
