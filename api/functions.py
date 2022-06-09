from ClassAllData import ClassAllData
from flask import request

# METODO all_data
def all_data(type, query):
    cl = ClassAllData(type)
    cl.setData = query
    cl.load_process
    return cl.resolved

# METODO get_request_json
def get_request_json():
    return request.get_json()