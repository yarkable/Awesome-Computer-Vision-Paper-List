import requests
from bs4 import BeautifulSoup

prefix = 'https://papers.nips.cc' #'https://www.ecva.net/'


for year in range(2022, 2024):

    year_title = f'NeurIPS{year}'
    file_name = f'nips{year}.md'

    home_page = []
    title = []
    author = []
    pdf_link = []
    info_dict = dict()

    url = f'{prefix}/paper/{year}'
    data = requests.get(url)
    data.encoding = data.apparent_encoding

    soup = BeautifulSoup(data.text, 'html.parser')
    paper_title_info = soup.find_all('li')
    if not paper_title_info:
        raise Exception('grab error, please check url!')
    for item in paper_title_info[2:]:   # 最上面两个除掉
        homepage_link = prefix + item.find('a').get('href')
        hash = homepage_link.split('/')[-1].split('-')[0]
        paper_title = item.find('a').string.strip()
        authors = item.find('i').string.strip() if item.find('i').string else 'No Author'
        link = f'{prefix}/paper/{year}/file/{hash}-Paper.pdf'


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