import requests
from bs4 import BeautifulSoup

prefix = 'http://proceedings.mlr.press/' #'https://www.ecva.net/'
info_dict = {
    2013: 28,
    2014: 32,
    2015: 37,
    2016: 48,
    2017: 70,
    2018: 80,
    2019: 97,
    2020: 119,
    2021: 139,
    2022: 162,
    2023: 202
}

for year in range(2022, 2024):

    year_title = f'ICML{year}'
    file_name = f'icml{year}.md'

    home_page = []
    title = []
    author = []
    pdf_link = []

    url = f'{prefix}v{info_dict[year]}'
    data = requests.get(url)
    data.encoding = data.apparent_encoding

    soup = BeautifulSoup(data.text, 'html.parser')
    paper_title_info = soup.find_all('div', class_='paper')
    if not paper_title_info:
        raise Exception('grab error, please check url!')
    for item in paper_title_info:   # 最上面两个除掉
        homepage_link = item.find('p', class_='links').find_all('a')[0].get('href')
        paper_title = item.find('p', class_='title').string.strip()
        print(paper_title)  # debug
        authors = item.find('p', class_='details').find('span', class_='authors').string.strip() if item.find('p', class_='details') else 'No Author'
        link = item.find('p', class_='links').find_all('a')[1].get('href')


        home_page.append(homepage_link)
        title.append(paper_title)
        pdf_link.append(link)
        author.append(authors)

    assert len(author) == len(home_page) == len(title) == len(pdf_link)

    f = open(file_name,'w', encoding='utf-8')
    f.write(f'# {year_title}\n\n')
    for home_page_, title_, author_, pdf_link_ in zip(home_page, title, author, pdf_link):
        f.write(f'- {author_}. **"{title_}"** | [[Home Page]]({home_page_}) | [[PDF]]({pdf_link_}) \n\n\n')
    f.close()
    print(f'[INFO] Writing {file_name} done')