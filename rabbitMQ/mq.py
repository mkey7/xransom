import pika
from rabbitMQ import common_pb2 
import hashlib
import json
import datetime

def date2time(datetime_str):
    # 将日期时间字符串转换为 datetime 对象
    datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")

    timestamp = datetime_obj.timestamp()
    return timestamp

# 天眼site站点的数据结构处理
def pack_pb(index, data, m_id):
    pb = common_pb2.OtherIndex()
    pb.index = index
    pb.data = data.encode('ascii')
    pb.mid = m_id

    res = pb.SerializeToString()
    return res

# url 的 sha256加密
def sha256_encode(code: str):
    s = hashlib.sha256()
    s.update(code.encode())
    res = s.hexdigest()
    return res


# 将groups.json的内容传换成天眼的site类型，并上传rabbitmq
def group2site(post,MQ):
    if type(post) == str:
        post = json.loads(post)
    site = {}
    site['isFirstView'] = True
    site['title'] = post['name']
    site['language'] = 'en'
    site['tag'] = '勒索软件'
    site['type'] = 'tor'
    site['priority'] = 4
    

    site['screenshot'] = None
    site['logo_path'] = None
    site['description'] = None
    for u in post['locations']:
        if not u['available']:
            continue
        site['lastSeen'] = date2time(u['lastscrape'])
        site['firstSeen'] = date2time(u['lastscrape'])
        site['url'] = u['slug'][u['slug'].find('//')+2:]
        site['urlSha256'] = sha256_encode(site['url'])
        
        MQ.send_site(json.dumps(site),site['urlSha256'])

    # 尚缺的字段
    # site['screenshot'] = True
    # site['logo_path'] = True
    
            
# 将posts.json的内容传换成天眼的page_info类型，并上传rabbitmq
def post2page(post,MQ):
    if type(post) == str:
        post = json.loads(post)
    page = common_pb2.WebPage()
    page.title = post['post_title']
    page.url = post['post_url'] if len(post['post_url']) else 'daiding'
    page.urlSha256 = sha256_encode(page.url)
    page.body = str(post)
    page.language = 'en'
    page.type = "tor"
    page.tag = 'web'
    page.date = int(date2time(post['discovered'])*1000)
    # page.site = "bianlianlbc5an4kgnay3opdemgcryg2kpfcbgczopmm3dnbz3uaunad.onion"
    
    print(page)
    MQ.send_page(page)
    


class MQ:
    def __init__(self,default_password='guest', default_username='guest', ip="localhost", p='5672'):
        credentials = pika.credentials.PlainCredentials(
            default_username, default_password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials,heartbeat=0, host=ip, port=p))
        self.client = connection.channel()
        self.topic = {}

        print("mq init successed")

        
    def producer(self, topic: str, msg: bytes):
        if topic not in self.topic.keys():
            self.client.exchange_declare(exchange=topic, exchange_type="topic", durable=True)
            self.topic[topic] = ""
        self.client.basic_publish(
            exchange=topic,
            routing_key="",
            body=msg,
            mandatory=True,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        ) 

    # 想rabbitMQ发送groups.json的信息
    def send_site(self,data,urlSha256,exchange="zeronet_other"):

        self.producer(exchange, pack_pb('deep_site_v3', data,urlSha256 ))
        
        print('push sucessed!')

    # 想rabbitMQ发送post.json的信息
    def send_page(self,data,exchange="zeronet_webpage"):
        self.producer(exchange, data.SerializeToString())
        print('push sucessed!')

