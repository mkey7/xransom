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
        "domain": "http://"+i["locations"][-1]["fqdn"],
        "net_type": "tor",
        "user_name": i["name"],
        "user_description": str(i["profile"]),
        "user_id": calculate_sha1(i["name"]),
        "url": i["locations"][-1]["fqdn"],
        "user_nickname": str([]),
        "identity_tags": str(['勒索组织']),
        "register_time": "2000-01-01 00:00:00",
        "last_active_time": "2000-01-01 00:00:00",
        "goods_orders": -1,
        "level": str([]),
        "member_degree": str([]),
        "ratings": str([]),
        "user_img": str({}),
        "topic_nums": 1,
        "post_counts": 0,
        "area": str([]),
        "user_verification": str([]),
        "user_order_count": -1,
        "user_viewed_count": -1,
        "user_feedback_count": -1,
        "user_followed_count": -1,
        "emails": str([]),
        "bitcoin_addresses": str([]),
        "eth_addresses": str([]),
        "crawl_time": timestamp,
        "user_hazard_level": str([]),
        "topic_counts": "",
        "user_related_url_and_address": str([]),
        "user_related_images": str([]),
        "user_related_files": str([]),
        "user_recent_day": -1,
        "user_related_crawl_tags": str(['勒索软件']),
        "lang": "en_us",
    }
    users.append(user)

    for l in i["locations"]:
        site = {
            "domain": "http://" + l["fqdn"],
            "platform": i["name"],
            "url": l["slug"],
            "content_encode": "utf-8",
            "title": l["title"] if l["title"] else "",
            "site_name": i["name"],
            "index_url": l["slug"],
            "description": str(i["profile"]),
            # "uuid": calculate_sha1(l["fqdn"]+i["name"]),
            "net_type": "tor",
            "lang": "en_us",
            # "snapshot": str({}),
            "name": "",
            "path": "",
            "image_hash": "",
            "last_status": "online" if l["enabled"] else "offline",
            "first_publish_time": l["lastscrape"],
            "last_publish_time": l["lastscrape"],
            "service_type": "勒索软件",
            "is_recent_online": "online" if l["enabled"] else "offline",
            "scale": str({}),
            "active_level": str([]),
            "label": str(['勒索软件']),
            "site_hazard": str([]),
            "goods_label": str(['data']),
            "goods_count": -1,
            "pay_methods": str([]),
            "goods_user_count": -1,
            "user_info": str({}),
        }
        sites.append(site)

with open("sites.json", "w", encoding='utf-8') as jsonfile:
    json.dump(sites, jsonfile, indent=4, ensure_ascii=False)
# with open("users.json", "w", encoding='utf-8') as jsonfile:
#     json.dump(users, jsonfile, indent=4, ensure_ascii=False)

if not os.path.exists("pages.json"):
    pages = []
    with open("pages.json", "w", encoding='utf-8') as jsonfile:
        json.dump(pages, jsonfile, indent=4, ensure_ascii=False)

if not os.path.exists("posts.json"):
    posts = []
    with open("posts.json", "w", encoding='utf-8') as jsonfile:
        json.dump(posts, jsonfile, indent=4, ensure_ascii=False)
