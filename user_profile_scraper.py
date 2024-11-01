import requests
import json
import random
import string
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
from faker import Faker

fake = Faker()

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_cookies():
    timestamp = int(time.time())
    cookie_template = {
        'bcookie': f'"v=2&{generate_random_string(8)}-{generate_random_string(4)}-{generate_random_string(4)}-{generate_random_string(4)}-{generate_random_string(12)}"',
        'lidc': f'"b=VGST04:s=V:r=V:a=V:p=V:g=3275:u=1:x=1:i={timestamp}:t={timestamp+86400}:v=2:sig={generate_random_string(24)}"',
        'JSESSIONID': f'ajax:{random.randint(1000000000000000000, 9999999999999999999)}',
        'lang': 'v=2&lang=en-us',
    }
    return cookie_template

def extract_education(page_soup):
    try:
        html_content = page_soup.find('section', {'data-section': 'educationsDetails'})
        if not html_content:
            return []

        soup = BeautifulSoup(str(html_content), 'html.parser')
        education_section = soup.find('div', {'class': 'core-section-container__content break-words'})
        if not education_section:
            return []

        education_list = education_section.find_all('li', {'class': 'education__list-item'})
        education_data = []

        for edu in education_list:
            try:
                school = edu.find('h3').text.strip() if edu.find('h3') else ''
                url = edu.find('a')['href'] if edu.find('a') else ''
                degree_spans = edu.find('h4').find_all('span') if edu.find('h4') else []
                degree = degree_spans[0].text.strip() if degree_spans else ''
                field_of_study = degree_spans[1].text.strip() if len(degree_spans) > 1 else ''
                dates = edu.find('span', {'class': 'date-range'})
                start_date = dates.find_all('time')[0].text if dates and len(dates.find_all('time')) > 0 else ''
                end_date = dates.find_all('time')[1].text if dates and len(dates.find_all('time')) > 1 else ''
                description = edu.find('div', {'class': 'show-more-less-text'}).text.strip() if edu.find('div', {'class': 'show-more-less-text'}) else ''

                education_data.append({
                    "school": school,
                    "location": "",
                    "url": url,
                    "start_date": start_date,
                    "end_date": end_date,
                    "degree": degree,
                    "field_of_study": field_of_study,
                    "description": description
                })
            except Exception as e:
                continue

        return education_data

    except Exception as e:
        return []

def extract_experience(soup):
    try:
        experience_section = soup.find('section', {'data-section': 'experience'})
        all_experiences = []

        if not experience_section:
            return all_experiences

        # Iterate through each experience group
        for group in experience_section.find_all('li', class_='experience-group'):
            company_tag = group.find('h4', class_='experience-group-header__company')
            company = company_tag.get_text(strip=True) if company_tag else ''
            company_url_tag = group.find('a', class_='experience-group-header__url')
            company_url = company_url_tag['href'] if company_url_tag else ''

            # Iterate through each position within the group
            for position in group.find_all('li', class_='profile-section-card'):
                try:
                    title_tag = position.find('span', class_='experience-item__title')
                    title = title_tag.get_text(strip=True) if title_tag else ''

                    date_range_tag = position.find('span', class_='date-range')
                    time_tags = date_range_tag.find_all('time') if date_range_tag else []
                    if len(time_tags) == 2:
                        start_date = time_tags[0].get_text(strip=True)
                        end_date = time_tags[1].get_text(strip=True)
                    else:
                        start_date = time_tags[0].get_text(strip=True) if time_tags else ''
                        end_date = 'Present' if start_date else ''

                    duration = date_range_tag.find('span', class_='before:middot').get_text(strip=True) if date_range_tag else ''

                    location_tag = position.find_all('p', class_='experience-item__meta-item')
                    location = location_tag[1].get_text(strip=True) if len(location_tag) > 1 else ''

                    # Try extracting description from both less and more tags
                    description_tag_less = position.find('p', class_='show-more-less-text__text--less')
                    description_tag_more = position.find('p', class_='show-more-less-text__text--more')
                    if description_tag_more:
                        description = description_tag_more.get_text(" ", strip=True).replace('Show less', '').replace('Show more', '').strip()
                    elif description_tag_less:
                        description = description_tag_less.get_text(" ", strip=True).replace('Show less', '').replace('Show more', '').strip()
                    else:
                        description = ''

                    # Format data
                    experience_info = {
                        "title": title,
                        "company": company,
                        "url": company_url,
                        "location": location,
                        "start_date": start_date,
                        "end_date": end_date,
                        "duration": duration,
                        "description": description
                    }

                    all_experiences.append(experience_info)

                except Exception as e:
                    # print(f"An error occurred: {e}")
                    all_experiences.append({
                        "title": '',
                        "company": company,
                        "url": company_url,
                        "location": '',
                        "start_date": '',
                        "end_date": '',
                        "duration": '',
                        "description": ''
                    })

        # Iterate through each individual experience item not within a group
        for exp_soup in experience_section.find_all('li', class_='experience-item'):
            try:
                title_tag = exp_soup.find('span', class_='experience-item__title')
                title = title_tag.get_text(strip=True) if title_tag else ''

                company_tag = exp_soup.find('span', class_='experience-item__subtitle')
                company = company_tag.get_text(strip=True) if company_tag else ''

                company_url_tag = exp_soup.find('a', class_='profile-section-card__image-link')
                company_url = company_url_tag.get('href') if company_url_tag else ''

                date_range_tag = exp_soup.find('span', class_='date-range')
                time_tags = date_range_tag.find_all('time') if date_range_tag else []
                if len(time_tags) == 2:
                    start_date = time_tags[0].get_text(strip=True)
                    end_date = time_tags[1].get_text(strip=True)
                else:
                    start_date = time_tags[0].get_text(strip=True) if time_tags else ''
                    end_date = 'Present' if start_date else ''

                duration_tag = date_range_tag.find('span', class_='before:middot').get_text(strip=True) if date_range_tag else ''

                location_tag = exp_soup.find_all('p', class_='experience-item__meta-item')
                location = location_tag[1].get_text(strip=True) if len(location_tag) > 1 else ''

                # Try extracting description from both less and more tags
                description_tag_less = exp_soup.find('p', class_='show-more-less-text__text--less')
                description_tag_more = exp_soup.find('p', class_='show-more-less-text__text--more')
                if description_tag_more:
                    description = description_tag_more.get_text(" ", strip=True).replace('Show less', '').replace('Show more', '').strip()
                elif description_tag_less:
                    description = description_tag_less.get_text(" ", strip=True).replace('Show less', '').replace('Show more', '').strip()
                else:
                    description = ''

                # Format data
                experience_info = {
                    "title": title,
                    "company": company,
                    "url": company_url,
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "duration": duration_tag,
                    "description": description
                }

                all_experiences.append(experience_info)

            except Exception as e:
                # print(f"An error occurred: {e}")
                all_experiences.append({
                    "title": '',
                    "company": '',
                    "url": '',
                    "location": '',
                    "start_date": '',
                    "end_date": '',
                    "duration": '',
                    "description": ''
                })

        return all_experiences

    except Exception as e:
        return []

