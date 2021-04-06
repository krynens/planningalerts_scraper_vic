import requests
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd
import csv

authorities = ['brimbank',
'ballarat_city',
'banyule',
'baw_baw',
'bayside_vic',
'boroondara_city',
'brimbank',
'campaspe_shire',
'cardinia',
'casey',
'glen_eira',
'greater_bendigo',
'geelong_city',
'mooney_valley',
'city_of_port_phillip',
'stonnington',
'city_of_whittlesea',
'corangamite',
'darebin',
'east_gippsland',
'frankston_city',
'golden_plains_shire',
'greater_shepparton',
'hume_city_council',
'kingston',
'knox',
'latrobe',
'macedon_ranges',
'manningham',
'maroondah_city',
'melbourne_city',
'monash',
'moreland_city',
'mornington_peninsula',
'nillumbik',
'rural_city_of_wangaratta',
'south_gippsland_shire',
'spear_victoria',
'surf_coast_shire',
'vcglr',
'whitehorse',
'wyndham',
'yarra_city',
'yarra_ranges']


csv_file = open('vic.csv', 'w+')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['reference', 'address', 'description', 'link', 'authority'])

def getData(url):
    print(f'Getting page {url}')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('ol', class_='applications')
    applications = table.find_all('article', class_='application')
    page = url.split('page=')[1]
    for application in applications:
        print('Getting application...')
        address = application.find('div', class_='address').text.strip()
        description = application.find('p', class_='description').text.strip()
        link = 'https://www.planningalerts.org.au' + str(application.find('a')).split('"')[1]
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
        reference = soup.find('p', class_='source').text.split('reference ')[1].split(')')[0].strip()
        authority = url.split('authorities/')[1].split('/')[0]
        with open('vic.csv', 'a+'):
            csv_writer.writerow([reference, address, description, link, authority])

with concurrent.futures.ThreadPoolExecutor() as executor:
    urls = [f'https://www.planningalerts.org.au/authorities/{authority}/applications?page=1' for authority in authorities]
    for url in urls:
        executor.submit(getData, url)



csv_file.close()

