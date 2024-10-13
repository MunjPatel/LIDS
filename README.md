# LIDS

Also called LinkedIn Data Scraper, is designed to scrape publicly accessible LinkedIn profile information, including company details, user data, and individual profiles. It is helpful for users looking to gather large amounts of LinkedIn data for analytics, research, or personal use.

## Why LIDS?

LIDS provides an efficient way to gather publicly available information from LinkedIn profiles for use in business research, competitor analysis, or personal network management. Whether you're tracking companies in your industry or analyzing profiles for hiring or data insights, LIDS simplifies the process of scraping and organizing relevant information.

## Example Use Cases:

- **Company Research**: Scrape company profiles to analyze key metrics like company size, industry, and latest updates for competitors or market analysis.
- **Recruitment**: Gather detailed information on prospective candidates based on job roles, education, and experience.
- **Data Analytics**: Use scraped data to build models for trend analysis in job markets, geographic distributions, or talent acquisition.

## Data Scraping Disclaimer:

This tool scrapes publicly accessible data from LinkedIn profiles. Please ensure that you comply with LinkedIn's terms of service and avoid using the scraper in ways that may violate their usage policies or any applicable laws. LinkedIn data belongs to its users, and their privacy should be respected. Avoid misuse or re-selling of scraped data. Use LIDS responsibly.

## Features

1. Scrape LinkedIn company profiles to extract company details.
2. Scrape multiple user profiles based on names.
3. Scrape specific user profile with detailed information.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MunjPatel/LIDS.git
    ```
2. Change the working directory:

   ```bash
   cd LIDS
   ```
3. Create and activate virtual environment:
   
   ```bash
   conda create --prefix ./env python=3.9 -y
   conda activate ./env
   ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Scraping Company Data:

1. Open the `company_profile_scraper.py` file.

2. Update the `url` variable with the LinkedIn company URL. 

3. Run the scraper:

    ```bash
    python company_profile_scraper.py
    ```

4. Example Output: JSON data of the company:

   ```bash
   {
    "name": "Google",
    "profile_link": "https://www.linkedin.com/company/google?originalSubdomain=in",
    "followers": 34403269,
    "industry": "Software Development",
    "location": "Mountain View, CA  34,403,269 followers",
    "website": "https://goo.gle/3DLEokh",
    "company_size": "10,001+ employees",
    "headquarters": "Mountain View, CA",
    "type": "Public Company",
    "founded": null,
    "slogan": null,
    "description": "A problem isn't truly solved until it's solved for all. Googlers build products that help create opportunities for everyone, whether down the street or across the globe. Bring your insight, imagination and a healthy disregard for the impossible. Bring everything that makes you unique. Together, we can build for everyone.\n\nCheck out our career opportunities at goo.gle/3DLEokh",
    "logo_url": null,
    "cover_image_url": null,
    "employees": null,
    "latest_updates": null
   }
   ```

### Scraping Multiple User Profiles:

1. Open `users_profile.py`.

2. Update the `first_name` and `last_name` variables.

3. Run the script:

    ```bash
    python users_profile.py
    ```

4. Example Output: A table of matching profiles:

```bash
            name                                           subtitle  ...                                          education                                        profile_url
0   Shreya Patel  Assistant HR Manager | IT Recruitment & Talent...  ...  Madan Mohan Malaviya University of Technology,...  https://in.linkedin.com/in/shreya-patel2402?tr...    
1   Shreya Patel  CORE Cybersecurity Associate @ Comcast NBCUniv...  ...           Stevens Institute of Technology, +1 more  https://www.linkedin.com/in/shreya-patel-b0524...    
2   Shreya Patel                                                     ...                                                     https://www.linkedin.com/in/patelshreya?trk=pe...    
3   Shreya Patel  Hiring |Business Development Executive | Busin...  ...  Shri Jairambhai Patel Institute of Business Ma...  https://in.linkedin.com/in/shreya-patel-622406...    
4   Shreya Patel                                                     ...                                          , +1 more  https://www.linkedin.com/in/shreya-patel-37868...    
5   Shreya Patel  Chemistry & Pre-Pharmacy Student at University...  ...            University of Illinois Chicago, +1 more  https://www.linkedin.com/in/shreya-patel-ba8b3...    
6   Shreya Patel                                                     ...                                                     https://uk.linkedin.com/in/shreyapateluk?trk=p...    
7      Shreya P.  LinkedIn Associate Product Manager | Co-Founde...  ...        Washington University in St. Louis, +2 more  https://www.linkedin.com/in/shreya-p?trk=peopl...    
8   Shreya Patel                         Human Resources management  ...                           York University, +2 more  https://nz.linkedin.com/in/shreyapatel183?trk=...    
9   Shreya Patel                                                     ...                                          , +1 more  https://www.linkedin.com/in/shreya-d-patel?trk...    
10  Shreya Patel  Doctoral Candidate| Oncology and Rare Bone Dis...  ...                                                     https://www.linkedin.com/in/shreya-patel-0504?...    

[10 rows x 6 columns]

```

