from pymongo import *
from scrapy import Request


def test():
    client = MongoClient()
    # 创建数据库
    db = client['test']
    dblist = client.list_database_names()
    if "admin" in dblist:
        print("create database complete!")

    # 创建集合
    col = db["testA"]
    collist = db.list_collection_names()
    if "testA" in collist:
        print("create set complete!")

    # 增
    dic = {"name": "A", "attribute": "A"}
    diclist = [
        {"name": "B", "attribute": "B"},
        {"name": "C", "attribute": "C"}
    ]
    id_1 = col.insert_one(dic)
    id_2 = col.insert_many(diclist)

    # 查: 同mongodb操作, 不再展示
    for x in col.find():
        print(x)

    # 改: 同mongodb操作
    query = {"name": "A"}
    values = {"$set": {"attribute": "a"}}
    col.update_one(query, values)

    # 删:
    query = {"name": "A"}
    col.delete_one(query)
    col.delete_many(query)
    col.drop()



