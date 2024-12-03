
from src import app
import json
from flask import jsonify, request
from src.controllers import (
    ItemController as Item,
)


@app.route("/item/all", methods=["GET"])
def GetAllItems():
    result = Item.GetAllItems()
    return result.jsonify()

