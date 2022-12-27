import requests
from bs4 import BeautifulSoup

prefix = 'https://dblp.org/db/conf/bmvc/bmvc{}.html'


for year in range(2021, 2022):

    year_title = f'BMVC{year}'
    file_name = f'bmvc{year}.md'

    home_page = []
    title = []
    author = []
    pdf_link = []

    url = prefix.format(year)
    data = requests.get(url)
    data.encoding = data.apparent_encoding

    soup = BeautifulSoup(data.text, 'html.parser')
    paper_title_info = soup.find_all('cite', class_='data tts-content')
    paper_link_info = soup.find_all('nav', class_='publ')
    if not paper_title_info:
        raise Exception('grab error, please check url!')
    if not paper_link_info:
        raise Exception('grab error, please check pdf link!')
    for item, pdf in zip(paper_title_info[1:], paper_link_info[1:]):   # 最上面一个除掉
        homepage_link = 'None'
        paper_title = item.find('span', class_="title").text.strip()
        print(paper_title)  # debug
        authors = ','.join([x.string.strip() for x in item.find_all('span', itemprop="name")[:-1]])
        try:
            link = pdf.find_all('div', class_='head')[0].find('a').get('href')
        except:
            link = 'unavailable!'


        home_page.append(homepage_link)
        title.append(paper_title)
        pdf_link.append(link)
        author.append(authors)

    assert len(author) == len(home_page) == len(title) == len(pdf_link)

    f = open(file_name,'w', encoding='utf-8')
    f.write(f'# {year_title}\n\n')
    for title_, author_, pdf_link_ in zip(title, author, pdf_link):
        f.write(f'- {author_}. **"{title_}"** | [[PDF]]({pdf_link_}) \n\n\n')
    f.close()
    print(f'[INFO] Writing {file_name} done')