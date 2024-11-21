from models import db, ma, Item
from flask import Blueprint, request

item_routes = Blueprint('item_routes', __name__)

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'name', 'addedDate', 'expirationDate', 'fridge_id')

ItemsSchema = ItemSchema(many=True)

@item_routes.route('/items', methods=['POST'])
def add_item():
    name = request.json['name']
    expirationDate = request.json['expirationDate']
    fridge_id = request.json['fridge_id']

    new_item = Item()
    new_item.name = name
    new_item.expirationDate = expirationDate
    new_item.fridge_id = fridge_id


    db.session.add(new_item)
    db.session.commit()
    return ItemSchema().jsonify(new_item), 201

@item_routes.route('/items', methods=['GET'])
def get_items():
    all_items = Item.query.all()
    result = ItemsSchema.dump(all_items)
    return {"items": result}, 200