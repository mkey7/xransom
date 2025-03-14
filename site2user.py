import json
from group2site import calculate_sha1
from datetime import datetime


def s2user(site):
    current_datetime = datetime.now()
    current_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    user = {
        "platform": site["name"],
        "uuid": calculate_sha1(site["name"]),
        "domain": site["domain"],
        "net_type": "tor",
        "user_name": site["name"],
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
