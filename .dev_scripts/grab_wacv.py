import requests
from bs4 import BeautifulSoup


prefix = 'https://openaccess.thecvf.com/' #'https://www.ecva.net/'


for year in range(2020, 2022):
    url = f'https://openaccess.thecvf.com/WACV{year}'
    year_title = f'WACV{year}'
    file_name = f'wacv{year}.md'
    ###############################################################
    home_page = []
    title = []
    author = []
    pdf_link = []
    ###############################################################

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