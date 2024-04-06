import requests
from bs4 import BeautifulSoup

days = ['all']# ['2020-06-16', '2020-06-17', '2020-06-18']
info_dict = dict()
year_title = 'ACCV2022'
file_name = '../ACCV/accv2022.md'
prefix = 'https://openaccess.thecvf.com/' #'https://www.ecva.net/'
###############################################################
home_page = []
title = []
author = []
pdf_link = []
###############################################################

for day in days:
    url = f'https://openaccess.thecvf.com/ACCV2022?day={day}'
    # url = 'https://openaccess.thecvf.com/ACCV2020'
    # url = 'https://www.ecva.net/papers.php'
    data = requests.get(url)
    data.encoding = data.apparent_encoding


    soup = BeautifulSoup(data.text, 'html.parser')
    paper_title_info = soup.find_all('dt')
    if not paper_title_info:
        raise Exception('grab error, please check url!')
    for item in paper_title_info:
        homepage_link = prefix + item.find('a').get('href')
        paper_title = item.find('a').string.strip()
        home_page.append(homepage_link)
        title.append(paper_title)

    sup_info = soup.find_all('dd')
    for item in sup_info:
        authors = []
        # normal version
        if item.find('form'):  # author
            for auth_info in item.find_all('form'):
                authors.append(auth_info.text.replace(',', '').strip())
            author.append(authors)
        # eccv2020 version
        # if not item.find('a'):  # author
        #     authors = item.text.strip().split(',')
        #     author.append(authors)
        else:  # supplement details
            if item.find('a').string not in ['Go back', 'Back']:
                link = prefix + item.find('a').get('href')
                pdf_link.append(link)

assert len(author) == len(home_page) == len(title) == len(pdf_link)

f = open(file_name,'w', encoding='utf-8')
f.write(f'# {year_title}\n\n')
for home_page_, title_, author_, pdf_link_ in zip(home_page, title, author, pdf_link):
    f.write(f'- {",".join(author_)}. **"{title_}"** | [[Home Page]]({home_page_}) | [[PDF]]({pdf_link_}) \n\n\n')
f.close()