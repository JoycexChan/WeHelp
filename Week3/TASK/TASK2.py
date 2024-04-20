import urllib.request
from bs4 import BeautifulSoup
import csv


def fetch_html(url):
    # 創建一個請求對象，添加用戶代理和cookie
    req = urllib.request.Request(
        url,
        headers={
            'cookie': 'over18=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    )
    with urllib.request.urlopen(req) as response:
        html = response.read()
    return html

def parse_articles_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    article_divs = soup.find_all('div', class_='r-ent')
    for div in article_divs:
        try:
            title_tag = div.find('div', class_='title').find('a')
            if title_tag:
                title = title_tag.text.strip()
                link = 'https://www.ptt.cc' + title_tag['href']
                article_html = fetch_html(link)
                article_soup = BeautifulSoup(article_html, 'html.parser')
                like_dislike = div.find('div', class_='nrec').text.strip()
                if like_dislike == '':
                    like_dislike = '0'  # 如果沒有抓到任何資料，設為0
                meta_value = article_soup.find_all('span', class_='article-meta-value')
                publish_time = meta_value[3].text if len(meta_value) > 3 else ''
                articles.append({
                    'title': title,
                    'like_dislike_count': like_dislike,
                    'publish_time': publish_time
                })
        except Exception as e:
            print(f"Error processing entry: {str(e)}")
    return articles

def get_previous_page_link(soup):
    # 尋找上一頁的連結
    controls = soup.find('div', class_='btn-group btn-group-paging')
    prev_link = controls.find_all('a')[1]['href']
    return 'https://www.ptt.cc' + prev_link if prev_link else None

def save_articles_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(['ArticleTitle', 'Like/DislikeCount', 'PublishTime']) # 注釋掉這一行將不寫入標題
        for article in articles:
            writer.writerow([article['title'], article['like_dislike_count'], article['publish_time']])

base_url = 'https://www.ptt.cc/bbs/Lottery/index.html'
all_articles = []
current_url = base_url

for _ in range(3):  # 迭代三次來抓取三頁的數據
    html_content = fetch_html(current_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = parse_articles_from_html(html_content)
    all_articles.extend(articles)
    current_url = get_previous_page_link(soup)
    if not current_url:
        break

save_articles_to_csv(all_articles, 'article.csv')
