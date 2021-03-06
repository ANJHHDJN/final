import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer

# 使用torch.hub加载bert中文模型的字映射器
# tokenizer = torch.hub.load('huggingface/pytorch-transformers', 'tokenizer', 'bert-base-chinese')
# 使用torch.hub加载bert中文模型
# model = torch.hub.load('huggingface/pytorch-transformers', 'model', 'bert-base-chinese')


model = BertModel.from_pretr/bert-base-chiained('.nese')
tokenizer = BertTokenizer.from_pretrained('./bert-base-chinese/')

# 编写获取bert编码的函数
def get_bert_encode(text_1, text_2, mark=102, max_len=10):
    # 第一步使用tokenizer进行两个文本的字映射
    indexed_tokens = tokenizer.encode(text_1, text_2)
    # 接下来要对两个文本进行补齐, 或者截断的操作
    # 首先要找到分隔标记的位置
    k = indexed_tokens.index(mark)

    # 第二步处理第一句话, 第一句话是[:k]
    if len(indexed_tokens[:k]) >= max_len:
        # 长度大于max_len, 进行截断处理
        indexed_tokens_1 = indexed_tokens[:max_len]
    else:
        # 长度小于max_len, 需要对剩余的部分进行0填充
        indexed_tokens_1 = indexed_tokens[:k] + (max_len - len(indexed_tokens[:k])) * [0]

    # 第三步处理第二句话, 第二句话是[k:]
    if len(indexed_tokens[k:]) >= max_len:
        # 长度大于max_len, 进行截断处理
        indexed_tokens_2 = indexed_tokens[k:k+max_len]
    else:
        # 长度小于max_len, 需要对剩余的部分进行0填充
        indexed_tokens_2 = indexed_tokens[k:] + (max_len - len(indexed_tokens[k:])) * [0]

    # 接下来将处理后的indexed_tokens_1和indexed_tokens_2进行相加合并
    indexed_tokens = indexed_tokens_1 + indexed_tokens_2

    # 需要一个额外的标志列表, 来告诉模型那部分是第一句话, 哪部分是第二句话
    # 利用0元素来表示第一句话, 利用1元素来表示第二句话
    # 注意: 两句话的长度都已经被我们规范成了max_len
    segments_ids = [0] * max_len + [1] * max_len

    # 利用torch.tensor将两个列表封装成张量
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensor = torch.tensor([segments_ids])

    # 利用模型进行编码不求导
    with torch.no_grad():
        # 使用bert模型进行编码, 传入参数tokens_tensor和segments_tensor, 最终得到模型的输出encoded_layers
        encoded_layers = model(tokens_tensor, token_type_ids=segments_tensor)
    encoded_layers = encoded_layers.last_hidden_state
    encoded_layers = encoded_layers[0]
    return encoded_layers

   
text_1 = "人生该如何起头"
text_2 = "改变要如何起手"

encoded_layer = get_bert_encode(text_1, text_2)
print(encoded_layer)
print(encoded_layer.shape)
 













