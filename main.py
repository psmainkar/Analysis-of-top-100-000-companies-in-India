import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

final = pd.DataFrame()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) '
                         'Chrome/80.0.3987.162 Safari/537.36'}
for j in range(1, 500):
    wp = requests.get('https://www.ambitionbox.com/list-of-companies?page={}'.format(j), headers=headers).text
    soup = BeautifulSoup(wp, 'lxml')
    print(soup.prettify())
    company = soup.find_all('div', class_='companyCardWrapper')
    name = []
    rating = []
    avg_salary = []
    jobs = []
    benefits = []
    data = []
    type_of_company = []
    state = []
    how_old = []
    positives = []
    negatives = []
    city = []
    team_size = []

    for i in company:
        try:
            name.append(i.find('h2').text.strip())
        except:
            name.append(np.nan)

        try:
            rating.append(i.find('span', class_='companyCardWrapper__companyRatingValue').text.strip())
        except:
            rating.append(np.nan)

        try:
            avg_salary.append(i.find_all('span', class_='companyCardWrapper__ActionCount')[1].text.strip())
        except:
            avg_salary.append(np.nan)

        try:
            jobs.append(i.find_all('span', class_='companyCardWrapper__ActionCount')[3].text.strip())
        except:
            jobs.append(np.nan)

        try:
            benefits.append(i.find_all('span', class_='companyCardWrapper__ActionCount')[4].text.strip())
        except:
            benefits.append(np.nan)

        try:
            type_of_company.append(i.find('span', class_='companyCardWrapper__interLinking').text.split('|')[0].strip())
        except:
            type_of_company.append(np.nan)

        try:
            team_size.append(i.find('span', class_='companyCardWrapper__interLinking').text.split('|')[1].strip())
        except:
            team_size.append(np.nan)

        try:
            state.append(i.find('span', class_='companyCardWrapper__interLinking').text.split('|')[2].strip())
        except:
            state.append(np.nan)

        try:
            how_old.append(
                i.find('span', class_='companyCardWrapper__interLinking').text.split('|')[3].split(' ')[1].strip())
        except:
            how_old.append(np.nan)

        try:
            city.append(
                i.find('span', class_='companyCardWrapper__interLinking').text.split('|')[4].split('+')[0].strip())
        except:
            city.append(np.nan)

        try:
            if i.find('span', class_="companyCardWrapper__ratingHeader--high").text.strip() == 'Highly Rated For':
                positives.append(i.find_all('span', class_='companyCardWrapper__ratingValues')[0].text.strip())

        except:
            positives.append(np.nan)

        try:
            if i.find('span',
                      class_="companyCardWrapper__ratingHeader--critical").text.strip() == 'Critically Rated For':
                try:
                    negatives.append(i.find_all('span', class_='companyCardWrapper__ratingValues')[1].text.strip())
                except:
                    negatives.append(i.find_all('span', class_='companyCardWrapper__ratingValues')[0].text.strip())

        except:
            negatives.append(np.nan)

    df = pd.DataFrame({'name': name, 'rating': rating, 'avg_salary': avg_salary, 'jobs': jobs, 'benefits': benefits,
                       'type_of_company': type_of_company, 'state': state, 'how_old': how_old, 'city': city,
                       'team_size': team_size, 'positives': positives, 'negatives': negatives})

    final = pd.concat([final, df], ignore_index=True)
    print(final)
    final.to_csv('jobs.csv')
