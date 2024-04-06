import requests
from bs4 import BeautifulSoup
import re

prefix = 'https://dl.acm.org' #'https://www.ecva.net/'
info_dict = {
	2016: 2964284,
	2017: 3123266,
	2018: 3240508,
	2019: 3343031,
	2020: 3394171,
	2021: 3474085,
	2022: 3503161,
	2023: 3581783,
}
proxy = '127.0.0.1:7890'
proxies = {
	'http': f'http://{proxy}',
	'https': f'https://{proxy}',
}
for year in [2023, 2024]:#[2018, 2019, 2020]:

	year_title = f'ACMMM{year}'
	file_name = f'acmmm{year}.md'

	home_page = []
	title = []
	author = []
	pdf_link = []

	url = f'{prefix}/doi/proceedings/10.1145/{info_dict[year]}/'
	print(url)
	data = requests.get(url)
	data.encoding = data.apparent_encoding

	soup = BeautifulSoup(data.text, 'html.parser')

	global_info = soup.find_all('a', class_='section__title accordion-tabbed__control left-bordered-title')
	if not global_info:
		raise Exception('grab error, please check url!')

	for each_batch_info in global_info:   # 最上面两个除掉
		child_url =  f"{prefix}{each_batch_info.get('href')}"
		batch_data = requests.get(child_url)
		batch_data.encoding = batch_data.apparent_encoding
		child_soup = BeautifulSoup(batch_data.text, 'html.parser')
		single_info = child_soup.find_all('div', class_='issue-item__content-right')
		for item in single_info:
			if item.find('h5').find('sub'):
				print(item.find('h5').find('sub').next.next)
				item.find('h5').find('sub').decompose()
			paper_title = item.find('h5').find('a').text.replace('\n', '')
			paper_title = re.sub(' +', ' ', paper_title)
			# print(paper_title)  # debug
			page = f"{prefix}{item.find('h5').find('a').get('href')}"
			author_wraper = item.find('ul', class_='rlist--inline loa truncate-list')
			authors = ','.join([x.find('a').get('title') for x in author_wraper.find_all('li')])
			link = list(page)
			link.insert(23, 'pdf/')
			link = ''.join(link)

			home_page.append(page)
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
