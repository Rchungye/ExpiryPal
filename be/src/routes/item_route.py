from models import db, ma, Item
from flask import Blueprint, request

item_routes = Blueprint('item_routes', __name__)

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'addedDate', 'expirationDate', 'fridge_id')

ItemSchema = ItemSchema()
ItemsSchema = ItemSchema(many=True)

@item_routes.route('/items', methods=['POST'])
def add_item():
    name = request.json['name']
    expirationDate = request.json['expirationDate']
    fridge_id = request.json['fridge_id']

    new_item = Item(name, expirationDate, fridge_id)

    db.session.add(new_item)
    db.session.commit()
    return ItemSchema.jsonify(new_item)
