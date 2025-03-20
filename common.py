import json
from group2site import calculate_sha1
from datetime import datetime


def s2user(site):
    current_datetime = datetime.now()
    current_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    user = {
        "platform": site["platform"],
        "uuid": calculate_sha1(site["platform"]),
        "domain": site["domain"],
        "net_type": "tor",
        "user_name": site["platform"],
        "user_description": site["description"],
        "user_id": calculate_sha1(site["name"]),
        "url": site["url"],
        "user_nickname": str([]),
        "identity_tags": str(['勒索组织']),
        "register_time": "2000-01-01 00:00:00",
        "last_active_time": current_time,
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
        "crawl_time": current_time,
        "user_hazard_level": str([]),
        "topic_counts": "",
        "user_related_url_and_address": str([]),
        "user_related_images": str([]),
        "user_related_files": str([]),
        "user_recent_day": -1,
        "user_related_crawl_tags": str(['勒索软件']),
        "lang": "en_us",
    }

    return user

def siteUpdate(site,page,play):
    # 更新site
    site["last_publish_time"] = page["publish_time"]

    if site["first_publish_time"] == "":
        site["first_publish_time"] = page["publish_time"]

    site["last_status"] = "online"
    site["is_recent_online"] = "online"

    if site["url"] == site["domain"] or site["url"][:-1] == site["domain"] or site["url"] == site["domain"][:-1]:
        # site["snapshot"] = page["snapshot"]
        site["name"] = page["snapshot_name"]
        site["image_hash"] = page["snapshot_hash"]
        site["path"] = page["snapshot_oss_path"]

    else:
        try:
            apage = play.scrape(site, site["domain"])
            # site["snapshot"] = apage["snapshot"]
            site["name"] = apage["snapshot_name"]
            site["image_hash"] = apage["snapshot_hash"]
            site["path"] = apage["snapshot_oss_path"]
        except Exception as e:
            # site["snapshot"] = page["snapshot"]
            site["name"] = page["snapshot_name"]
            site["image_hash"] = page["snapshot_hash"]
            site["path"] = page["snapshot_oss_path"]
            
    return site

if __name__ == "__main__":
    site = {
        "domain": "http://marketojbwagqnwx.onion",
        "platform": "marketo",
        "url": "http://marketojbwagqnwx.onion",
        "content_encode": "utf-8",
        "title": "",
        "site_name": "marketo",
        "index_url": "http://marketojbwagqnwx.onion",
        "description": "['https://www.digitalshadows.com/blog-and-research/marketo-a-return-to-simple-extortion', 'https://securityaffairs.co/wordpress/121617/cyber-crime/puma-available-marketo.html', 'https://t.me/marketo_leaks', 'https://t.me/marketocloud']",
        "net_type": "tor",
        "lang": "en_us",
        "name": "",
        "path": "",
        "image_hash": "",
        "last_status": "offline",
        "first_publish_time": "2021-05-01 00:00:00.000000",
        "last_publish_time": "2021-05-01 00:00:00.000000",
        "service_type": "勒索软件",
        "is_recent_online": "offline",
        "scale": "{}",
        "active_level": "[]",
        "label": "['勒索软件']",
        "site_hazard": "[]",
        "goods_label": "['data']",
        "goods_count": -1,
        "pay_methods": "[]",
        "goods_user_count": -1,
        "user_info": "{}"
    }
    
    user = s2user(site)
    print(user)
