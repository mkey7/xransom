import os
from minio import Minio
from minio.error import S3Error


# 配置MinIO客户端
def minio_client_setup(endpoint="192.168.3.111:9000",
                       access_key="Ww0kDlABN5CUWMrl7sOD",
                       secret_key="wKCYTDsLDvGscTJBUX7azeMO9nbhE3RhfzeEjFoY"):
    return Minio(endpoint, access_key=access_key, secret_key=secret_key,
                 secure=False)


# 上传文件到MinIO
def upload_to_minio(minio_client, file_path, object_name, bucket_name):
    try:
        file_size = os.path.getsize(file_path)

        with open(file_path, "rb") as file_data:
            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_data,
                length=file_size,
                content_type="image/png",
            )
        print(f"File {file_path} has been successfully uploaded to {object_name}.")
    except S3Error as exc:
        print("Error occurred: ", exc)


# 主函数
def main():
    # 设置MinIO客户端
    minio_client = minio_client_setup()
    file_path = "screenshots/ffe99e11718877b3526260d6dd8629f44d23fc09.png"
    object_name = "xransom/ffe99e11718877b3526260d6dd8629f44d23fc09.png"
    bucket_name = "xransoms"

    # 上传截图到MinIO
    upload_to_minio(minio_client, file_path, object_name, bucket_name)


if __name__ == "__main__":
    main()
