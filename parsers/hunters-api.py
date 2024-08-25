import requests
from datetime import datetime
import urllib3

# NOTE 这个网站目前非常复杂，需要重构
# TODO 这个网站目前非常复杂，需要重构
onion_url= 'https://hunters55rdxciehoqzwv7vgyv6nt37tbwax2reroyzxhou7my5ejyid.onion/api/public/companies'

# Disable the warning about certificate verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_country(id):
# Define the base URL of the API and the endpoint
    base_url = "https://api.ransomware.live"  # Replace with the actual API base URL
    endpoint = f"/country/{id}"  # Replace with the actual endpoint

    # Send a GET request to the API endpoint
    response = requests.get(f"{base_url}{endpoint}")

    # Check the response status code
    if response.status_code == 200:
        # The request was successful, and we can extract the country name from the JSON response
        data = response.json()
        country_name = data.get("title")
        return country_name
    elif response.status_code == 404:
        # The API returned a 404 error, which means the country was not found
        return "N/A"
    elif response.status_code == 500:
        # The API returned a 500 error, which means the country was not found
        return "N/A"
    else:
        # Handle other HTTP status codes as needed
        return "Internal Error"

# NOTE 这个函数可以获取这个网站的勒索对象，不过获取的类型为json类型，数据样例如下：
# title, 勒索金额，国家，网站
# 'id' : '8980157002', 'title': 'Toyota Brazil', 'revenue': 1700000000, 'empl oyees': 3309, 'country': 'br', 'stocks': [], 'website': 'https://www.t oyota.com.br', 'exfiltrated_data': True, 'encrypted_data': False, 'upd ated_at': 1713002964
def fetch_json_from_onion_url(onion_url):
    try:
        response = requests.get(onion_url, proxies=proxies,verify=False)
        response.raise_for_status()  # Check for any HTTP errors
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

    # Assuming the response contains JSON data, parse it
    json_data = response.json()
    return json_data

def convert_date(unix_timestamp):
    # Convert the Unix timestamp to a datetime object
    dt = datetime.fromtimestamp(unix_timestamp)
    # Format the datetime object as a string with microseconds
    formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    return formatted_datetime

def convert_text(txt):
    if txt == True:
        return "yes"
    else:
        return "no"

def main(scrapy,page,site):
    url = page["domain"]
    try:
        json_data = fetch_json_from_onion_url(onion_url)
        if json_data is not None:
            for item in json_data:
                id = item['id']
                title = item['title'].strip()
                country = get_country(item['country'])
                website = item['website']
                revenue = item['revenue']
                exfiltration = item['exfiltrated_data']
                encryption = item['encrypted_data']
                published = item['updated_at']
                description = "Country : " +  country + " - Exfiltraded data : " + convert_text(exfiltration) +  " - Encrypted data : " + convert_text(encryption)
                post_url = "https://hunters55rdxciehoqzwv7vgyv6nt37tbwax2reroyzxhou7my5ejyid.onion/companies/" + id 
                try:
                    apage = scrapy.scrape(site,post_url)
                except:
                    screenpath = ""
                    apage = None
                #print('-- ' + title + ' --> ' + post_url)
               
                """
                    def appender(post_title, group_name, description="", website="", published="", post_url=""):
                """
                scrapy.appender(title, 'hunters', description,website, convert_date(published),post_url,price=revenue,country=country,screenPath=screenpath,page=apage)
    except:
        print('hunters: ' + 'parsing fail: '+url)
        
