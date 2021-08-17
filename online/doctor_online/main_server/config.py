# 设置redis相关的配置信息
REDIS_CONFIG = {
	"host": "www.booksell.cn",
	"port": 6380
}

# 设置neo4j图数据库的配置信息
NEO4J_CONFIG = {
	"uri": "bolt://www.booksell.cn:7688",
	"auth": ("neo4j", "yunda618"),
	"encrypted": False
}

# 设置句子相关服务的请求地址
model_serve_url = "http://0.0.0.0:5002/v1/recognition/"

# 设置服务的超时时间
TIMEOUT = 2

# 设置规则对话的模板加载路径
reply_path = "./reply.json"

# 用户对话信息保存的过期时间
ex_time = 36000

