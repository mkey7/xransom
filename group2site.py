import json
import os
import hashlib

def calculate_sha1(data):
    # 创建一个新的sha1 hash对象
    hash_object = hashlib.sha1()
    # 提供需要散列的数据
    hash_object.update(data.encode())
    # 获取十六进制格式的散列值
    return hash_object.hexdigest()

users = []
sites = []
data = []
with open("groups.json", encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

for i in data:
    user = {
            "platform" : i["name"],
            "uuid" : calculate_sha1(i["name"]),
            "domain" : i["locations"][-1]["fqdn"],
            "net_type" : "tor",
            "user_name" : i["name"],
            "user_description" : str(i["profile"]),
            "user_id" : calculate_sha1(i["name"]),
            "url" : i["locations"][-1]["fqdn"],
            "user_nickname" : "",
            "identity_tags" : "勒索组织",
            "register_time" : "",
            "last_active_time" : "",
            "goods_orders" : 0,
            "level" : "1",
            "member_degree" : "",
            "ratings" : "",
            "user_img" : "",
            "topic_nums" : 0,
            "area" : "",
            "user_verification" : "",
            "user_order_count" : 0,
            "user_viewed_count" : 0,
            "user_feedback_count" : 0,
            "user_followed_count" : 0,
            "emails" : "",
            "bitcoin_addresses" : "",
            "eth_addresses" : "",
            "crawl_time" : "",
            "user_hazard_level" : "3",
            "topic_counts" : "",
            "user_related_url_and_address" : "",
            "user_related_images" : "",
            "user_related_files" : "",
            "user_recent_day" : 0,
            "user_related_crawl_tags" : "",
    }
    users.append(user)
    
    for l in i["locations"]:
        site = {
                "uuid" : calculate_sha1(l["fqdn"]+i["name"]),
                "domain" : l["fqdn"],
                "net_type" : "tor",
                "url" : l["slug"],
                "title" : l["title"],
                "description" : str(i["profile"]),
                "lang" : "en",
                "snapshot" : {
                    "name" : "",
                    "path" : "",
                    "image_id" : "",
                },
                "last_status" : l["enabled"],
                "first_publish_time" : l["lastscrape"],
                "last_publish_time" : l["lastscrape"],
                "service_type" : "勒索",
                "is_recent_online" : l["enabled"],
                "scale" : 5,
                "active_level" : 5,
                "label" : {
                    "type" : "勒索",
                    "name" : i["name"]
                },
                "site_hazard" : "高危",
                "goods_label" : "data",
                "goods_count" : 0,
                "pay_methods" : "",
                "goods_user_count" : 0,
        }
        sites.append(site)

with open("sites.json","w", encoding='utf-8') as jsonfile:
    json.dump(sites, jsonfile, indent=4, ensure_ascii=False)
with open("users.json","w", encoding='utf-8') as jsonfile:
    json.dump(users, jsonfile, indent=4, ensure_ascii=False)
    
if not os.path.exists("pages.json"):
    pages = []
    with open("pages.json","w", encoding='utf-8') as jsonfile:
        json.dump(pages, jsonfile, indent=4, ensure_ascii=False)

if not os.path.exists("posts.json"):
    posts = []
    with open("posts.json","w", encoding='utf-8') as jsonfile:
        json.dump(posts, jsonfile, indent=4, ensure_ascii=False)