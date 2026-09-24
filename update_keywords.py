import glob, re

keywords = 'ecommerce website designed for web scraping students, dummy ecommerce website for college project, ecommerce scraping website no anti bot, fake ecommerce site product data web scraping, practice website for BeautifulSoup ecommerce scraping, ecommerce product catalog scraping practice, dummy ecommerce website for web scraping, fake ecommerce website for scraping practice, ecommerce website dummy data scraping, test ecommerce website for students, ecommerce scraping practice website, mock ecommerce website products, sample ecommerce product website, fake online store for web scraping, ecommerce dataset website for scraping, product catalog website for web scraping, BeautifulSoup ecommerce scraping practice website, BeautifulSoup fake ecommerce website, Python web scraping practice ecommerce site, web scraping sandbox ecommerce products, static ecommerce website for web scraping'

for f in glob.glob('site/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords}">', content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print("Keywords updated successfully.")
