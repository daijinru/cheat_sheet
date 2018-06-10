from flask import Flask, request
from pymongo import MongoClient
from app.common.response import responseNormal
from app.config.main import *

app = Flask(__name__)
conn = MongoClient(Config.database, Config.databasePort)
db = conn.devlint

# API V1 '/api/v1/'

# 获取所有集合
@app.route('/api/v1/datas/collections')
def getCollectionsAll():
    collectionNames = db.collection_names()
    returnData = responseNormal(200, '返回数据', collectionNames)
    return returnData

# 查询指定文档
@app.route('/api/v1/datas/<sheet>')
def sheetQuery(sheet):
    sheet = sheet.lower()
    documentCursor = db[sheet].find()

    # 如果文档不存在
    documentCount = documentCursor.count()
    if documentCount < 1:
        # 关闭游标
        documentCursor.close()
        returnData = responseNormal(200, '数据尚未生成', [])
        return returnData

    documentList = []
    for document in documentCursor:
        documentCache = {}
        del document['_id']
        for keyname in document:
            documentCache[keyname] = document[keyname]
        documentList.append(documentCache)
    documentCursor.close()

    # 返回查询信息
    returnData = responseNormal(200, '查询成功', documentList)
    return returnData

# 上传文档
@app.route('/api/v1/document/upload', methods=['POST'])
def documentUpload():
    collectionDict = request.form.to_dict()

    # collectionName to lowercase
    collectionName = collectionDict['collection'].lower()
    documentName = collectionDict['document']
    documentContent = collectionDict['content']

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
    documentDict['content'] = documentContent

    db[collectionName].insert(documentDict)

    returnData = responseNormal(200, '提交成功')
    return returnData

# 更新文档
@app.route('/api/v1/document/update', methods=['POST'])
def documentUpdate():
    collectionDict = request.form.to_dict()
    collectionName = collectionDict['collection'].lower()
    documentName = collectionDict['document']
    documentContent = collectionDict['content']

    documentCursor = db[collectionName].find({'document': documentName})
    documentCount = documentCursor.count()
    documentCursor.close()

    # 如果文档不存在则返回
    returnData = {}
    if documentCount < 1:
        returnData = responseNormal(200, '%s 文档不存在' % documentName)
        return returnData

    documentDict = {}
    documentDict['document'] = documentName
    documentDict['content'] = documentContent
    db[collectionName].update(
        {'document': documentName},
        documentDict
    )

    returnData = responseNormal(200, '%s 文档更新成功' % documentName)
    return returnData

# 文档【有用】按钮点击接口，每点击一次增加 1
@app.route('/api/v1/document/like', methods=['POST'])
def documentLikeNum():
    collectionDict = request.form.to_dict()

    collectionName = collectionDict['collection'].lower()
    documentName = collectionDict['document']

    db[collectionName].find_and_modify(
        query={'document': documentName},
        update={'$inc': {'likenum': 1}}
    )

    returnData = responseNormal(200, '提交成功')
    return returnData

# TODO: [待定接口] 读取 MD 文档并返回字符串
@app.route('/api/v1/document/<sheet>', methods=['GET'])
def returnDocument(sheet):
    sheet = sheet.lower()

    # 读取 /static/source/<sheet>.md，返回字符串
    mdDocument = ''
    resultQuery = ''
    try:
        mdUrlStr = 'app/static/source/' + sheet + '.md'
        file = open(mdUrlStr, 'r')
    except IOError:
        resultQuery = '文件不存在'
    else:
        resultQuery = '查询成功'
        mdDocument = file.read()
        # mdDocument = markdown.markdown(mdDocument)
        file.close()
    returnData = responseNormal(200, resultQuery, mdDocument)
    return returnData

