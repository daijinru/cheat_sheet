from flask import Flask, request
from pymongo import MongoClient
from app.common.response import responseNormal
from app.config.main import *

app = Flask(__name__)
conn = MongoClient(Config.dev['database'], Config.dev['databasePort'])
db = conn.devlint

@app.route('/<tech>')
def index(tech):
    tech = tech.lower()
    documentCursor = db[tech].find()

    documentList = []
    for document in documentCursor:
        documentCache = {}
        del document['_id']
        for keyname in document:
            documentCache[keyname] = document[keyname]
        documentList.append(documentCache)

    # 关闭游标
    documentCursor.close()

    # 返回查询信息
    returnData = responseNormal(200, '查询成功', documentList)
    return returnData

@app.route('/upload/document', methods=['POST'])
def upload():
    collectionDict = request.form.to_dict()

    # collectionName to lowercase
    collectionName = collectionDict['collection'].lower()
    documentName = collectionDict['document']

    # 阻止重复提交
    documentCursor = db[collectionName].find({'document': documentName})
    documentCount = documentCursor.count()
    documentCursor.close()

    # 返回信息
    returnData = {}
    if documentCount > 0:
        returnData = responseNormal(200, '%s 文档已经存在，请勿重复提交' % documentName)
        return returnData

    # 过滤数据
    documentDict = {}
    documentDict['document'] = documentName
    documentDict['content'] = collectionDict['content']
    db[collectionName].insert(documentDict)

    returnData = responseNormal(200, '提交成功')
    return returnData

# 文档【有用】按钮点击接口，每点击一次增加 1
@app.route('/update/document/use', methods=['POST'])
def update():
    collectionDict = request.form.to_dict()

    collectionName = collectionDict['collection'].lower()
    documentName = collectionDict['document']

    db[collectionName].find_and_modify(
        query={'document': documentName},
        update={'$inc': {'likenum': 1}}
    )

    returnData = responseNormal(200, '提交成功')
    return returnData
