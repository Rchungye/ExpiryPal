from flask import request, g
from src import app
from src.models import User
from src.controllers import get_user_fridge_id

@app.before_request
def attach_user_context():
    """
    Middleware para agregar el contexto del usuario y el refrigerador al request.
    """
    auth_token = request.cookies.get('auth_token')
    if auth_token:
        user = User.query.filter_by(auth_token=auth_token).first()
        if user:
            g.user = user  # Guarda el usuario en el contexto global
            g.fridge_id = get_user_fridge_id(auth_token)  # Vincula el fridge_id dinámicamente
        else:
            g.user = None
            g.fridge_id = None
    else:
        g.user = None
        g.fridge_id = None
