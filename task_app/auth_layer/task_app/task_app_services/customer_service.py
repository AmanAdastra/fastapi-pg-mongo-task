import base64
import io
from http import HTTPStatus
from sqlalchemy import insert, select
from fastapi import UploadFile, HTTPException
from database import engine
from database import db
from common_layer import constants
from common_layer.utils import Hash
from logging_module import logger
from auth_layer.task_app.task_app_schemas.customer_schema import User
from auth_layer.task_app.task_app_models.customer_models import (
    UserRegisterRequest,
    ResponseMessage,
)


def health_check():
    logger.debug("Inside Health Check Function")
    response = ResponseMessage(
        type=constants.HTTP_RESPONSE_SUCCESS,
        data={constants.MESSAGE_KEY: constants.HEALTH_CHECK},
        status_code=HTTPStatus.OK,
    )
    logger.debug("Returning From the Health Check Function")
    return response


def register_customer(request: UserRegisterRequest):
    logger.debug("Inside the Register Customer Function")
    try:
        email_check_statement = select(User).where(User.email == request.email)

        request.password = Hash.get_password_hash(request.password)
        statement = insert(User).values(
            fullname=request.fullname,
            email=request.email,
            phone=request.phone,
            password=request.password,
        )
        with engine.connect() as conn:
            record_exist = conn.execute(email_check_statement)
            if list(record_exist):
                response = ResponseMessage(
                    type=constants.HTTP_RESPONSE_FAILURE,
                    data={constants.MESSAGE_KEY: constants.EMAIL_ALREADY_EXIST},
                    status_code=HTTPStatus.NOT_ACCEPTABLE,
                )
                logger.debug(f"Email already used!")
                return response
            inserted_record = conn.execute(statement)
            conn.commit()
        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_SUCCESS,
            data={
                constants.MESSAGE_KEY: constants.USER_ADDED,
                constants.USER_ID_FIELD: (inserted_record.inserted_primary_key)[0],
            },
            status_code=HTTPStatus.CREATED,
        )
        logger.debug("Returning from the Register Customer Function")
        return response
    except Exception as e:
        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_FAILURE,
            data={constants.MESSAGE_KEY: f"{constants.PROCESS_FAILED} with error {e}"},
            status_code=HTTPStatus.NOT_ACCEPTABLE,
        )
        logger.debug(f"Error in the Register Customer Function: {e}")
        return response


def upload_profile_picture(user_id: int, file: UploadFile):
    logger.debug("Inside Upload Profile Picture Function")
    try:
        contents = file.file.read()
        fileobj = io.BytesIO()
        fileobj.write(contents)
        fileobj.seek(0)
        base_64_image = base64.b64encode(fileobj.getvalue())
        # View at : https://base64.guru/converter/decode/image
        profile_picture_collection = db[constants.PROFILE_PICTURES_SCHEMA]

        user_profile_index = profile_picture_collection.find_one(
            {constants.USER_ID_FIELD: user_id}
        )
        if user_profile_index:
            profile_picture_collection.update_one(
                {constants.USER_ID_FIELD: user_id},
                {
                    constants.UPDATE_INDEX_FIELD: {
                        constants.PROFILE_IMAGE_FIELD: base_64_image
                    }
                },
            )
        else:
            profile_picture_collection.insert_one(
                {
                    constants.USER_ID_FIELD: user_id,
                    constants.PROFILE_IMAGE_FIELD: base_64_image,
                }
            )
        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_SUCCESS,
            data={constants.MESSAGE_KEY: constants.PROFILE_PICTURE_ADDED},
            status_code=HTTPStatus.ACCEPTED,
        )
        logger.debug("Returning From the Upload Profile Picture Function")
        return response
    except Exception as e:
        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_FAILURE,
            data={constants.MESSAGE_KEY: f"{constants.PROCESS_FAILED} with error {e}"},
            status_code=HTTPStatus.NOT_ACCEPTABLE,
        )
        logger.debug(f"Error in the Upload Profile Picture Function: {e}")
        return response


def get_user_details(user_id: int):
    try:
        logger.debug("Inside Get User Details Function")
        profile_picture_collection = db[constants.PROFILE_PICTURES_SCHEMA]
        user_data = []
        user_profile_index = profile_picture_collection.find_one(
            {constants.USER_ID_FIELD: user_id}
        )
        if user_profile_index is None:
            response = ResponseMessage(
                type=constants.HTTP_RESPONSE_FAILURE,
                data={constants.MESSAGE_KEY: constants.PROFILE_PICTURE_NOT_UPLOADED},
                status_code=HTTPStatus.NOT_FOUND,
            )
            return response
        statement = select(User).where(User.id == user_id)
        with engine.connect() as conn:
            for row in conn.execute(statement):
                row_user_id = row[0]
                if user_id == row_user_id:
                    user_data = {
                        constants.USER_ID_FIELD: row[0],
                        constants.FULLNAME_FIELD: row[1],
                        constants.EMAIL_FIELD: row[2],
                        constants.PASSWORD_FIELD: row[3],
                        constants.PROFILE_IMAGE_FIELD: user_profile_index.get(
                            constants.PROFILE_IMAGE_FIELD
                        ),
                    }

        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_SUCCESS,
            data={
                constants.MESSAGE_KEY: constants.USER_DATA_FETCHED,
                constants.USER_DATA: user_data,
            },
            status_code=HTTPStatus.ACCEPTED,
        )
        logger.debug("Returning From the Get User Details Function")
        return response
    except Exception as e:
        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_FAILURE,
            data={constants.MESSAGE_KEY: f"{constants.PROCESS_FAILED} with error {e}"},
            status_code=HTTPStatus.NOT_ACCEPTABLE,
        )
        logger.debug(f"Error in the Get User Details Function: {e}")
        return response
