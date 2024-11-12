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
        """
        创建mq连接
        """
        credentials = pika.PlainCredentials(self.mq_username, self.mq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.mq_ip, self.mq_port, '/', credentials))
        self.channel = connection.channel()

    def mqSend(self, data, routing_key):
        # 将 JSON 数据转换为字符串
        message = json.dumps(data)

        try:
            # 检查队列是否存在
            if not self.channel.queue_declare(queue=routing_key, durable=True).method.queue:
                print(f"Queue '{routing_key}' does not exist. Creating it.")
                # 创建队列，durable=True 表示队列将在 broker 重启后依然存在
                self.channel.exchange_declare(exchange="scrapy", exchange_type="direct", durable=True)
                self.channel.queue_declare(queue=routing_key, durable=True)
                self.channel.queue_bind(exchange="scrapy",queue=routing_key, routing_key=routing_key)

            # 发布消息到队列
            self.channel.basic_publish(exchange='scrapy',
                                       routing_key=routing_key,
                                       body=message)
        except Exception as e:
            print("mq通道关闭" + str(e))
            self.mqinit()
            self.channel.basic_publish(exchange='', routing_key=routing_key, body=message)

