import pika
import argparse


def setup_rabbitmq(array_content, host, username='spider', password='spider', port=5672, virtual_host='/'):
    # 设置连接参数
    credentials = pika.PlainCredentials(username, password)  # 用户名和密码
    connection_params = pika.ConnectionParameters(
        host=host,  # RabbitMQ 主机地址
        port=port,  # RabbitMQ 端口号
        virtual_host=virtual_host,  # 虚拟主机
        credentials=credentials  # 连接凭证
    )

    # 创建连接和通道
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # 声明交换机
    exchange_name = 'scrapy'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

    # 队列名称列表
    queues = ['goods', 'site', 'post', 'page', 'user', 'ransom']

    for queue in queues:
        # 声明队列
        channel.queue_declare(queue=queue, durable=True)
        if not array_content:  # 检查列表是否为空
            #print("列表为空，执行操作。")
            channel.queue_declare(queue=queue, durable=True)
            # 将队列绑定到交换机
            channel.queue_bind(exchange=exchange_name, queue=queue, routing_key=queue)
            print(queue, "队列创建完成")

        else:
            queue_name = f"{array_content}_{queue}"
            # 声明队列
            channel.queue_declare(queue=queue_name, durable=True)
            # 将队列绑定到交换机
            channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=queue)
            print(queue_name, "队列创建完成")

    print("交换机和队列已设置完成。")

    # 关闭连接
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup RabbitMQ with specified parameters.")

    parser.add_argument('--host', type=str, required=True, help='RabbitMQ host address')
    parser.add_argument('--username', type=str, default='spider', help='RabbitMQ username')
    parser.add_argument('--password', type=str, default='spider', help='RabbitMQ password')
    parser.add_argument('--port', type=int, default=5672, help='RabbitMQ port number')
    parser.add_argument('--virtual_host', type=str, default='/', help='RabbitMQ virtual host')

    # array_content 改为只接受单个值
    parser.add_argument('--array_content', type=str, default='', help='Single content for array')

    args = parser.parse_args()

    setup_rabbitmq(args.array_content, args.host, args.username, args.password, args.port, args.virtual_host)