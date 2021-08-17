import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer

# bert预训练模型编码函数
model = BertModel.from_pretrained('./bert-base-chinese')
tokenizer = BertTokenizer.from_pretrained('./bert-base-chinese/')

def get_bert_encode_for_single(text):
    # 首先使用字符映射器对每个汉子进行映射
    # bert中的tokenizer映射后会加入开始和结束的标记, 101, 102, 这两个标记对我们不需要，采用切片的方式去除
    indexed_tokens = tokenizer.encode(text)[1:-1]

    # 封装成tensor张量
    tokens_tensor = torch.tensor([indexed_tokens])
    print(tokens_tensor)

    # 预测部分需要使得模型不自动求导
    with torch.no_grad():
        encoded_layers = model(tokens_tensor)

    print(encoded_layers.last_hidden_state.shape)
    encoded_layers = encoded_layers.last_hidden_state
    # print('encoded_layers_shape:{}'.format(encoded_layers.shape))
    # 模型的输出都是三维张量,第一维是1,使用[0]来进行降维,只提取我们需要的后两个维度的张量
    # print(encoded_layers)
    encoded_layers = encoded_layers[0]
    return encoded_layers


if __name__ == '__main__':
    text = "你好,周杰伦吗"
    outputs = get_bert_encode_for_single(text)
    print(outputs)
    # print(outputs.shape)

