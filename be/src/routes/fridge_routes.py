from flask import Blueprint, request
from models import db, Fridge
from models import ma

fridge_routes = Blueprint('fridge_routes', __name__)

class FridgeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'model', 'brand', 'code')

fridge_schema = FridgeSchema()
fridges_schema = FridgeSchema(many=True)

@fridge_routes.route('/fridges', methods=['POST'])
def add_fridge():
    data = request.json
    if not all(key in data for key in ['model', 'brand', 'code']):
        return {"error": "Missing required fields"}, 400

    model = data['model']
    brand = data['brand']
    code = data['code']

    if Fridge.query.filter_by(code=code).first():
        return {"error": "Fridge code already exists"}, 400

    new_fridge = Fridge(model, brand, code)

    db.session.add(new_fridge)
    db.session.commit()
    return fridge_schema.jsonify(new_fridge), 201


@fridge_routes.route('/fridges', methods=['GET'])
def get_fridges():
    all_fridges = Fridge.query.all()
    result = fridges_schema.dump(all_fridges)
    return {"fridges": result}, 200