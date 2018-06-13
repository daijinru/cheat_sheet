# 返回信息处理
from flask import make_response, jsonify

def responseNormal(status, message = '', data = {}):
    returnData = {}
    returnData['status'] = status
    returnData['message'] = message
    returnData['data'] = data
    returnData = make_response(jsonify(returnData))
    returnData.headers['Access-Control-Allow-Origin'] = '*'
    return returnData