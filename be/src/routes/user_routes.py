import datetime
from src import app, scheduler, db
import firebase_admin
from firebase_admin import credentials, messaging
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(current_dir, "../secret/expirypalnotifications-firebase-adminsdk-nfft8-d43dbaa900.json")
resolved_path = os.path.abspath(cred_path)
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

import json
from flask import jsonify, request
from src.controllers import (
    userController as UserController,
    notificationPreferencesController as NPC,
    ItemController as Item,
    FridgeController as Fridge
)
from src.models.user import (
    User as UserClass
)

from src.middleware import (
    secure as middelware
)

@app.route('/groceries', methods=['GET'])
@middelware.require_auth
def groceries():
    return jsonify({"message": "Welcome to groceries"})


@app.route("/user/all", methods=["GET"])
def GetAllUsers():
    result = UserController.GetAllUsers()
    return result.jsonify()


@app.route('/api/register-token', methods=['POST'])
def register_token():
    cookies = request.cookies
    print("\n\nRequest cookies in register-token: ", cookies)

    data = request.get_json()
    print("Data received in register_rotoken : ", data)

    result =  UserController.saveCMFToken(data, cookies)
     # Accede al cuerpo de la respuesta
    if isinstance(result, tuple):
        response_body = result[0].get_data(as_text=True)  # Obtiene el cuerpo de la respuesta como texto
    else:
        response_body = result.get_data(as_text=True)

    print("Result body: ", response_body)  # Muestra el cuerpo de la respuesta

    return result

@scheduler.task("interval", id="send_notifications", minutes=0.2)
def send_notifications():
    print("\n\nChecking if notifications should be sent...")
    with app.app_context():  # Necesario para acceder al contexto de Flask
        today = datetime.datetime.now().date()

        fridges = Fridge.GetAllFridges()


        for fridge in fridges:
            print(f"Processing fridge {fridge.id}")
            response, status_code = NPC.GetNotificationPreferencesByFridgeId(fridge.id).jsonify()

            # Imprimir el código de estado
            print(f"HTTP Status Code: {status_code}")

            # Acceder al contenido de la respuesta
            preferences = response.get_json()  # Parsear el contenido JSON

            # Imprimir el contenido de las preferencias
            print(f"Preferences: {preferences}")
            expiration_date_user_preference = preferences["expiration"]
            unused_item_user_preference = preferences["unusedItem"]
            
            items_response = Item.getItemsByFridgeId(fridge.id)
            
            items = items_response.get('payload', [])
            
            users = Fridge.get_user_by_fridge(fridge.id)
            print(f"Users: {users}")
            if not users:
                print(f"No users found for fridge {fridge.id}, skipping notifications.")
                continue  # Si no hay usuarios, continuar con el siguiente refrigerador

            for item in items:

                added_date = item.get("addedDate")
                expiration_date = item.get("expirationDate")
                
                item_name = item.get("name")
                item_id = item.get("id")


                print(f"\nAdded date: {added_date}")
                print(f"Today: {today}")
                print(f"unused_item_user_preference: {unused_item_user_preference}")
                print(f"\nexpiration date: {expiration_date}")
                print(f"expiration_date_user_preference: {expiration_date_user_preference}")
                print(f"today: {today}")
                print(f"Item name: {item_name}")

                for user in users: 
                    print(f"Processing user_id {user.id} username: {user.username}")
                    # Notificaciones de expiración
                    print(f"Expiration date: {expiration_date}, ")
                    if (expiration_date == "0000-00-00"):
                        print(f"Item {item_id} has no expiration date. {expiration_date} Skipping expiration notification.")
                    else:
                        print(f"Item {item_id} has expiration date. {expiration_date} Checking if notification should be sent.")
                        Item.should_notify_expiration(expiration_date, today, expiration_date_user_preference)
                        message = messaging.Message(
                            notification=messaging.Notification(
                                title="Item Expiration Alert",
                                body=f"The item '{item_name}' will expire soon."
                            ),
                            token=user.fcm_token,
                        )
                        
                        print(f"EXP NOT: Sending notification to user {user.id} for item {item_id}")
                        messaging.send(message)

                    # Notificaciones de ítems no usados
                    if Item.should_notify_unused(added_date, today, unused_item_user_preference):
                        message = messaging.Message(
                            notification=messaging.Notification(
                                title="Unused Item Alert",
                                body=f"The item '{item.get("name")}' has not been used for a while."
                            ),
                            token=user.fcm_token,
                        )
                        print(f"UNUSED NOT: Sending notification to user {user.id} for item {item.get("id")}")
                        messaging.send(message)

@app.route('/getcookies', methods=['GET'])
def getcookies():
    return jsonify(request.cookies)


@app.route("/checkIfCMFToken", methods=['GET'])
def checkIfCMFToken():
    data = request.cookies
    return UserController.checkIfCMFToken(data)