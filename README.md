
# FastAPI User Registration with PostgreSQL and MongoDB

This repository contains a FastAPI application that allows users to register, upload profile pictures, and retrieve their details. The user registration data is stored in PostgreSQL, while the profile pictures are stored in MongoDB.

## Endpoints

1. **Health Check** (GET)
   - Endpoint: `/api/v1/test`
   - Description: This endpoint can be used to check the health of the application. It will return a simple response indicating that the application is running.

2. **Register Customer** (POST)
   - Endpoint: `/api/v1/register-customer`
   - Description: This endpoint allows users to register by providing their Full Name, Email, Password, Phone.
   - Request Body:
      ```json
      {
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "mypassword",
        "phone": "1234567890",
      }
      ```
   - Response: Upon successful registration, the endpoint will return a unique `user_id` for the user.

3. **Upload Profile Picture** (POST)
   - Endpoint: `/profile-picture?user_id={user_id}`
   - Description: This endpoint is used to upload the profile picture for a registered user identified by their `user_id`.
   - Request Body: The profile picture should be sent as `multipart/form-data` with the key "file".
   - Response: If the profile picture upload is successful, it will return a message confirming the update.

4. **Get User Details** (GET)
   - Endpoint: `/get-user-details?user_id={user_id}`
   - Description: This endpoint is used to retrieve the details of a registered user by providing their `user_id`.
   - Response: The endpoint will return the user's details in the following format:
      ```json
      {
        "user_id": "unique_user_id",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "b64_profile_picture":"Vi..."
      }
      ```
## Configuration (.env.example)

To run the FastAPI application successfully, you need to create a `.env` file based on the provided `.env.example` file and fill in the required values for each variable. The variables you need to set in the `.env` file are:

- `POSTGRES_USERNAME`: The connection URL for the PostgreSQL database.
- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_HOST`: The host for the PostgreSQL database.
- `POSTGRES_PORT`: The post for the PostgreSQL database.
- `POSTGRES_DATABASE_NAME`: The name for the PostgreSQL database.

- `MONGODB_URL`: The Connection URL for the MongoDB database.


Ensure that all the above variables are correctly filled in the `.env` file before running the FastAPI application.

## Running the Application

To run the FastAPI application, follow these steps:

1. Install the required dependencies by running:

`pip install -r requirements.txt`

2. Run the FastAPI application using the following command:
`python application.py`


Now, you should have the FastAPI application up and running, and you can test the endpoints using OpenAPI/ Swagger

Please note that this Readme is a general template and may need to be adapted based on your specific project structure and configuration details. Make sure to update it accordingly.

