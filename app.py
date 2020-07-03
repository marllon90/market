from flask import Flask, abort, request
from flask_restplus import Api, Resource, fields
from sqlalchemy.exc import DataError

from db import session
from models import Order, OrderDetail, Product, User
from schemas import OrderDetailSchema, OrderSchema, ProductSchema, UserSchema
from service import ApiService

app = Flask(__name__)

app.config.from_object('config.Development')


api = Api(app, doc='/docs', version='0.1', title='A simple e-commerce service Api',
    description='This API can be used to Create, Retrieve, Update and Delete e-commerce resources (users, products, orders) with Postgres SQL and SQLAlchemy ORM', )

ns_user = api.namespace('users', description='Users API')
ns_order = api.namespace('orders', description='Orders API')
ns_product = api.namespace('products', description='Products API')


userSwagger = api.model('User', {
    'username': fields.String(required=True, description='Unique username for login'),
    'name': fields.String(required=True, description='Full user name'),
    'email': fields.String(required=True, description='Email address'),
    'city': fields.String(required=True, description='User city'),
    'province': fields.String(required=True, description='User province'),
    'country': fields.String(required=True, description='User country'),
    'address': fields.String(required=True, description='User main address'),
    'zip_code': fields.String(required=True, description='User address zip-code'),
    'phone': fields.String(required=True, description='User phone number')
})

orderSwagger = api.model('OrderDetails', {
    'user_id': fields.String(required=True, description='User id for order'),
    'product_id': fields.String(required=True, description='Product id for order'),
    'quantity': fields.Integer(required=True, description='Product quantity')
})

productSwagger = api.model('Product', {
    'name': fields.String(required=True, description='Product name'),
    'sku': fields.String(required=True, description='Product SKU'),
    'price': fields.Float(required=True, description='Product price'),
    'image_url': fields.String(required=False, description='Product image cdn url'),
    'description': fields.String(required=True, description='Product full description')
})

@ns_user.route('/<uuid:id>')
class UserResource(Resource):
    @api.doc(
        responses={
            200: 'OK',
            400: 'Not Found',
            500: 'Internal Error'
        }
    )
    def get(self, id):
        """
        Get User by id
        """
        aps = ApiService()        
        return {
            'data': aps.get_by_id(User, UserSchema(), id)
        }
    
    @ns_user.expect(userSwagger)
    def put(self, id):
        """
        Update User by id
        """
        aps = ApiService()
        payload = request.get_json()  
        return {
            'data': aps.update_data(User, UserSchema(), payload, id)
        }
    
    def delete(self, id):
        """
        Remoce User by id
        """
        aps = ApiService()        
        return {
            'data': aps.delete_data(User, UserSchema(), id)
        }

@ns_user.route('/')    
class UserListResource(Resource):
    
    @ns_user.expect(userSwagger)
    def post(self):
        """
        Create User
        """
        aps = ApiService()
        payload = request.get_json()
        expected_fields = [
            "username", "name", "email", "city", "province", "country", "address", "zip_code", "phone"
        ]

        status, response = aps.set_data(User(), UserSchema(), expected_fields, payload)
        
        if status:
            return {
                "data": response
            }

        abort(400, response)
    
    def get(self):
        """
        List all users
        """
        aps = ApiService()     
        return {
            'data': aps.get_all(User, UserSchema())
        }


@ns_product.route('/')    
class ProductListResource(Resource):
    @ns_product.expect(productSwagger)
    def post(self):
        """
        Create Product
        """
        aps = ApiService()
        payload = request.get_json()
        expected_fields = [
            "name", "sku", "price", "image_url", "description"
        ]

        status, response = aps.set_data(Product(), ProductSchema(), expected_fields, payload)
        
        if status:
            return {
                "data": response
            }

        abort(400, response)
    
    def get(self):
        """
        List all products
        """
        aps = ApiService() 
        return {
            'data': aps.get_all(Product, ProductSchema())
        }


@ns_product.route('/<uuid:id>')
class ProductResource(Resource):
    @api.doc(
        responses={
            200: 'OK',
            400: 'Not Found',
            500: 'Internal Error'
        }
    )
    def get(self, id):
        """
        Get Product by id
        """
        aps = ApiService()        
        return {
            'data': aps.get_by_id(Product, ProductSchema(), id)
        }
    
    @ns_product.expect(productSwagger)
    def put(self, id):
        """
        Update Product by id
        """
        aps = ApiService()
        payload = request.get_json()  
        return {
            'data': aps.update_data(Product, ProductSchema(), payload, id)
        }
    
    def delete(self, id):
        """
        Remoce Product by id
        """
        aps = ApiService()        
        return {
            'data': aps.delete_data(Product, ProductSchema(), id)
        }
@ns_order.route('/')
class OrderListResource(Resource):
    @api.doc(
        responses={
            200: 'OK',
            400: 'Not Found',
            500: 'Internal Error'
        }
    )
    @ns_order.expect(orderSwagger)
    def post(self):
        """
        Create Order
        """
        payload = request.get_json()
        product_id = payload.get('product_id')
        user_id = payload.get('user_id')
        quantity = payload.get('quantity')
        
        try:
            if quantity < 1:
                abort(400, 'Quantity must be greater than 1')
        
        except TypeError:
            abort(500, 'Quantity must be an integer type')
            
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            user = session.query(User).filter(User.id == user_id).first()

            order = Order()

            #Create new order
            order.user = user.id
            session.add(order)
            session.commit()


            order_detail = OrderDetail()
            order_detail.order = order.id
            order_detail.product = product.id
            order_detail.quantity = quantity
            order_detail.total_price = quantity * (product.price or 1)

            #Create new order detail
            session.add(order_detail)
            session.commit()

            schema = OrderDetailSchema()

            return {
                "data": schema.dump(order_detail)
            }
        
        except DataError:
            abort(400, 'Product or Customer not found')
        

    def get(self):
        """
        List all orders
        """
        aps = ApiService()     
        return {
            'data': aps.get_all(OrderDetail, OrderDetailSchema())
        }

@ns_order.route('/<uuid:id>')
class OrderResource(Resource):
    def get(self, id):
        aps = ApiService()
        return {
            'data': aps.get_by_id(OrderDetail, OrderDetailSchema(), id)
        }

@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error)}, getattr(error, 'code', 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