def extract_volunteer_experience(soup):
    try:
        volunteer_experience_section = soup.find('section', {'data-section': 'volunteering'})
        volunteer_experience = []

        for item in volunteer_experience_section.find_all('li', class_='profile-section-card'):
            try:
                title = item.find('h3').get_text(strip=True)
            except AttributeError:
                title = ''
            
            try:
                organization_tag = item.find('h4').find('a')
                organization = organization_tag.get_text(strip=True)
                organization_link = organization_tag['href']
            except AttributeError:
                organization = ''
                organization_link = ''
            
            try:
                date_range = item.find('span', class_='date-range')
                time_tags = date_range.find_all('time') if date_range else []
                if len(time_tags) == 2:
                    start_date = time_tags[0].get_text(strip=True)
                    end_date = time_tags[1].get_text(strip=True)
                else:
                    start_date = time_tags[0].get_text(strip=True) if time_tags else ''
                    end_date = 'Present' if start_date else ''
                duration = date_range.find(string=lambda x: 'months' in x or 'years' in x).strip() if date_range else ''
            except (AttributeError, IndexError):
                start_date = ''
                end_date = ''
                duration = ''
            
            try:
                organization_logo_url = item.find('img')['data-delayed-url']
            except (AttributeError, KeyError):
                organization_logo_url = ''
            
            try:
                description_tag_more = item.find('p', class_='show-more-less-text__text--more')
                description = description_tag_more.get_text(" ", strip=True).replace('Show less', '').replace('Show more', '').strip() if description_tag_more else ''
            except AttributeError:
                description = ''

            volunteer_experience.append({
                'title': title,
                'organization': organization,
                'organization_link': organization_link,
                'duration': duration,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'organization_logo_url': organization_logo_url,
                'description': description
            })

        return volunteer_experience

    except Exception as e:
        return []
    
def extract_languages(soup):
    languages = []
    try:
        langs_soup = soup.find('section', {'data-section': 'languages'})
        if langs_soup:
            for li in langs_soup.find_all('li', class_='profile-section-card'):
                try:
                    name = li.find('h3').text.strip()
                    proficiency = li.find('h4').text.strip()
                    languages.append({"name": name, "proficiency": proficiency})
                except AttributeError as e:
                    continue
        return languages
    except Exception as e:
        return languages


def extract_projects(soup):
    try:

        projects_section = soup.find('section', {'data-section': 'projects'})
        if not projects_section:
            return []

        project_items = projects_section.find_all('li', class_='profile-section-card')
        if not project_items:
            return []

        projects = []

        for item in project_items:
            try:
                title = item.find('h3').get_text(strip=True)
            except AttributeError:
                title = ""

            try:
                duration = item.find('h4').get_text(strip=True)
            except AttributeError:
                duration = ""

            details = item.find('p', class_='show-more-less-text__text--more')
            if not details:
                details = item.find('p', class_='show-more-less-text__text--less')

            if details:
                details_text = details.get_text(strip=True).replace('\u2022', '-').replace('Show less', '').replace('Show more', '')
            else:
                details_text = ""

            projects.append({
                'title': title,
                'duration': duration,
                'details': details_text
            })

        return projects

    except Exception as e:
        return []
    

