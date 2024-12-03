from src import app
import json
from flask import jsonify, request
from src.controllers import (
    camaraController as Camera,
)


@app.route("/camera/all", methods=["GET"])
def GetAllCameras():
    result = Camera.GetAllCameras()
    return result.jsonify()

