import json
import random
import requests

# client_id 为官网获取的api_key， client_secret 为官网获取的secret_key
client_id = "GfCLA0uU01Bid4APRuM581pj"
client_secret = "F3bgl64qbW95eZmbGwMjmiHihfrXm9Xj"


def unit_chat(chat_input, user_id="88888"):
    """
    description:调用百度UNIT接口，回复聊天内容
    Parameters
      ----------
      chat_input : str
          用户发送天内容
      user_id : str
          发起聊天用户ID，可任意定义
    Return
      ----------
      返回unit回复内容
    """
    # 设置默认回复内容,  一旦接口出现异常, 回复该内容
    chat_reply = "不好意思，我正在学习中，随后回复你。"

    # 两个url，第一个获取access_token, 第二个获取百度unit_api
    # 根据 client_id 与 client_secret 获取access_token(获取访问token)
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (
    client_id, client_secret)
    res = requests.get(url)
    access_token = eval(res.text)["access_token"]
    # 根据 access_token 获取聊天机器人接口数据
    unit_chatbot_url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + access_token

    # 拼装聊天接口对应请求发送数据，主要是填充 query 值，构建访问数据
    post_data = {
                "log_id": str(random.random()),
                "request": {
                    "query": chat_input,# 聊天语句
                    "user_id": user_id # 用户id
                },
                "session_id": "",
                "service_id": "S53779",# 医生id
                "version": "2.0"
            }
    # 将封装好的数据作为请求内容, 发送给Unit聊天机器人接口, 并得到返回结果
    res = requests.post(url=unit_chatbot_url, json=post_data)


    # 获取聊天接口返回数据 res.content为返回信息
    unit_chat_obj = json.loads(res.content)

    print(unit_chat_obj)
    # 打印返回的结果
    # 判断聊天接口返回数据是否出错 error_code == 0 则表示请求正确
    if unit_chat_obj["error_code"] != 0:
        return chat_reply

    # 解析聊天接口返回数据，找到返回文本内容 result -> response_list -> schema -> intent_confidence(>0) -> action_list -> say
    unit_chat_obj_result = unit_chat_obj["result"]
    unit_chat_response_list = unit_chat_obj_result["response_list"] # 同时返回若干句

    # 随机选取一个"意图置信度"[+response_list[].schema.intent_confidence]不为0的技能作为回答
    # 选取一个意图置信度大于0的拿出来，之后在整体列表里随机选一个
    print(unit_chat_response_list)
    unit_chat_response_obj = random.choice(
       [unit_chat_response for unit_chat_response in unit_chat_response_list
        if unit_chat_response["schema"]["intent_confidence"] > 0.0])

    # 行动列表
    unit_chat_response_action_list = unit_chat_response_obj["action_list"]
    unit_chat_response_action_obj = random.choice(unit_chat_response_action_list)
    unit_chat_response_say = unit_chat_response_action_obj["say"]
    return unit_chat_response_say


if __name__ == '__main__':
    while True:
        chat_input = input("请输入:")
        print(chat_input)
        chat_reply = unit_chat(chat_input)
        print("用户输入 >>>", chat_input)
        print("Unit回复 >>>", chat_reply)
        if chat_input == 'Q' or chat_input == 'q':
            break
