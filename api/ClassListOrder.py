from models import *
from sqlalchemy import create_engine, insert

class ClassListOrder:

    def __init__(self, data, FULL_URL_DB):
        self.__data = data
        self.__FULL_URL_DB = FULL_URL_DB
        self._load()
    
    def _load(self):
        self._get_customer_id()
        self._load_process()
        
    def _get_customer_id(self):
        customer = self.__data['customer']
        self.__init_date = self.__data['init_date']
        self.__end_date = self.__data['end_date']
        query = f"SELECT * FROM customer WHERE name = '{customer}' "
        tupla = self._sql_query(query)
        tupla = tupla[0]
        self.__customer_id = tupla[0]
    
    def _load_process(self):
        query = f"""
        SELECT O.order_id, TO_CHAR( O.creation_date :: DATE, 'yyyy/mm/dd'), O.total, O.delevery_address, OD.quantity, PO.name
        FROM "order" AS O, "order_detail" OD, "product" PO
        WHERE O.customer_id = {self.__customer_id}
        AND O.order_id = OD.order_id
        AND OD.product_id = PO.product_id
        AND O.creation_date BETWEEN  '{self.__init_date}' AND '{self.__end_date}' 
        GROUP BY O.order_id,OD.quantity,PO.name
        """
        tupla = self._sql_query(query)
        d = {}
        for v, t in enumerate(tupla):
            if t[0] not in d.keys():
                d[t[0]] = [t[0],t[1],t[2],t[3], f'* {t[4]}   {t[5]}']
            if v > 0:
                if d[t[0]][0] == t[0]:
                    d[t[0]][3] = d[t[0]][3] + ', ' + t[3]
                    if d[t[0]][4][6:] != t[5]:
                        d[t[0]][4] = f' {d[t[0]][4]} * {t[4]} {t[5]}'

        ress = []
        for f,k in d.items():
            ress.append({
                'creation Date': k[1],
                'Order Id': k[0],
                'Total': k[2],
                'Delivery Address':k[3],
                'Products':k[4]
            })
        self._setResponse(ress)

    @property
    def getResponse(self):
        return self.__response
    
    def _setResponse(self,response):
        self.__response = response

    def _sql_query(self, query):
        engine = create_engine(self.__FULL_URL_DB)

        with engine.connect() as conn:
            result = conn.execute(query)
            return result.fetchall()