from fastapi import APIRouter
from logging_module import logger
from auth_layer.task_app.task_app_services import customer_service

router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
    tags=["CUSTOMER MANAGEMENT"],
)


@router.get("/test")
def health_check():
    logger.debug("Inside Health Check Router")
    response = customer_service.health_check()
    logger.debug("Returning from the Health Check Router")
    return response