def extract_certifications(soup):
    certifications_section = soup.find('section', {'data-section': 'certifications'})
    if not certifications_section:
        return []

    certification_list = certifications_section.find_all('li', class_='profile-section-card')
    time_tags = certifications_section.find_all('time')
    
    certifications_data = []
    time_index = 0

    for cert in certification_list:
        try:
            title_tag = cert.find('h3')
            title = title_tag.text.strip() if title_tag else ''

            issuing_organization_tag = cert.find('h4')
            issuing_organization = issuing_organization_tag.text.strip() if issuing_organization_tag else ''

            # Correctly extract issue date from the pre-fetched time tags
            issue_date = time_tags[time_index].text if time_index < len(time_tags) else ''
            time_index += 1

            credential_id_tag = cert.find('div', string=lambda text: 'Credential ID' in text if text else False)
            credential_id = credential_id_tag.text.split('Credential ID ')[-1].strip() if credential_id_tag else ''

            credential_url_tag = cert.find('a', {'data-tracking-control-name': 'public_profile_see-credential'})
            credential_url = credential_url_tag['href'] if credential_url_tag else ''

            certifications_data.append({
                "title": title,
                "issuing_organization": issuing_organization,
                "issue_date": issue_date,
                "credential_id": credential_id,
                "credential_url": credential_url
            })

        except Exception as e:
            continue

    return certifications_data

def random_user_agent():
    return fake.user_agent()

def random_referer():
    referers = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.yahoo.com/',
    ]
    return random.choice(referers)

def random_sec_ch_ua():
    sec_ch_ua = [
        '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        '"Not/A)Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        '"Not/A)Brand";v="90", "Chromium";v="90", "Google Chrome";v="90"',
    ]
    return random.choice(sec_ch_ua)

def random_accept_language():
    accept_languages = [
        'en-US,en;q=0.9',
        'en-GB,en;q=0.8',
        'en-CA,en;q=0.7',
    ]
    return random.choice(accept_languages)

def scrape_linkedin_profile(url):
    try:
        
        session = requests.Session()
        retries = Retry(total=50, backoff_factor=0.1, status_forcelist=[402, 403, 429, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        cookies = generate_random_cookies()
        session.cookies.update(cookies)

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': random_accept_language(),
            'dnt': '1',
            'priority': 'u=0, i',
            'referer': random_referer(),
            'sec-ch-ua': random_sec_ch_ua(),
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': random.choice(['"Windows"', '"macOS"', '"Linux"']),
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': random_user_agent(),
        }
                
        response = session.get(url, cookies=cookies, headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        # Extracting name
        name_tag = soup.find('meta', {'property': 'profile:first_name'})
        first_name = name_tag['content'] if name_tag else ''
        last_name_tag = soup.find('meta', {'property': 'profile:last_name'})
        last_name = last_name_tag['content'] if last_name_tag else ''
        data['name'] = f"{first_name} {last_name}".strip()

        # Extracting job title
        job_title_tag = soup.find('h2', {'class': 'top-card-layout__headline'})
        data['headline'] = job_title_tag.get_text(strip=True) if job_title_tag else ''

        # Extracting company
        company_tag = soup.find('meta', {'property': 'og:title'})
        company = company_tag['content'].split(' - ')[-1].replace(' | LinkedIn', '') if company_tag else ''
        data['company'] = company

        # Extracting location
        location_tag = soup.find('div', {'class': 'not-first-middot'})
        location = location_tag.find('span').get_text(strip=True) if location_tag and location_tag.find('span') else ''
        data['location'] = location

        # Extracting profile URL
        profile_url_tag = soup.find('meta', {'property': 'og:url'})
        data['profile_url'] = profile_url_tag['content'] if profile_url_tag else ''

        # Extracting follower and connection counts
        followers_span = soup.find('span', string=lambda x: x and ('followers' in x or 'follower' in x))
        follower_count = followers_span.text.replace('followers', "").strip() if followers_span else ''
        data['followers'] = follower_count

        connections_span = soup.find('span', string=lambda x: x and ('connections' in x or 'connection' in x))
        connection_count = connections_span.text.replace('connections', "").strip() if connections_span else ''
        data['connections'] = connection_count

        experience = extract_experience(soup)
        data['experience'] = experience
        
        volunteer_experience = extract_volunteer_experience(soup)
        data['volunteer_experience'] = volunteer_experience
        
        education = extract_education(soup)
        data['education'] = education
        
        projects = extract_projects(soup)
        data['projects'] = projects
        
        certifications_data = extract_certifications(soup)
        data['cerifications'] = certifications_data
        
        languages = extract_languages(soup)
        data['languages'] = languages
        
        return json.dumps(data, indent=4)

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return json.dumps({"error": "Request error"}, indent=4)
    except Exception as e:
        return json.dumps({"error": "An error occurred"}, indent=4)
    
# # Example usage
# url = 'https://www.linkedin.com/in/munj-patel-a1812b233/'
# profile_summary = scrape_linkedin_profile(url)
# print(profile_summary)