# -*- coding: UTF-8 -*-
"""
@author:rebootcat
@file:config.py
@time:2022/06/30
@target: 
"""
import pymysql
import pymongo
import redis

lenovo_redis = redis.Redis(host="anonymous", port=6379, db=0, password="anonymous", decode_responses=True)

connect = pymysql.connect(host="anonymous", port=3306, user="anonymous", passwd="anonymous", db="anonymous",
                          charset="utf8")
cursor = connect.cursor()

mongo = pymongo.MongoClient("anonymous")
scientificData = mongo["scientificData"]

cherry = scientificData["cherryCorrection"]
cherryVariable = scientificData["cherryVariable"]

ginkgo = scientificData["ginkgoCorrection"]
ginkgoVariable = scientificData["ginkgoVariable"]
