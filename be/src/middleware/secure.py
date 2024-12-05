from flask import request, jsonify
from functools import wraps
from src.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Obtain the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        # Extract the token (e.g "Bearer <token>")
        try:
            token = token.split(" ")[-1]  # only take the token part
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 400

        # look up the user by the token
        user = User.query.filter_by(auth_token=token).first()
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 403

        # pass the user to the route handler
        return f(user, *args, **kwargs)
    return decorated
