import json
import random
import requests

client_id = "GfCLA0uU01Bid4APRuM581pj"
client_secret = "F3bgl64qbW95eZmbGwMjmiHihfrXm9Xj"

def unit_chat(chat_input, user_id="8888"):
    chat_reply = "不好意思，俺们正在学习中，随后回复你。"
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
    res = requests.get(url)
    access_token = eval(res.text)["access_token"]
    unit_chatbot_url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + access_token
    post_data = {
                "log_id": str(random.random()),
                "request": {
                    "query": chat_input,
                    "user_id": user_id
                },
                "session_id": "",
                "service_id": "S53779",
                "version": "2.0"
            }
    res = requests.post(url=unit_chatbot_url, json=post_data)

    unit_chat_obj = json.loads(res.content)
    if unit_chat_obj["error_code"] != 0: return chat_reply
    unit_chat_obj_result = unit_chat_obj["result"]
    unit_chat_response_list = unit_chat_obj_result["response_list"]
    unit_chat_response_obj = random.choice(
       [unit_chat_response for unit_chat_response in unit_chat_response_list if
        unit_chat_response["schema"]["intent_confidence"] > 0.0])
    unit_chat_response_action_list = unit_chat_response_obj["action_list"]
    unit_chat_response_action_obj = random.choice(unit_chat_response_action_list)
    unit_chat_response_say = unit_chat_response_action_obj["say"]
    return unit_chat_response_say


if __name__ == "__main__":
    while True:
        chat_input = input("请输入:")
        # print(chat_input)
        chat_reply = unit_chat(chat_input)
        print("用户输入 >>>", chat_input)
        print("Unit回复 >>>", chat_reply)
        if chat_input == 'Q' or chat_input == 'q':
            break