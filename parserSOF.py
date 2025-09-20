from bs4 import BeautifulSoup
from time import sleep
import requests
import lxml
urlget = 'https://stackoverflow.com/users?tab=Reputation&filter=all'
res = requests.get(urlget)
if res:
    root = BeautifulSoup(res.content, 'lxml')
    table = root.find('div', class_='d-grid grid__4 lg:grid__3 md:grid__2 sm:grid__1 g12')
    users = table.find_all('div', class_="user-details")
    for user in users:
        print('Имя пользователя: ' + user.find('a').text)
        link = user.find('a')['href']
        reqlink = 'https://stackoverflow.com'+link
        res = requests.get(reqlink)
        if res:
            root = BeautifulSoup(res.content, 'lxml')
            table = root.find('div', class_='s-card fc-black-400 bar-md')
            c = table.find_all('div', class_='flex--item md:fl-auto')
            print('Кол-во ответов: '+c[2].text.split()[0])
            print('Кол-во вопросов : '+c[3].text.split()[0])
            badges_url = root.find('a', class_='s-link s-link__muted flex--item js-gps-track')
            print('Все значки:')
            i = 1
            while True:
                nreqlink = 'https://stackoverflow.com' + badges_url['href'] + f'&sort=recent&page={i}'
                res = requests.get(nreqlink)
                if res:
                    root = BeautifulSoup(res.content, 'lxml')
                    badges = root.find_all('div', class_='grid--item')
                    for badge in badges:
                        name = badge.find('a').text
                        print(name, end=', ' if badge != badges[-1] else '\n')
                    lastp = root.find_all('a', class_='s-pagination--item js-pagination-item')
                    i += 1
                    if lastp[-1].text != ' Next':
                        break
        sleep(5)
