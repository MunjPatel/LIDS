import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import random
import string
import faker
import time
import uuid
import pandas as pd
import warnings

# warnings.filterwarnings(action='ignore')

fake = faker.Faker()

# Generates a random string of the specified length using letters and digits
def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Generates time-stamp corresponding to the instant of code-execution
def generate_timestamp():
    return int(time.time())

# Generates a set of random cookies with timestamps and unique identifiers for session management
def generate_cookies():
    current_timestamp = generate_timestamp()
    expiration_timestamp = current_timestamp + 86400  # 24 hours from now

    bcookie_uuid = str(uuid.uuid4())

    cookies = {
        'lang': 'v=2&lang=en-us',
        'bcookie': f'"v=2&{bcookie_uuid}"',
        'lidc': f'"b=OGST03=O=O=O=O={current_timestamp}=1=1={current_timestamp}={expiration_timestamp}=2=AQEXPsIrcDzjOrXtw5i1IQ9wJaAXYJ30"',
        'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
        'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': f'-{current_timestamp}%7CMCIDTS%7C19894%7CMCMID%7C{uuid.uuid4()}%7CMCAAMLH-{current_timestamp}%7C12%7CMCAAMB-{current_timestamp}%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-{expiration_timestamp}s%7CNONE%7CvVersion%7C5.1.1',
    }
    return cookies

# Generates a table of profiles corresponding to the provided first and last name
def generate_profile_links(first_name, last_name):
    headers = {
        'Host': 'www.linkedin.com',
        'user-agent': fake.user_agent(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'dnt': '1',
        'sec-gpc': '1',
        'referer': f'https://www.linkedin.com/pub/dir?firstName={first_name}&lastName={last_name}/',
        'upgrade-insecure-requests': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'priority': 'u=1',
    }

    params = {
        'firstName': first_name,
        'lastName': last_name,
        'trk': 'people-guest_people-search-bar_search-submit',
        'original_referer': 'https://www.linkedin.com/',
    }

    session = requests.Session()

    # Define retry strategy
    retry_strategy = Retry(
        total=50,
        backoff_factor=0.1,
        status_forcelist=[402, 403, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    profiles = []

    # Function to extract profile data from a page
    def extract_profiles(soup):
        extracted_profiles = []
        for profile in soup.select("li.pserp-layout__profile-result-list-item"):
            name = profile.select_one("h3.base-search-card__title")
            subtitle = profile.select_one("h4.base-search-card__subtitle")
            location = profile.select_one("p.people-search-card__location")
            current = profile.select_one("div.entity-list-meta span")

            education_spans = profile.select("div.entity-list-meta span")
            education = education_spans[1] if len(education_spans) > 1 else None

            profile_url = profile.select_one("a.base-card--link")

            extracted_profiles.append({
                "name": name.get_text(strip=True) if name else "",
                "subtitle": subtitle.get_text(strip=True) if subtitle else "",
                "location": location.get_text(strip=True) if location else "",
                "current": current.get_text(strip=True) if current else "",
                "education": education.get_text(strip=True) if education else "",
                "profile_url": profile_url["href"] if profile_url else ""
            })
        return extracted_profiles

    page = 1
    params['page'] = page
    session.cookies.update(generate_cookies())
    response = session.get('https://www.linkedin.com/pub/dir', params=params, headers=headers, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        profiles.extend(extract_profiles(soup))
        profile_results = pd.DataFrame(profiles)
        profile_results = profile_results.drop_duplicates().reset_index(drop=True)
        print(f'Successfully scraped profiles. Total profiles fetched: {profile_results.shape[0]}.')
    else:
        print(f"Failed to retrieve page {page}")
    
    return profile_results

# Example usage
profiles = generate_profile_links(first_name='Shreya', last_name='Patel')
print(profiles)