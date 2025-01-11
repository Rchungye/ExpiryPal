from flask import request, jsonify, redirect

def require_auth(func):
    def wrapper(*args, **kwargs):
        # Obtén el auth_token de las cookies
        auth_token = request.cookies.get('auth_token')
        if not auth_token:
            # Si no hay token, redirige o retorna un error
            return jsonify({"error": "Unauthorized access"}), 401
        # Puedes agregar más validaciones aquí, como decodificar el token
        # y verificar su validez
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
