import pika
import json
import os
from dotenv import load_dotenv


# 连接到 RabbitMQ 服务器
class mqClient:
    def __init__(self) -> None:
        load_dotenv()
        self.mq_ip = os.getenv('MQ_IP')
        self.mq_port = int(os.getenv('MQ_PORT'))
        self.mq_username = os.getenv('MQ_USERNAME')
        self.mq_password = os.getenv('MQ_PASSWORD')

        self.mqinit()

    def mqinit(self):
        credentials = pika.PlainCredentials(self.mq_username, self.mq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.mq_ip, self.mq_port, '/', credentials))
        self.channel = connection.channel()


    def mqSend(self, data, routing_key):
        # 将 JSON 数据转换为字符串
        message = json.dumps(data)

        try:
            # 发布消息到队列
            self.channel.basic_publish(exchange='',
                                  routing_key=routing_key,
                                  body=message)
        except Exception as e:
            print("mq通道关闭" + str(e))
            self.mqinit()
            self.channel.basic_publish(exchange='', routing_key=routing_key, body=message)

