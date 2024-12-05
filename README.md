# ExpiryPal

DESCRIPTION OF THE PROJECT

## Technologies Used

- MySQL
- Python with Flask
- SQLAlchemy
- JavaScript with Vite + React.js
- TailwindCSS
- Material UI

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
- Install the Flask project dependencies with the command:
    ```sh
    pip install -r .\requirements.txt
    ```
- Create a `.env` file in the root directory with the following structure:
    ```sh
    DB_CONN = "mysql+pymysql://user:password@host:port/expirypal"
    # Replace user, password, host, and port according to your MySQL configuration.
    ```
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
- Run the following command to start the Flask project:
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
- Create a `.env` file in the root directory with the following structure:
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