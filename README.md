﻿# Doctor Robot 

这是一个用于解决用户医疗问题的对话机器人。

生活中身体时常会出现各种各样的问题，肚子疼，头痛等问题都十分常见，但许多用户都不知道如何解决生活中的各种突发问题，基于此我提出了常见身体病症信息智能问答系统。以微信小程序为接口，让用户与常见身体病症信息智能问答系统描述身体上的的问题，系统将给予用户一份问题原因以及具体解决方案。

我首先利用爬虫获取网络上的有关身体的各种病症以及解决方案，其次利用实体审核模型RNN对其审核，之后存入到我建立的Neo4j图数据库中，将身体病症与病情连接起来，最后通过微信小程序获取用户输入问题，之后回答用户一份身体病情的问题以及解决方案。

用户可以输入身体具体表现的症状来获取相关的医疗建议。



# 使用方式

以下模拟了数条目标客户可能会通过微信公众号发送的语句，测试其对不同语句的反应过程。

如下图所示：
![用户界面演示](https://github.com/ANJHHDJN/final/blob/master/img/4.gif)

## 服务器未处于运行状态

如下图所示，当服务器未处于运行状态时，对于用户发送的任何语句，都将回答如下默认语句。
![对话情景一](https://github.com/ANJHHDJN/final/blob/master/img/1.jpg)

## 短暂对话

如下图所示，该场景包含日常寒暄，数据库包含症状描述所对应额治疗方案，数据库不包含症状所描述的治疗方案：

对于客户所说的第一句话：你好。此时并未检测到有任何关于身体病症的关键词，所以此时会调用百度unit对话，随机选取一个语句进行自动回复。

对于客户所说的第二句话：我肚子有点不舒服。此时客户的本意是想得到公众号的进一步询问，但是“肚子不舒服”这句话依然没有包含我数据库所储存的关键词，所以我的公众号依然调用的是百度unit进行回复。并且，unit服务对于肚子不舒服恰好有一个符合语境的回答。

然后我在第三句话补充道：还有点头晕。此时，“头晕”属于我的关键词之一，此时就调用了数据库中关于头晕这个症状的相关问题，并且给与客户可能的症状。

但是，我的第四句话：心律失常怎么治疗呢。用户本意想要得到治疗方案，但是由于我的图数据库数据量不足，并没有“心律失常”的治疗方案，所以对于这句话又进行了一次症状的判断。因此，这也暴露出了我数据库数据不够充分的缺点。

同样的，对于第五句话，我又提出了一个问题：微囊肿腺癌。也没有相关数据进行回复，此时就回复固定语句：你这个问题难倒我了。
![对话情景二](https://github.com/ANJHHDJN/final/blob/master/img/2.jpg)

## 持续对话

 对于同一个用户，公众号会将其发送的语句存入redis数据库10小时。因此10小时内，客户所说的任何一条语句都会同客户所说的上一条语句判断联系。如下图所示，当我第一次描述：“我头晕”这个症状时，公众号会向我询问具体症状，但是如果我在10小时以内，再次描述相同或者相似的信息，这个时候公众号会统计这条信息并且进行再判断，如果没有接收到更多的关键词，就会要求客户发送更多的描述信息。
![对话情景三](https://github.com/ANJHHDJN/final/blob/master/img/3.jpg)

# 调用的API

为了更好地实现项目的功能，调用了百度Unit对话这个API。

Unit是百度提供的一个智能对话接口，它能够加入技能并智能与用户对话，在本项目中unit对话主要用于与用户闲聊，当智能对话答不出用户所提问题时采用。使得智能对话更加的人性化。





```