### Scraping Specific User Profile:

1. Open `user_profile_scraper.py`.

2. Update the `url` variable with the user profile URL.

3. Run the script:

    ```bash
    python user_profile_scraper.py
    ```

4. Example Output: JSON data of the user:

   ```bash
   {
    "name": "Manan Patel",
    "headline": "Summer Strategy Consultant @ BYD | University of Warwick | BSc Computer Science with Business Analytics",
    "company": "BYD EUROPE",
    "location": "London Area, United Kingdom",
    "profile_url": "https://uk.linkedin.com/in/mananpatel9",
    "followers": "2K",
    "connections": "500+",
    "experience": [
        {
            "title": "Strategy Consultant",
            "company": "BYD EUROPE",
            "url": "https://nl.linkedin.com/company/bydeurope?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "United Kingdom",
            "start_date": "Jun 2024",
            "end_date": "Present",
            "duration": "5 months",
            "description": ""
        },
        {
            "title": "Associate Consultant",
            "company": "180 Degrees Consulting",
            "url": "https://au.linkedin.com/company/180degreesconsulting?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "United Kingdom",
            "start_date": "Jun 2024",
            "end_date": "Present",
            "duration": "5 months",
            "description": ""
        },
        {
            "title": "Summer Hedge Fund Intern",
            "company": "Broad Reach Investment Management LLP",
            "url": "https://uk.linkedin.com/company/broad-reach-investment-management-llp?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "London, England, United Kingdom",
            "start_date": "Jul 2023",
            "end_date": "Aug 2023",
            "duration": "2 months",
            "description": ""
        },
        {
            "title": "Endorsed Software Development Project Manager",
            "company": "Deutsche Bank",
            "url": "https://de.linkedin.com/company/deutsche-bank?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "Coventry, England, United Kingdom",
            "start_date": "Jan 2022",
            "end_date": "Mar 2022",
            "duration": "3 months",
            "description": ""
        },
        {
            "title": "Event Coordinator",
            "company": "Warwick Punjabi Society",
            "url": "https://uk.linkedin.com/company/warwick-punjabi-society?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "Coventry, England, United Kingdom",
            "start_date": "May 2021",
            "end_date": "Mar 2022",
            "duration": "11 months",
            "description": ""
        },
        {
            "title": "STEM Learning Ambassador",
            "company": "Aveea",
            "url": "https://uk.linkedin.com/company/aveea?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "Leicester, England, United Kingdom",
            "start_date": "Feb 2019",
            "end_date": "Dec 2019",
            "duration": "11 months",
            "description": ""
        },
        {
            "title": "Maths & English Tutor",
            "company": "Kumon UK",
            "url": "https://uk.linkedin.com/company/kumon-educational-uk?trk=public_profile_experience-item_profile-section-card_image-click",
            "location": "Leicester, England, United Kingdom",
            "start_date": "Mar 2017",
            "end_date": "Jun 2018",
            "duration": "1 year 4 months",
            "description": ""
        }
    ],
    "volunteer_experience": [
        {
            "title": "Community Service",
            "organization": "BAPS Swaminarayan Sanstha",
            "organization_link": "https://www.linkedin.com/company/bapsswaminarayansanstha?trk=public_profile_volunteering-position_profile-section-card_subtitle-click",
            "duration": "6 years 5 months",
            "date_range": {
                "start": "Jun 2018",
                "end": "Present"
            },
            "organization_logo_url": "https://media.licdn.com/dms/image/v2/C4D0BAQFqGA-XEoCp6Q/company-logo_100_100/company-logo_100_100/0/1646619742650/bapsswaminarayansanstha_logo?e=2147483647&v=beta&t=0TtKRLm2kREw5hSuoI8GvyXvuXxmXwJMoRVbiRR_h-g",
            "description": ""
        },
        {
            "title": "Public Relations Coordinator",
            "organization": "National Hindu Students'\u200b Forum (UK)",
            "organization_link": "https://uk.linkedin.com/company/nhsf?trk=public_profile_volunteering-position_profile-section-card_subtitle-click",
            "duration": "9 months",
            "date_range": {
                "start": "Feb 2024",
                "end": "Present"
            },
            "organization_logo_url": "https://media.licdn.com/dms/image/v2/C4D0BAQHRqNN2nQTP1Q/company-logo_100_100/company-logo_100_100/0/1649267366293/nhsf_logo?e=2147483647&v=beta&t=GT-sNsLuj9vtk5FdmgyS7kZgBj5uGbH3JPxy74Sy26Y",
            "description": ""
        }
    ],
    "education": [
        {
            "school": "University of Warwick - Warwick Business School",
            "location": "",
            "url": "https://uk.linkedin.com/school/warwick-business-school/?trk=public_profile_school_profile-section-card_image-click",
            "start_date": "2023",
            "end_date": "2025",
            "degree": "Master of Science - MSc",
            "field_of_study": "",
            "description": ""
        },
        {
            "school": "University of Warwick",
            "location": "",
            "url": "https://uk.linkedin.com/school/uniofwarwick/?trk=public_profile_school_profile-section-card_image-click",
            "start_date": "2020",
            "end_date": "2023",
            "degree": "Bachelor of Science - BSc Hons",
            "field_of_study": "",
            "description": ""
        },
        {
            "school": "Lionheart Educational Trust",
            "location": "",
            "url": "https://uk.linkedin.com/school/lionhearttrust/?trk=public_profile_school_profile-section-card_image-click",
            "start_date": "2018",
            "end_date": "2020",
            "degree": "",
            "field_of_study": "",
            "description": ""
        },
        {
            "school": "Soar Valley College",
            "location": "",
            "url": "",
            "start_date": "2013",
            "end_date": "2018",
            "degree": "",
            "field_of_study": "",
            "description": ""
        }
    ],
    "projects": [
        {
            "title": "Financial Lead Conversion",
            "duration": "Oct 2023-Dec 2023",
            "details": "Leveraged machine learning algorithms in R for a consultancy project, aiming to identify high-value customers for targeting by a mid-sized private bank."
        },
        {
            "title": "Database Management for a Music Promotion Company",
            "duration": "Nov 2021-Dec 2021",
            "details": "Designed a robust SQL schema, executing advanced queries involving complex joins, subqueries, and aggregate functions to extract information from datasets, such as identifying economically feasible gigs and discovering popular customer segments."
        },
        {
            "title": "Simulated Restaurant Web Application (Java)",
            "duration": "Feb 2021-Apr 2021",
            "details": "Designed and implemented data structures such as hash maps and array lists from scratch in a simulated restaurant website.Developed an efficient merge sort algorithm independently to allow searching of various parameters."
        },
        {
            "title": "Command Line File Management System (C)",
            "duration": "Nov 2020-Jan 2021",
            "details": "Developed a command line editor capable of creating, displaying and manipulating text files, with attempt to achieve maximum accessibility for desired functionalities.Implemented a convenient user interface with menus, allowing several operations of type file, line or general to be performed without the file being open,increasing efficiency."
        },
        {
            "title": "\u2018WORMS\u2019 Project (Python) (2019)",
            "duration": "Feb 2019-Jun 2019",
            "details": "Used python on a Raspberry Pi to develop several programs that would allow calibrating and operating ofvarious sensors, required to monitor conditions for the growth of tardigrades."
        }
    ],
    "cerifications": [
        {
            "title": "Data Science & Analytics Virtual Experience",
            "issuing_organization": "Boston Consulting Group (BCG)",
            "issue_date": "Jul 2023",
            "credential_id": "",
            "credential_url": ""
        },
        {
            "title": "Investment Banking Virtual Experience",
            "issuing_organization": "JPMorgan Chase & Co.",
            "issue_date": "Jul 2023",
            "credential_id": "",
            "credential_url": ""
        },
        {
            "title": "Data Analytics Consulting Virtual Internship",
            "issuing_organization": "KPMG",
            "issue_date": "Nov 2021",
            "credential_id": "",
            "credential_url": ""
        },
        {
            "title": "Software Engineering Virtual Experience",
            "issuing_organization": "JPMorgan Chase & Co.",
            "issue_date": "Nov 2021",
            "credential_id": "",
            "credential_url": ""
        },
        {
            "title": "LIBF Level 3 Certificate in Financial Studies",
            "issuing_organization": "The London Institute of Banking & Finance",
            "issue_date": "Oct 2019",
            "credential_id": "",
            "credential_url": ""
        },
        {
            "title": "Abacus and Mental Arithmetic \u2013 Certificate of Completion",
            "issuing_organization": "UCMAS",
            "issue_date": "Jun 2014",
            "credential_id": "",
            "credential_url": ""
        }
    ],
    "languages": [
        {
            "name": "Gujarati",
            "proficiency": "Native or bilingual proficiency"
        },
        {
            "name": "Hindi",
            "proficiency": "Full professional proficiency"
        },
        {
            "name": "German",
            "proficiency": "Professional working proficiency"
        },
        {
            "name": "English",
            "proficiency": "Native or bilingual proficiency"
        }
    ]
    }
   ```

## Error Handling:

- Rate Limiting: If you are blocked, consider adding delays between requests or using proxies.
- Parsing Errors: Occasionally, LinkedIn may update its HTML structure, causing the scraper to break. In such cases, raise an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
