import requests
import time
import uuid
import random
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from faker import Faker
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter, Retry

class LinkedInScraper:
    def __init__(self):
        self.fake = Faker()

    def generate_linkedin_cookies(self):
        try:
            current_timestamp = int(time.time())
            expiration_timestamp = current_timestamp + 86400  # 24 hours from now

            bcookie_uuid = str(uuid.uuid4())

            cookies = {
                'lang': 'v=2&lang=en-us',
                'bcookie': f'"v=2&{bcookie_uuid}"',
                'lidc': f'"b=OGST03=O=O=O=O={current_timestamp}=1=1={current_timestamp}={expiration_timestamp}=2=AQEXPsIrcDzjOrXtw5i1IQ9wJaAXYJ30"',
                'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
                'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': f'-{current_timestamp}%7CMCIDTS%7C19894%7CMCMID%7C{uuid.uuid4()}%7CMCAAMLH-{current_timestamp}%7C12%7CMCAAMB-{current_timestamp}%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-{expiration_timestamp}s%7CNONE%7CvVersion%7C5.1.1',
                'aam_uuid': str(uuid.uuid4()),
            }
            return cookies
        except Exception as e:
            print(f"Error generating LinkedIn cookies: {e}")
            return {}

    def get_random_user_agent(self):
        try:
            return self.fake.user_agent()
        except Exception as e:
            print(f"Error generating random user agent: {e}")
            return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        
    def random_referer(self):
        referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.yahoo.com/',
        ]
        return random.choice(referers)

    def random_sec_ch_ua(self):
        sec_ch_ua = [
            '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            '"Not/A)Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            '"Not/A)Brand";v="90", "Chromium";v="90", "Google Chrome";v="90"',
        ]
        return random.choice(sec_ch_ua)

    def random_accept_language(self):
        accept_languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.8',
            'en-CA,en;q=0.7',
        ]
        return random.choice(accept_languages)

    def get_random_headers(self, domain):
        try:
            headers = {
                'host': domain.replace('https://www.','').replace('/',''),
                'sec-ch-ua': self.random_sec_ch_ua(),
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': random.choice(['"Windows"', '"macOS"', '"Linux"']),
                'upgrade-insecure-requests': '1',
                'dnt': '1',
                'user-agent': self.get_random_user_agent(),
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': self.random_referer(),
                'accept-language': self.random_accept_language(),
                'priority': 'u=0, i',
            }
            return headers
        except Exception as e:
            print(f"Error generating random headers: {e}")
            return {}

    def search_linkedin_company(self, url):
        cookies = self.generate_linkedin_cookies()
        headers = self.get_random_headers(urlparse(url).hostname)
        
        session = requests.Session()
        retries = Retry(total=50, backoff_factor=0.1, status_forcelist=[402, 403, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        session.cookies.update(cookies)
        
        try:
            response = session.get(url, headers=headers, verify=False)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching LinkedIn page: {e}")
            return None

    def parse_company_info(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            company_profile = {}

            try:
                company_profile['name'] = soup.title.string.split('|')[0].strip()
            except Exception as e:
                company_profile['name'] = None
                print(f"Error extracting name: {e}")
                
            company_profile['profile_link'] = url

            try:
                followers_tag = soup.find('h3', class_='top-card-layout__first-subline')
                if followers_tag:
                    followers_text = followers_tag.text.strip()
                    followers_split = [part for part in followers_text.split() if part.replace(',', '').isdigit()]
                    company_profile['followers'] = int(followers_split[0].replace(',', '')) if followers_split else None
            except Exception as e:
                company_profile['followers'] = None
                print(f"Error extracting followers: {e}")

            try:
                industry_tag = soup.find('h2', class_='top-card-layout__headline')
                company_profile['industry'] = industry_tag.text.strip() if industry_tag else None
            except Exception as e:
                company_profile['industry'] = None
                print(f"Error extracting industry: {e}")

            try:
                location_tag = soup.find('h3', class_='top-card-layout__first-subline')
                location_text = location_tag.text.strip() if location_tag else None
                company_profile['location'] = location_text.split('<span')[0].strip() if location_text else None
            except Exception as e:
                company_profile['location'] = None
                print(f"Error extracting location: {e}")

            try:
                website_tag = soup.find('a', {'data-tracking-control-name': 'about_website'})
                company_profile['website'] = website_tag.text.strip() if website_tag else None
            except Exception as e:
                company_profile['website'] = None
                print(f"Error extracting website: {e}")

            try:
                size_tag = soup.find('div', {'data-test-id': 'about-us__size'})
                size_dd_tag = size_tag.find('dd') if size_tag else None
                company_profile['company_size'] = size_dd_tag.text.strip() if size_dd_tag else None
            except Exception as e:
                company_profile['company_size'] = None
                print(f"Error extracting company size: {e}")

            try:
                headquarters_tag = soup.find('div', {'data-test-id': 'about-us__headquarters'})
                headquarters_dd_tag = headquarters_tag.find('dd') if headquarters_tag else None
                company_profile['headquarters'] = headquarters_dd_tag.text.strip() if headquarters_dd_tag else None
            except Exception as e:
                company_profile['headquarters'] = None
                print(f"Error extracting headquarters: {e}")

            try:
                type_tag = soup.find('div', {'data-test-id': 'about-us__organizationType'})
                type_dd_tag = type_tag.find('dd') if type_tag else None
                company_profile['type'] = type_dd_tag.text.strip() if type_dd_tag else None
            except Exception as e:
                company_profile['type'] = None
                print(f"Error extracting type: {e}")

            try:
                founded_tag = soup.find('div', {'data-test-id': 'about-us__foundedOn'})
                founded_dd_tag = founded_tag.find('dd') if founded_tag else None
                company_profile['founded'] = founded_dd_tag.text.strip() if founded_dd_tag else None
            except Exception as e:
                company_profile['founded'] = None
                print(f"Error extracting founded year: {e}")

            try:
                slogan_tag = soup.find('h4', class_='top-card-layout__second-subline')
                company_profile['slogan'] = slogan_tag.text.strip() if slogan_tag else None
            except Exception as e:
                company_profile['slogan'] = None
                print(f"Error extracting slogan: {e}")

            try:
                description_tag = soup.find('p', {'data-test-id': 'about-us__description'})
                company_profile['description'] = description_tag.text.strip() if description_tag else None
            except Exception as e:
                company_profile['description'] = None
                print(f"Error extracting description: {e}")

            try:
                logo_img = soup.find('img', {'data-tracking-control-name': 'about_us_logo'})
                company_profile['logo_url'] = logo_img['src'] if logo_img else None
            except Exception as e:
                company_profile['logo_url'] = None
                print(f"Error extracting logo URL: {e}")

            try:
                cover_img = soup.find('img', {'data-tracking-control-name': 'cover_photo'})
                company_profile['cover_image_url'] = cover_img['src'] if cover_img else None
            except Exception as e:
                company_profile['cover_image_url'] = None
                print(f"Error extracting cover image URL: {e}")

            try:
                employees_tag = soup.find('span', class_='company-employees')
                company_profile['employees'] = employees_tag.text.strip() if employees_tag else None
            except Exception as e:
                company_profile['employees'] = None
                print(f"Error extracting employees count: {e}")

            try:
                updates_tag = soup.find_all('div', class_='feed-item')
                company_profile['latest_updates'] = [update.text.strip() for update in updates_tag] if updates_tag else None
            except Exception as e:
                company_profile['latest_updates'] = None
                print(f"Error extracting latest updates: {e}")

            return company_profile
        except Exception as e:
            print(f"Error parsing company profile: {e}")
            return {}

# Example usage:
scraper = LinkedInScraper()
url = "https://www.linkedin.com/company/iamneoai?originalSubdomain=in"
html_content = scraper.search_linkedin_company(url)
if html_content:
    company_info = scraper.parse_company_info(html_content)
    print(json.dumps(company_info, indent=4))
else:
    print("Failed to retrieve company information.")
