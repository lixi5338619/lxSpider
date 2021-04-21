# -*- coding: utf-8 -*-
# @IDE ：PyCharm

import pymongo

class DB():
    def __init__(self):
        self.client = pymongo.MongoClient("127.0.0.1", port=27017)
        self.db = self.client["maimai"]
        self.userList = self.db["userList"]
        self.userDetail = self.db["userDetail"]


    def select_List(self):
        """ insert
        :param item: select of List
        """
        result = [i for i in self.userList.find({"valid":0})]
        self.client.close()
        return result

    def insert_list(self,item):
        """ dump filter
        :param item: save to List
        """
        if self.userList.find({"id":item['id']}):
            return
        else:
            self.userList.insert_one(item)
            print(item['id'])
        self.client.close()


    def insert_Detail(self,item):
        """ insert
        :param item: save to Detail
        """
        self.userDetail.insert_one(item)
        self.client.close()



    def update_list_valid(self,uid):
        self.userList.update_one({"id": uid}, {"$set": {"valid": 1}})
        self.client.close()

