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
    userController as User,
    notificationPreferencesController as NPC,
    ItemController as Item,
    FridgeController as Fridge
)


@app.route("/user/all", methods=["GET"])
def GetAllUsers():
    result = User.GetAllUsers()
    return result.jsonify()

@app.route('/api/register-token', methods=['POST'])
def register_token():
    data = request.get_json()
    auth_token = request.cookies.get('auth_token')
    print("data in user_routes.py > register_token", data)
    print("auth_token in user_routes.py > register_token", auth_token)
    return User.saveCMFToken(data, auth_token)

@scheduler.task("interval", id="send_notifications", minutes=1)
def send_notifications():
    print("\n\nSending notifications")
    with app.app_context():  # Necesario para acceder al contexto de Flask
        today = datetime.datetime.now().date()

        fridges = Fridge.GetAllFridges()
        for fridge in fridges:
            preferences = NPC.GetNotificationPreferencesByFridgeId(fridge.id)
            items = Item.getItemsByFridgeId(fridge.id)
            user = User.get_user_by_fridge(fridge.id)

            if not user or not user.fcm_token:
                continue

            for item in items:
                # Notificaciones de expiración
                if Item.should_notify_expiration(item, today, preferences.expiration):
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="Item Expiration Alert",
                            body=f"The item '{item.name}' will expire soon."
                        ),
                        token=user.fcm_token,
                    )
                    messaging.send(message)

                # Notificaciones de ítems no usados
                if Item.should_notify_unused(item, today, preferences.unusedItem):
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="Unused Item Alert",
                            body=f"The item '{item.name}' has not been used for a while."
                        ),
                        token=user.fcm_token,
                    )
                    messaging.send(message)

@app.route('/getcookies', methods=['GET'])
def getcookies():
    return jsonify(request.cookies)