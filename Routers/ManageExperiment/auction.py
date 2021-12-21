import re
from flask import Flask, request, jsonify,send_from_directory
from flask.globals import current_app
from flask_cors import CORS
from flask import Blueprint
import json

from flask_login.mixins import AnonymousUserMixin
from Model.Model import Class, Experiment,StudentClass,Teacher,Student,Auction
import dbManage
from sqlalchemy import and_, or_
import os
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role

auctionRoute = Blueprint('auctionRoute', __name__)
CORS(auctionRoute, resources=r'/*')


basepath = os.path.dirname(__file__)

def checkToken(token,role):
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return 301
    
    if token_role != role:
        return 404
    else:
        return 200


@auctionRoute.route('/auction/addAuctionItem',methods=['POST'])  
def addAuctionItem():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    ex_id = data['ex_id']
    token = data['token']
    price = data['price']
    good = data['good']
    role = data['role']
    res = checkToken(token,Role.StudentRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        stu_list = Auction.query.filter(and_(Auction.s_id==s_id,Auction.experiment_id==ex_id)).all()
        if len(stu_list)>=3:
            return jsonify({'code':400,'message':'不能竞价大于3次'})
        if role == "需求者":
            _role = 0
        else:
            _role = 1
        auc = Auction(s_id = s_id,experiment_id = ex_id,good = good,price = price,role = _role)
        dbManage.db.session.add(auc)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"成功",'data':len(stu_list)+1})  #data代表竞价次数


@auctionRoute.route('/auction/getAuctionRole',methods=['POST'])  
def getAuctionRole():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    ex_id = data['ex_id']
    token = data['token']
    res = checkToken(token,Role.StudentRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        auction_item = Auction.query.filter(and_(Auction.s_id==s_id,Auction.experiment_id==ex_id)).first()
        if not auction_item:   #还没有出现过在里面，随机安排
            num = random.randint(0,1)
        else:
            num = auction_item.role

        if num==0:
            role = "需求者"
        else:
            role = "供给者"

        return jsonify({'code':200,'message':"成功获取角色",'data':role})

@auctionRoute.route('/auction/getDemand',methods=['POST'])  
def getDemand():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    ex = Experiment.query.filter(Experiment.experiment_id==ex_id).first()
    if not ex:
        return jsonify({'code':400,'message':"找不到实验",'data':None})
    else:
        xPotRange,yPotData = getSpecificItem(ex_id,1,0)  #demand都是0，provide最后一个是1,pot是1
        xBagRange,yBagData = getSpecificItem(ex_id,2,0)
        xPillowRange,yPillowData = getSpecificItem(ex_id,3,0)
        all_result={}

        this_max = len(xPotRange)
        choose_range = xPotRange
        for item in [xBagRange,xPillowRange]:
            if len(item)>this_max:
                this_max = len(item)
                choose_range = item
        if len(choose_range)==0:
            all_result["xData"] = []
        else:
            all_result["xData"] = list(range(1,eval(choose_range[-1])+1))
        all_result["yPotData"] = yPotData
        all_result["yBagData"] = yBagData
        all_result["yPillowData"] = yPillowData

        return jsonify({'code':200,'message':"获得需求曲线",'data':all_result})

@auctionRoute.route('/auction/getProvide',methods=['POST'])  
def getProvide():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    ex = Experiment.query.filter(Experiment.experiment_id==ex_id).first()
    if not ex:
        return jsonify({'code':400,'message':"找不到实验",'data':None})
    else:
        xPotRange,yPotData = getSpecificItem(ex_id,1,1)  #demand都是0，provide最后一个是1,pot是1
        xBagRange,yBagData = getSpecificItem(ex_id,2,1)
        xPillowRange,yPillowData = getSpecificItem(ex_id,3,1)
        all_result={}

        this_max = len(xPotRange)
        choose_range = xPotRange
        for item in [xBagRange,xPillowRange]:
            if len(item)>this_max:
                this_max = len(item)
                choose_range = item

        if len(choose_range)==0:
            all_result["xData"] = []
        else:
            all_result["xData"] = list(range(1,eval(choose_range[-1])+1))
        all_result["yPotData"] = yPotData
        all_result["yBagData"] = yBagData
        all_result["yPillowData"] = yPillowData

        return jsonify({'code':200,'message':"获得供给曲线",'data':all_result})
        
#获取参与次数
@auctionRoute.route('/auction/getExCount',methods=['POST'])  
def getExCount():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    ex = Experiment.query.filter(Experiment.experiment_id==ex_id).first()
    if not ex:
        return jsonify({'code':400,'message':"找不到实验",'data':None})
    else:
        auc_list = Auction.query.filter(Auction.experiment_id==ex_id).all()
        return jsonify({'code':200,'message':"获得供给曲线",'data':len(auc_list)})


def getSpecificItem(ex_id,thisType,role):
        demand_list = Auction.query.filter(and_(Auction.experiment_id==ex_id,Auction.good==thisType,Auction.role==role)).all()
        price_list = []
        result = []
        for item in demand_list:
            price_list.append(item.price)

        price_list.sort(key=None, reverse=False) #排序

        count = 1
        if len(price_list)==1:
            result.append([1,price_list[0]])
        else:
            for idx in range(1,len(price_list)):
                if price_list[idx] == price_list[idx-1]:
                    count += 1
                    continue
                else:
                    if idx==1:
                        tp_list = [1,price_list[0]]
                        result.append(tp_list)
                    tp_list = [idx+count,price_list[idx]]
                    result.append(tp_list)
                    count = 1

        #返回给前端范围和y值
        xRange = []
        yData = []
        for item in result:
            xRange.append(str(item[0]))
            yData.append(str(item[1]))

        return xRange,yData