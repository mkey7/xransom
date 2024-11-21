import json
import os
import hashlib
import time


def calculate_sha1(data):
    # 创建一个新的sha1 hash对象
    hash_object = hashlib.sha1()
    # 提供需要散列的数据
    hash_object.update(data.encode())
    # 获取十六进制格式的散列值
    return hash_object.hexdigest()


timestamp = str(int(time.time()))

users = []
sites = []
data = []
with open("groups.json", encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

for i in data:
    user = {
        "platform": i["name"],
        "uuid": calculate_sha1(i["name"]),
        "domain": i["locations"][-1]["fqdn"],
        "net_type": "tor",
        "user_name": i["name"],
        "user_description": str(i["profile"]),
        "user_id": calculate_sha1(i["name"]),
        "url": i["locations"][-1]["fqdn"],
        "user_nickname": "",
        "identity_tags": "勒索组织",
        "register_time": "",
        "last_active_time": "",
        "goods_orders": 0,
        "level": "1",
        "member_degree": "",
        "ratings": "",
        "user_img": "",
        "topic_nums": 0,
        "post_counts": 0,
        "area": "[]",
        "user_verification": "[]",
        "user_order_count": -1,
        "user_viewed_count": -1,
        "user_feedback_count": -1,
        "user_followed_count": -1,
        "emails": "",
        "bitcoin_addresses": "",
        "eth_addresses": "",
        "crawl_time": timestamp,
        "user_hazard_level": "3",
        "topic_counts": "",
        "user_related_url_and_address": [],
        "user_related_images": [],
        "user_related_files": [],
        "user_recent_day": 0,
        "user_related_crawl_tags": ["勒索"],
    }
    users.append(user)

    for l in i["locations"]:
        site = {
            "site_name": i["name"],
            "uuid": calculate_sha1(l["fqdn"]+i["name"]),
            "domain": l["fqdn"],
            "net_type": "tor",
            "url": l["slug"],
            "index_url": l["slug"],
            "title": l["title"],
            "description": i["profile"],
            "lang": "en",
            "snapshot": {
                    "name": "",
                    "path": "",
                    "image_id": "",
            },
            "name": "",
            "path": "",
            "image_hash": "",
            "last_status": l["enabled"],
            "first_publish_time": l["lastscrape"],
            "last_publish_time": l["lastscrape"],
            "service_type": "勒索",
            "is_recent_online": l["enabled"],
            "scale": {},
            "active_level": [],
            "label": {
                    "type": "勒索",
                    "name": i["name"]
            },
            "site_hazard": [],
            "goods_label": "data",
            "goods_count": -1,
            "pay_methods": "",
            "goods_user_count": 0,
            "user_info": {},
            "created_at": l["lastscrape"],
            "update_at": l["lastscrape"],
        }
        sites.append(site)

with open("sites.json", "w", encoding='utf-8') as jsonfile:
    json.dump(sites, jsonfile, indent=4, ensure_ascii=False)
with open("users.json", "w", encoding='utf-8') as jsonfile:
    json.dump(users, jsonfile, indent=4, ensure_ascii=False)

if not os.path.exists("pages.json"):
    pages = []
    with open("pages.json", "w", encoding='utf-8') as jsonfile:
        json.dump(pages, jsonfile, indent=4, ensure_ascii=False)

if not os.path.exists("posts.json"):
    posts = []
    with open("posts.json", "w", encoding='utf-8') as jsonfile:
        json.dump(posts, jsonfile, indent=4, ensure_ascii=False)
