import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv


class minioClient:
    def __init__(self) -> None:
        load_dotenv()
        self.minio_ip = os.getenv('MINIO_IP')
        self.minio_access_key = os.getenv('MINIO_ACCESS_KEY')
        self.minio_secret_key = os.getenv('MINIO_SECRET_KEY')

    # 配置MinIO客户端
    def minio_client_setup(self):
        self.minio = Minio(self.minio_ip, access_key=self.minio_access_key, secret_key=self.minio_secret_key, secure=False)

    def push_minio(self, file_path, file_size, object_name, bucket_name):
        with open(file_path, "rb") as file_data:
            self.minio.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_data,
                length=file_size,
                content_type="image/png",
            )
        print(f"File {file_path} has been successfully uploaded to {object_name}.")

    # 上传文件到MinIO
    def upload_to_minio(self, file_path, object_name, bucket_name, retry=True):
        try:
            file_size = os.path.getsize(file_path)
        except FileNotFoundError:
            print(f"Minio file {file_path} not exist")
            return

        try:
            self.push_minio(file_path, file_size, object_name, bucket_name)
        except S3Error as e:
            print("Minio Error occurred: ", e)

            # 如果是因为bucket不存在，则创建bucket
            if e.code == 'NoSuchBucket':
                print(f"创建bucket：{bucket_name}")
                self.minio.make_bucket(bucket_name)

            # 断开重连
            self.minio_client_setup()
            if retry:
                self.push_minio(file_path, object_name, bucket_name, False)


# 主函数
def main():
    # 设置MinIO客户端
    minio_client = minioClient()
    minio_client.minio_client_setup()
    file_path = "screenshots/ffe99e11718877b3526260d6dd8629f44d23fc09.png"
    object_name = "xransom/ffe99e11718877b3526260d6dd8629f44d23fc09.png"
    bucket_name = "xransoms"

    # 上传截图到MinIO
    minio_client.upload_to_minio(minio_client, file_path, object_name, bucket_name)


if __name__ == "__main__":
    main()
