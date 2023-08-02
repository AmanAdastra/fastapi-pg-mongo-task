import os

# Configuration
LOG_LEVEL = "DEBUG"
HTTP_RESPONSE_SUCCESS = "success"
HTTP_RESPONSE_FAILURE = "error"
MONGODB_URL = os.getenv("MONGODB_URL")


# Postgres Connection
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")


# Messages Keys
MESSAGE_KEY = "message"
USER_DATA = "user_data"

# Messages
USER_ADDED = "User Inserted"
PROFILE_PICTURE_ADDED = "Profile Picture added successfully"
HEALTH_CHECK = "Health Check Completed"
USER_NOT_FOUND = "User not found, Please check the entered user id"
USER_DATA_FETCHED = "User data fetched successfully"


# Database Model Names
PROFILE_PICTURES_SCHEMA = "profile_pictures"


# Database Fields
USER_ID_FIELD = "user_id"
PROFILE_IMAGE_FIELD = "profile_image"
UPDATE_INDEX_FIELD = "$set"
