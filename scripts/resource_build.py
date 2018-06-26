import os
import re
import sys
import urllib.parse as UrlParse
from pymongo import MongoClient

sys.path.append('../')
from app.config.main import *

ConnectClient = MongoClient(Config.database, Config.databasePort)
db = ConnectClient.devsheets

# collectionName 集合
collectionDict = {}
fileList = os.listdir('../resource/')
for fileName in fileList:
    if '.md' in fileName:
        filePath = '../resource/' + fileName
        file = open(filePath, 'r')
        fileContent = file.read()

        # 如果文档同时具备 title 和 category 字段则执行以下操作
        documentTitle = re.search('(?<=title:).+(?=\n)', fileContent)
        documentCategory = re.search('(?<=category:).+(?=\n)', fileContent)
        if documentTitle is not None:

            # 处理掉顶部文档信息和花括号内的信息
            fileContentClear = re.sub('{.+(}\n)', '', fileContent)
            fileContentClear = fileContentClear[fileContentClear.find('\n---\n') + 4:].lstrip()

            # 如果 documentCategory 为空，则归类为 Others
            if documentCategory is not None:
                collectionName = UrlParse.quote(documentCategory.group().strip())
            else:
                collectionName = 'Others'

            documentName = UrlParse.quote(documentTitle.group().strip())
            documentName = re.sub('\..+', '', documentName)
            documentContent = fileContentClear

            documentDict = {}
            documentDict['document'] = documentName
            documentDict['content'] = documentContent

            if collectionName in collectionDict:
                collectionDict[collectionName].append(documentDict)
            else:
                collectionDict[collectionName] = []

            file.close()

for collection in collectionDict:
    collectionSubList = collectionDict[collection]
    for document in collectionSubList:
        try:
            _id = db[collection].find_and_modify(
                query={'document': 'sequenceValue'},
                update={'$inc': {'increase': 1}},
                upsert=True
            )['increase']
        except:
            _id = 0
        document['id'] = _id
        db[collection].find_and_modify(
            query={'document': document['document']},
            update=document,
            upsert=True
        )
        print('已添加：' + document['document'])

