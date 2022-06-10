from models import *
from sqlalchemy import create_engine, insert

class ClassCreateOrder:

    def __init__(self, post, FULL_URL_DB):
        self.__order = post
        self.__customer = self.__order['customer']
        self.__FULL_URL_DB = FULL_URL_DB
        self.__response = {}
    
    @property
    def getResponse(self):
        return self.__response
    
    def _setResponse(self,response):
        self.__response = response
    
    @property
    def load_process(self):
        if self._validate_max_order_products():
            self._validate_data_empty()
            self._get_customer_id()
            self._ready_order()
    
    def _validate_max_order_products(self):
        if len(self.__order['Products']) > 5:
            self._setResponse({"error_mensaje": f'maximo cinco productos por orden'})
            return False
        return True
            
    
    def _validate_data_empty(self):
        for key, item in self.__order.items():
            if  key !="Products" and len(item.strip()) == 0:
                self._setResponse({"error_mensaje": f'el item {key} es obligatorio para montar la orden'})
                return False
            elif len(item) == 0:
                self._setResponse({"error_mensaje": f'el item {key} es obligatorio para montar la orden'})
                return False

    def _get_customer_id(self):
        customer = self.__customer
        query = f"SELECT * FROM customer WHERE name = '{customer}' "
        tupla = self._sql_query(query)
        tupla = tupla[0]
        self.__customer_id = tupla[0]
    
    def _ready_order(self):
        query2 = f"SELECT P.name, P.price, P.product_id, P.product_description  FROM customer_product AS C, product AS P WHERE C.customer_id = {self.__customer_id } AND C.product_id = P.product_id"
        products = self._sql_query(query2)
        
        self.__customer_product = []
        self.__total = 0
        self.__order_list = []
        
        for product in products:
            
            if product[0] in self.__order['Products']:
                self.__order_list.append([product[2],product[3],product[1], self.__order['Products'].count(product[0])])
            
            for p in self.__order['Products']:
                if p == product[0]:
                    self.__total = self.__total + product[1]
                    
            self.__customer_product.append(product[0])
            
        order_products = list(dict.fromkeys(self.__order['Products']))
        
        not_product = ''
        ok_product = ''
        for o in order_products:
            if o not in  self.__customer_product:
                not_product += f'{o}, '
            else:
                ok_product += f'{o}, '

        if(len(not_product)> 0):
            self._setResponse(
             {
                'a_mensaje':f'El cliente: {self.__customer} no tiene acceso para algunos productos por favor revise lo orden',
                'sin acceso': f'{not_product}',
                'con acceso': f'{ok_product}',
                }
            )
        else:
            self._add_order()
    

    def _add_order(self):
        add_order = Order(self.__customer_id, self.__order['creation_date'], self.__order['delevery_address'], self.__total)
        db.session.add(add_order)
        db.session.commit()
        db.session.flush()
        self.__order_id = add_order.order_id
        self._add_order_detail()
    
    def _add_order_detail(self):
        if self.__order_id > 0:
            for orders in self.__order_list:
                add_order_detail = OrderDetail(self.__order_id,orders[0],orders[1],orders[2],orders[3])
                db.session.add(add_order_detail)
                db.session.commit()
                db.session.flush()
                order_detail_id = add_order_detail.order_detail_id
        
        new_order = {
            "customer":self.__customer ,
            "creation_date": self.__order['creation_date'],
            "delevery_address":self.__order['delevery_address'],
            "total":self.__total
        }
        self._setResponse(new_order)
        
    
    def _sql_query(self, query):
        engine = create_engine(self.__FULL_URL_DB)

        with engine.connect() as conn:
            result = conn.execute(query)
            return result.fetchall()
    