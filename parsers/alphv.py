import requests
import datetime


# Assuming Tor is running on default port 9050.
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

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

def convert_date(timestamp):
    # Convert the timestamp to a datetime object
    date_object = datetime.datetime.fromtimestamp(timestamp /  1000)
    # Format the date as per your desired output format, including microseconds
    formatted_date = date_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date

def main(scrapy,page,site):
    onion_url= 'http://alphvuzxyxv6ylumd2ngp46xzq3pw6zflomrghvxeuks6kklberrbmyd.onion/api/blog/brief/0/10'
    try:
        json_data = fetch_json_from_onion_url(onion_url)
    except:
        json_data = None
    if json_data is not None:
        for item in json_data['items']:
            id = item['id']
            desc_url = 'http://alphvuzxyxv6ylumd2ngp46xzq3pw6zflomrghvxeuks6kklberrbmyd.onion/api/blog/' + id
            json_data_item = fetch_json_from_onion_url(desc_url)
            if json_data_item is not None:
                    created_dt = json_data_item.get('createdDt')
                    title = json_data_item.get('title').strip()
                    try: # Extract the required fields
                        url = json_data_item.get('publication', {}).get('url')
                    except:
                        url = ''
                    try:
                        description = json_data_item.get('publication', {}).get('description')
                    except:
                        description = ''
                    """
                    +------------------------------+------------------+----------+
                    | Description | Published Date | Victim's Website | Post URL |
                    +------------------------------+------------------+----------+
                    |      X      |      X         |                 |     x    |
                    +------------------------------+------------------+----------+
                    Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
                    """
                    scrapy.appender(title.rstrip('.'), 'alphv', description.replace('\n',' '),url,convert_date(created_dt)+'.123456','http://alphvuzxyxv6ylumd2ngp46xzq3pw6zflomrghvxeuks6kklberrbmyd.onion/' + id)
