import base64
import io
from http import HTTPStatus
from sqlalchemy import insert, select
from fastapi import UploadFile
from database import engine
from database import db
from common_layer import constants
from common_layer.utils import Hash
from auth_layer.task_app.task_app_schemas.customer_schema import User
from auth_layer.task_app.task_app_models.customer_models import (
    UserRegisterRequest,
    ResponseMessage,
)


def health_check():
    response = ResponseMessage(
        type=constants.HTTP_RESPONSE_SUCCESS,
        data={constants.MESSAGE_KEY: constants.HEALTH_CHECK},
        status_code=HTTPStatus.OK,
    )
    return response


def register_customer(request: UserRegisterRequest):
    request.password = Hash.get_password_hash(request.password)
    statement = insert(User).values(
        fullname=request.fullname,
        email=request.email,
        phone=request.phone,
        password=request.password,
    )
    with engine.connect() as conn:
        conn.execute(statement)
        conn.commit()
    response = ResponseMessage(
        type=constants.HTTP_RESPONSE_SUCCESS,
        data={constants.MESSAGE_KEY: constants.USER_ADDED},
        status_code=HTTPStatus.CREATED,
    )
    return response


def upload_profile_picture(user_id: int, file: UploadFile):
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
    return response


def get_user_details(user_id):
    profile_picture_collection = db[constants.PROFILE_PICTURES_SCHEMA]
    user_data = []
    user_profile_index = profile_picture_collection.find_one(
        {constants.USER_ID_FIELD: user_id}
    )
    if user_profile_index is None:
        response = ResponseMessage(
            type=constants.HTTP_RESPONSE_FAILURE,
            data={constants.MESSAGE_KEY: constants.USER_NOT_FOUND},
            status_code=HTTPStatus.NOT_FOUND,
        )
        return response
    statement = select(User).where(User.id == user_id)
    with engine.connect() as conn:
        for row in conn.execute(statement):
            row_user_id = row[0]
            if user_id == row_user_id:
                user_data = [
                    *row[:4],
                    user_profile_index.get(constants.PROFILE_IMAGE_FIELD),
                ]

    response = ResponseMessage(
        type=constants.HTTP_RESPONSE_SUCCESS,
        data={
            constants.MESSAGE_KEY: constants.USER_DATA_FETCHED,
            constants.USER_DATA: user_data,
        },
        status_code=HTTPStatus.ACCEPTED,
    )
    return response
