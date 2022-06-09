class ClassAllData:
    
    def __init__(self, type):
        self.__type = type
        
    
    @property
    def getData(self):
        return self.__data
    
    @getData.setter
    def setData(self, data):
        self.__data = data
    
    @property
    def load_process(self):
        if(self.__type == 'customer'):
            self._load_customers()
        elif(self.__type == 'product'):
            self._load_product()
   
    def _load_customers(self):
        Customers = self.__data 
        d = []
        b = {}
        for customer in Customers:
            b = {'customer_id':customer.customer_id,'name':customer.name, 'email':customer.email}
            d.append(b)
        print("_load_customers",d)
        self.__list = d
    
   
    def _load_product(self):
        Products = self.__data 
        d = []
        b = {}
        for product in Products:
            b = {
                'product_id':product.product_id,
                'name':product.name, 
                'product_description':product.product_description,
                'price': product.price
            }
            d.append(b)
        self.__list = d

    @property
    def resolved(self):
        return self.__list

        
        