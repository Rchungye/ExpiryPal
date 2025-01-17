# ExpiryPal

DESCRIPTION OF THE PROJECT

## Technologies Used

- MySQL
- Python with Flask
- SQLAlchemy
- JavaScript with Vite + React.js
- TailwindCSS
- Material UI
- YOLO
- Cloudinary
- Firebase

## Backend Configuration (Flask)

Follow these steps and commands when cloning the project:

Inside the `/be` folder:
- Run the following command to navigate to the backend directory:
    ```sh
    cd .\be\
    ```
- Create a virtual environment in the root directory with the command:
    ```sh
    python -m venv name_of_venv
    ```
- Navigate to the virtual environment directory with the command:
    ```sh
    .\name_of_venv\Scripts\activate
    ```
- Install the Flask BE project dependencies with the command:
    ```sh
    pip install -r .\requirements.txt
    ```
- Create a `.env` file in the root BE directory with the following structure:
    ```sh
    DB_CONN = "mysql+pymysql://user:password@host:port/expirypal"
    # Replace user, password, host, and port according to your MySQL configuration.
    ML_URL = "your_MachineLearning_url_here"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    HASS_API_KEY = 'HOME_ASSISTANT_API_KEY'
    HASS_BASE_URL = 'https://hass.mdu-smartroom.se'
    CLOUDINARY_CLOUD_NAME = "CLOUDINARY_CLOUD_NAME"
    CLOUDINARY_API_KEY = "CLOUDINARY_API_KEY"
    CLOUDINARY_API_SECRET = "CLOUDINARY_API_SECRET"
    ```
- Create a `project-name-firebase-adminsdk.json` file in the be/secret directory with the following structure:
    ```sh
   {
  "type": "service_account",
  "project_id": "firebase_project_id",
  "private_key_id": "private_key",
  "private_key": "-----BEGIN PRIVATE KEY-----",
  "client_email": "firebase-adminsdk-*********.com",
  "client_id": "*******",
  "auth_uri": "*******",
  "token_uri": "*******",
  "auth_provider_x509_cert_url": "*******",
  "client_x509_cert_url": "*******",
  "universe_domain": "*******"
}

- [Steps to download project-name-firebase-adminsdk.json](#steps-to-download-project-name-firebase-adminsdk-json)


> If necessary, delete the migrations folder (only if the migration doesn't run properly).
- Run the following command to prepare the migration:
    ```sh
    flask db init
    ```
- Run the following command to perform the migration:
    ```sh
    flask db migrate
    ```
- Run the following command to update the migrated data:
    ```sh
    flask db upgrade
    ```
- Run the following command to start the Flask BE project:
    ```sh
    py app.py
    ```
- The backend should now be running.

## Frontend Configuration (Vite + React.js)

Follow these steps and commands when cloning the project:

Inside the `/fe` folder:
- Run the following command to navigate to the frontend directory:
    ```sh
    cd .\fe\
    ```
- Create a `.env` file in the root FE directory with the following structure:
    ```sh
    VITE_BE_URL=your_backend_url_here
    # Replace the URL with the one generated when running the backend.
    ```
- Run the following command to install all Node.js dependencies:
    ```sh
    npm i
    ```
- Run the following command to start the Vite + React.js project:
    ```sh
    npm run dev
    ```
- The frontend should now be running.

## Machine Learning Configuration (Flask)

Follow these steps and commands when cloning the project:

Inside the `/ML` folder:
- Run the following command to navigate to the backend directory:
    ```sh
    cd .\ML\
    ```
- Create a virtual environment in the root directory with the command:
    ```sh
    python -m venv name_of_venv
    ```
- Navigate to the virtual environment directory with the command:
    ```sh
    .\name_of_venv\Scripts\activate
    ```
- Enter the following link and download the 2 files (**yolov8x-seg.pt** and **clip-vit-base-patch32**):
    ```sh
    https://drive.google.com/drive/folders/1JH9ruRaYMBEmpRF97fKQDsGQayKEujhI
    ```
- Put both files in ML folder.
- Install the Flask ML project dependencies with the command:
    ```sh
    pip install -r .\requirements.txt
    ```
- Create a `.env` file in the root ML directory with the following structure:
    ```sh
    DB_CONN = "mysql+pymysql://user:password@host:port/expirypal"
    # Replace user, password, host, and port according to your MySQL configuration.
    BE_URL = "your_backend_url_here"
    CLOUDINARY_CLOUD_NAME = "CLOUDINARY_CLOUD_NAME"
    CLOUDINARY_API_KEY = "CLOUDINARY_API_KEY"
    CLOUDINARY_API_SECRET = "CLOUDINARY_API_SECRET"
    ```
- Run the following command to start the Flask ML project:
    ```sh
    py app.py
    ```
- The machine learning should now be running.

## Common Issues

If you cannot activate the Python environment and encounter an ExecutionPolicy error:
- Run one of the following commands in PowerShell:

    ```sh
    # Choose one of the following
    Set-ExecutionPolicy Unrestricted -Scope CurrentUser
    Set-ExecutionPolicy Unrestricted -Scope Process
    ```
- You can later reset it with the following command:
    ```sh
    set-executionpolicy remotesigned
    ```
- Then, simply activate the environment in the Visual Studio Code terminal by running:
    ```sh
    ./activate
    ```

 ##Steps to Download project-name-firebase-adminsdk.json
--Access Firebase Console

--Go to Firebase Console: https://console.firebase.google.com.
--Log in with your Google account.
--Select Your Project

--Click on your project (e.g., ExpiryPal).
--Go to Project Settings

--In the left-hand menu, select Project Settings.
--Navigate to "Service Accounts" Tab

--At the top of the settings page, click the Service Accounts tab.
--Generate a New Private Key

--Click on Generate new private key.
--A confirmation popup will appear. Click Generate Key.
--Download the JSON File

--The file project-name-firebase-adminsdk.json will be downloaded automatically.
--Move this file to your project directory be/secret.
--Add to .gitignore

--Ensure that the file is listed in your .gitignore to prevent accidental uploads to the repository.

  
