
from src import app
import json
from flask import jsonify, request
from src.controllers import (
    userController as User,
)


@app.route("/user/all", methods=["GET"])
def GetAllUsers():
    result = User.GetAllUsers()
    return result.jsonify()

