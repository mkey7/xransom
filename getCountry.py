import pycountry
import re
import whois
import tldextract

# 国家名称
countries = {
    country.name: {'alpha_2': country.alpha_2, 'alpha_3': country.alpha_3}
    for country in pycountry.countries
}

# 常见停用词列表
stopwords = {"is", "it", "It", "at", "in", "on", "an", "as", "us"}


def country_code_to_name(country_code):
    """
    将国家缩写（Alpha-2 或 Alpha-3）转换为国家名称
    :param country_code: ISO 国家缩写（如 'CN', 'USA'）
    :return: 国家全称（如 'China', 'United States'），若无匹配则返回 'Unknown'
    """
    try:
        # 尝试通过 Alpha-2 查找
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if not country:
            # 如果 Alpha-2 没找到，尝试通过 Alpha-3 查找
            country = pycountry.countries.get(alpha_3=country_code.upper())
        return country.name if country else ""
    except Exception as e:
        print(f"Error converting country code: {country_code}, {e}")
        return "Error"


def get_domain_country(website: str):
    """
    查询域名的 WHOIS 信息并提取注册国家
    """
    try:
        # 对url进行解析获取域名
        extracted = tldextract.extract(website)
        domain = f"{extracted.domain}.{extracted.suffix}"
        # 查询域名的 WHOIS 信息
        domain_info = whois.query(domain)

        # 提取注册国家信息
        if hasattr(domain_info, 'registrant_country') and domain_info.registrant_country:
            return country_code_to_name(domain_info.registrant_country)
        elif hasattr(domain_info, 'country') and domain_info.country:
            return country_code_to_name(domain_info.country)
        else:
            return ""
    except Exception as e:
        print(f"Error querying WHOIS for {domain}: {e}")
        return "Error"


def text2word(content):
    words = re.findall(r'\b\w+\b', content)
    return words


def text2country(text):
    # NOTE 识别正文中的国家全称
    for country_name, codes in countries.items():
        if country_name.lower() in text.lower():
            return country_name
    return ""


def words2country(text):
    # NOTE 识别单词中的国家后缀
    words = text2word(text)

    for word in words:
        if word in stopwords:
            continue
        for country_name, codes in countries.items():
            if word.upper() == codes['alpha_2'] or word.upper() == codes['alpha_3']:
                return country_name

    return ""


def main(content, website, title, country):
    """
    解析各个post的国家
    """
    # 域名识别
    if not country and website:
        country = words2country(website)
    # 域名whois识别
    if not country and website:
        country = get_domain_country(website)
    # 标题识别简称
    if not country and website:
        country = words2country(title)
    # 正文识别全称
    if not country and website:
        country = text2country(content)
    # 正文识别简称
    if not country and website:
        country = words2country(content)
    return country


if __name__ == "__main__":
    website = "https://kimi.moonshot.cn/"
    print(words2country(website))
    text = "Hello IT, world! This is a test text with some words.cn"
    print(text2country(text))
    print(words2country(text))
    website2 = "live.bilibili.com"
    print(get_domain_country(website))
