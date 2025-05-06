import codecs
from csv import DictReader
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from redis.asyncio.client import Redis

from examples.file_upload.schemas import (
    ProcessVehiclesInfoResponse,
    ProcessVehiclesInfoSchema,
    VehicleCheckUploadSchema,
    VehiclesUploadResponse,
)

router = APIRouter(prefix='/upload', tags=['File Upload'])


async def enqueue_vehicle(process_id, vehicle_indo):
    # Add vehicle to a queue to be processed
    pass


async def create_cache():
    client = Redis(single_connection_client=True)
    yield client
    await client.aclose()


T_Cache = Annotated[Redis, Depends(create_cache)]


@router.post('/upload_vehicles', response_model=VehiclesUploadResponse)
async def upload_vehicles(file: UploadFile, cache: T_Cache):
    csv_file = file.file
    reader = DictReader(codecs.iterdecode(csv_file, 'utf-8'))
    vehicles = list(reader)
    VehicleCheckUploadSchema.model_validate({'vehicles': vehicles})

    key = str(uuid4())
    expiration = timedelta(minutes=5)
    csv_file.seek(0)
    await cache.set(key, csv_file.read(), ex=expiration)

    valid_until = datetime.now(timezone.utc) + expiration
    return VehiclesUploadResponse(id=key, valid_until=valid_until)


@router.post(
    '/process_vehicles_infos', response_model=ProcessVehiclesInfoResponse
)
async def process_vehicles_info(
    solicitation: ProcessVehiclesInfoSchema, cache: T_Cache
):
    csv_bytes = await cache.get(solicitation.file_identification)
    if not csv_bytes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='File not found'
        )

    reader = DictReader(csv_bytes.decode('utf-8'))
    process_id = str(uuid4())

    for vehicle in reader:
        # Call the task to process vehicle
        await enqueue_vehicle(process_id, vehicle)

    return ProcessVehiclesInfoResponse(
        id=process_id, requester_email=solicitation.requester_email
    )
