import requests
from bs4 import BeautifulSoup

# 2020年前的网站布局不一样，fk
prefix = 'https://openreview.net' #'https://www.ecva.net/'

def get(url):
    try:
        res = requests.get(url, timeout=60)
    except:
        res = requests.get(url, timeout=60)
    res.encoding = res.apparent_encoding
    print(f'Finished Get URL: {url}')
    return res.json()['notes']


for year in range(2020, 2022):
    year_title = f'ICLR{year}'
    file_name = f'iclr{year}.md'
    total_1 = f'https://api.openreview.net/notes?invitation=ICLR.cc%2F{year}%2FConference%2F-%2FBlind_Submission&details=replyCount%2Cinvitation%2Coriginal&limit=1000&offset=0'
    total_2 = f'https://api.openreview.net/notes?invitation=ICLR.cc%2F{year}%2FConference%2F-%2FBlind_Submission&details=replyCount%2Cinvitation%2Coriginal&limit=1000&offset=1000'
    total_3 = f'https://api.openreview.net/notes?invitation=ICLR.cc%2F{year}%2FConference%2F-%2FBlind_Submission&details=replyCount%2Cinvitation%2Coriginal&limit=1000&offset=2000'
    res_1 = f'https://api.openreview.net/notes?invitation=ICLR.cc%2F{year}%2FConference%2FPaper.*%2F-%2FDecision&limit=1000&offset=0'
    res_2 = f'https://api.openreview.net/notes?invitation=ICLR.cc%2F{year}%2FConference%2FPaper.*%2F-%2FDecision&limit=1000&offset=1000'
    res_3 = f'https://api.openreview.net/notes?invitation=ICLR.cc%2F{year}%2FConference%2FPaper.*%2F-%2FDecision&limit=1000&offset=2000'
    res_data_1 = get(res_1)
    res_data_2 = get(res_2)
    res_data_3 = get(res_3)
    paper_data_1 = get(total_1)
    paper_data_2 = get(total_2)
    paper_data_3 = get(total_3)
    res_info = {}
    for i in res_data_1+res_data_2+res_data_3:
        res_info[i['id']] = i['content']['decision']
    paper_title_info = paper_data_1+paper_data_2+paper_data_3
    ###############################################################
    home_page = []
    title = []
    author = []
    pdf_link = []
    ###############################################################

    for item in paper_title_info:
        id_ = item['id']
        if 'Reject' in res_info[id_]:
            continue
        homepage_link = f"{prefix}/forum?id={item['id']}"
        paper_title = item['content']['title']
        home_page.append(homepage_link)
        title.append(paper_title)
        authors = ','.join(item['content']['authors'])
        author.append(authors)
        link = f"{prefix}/pdf?id={item['id']}"
        pdf_link.append(link)



    assert len(author) == len(home_page) == len(title) == len(pdf_link)

    f = open(file_name,'w', encoding='utf-8')
    f.write(f'# {year_title}\n\n')
    for home_page_, title_, author_, pdf_link_ in zip(home_page, title, author, pdf_link):
        f.write(f'- {",".join(author_)}. **"{title_}"** | [[Home Page]]({home_page_}) | [[PDF]]({pdf_link_}) \n\n\n')
    f.close()