import pycountry
import re


# 国家名称
countries = {
    country.name: {'alpha_2': country.alpha_2, 'alpha_3': country.alpha_3}
    for country in pycountry.countries
}

# 常见停用词列表
stopwords = {"is", "it", "It", "at", "in", "on", "an", "as", "us"}


def main(content, website, title, country):
    """
    解析各个post的国家
    """
    # 域名识别
    if not country and website:
        country = words2country(website)
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

if __name__ == "__main__":
    website = "https://kimi.moonshot.cn/"
    print(words2country(website))
    text = "Hello IT, world! This is a test text with some words.cn"
    print(text2country(text))
    print(words2country(text))
