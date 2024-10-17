import pika
import json


# 连接到 RabbitMQ 服务器
def mqinit(ip="192.168.3.111", username="spider", password="spider", port=5672):
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials))
    channel = connection.channel()
    return channel


def mqSend(channel, data, routing_key):
    # 将 JSON 数据转换为字符串
    message = json.dumps(data)

    # 发布消息到队列
    channel.basic_publish(exchange='scrapy',
                          routing_key=routing_key,
                          body=message)
