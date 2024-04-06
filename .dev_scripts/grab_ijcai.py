import requests
from bs4 import BeautifulSoup

prefix = 'https://www.ijcai.org'

# ijcai 2016-2017 年用一個大 p 包裹所有信息

# for year in range(2016,2017):
#
#     year_title = f'IJCAI{year}'
#     file_name = f'ijcai{year}.md'
#
#     home_page = []
#     title = []
#     author = []
#     pdf_link = []
#     info_dict = dict()
#
#     url = f'{prefix}/proceedings/{year}'
#     data = requests.get(url)
#     data.encoding = data.apparent_encoding
#
#     soup = BeautifulSoup(data.text, 'html.parser')
#     [x.decompose() for x in soup.select('strong')]  # 删除这标签
#     [x.decompose() for x in soup.select('br')]
#     paper_title_info = soup.find_all('p')
#     if not paper_title_info:
#         raise Exception('grab error, please check url!')
#     for item in paper_title_info[7: -2]:   # 最上面两个除掉
#         homepage_link = prefix + item.find_all('a')[1].get('href')
#         try:
#             paper_title = item.next.split('/')[0][:-1].strip()
#         except:
#             small_title = item.next.next
#             big_title = item.next.next
#             paper_title = (small_title + big_title).split('/')[0][:-1].strip()
#         print(paper_title) # debug
#         authors = item.find('i').string.strip() if item.find('i').string else 'No Author'
#         lk_ = item.find_all('a')[0].get('href')
#         link = f'{prefix}{lk_}'
#
#
#         home_page.append(homepage_link)
#         title.append(paper_title)
#         pdf_link.append(link)
#         author.append(authors)
#
#     assert len(author) == len(home_page) == len(title) == len(pdf_link)
#
#     f = open(file_name,'w', encoding='utf-8')
#     f.write(f'# {year_title}\n\n')
#     for home_page_, title_, author_, pdf_link_ in zip(home_page, title, author, pdf_link):
#         f.write(f'- {author_}. **"{title_}"** | [[Home Page]]({home_page_}) | [[PDF]]({pdf_link_}) \n\n\n')
#     f.close()
#     print(f'[INFO] Writing {file_name} done')

# ijcai 2018年以後改了樣式

for year in range(2022,2024):

    year_title = f'IJCAI{year}'
    file_name = f'ijcai{year}.md'

    home_page = []
    title = []
    author = []
    pdf_link = []
    info_dict = dict()

    url = f'{prefix}/proceedings/{year}'
    data = requests.get(url)
    data.encoding = data.apparent_encoding

    soup = BeautifulSoup(data.text, 'html.parser')
    [x.decompose() for x in soup.select('strong')]  # 删除这标签
    [x.decompose() for x in soup.select('br')]
    paper_title_info = soup.find_all('div', class_='title')
    if not paper_title_info:
        raise Exception('grab error, please check url!')
    author_info = soup.find_all('div', class_='authors')
    details_info = soup.find_all('div', class_='details')

    assert len(author) == len(home_page) == len(title) == len(pdf_link)

    for (title_, author_, details_) in zip(paper_title_info, author_info, details_info):
        paper_title = title_.string.strip()
        print(paper_title)  # debug
        authors = author_.string.strip()
        lk_ = details_.find_all('a')[0].get('href')
        hp_ = details_.find_all('a')[1].get('href')
        link = f'{prefix}/proceedings/{year}/{lk_}'
        home_page_link = f'{prefix}{hp_}'

        home_page.append(home_page_link)
        title.append(paper_title)
        pdf_link.append(link)
        author.append(authors)


    f = open(file_name, 'w', encoding='utf-8')
    f.write(f'# {year_title}\n\n')
    for home_page_, title_, author_, pdf_link_ in zip(home_page, title, author, pdf_link):
        f.write(f'- {author_}. **"{title_}"** | [[Home Page]]({home_page_}) | [[PDF]]({pdf_link_}) \n\n\n')
    f.close()
    print(f'[INFO] Writing {file_name} done')


