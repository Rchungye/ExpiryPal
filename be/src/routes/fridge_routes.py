from src import app
import json
from flask import jsonify, request
from src.controllers import (
    fridgeController as Fridge,
)


@app.route("/fridge/all", methods=["GET"])
def GetAllFridges():
    result = Fridge.GetAllFridges()
    return result.jsonify()
