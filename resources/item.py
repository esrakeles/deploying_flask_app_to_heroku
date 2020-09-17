from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id !"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item :
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        #if next(filter(lambda x : x['name'] == name, items), None):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            #item.insert() # ItemModel.insert(item)
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # Internal server error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        #item = next(filter(lambda x : x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        if item is None:
        #     try:
        #         updated_item.insert() #I temModel.insert(updated_item)
        #     except:
        #         return {"message": "An error occurred inserting the item."}, 500
            item = ItemModel(name, data['price'], data['store_id']) # we can write ...(name, **data)
        else:
            # try:
            #     #updated_item.update() # ItemModel.update(updated_item)
            #     updated_item.delete_from_db()
            # except:
            #         return {"message": "An error occurred updating the item."}, 500
            item.price = data['price']

        item.save_to_db()
        # return updated_item.json()
        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        #
        # items = []
        # for row in result:
        #     items.append({'name': row[1], 'price': row[2]})
        #
        # connection.close()
        #
        # return {'items':items}

        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} # üst satır ile aynı ancak performansı daha yüksek
