from fastapi import APIRouter
from logging_module import logger
from auth_layer.task_app.task_app_services import customer_service
from auth_layer.task_app.task_app_models import customer_models
from fastapi import UploadFile, File

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


@router.post("/register-customer")
def register_customer(
    request: customer_models.UserRegisterRequest,
):
    logger.debug("Inside the Register CUstomer Router")
    response = customer_service.register_customer(request)
    logger.debug("Returning from the Register Customer Router")
    return response


@router.post("/profile-picture")
def upload_profile_picture(user_id: int, profile: UploadFile = File(...)):
    logger.debug("Inside the Register CUstomer Router")
    response = customer_service.upload_profile_picture(user_id, profile)
    logger.debug("Returning from the Register Customer Router")
    return response


@router.get("/get-user-details")
def get_user_details(user_id: int):
    logger.debug("Inside the Get User Details Router")
    response = customer_service.get_user_details(user_id)
    logger.debug("Returning from Get User Details Router")
    return response
