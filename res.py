from bs4 import BeautifulSoup
import requests
import os

def get_url(url):
    headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    res = requests.get(url,headers = headers)
    res.encoding = res.apparent_encoding
    if res.status_code ==200:
        return res.text
    return None

def downloads(name,link):
    path = 'photo'
    if os.path.exists(path):
        os.mkdir(path)
    try:
        for photo_name ,photo_link in zip(name,link):
            filename = photo_name +'.jpg'
            res = requests.get(photo_link)             
            with open(filename,'wb') as f:
                f.write(res.content)
            print(filename,'download down!')
    except requests.ConnectionError:
        print('failed to saved!')
            
def save_links(html):
    names = []
    link = []
    soups = BeautifulSoup(html,'lxml')
    soups = soups.find_all(attrs = { "class":"related"})
    for soup in soups:        
        soup = soup.select('div img')         
        for links in soup:            
            names.append(links['alt'])
            link.append(links['src'])
    return downloads(names,link)       

             
def main():
    url = "https://www.lnlnl.cn/post/5698.html"
    html = get_url(url)
    links = save_links(html)

if __name__ =='__main__':
    main()
