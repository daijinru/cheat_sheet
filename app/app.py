from flask import Flask, request
from pymongo import MongoClient
from app.common.response import responseNormal
from app.common.login import loginToken
from app.config.main import *

app = Flask(__name__)
conn = MongoClient(Config.database, Config.databasePort)
db = conn.devsheets

# API V1 '/api/v1/'

# 登录接口

@app.route('/api/v1/login', methods=['POST'])
def loginTokenVerify():
    collectionDict = request.form.to_dict()

    try:
        username = collectionDict['username']
        pwd = collectionDict['password']
    except KeyError as ke:
        return responseNormal(400, '缺乏参数 %s' % ke)

    responseText = loginToken.loginVerify(username, pwd)
    responseCode = 200
    if responseText == '':
        responseCode = 400
    returnData = responseNormal(responseCode, '操作成功', responseText)
    return returnData

# 获取所有集合
@app.route('/api/v1/collections')
def getCollectionsAll():
    collectionNames = db.collection_names()
    returnData = responseNormal(200, '返回数据', collectionNames)
    return returnData

# 获取指定集合中的文档名
@app.route('/api/v1/<collection>')
def getCollection(collection):
    documentCursor = db[collection].find()

    documentList = []
    for document in documentCursor:
        documentList.append(document['document'])
    documentCursor.close()

    # 查询 sequenceValue 在列表中的位置并删除它
    if 'sequenceValue' in documentList:
        del documentList[documentList.index('sequenceValue')]

    returnData = responseNormal(200, '查询成功', documentList)
    return returnData

# 查询指定文档
@app.route('/api/v1/<collection>/<document>')
def getDocument(collection, document):
    documentCursor = db[collection].find({'document': document})

    # 如果文档不存在
    documentCount = documentCursor.count()
    if documentCount < 1:
        # 关闭游标
        documentCursor.close()
        returnData = responseNormal(400, '文档不存在', [])
        return returnData

    documentMap = {}
    for document in documentCursor:
        del document['_id']
        for key in document:
            documentMap[key] = document[key]
    documentCursor.close()

    # 返回查询信息
    returnData = responseNormal(200, '查询成功', documentMap)
    return returnData

# 上传文档
@app.route('/api/v1/document/upload', methods=['POST'])
def documentUpload():
    collectionDict = request.form.to_dict()

    # collectionName to lowercase
    try:
        collectionName = collectionDict['collection']
        documentName = collectionDict['document'].strip()
        documentContent = collectionDict['content']
        vertifyTokenResult = loginToken.verify_toekn(collectionDict['token'])
    except KeyError as ke:
        return responseNormal(400, '缺乏参数 %s' % ke)

    if vertifyTokenResult == -1:
        return responseNormal(400, 'token 错误，请重新登录')
    elif vertifyTokenResult == 1:
        return responseNormal(400, 'token 已过期，请重新登录')

    # 阻止重复提交
    documentCursor = db[collectionName].find({'document': documentName})
    documentCount = documentCursor.count()
    documentCursor.close()

    # 返回信息
    returnData = {}
    if documentCount > 0:
        returnData = responseNormal(200, '%s 文档已经存在，请勿重复提交' % documentName)
        return returnData

    # 获取自增 _id
    _id = 0
    try:
        _id = db[collectionName].find_and_modify(
            query={'document': 'sequenceValue'},
            update={'$inc': {'increase': 1}},
            upsert=True
        )['increase']
    except:
        _id = 0

    # 过滤数据
    documentDict = {}
    documentDict['document'] = documentName
    documentDict['content'] = documentContent
    documentDict['id'] = _id

    db[collectionName].insert(documentDict)

    responseText = {'id': _id}
    returnData = responseNormal(200, '提交成功', responseText)
    return returnData

# 更新文档
@app.route('/api/v1/document/update', methods=['POST'])
def documentUpdate():
    collectionDict = request.form.to_dict()

    try:
        collectionName = collectionDict['collection']
        documentName = collectionDict['document'].strip()
        documentContent = collectionDict['content']
        documentID = int(collectionDict['id'])
        token = collectionDict['token']
    except KeyError as ke:
        return responseNormal(400, '缺乏参数 %s' % ke)

    vertifyTokenResult = loginToken.verify_toekn(token)
    if vertifyTokenResult == -1:
        return responseNormal(400, 'token 错误，请重新登录')
    elif vertifyTokenResult == 1:
        return responseNormal(400, 'token 已过期，请重新登录')

    documentCursor = db[collectionName].find({'id': documentID})
    documentCount = documentCursor.count()
    documentCursor.close()

    # 如果文档不存在则返回
    returnData = {}
    if documentCount < 1:
        returnData = responseNormal(400, '你要更新的文档不存在')
        return returnData

    documentDict = {}
    documentDict['document'] = documentName
    documentDict['content'] = documentContent
    documentDict['id'] = documentID
    db[collectionName].update(
        {'id': documentID},
        documentDict
    )

    returnData = responseNormal(200, '%s 文档更新成功' % documentName)
    return returnData

# TODO: 文档【有用】按钮点击接口，每点击一次增加 1
@app.route('/api/v1/document/like', methods=['POST'])
def documentLikeNum():
    collectionDict = request.form.to_dict()

    collectionName = collectionDict['collection'].lower()
    documentName = collectionDict['document']

    db[collectionName].find_and_modify(
        query={'document': documentName},
        update={'$inc': {'likenum': 1}}
    )

    # TODO: 没有写限制点赞
    returnData = responseNormal(200, '提交成功')
    return returnData

# TODO: 读取 MD 文档并返回字符串
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
