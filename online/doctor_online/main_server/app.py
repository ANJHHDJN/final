from flask import Flask
from flask import request
app = Flask(__name__)
import requests
import redis
import json
from unit import unit_chat
from neo4j import GraphDatabase
from config import NEO4J_CONFIG
from config import REDIS_CONFIG
from config import model_serve_url
from config import TIMEOUT
from config import reply_path
from config import ex_time
pool = redis.onnectionPool( **REDIS_CONFIG)
_driver = GraphDatabase.driver( **NEO4J_CONFIG)


# 查询neo4j图数据的函数
def query_neo4j(text):
    # 开启一个会话session来操作图数据库
    with _driver.session() as session:
        cypher = "MATCH(a:Symptom) WHERE(%r contains a.name) WITH \
                 a MATCH(a)-[r:dis_to_sym]-(b:Disease) RETURN b.name LIMIT 5" %text
        record = session.run(cypher)
        # 从record中读取真正的疾病名称信息, 并封装成List返回
        result = list(map(lambda x: x[0], record))
    return result


# 主要逻辑服务类Handler类
class Handler(object):
    def __init__(self, uid, text, r, reply):
        # uid：用户id text：用户输入文本，r：redis链接 reply：unit规则对话
        self.uid = uid
        self.text = text
        self.r = r
        self.reply = reply

    # 编写非首句处理函数, 该用户不是第一句问话
    def non_first_sentence(self, previous):
        # 尝试请求语句模型服务, 如果失败, 打印错误信息，在此处打印信息, 说明服务已经可以进入到首句处理函数中
        print("准备请求句子相关模型服务!")
        try:
            data = {"text1": previous, "text2": self.text}
            result = requests.post(model_serve_url, data=data, timeout=TIMEOUT)
            # 如果回复为空, 说明服务暂时不提供信息, 转去百度机器人回复
            if not result.text:
                return unit_chat(self.text)
            print("句子相关模型服务请求成功, 返回结果为:", result.text)
        except Exception as e:
            print("模型服务异常:", e)
            return unit_chat(self.text)

        print("启动模型服务后, 准备请求neo4j查询服务!")
        s = query_neo4j(self.text)
        print("neo4j查询服务请求成功, 返回结果是:", s)
        if not s:
            return unit_chat(self.text)
        # 如果结果不是空, 从redis中获取上一次已经回复给用户的疾病名称
        old_disease = self.r.hget(str(self.uid), "previous_d")
        # 如果曾经回复过用户若干疾病名称, 将新查询的疾病和已经回复的疾病做并集, 再次存储
        if old_disease:
            new_disease = list(set(s) | set(eval(old_disease)))
            # 返回给用户的疾病res, 是本次查询结果和曾经的回复结果之间的差集
            res = list(set(s) - set(eval(old_disease)))
        else:
            res = new_disease = list(set(s))

        # 将new_disease存储进redis数据库中, 同时覆盖掉之前的old_disease，并设置过期时间
        self.r.hset(str(self.uid), "previous_d", str(new_disease))
        self.r.expire(str(self.uid), ex_time)

        print("使用规则对话模板进行返回对话的生成!")
        # 将列表转化为字符串, 添加进规则对话模板中返回给用户
        if not res:
            return self.reply["4"]
        else:
            res = ",".join(res)
            return self.reply["2"] %res

    # 编码首句请求的代码函数
    def first_sentence(self):
        print("该用户近期首次发言, 不必请求模型服务, 准备请求neo4j查询服务!")
        # 直接查询neo4j图数据库, 并得到疾病名称列表的结果
        s = query_neo4j(self.text)
        print("neo4j查询服务请求成功, 返回结果:", s)
        # 判断如果结果为空列表, 再次访问百度机器人
        if not s:
            return unit_chat(self.text)

        # 将查询回来的结果存储进redis, 并且做为下一次访问的"上一条语句"previous
        self.r.hset(str(self.uid), "previous_d", str(s))
        self.r.expire(str(self.uid), ex_time)

        # 将列表转换为字符串, 添加进规则对话模板中返回给用户
        res = ",".join(s)
        # 此处打印信息, 说明neo4j查询后有结果并且非空, 接下来将使用规则模板进行对话生成
        print("使用规则对话生成模板进行返回对话的生成!")
        return self.reply["2"] %res


# 设定主要逻辑服务的路由和请求方法
@app.route('/v1/main_serve/', methods=["POST"])
def main_serve():
    print("已经进入主要逻辑服务, werobot服务正常运行!")
    # 接收来自werobot服务的相关字段, uid: 用户唯一标识, text: 用户输入的文本信息
    uid = request.form['uid']
    text = request.form['text']
    # 从redis连接池中获得一个活跃的连接
    r = redis.StrictRedis(connection_pool=pool)
    # 获取该用户上一次说的话(注意: 可能为空)
    previous = r.hget(str(uid), "previous")
    # 将当前输入的text存入redis, 作为下一次访问时候的"上一句话"
    r.hset(str(uid), "previous", text)
    print("已经完成了初次会话管理, redis运行正常!")
    # 将规则对话模板的文件Load进内存
    reply = json.load(open(reply_path, "r"))
    print('*****')
    print('Hello Doctor.')
    print('*****')
    # 实例化Handler类
    handler = Handler(uid, text, r, reply)
    if previous:
        return handler.non_first_sentence(previous)
    else:
        return handler.first_sentence()


# if __name__ == '__main__':
#     text = "电脑找不到光驱怎么办"
#     result = query_neo4j(text)
#     print("疾病列表:", result)