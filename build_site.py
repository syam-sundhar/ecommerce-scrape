import csv
import os
import html
import math
import shutil
from datetime import datetime

PRODUCTS_PER_PAGE = 50
SITE_DIR = 'site'
BASE_URL = 'https://ecommerce-scrape-opal.vercel.app'


def escape(text):
    if not text:
        return ""
    return html.escape(str(text))


def escape_attr(text):
    """Escape text for use in HTML data attributes."""
    if not text:
        return ""
    return html.escape(str(text), quote=True)


def build_product_card(p):
    """Build the HTML for a single product card with ALL dataset fields."""
    img_url = p.get('image_links', '')
    if ',' in img_url:
        img_url = img_url.split(',')[0].strip()

    title = escape(p.get('title', ''))
    selling_price = escape(p.get('selling_price', ''))
    mrp = escape(p.get('mrp', ''))
    cat1 = escape(p.get('category_1', ''))
    cat2 = escape(p.get('category_2', ''))
    cat3 = escape(p.get('category_3', ''))
    rating = escape(p.get('product_rating', ''))
    seller = escape(p.get('seller_name', ''))
    seller_rating = escape(p.get('seller_rating', ''))
    description = escape_attr(p.get('description', ''))
    highlights = escape_attr(p.get('highlights', ''))

    return f"""
            <div class="product-card bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 flex flex-col"
                 data-category3="{cat3}"
                 data-seller-rating="{seller_rating}"
                 data-description="{description}"
                 data-highlights="{highlights}">
                <div class="relative pt-[100%] bg-gray-50">
                    <img src="{img_url}" alt="{title}" class="absolute top-0 left-0 w-full h-full object-contain p-4" loading="lazy">
                    <span class="absolute top-2 right-2 bg-white/80 backdrop-blur text-xs font-semibold px-2 py-1 rounded-full text-blue-600 border border-blue-100">
                        ★ {rating if rating else 'N/A'}
                    </span>
                </div>
                <div class="p-4 flex-1 flex flex-col">
                    <p class="text-xs text-indigo-500 font-medium mb-1 truncate">{cat1} &gt; {cat2}</p>
                    <h3 class="text-sm font-semibold text-gray-900 mb-2 line-clamp-2" title="{title}">{title}</h3>
                    <div class="mt-auto">
                        <div class="flex items-center gap-2 mb-2">
                            <span class="text-lg font-bold text-gray-900">{selling_price}</span>
                            <span class="text-xs text-gray-500 line-through">{mrp}</span>
                        </div>
                        <p class="text-xs text-gray-500 truncate">Sold by: {seller}</p>
                    </div>
                </div>
            </div>
"""


def build_page_html(products, page_num, total_pages, total_products, is_root=False):
    """Build a complete HTML page with products and pagination."""
    seo_block = ""
    if page_num == 1:
        seo_block = f"""
    <meta name="google-site-verification" content="V_-grCcQCBGEfc7HZu91aoVMrcVZPCbL73zxPY1z-hQ" />
    <meta name="description" content="A comprehensive e-commerce product dataset and mock store designed for students and developers practicing web scraping projects, BeautifulSoup, and data extraction.">
    <meta name="keywords" content="ecommerce data for web scraping, ecommerce dataset for students, web scraping practice website, product data for web scraping, ecommerce dataset for college projects, product price dataset, web scraping dataset, ecommerce product dataset, product data scraping, ecommerce data scraping practice, web scraping project for students, ecommerce project dataset, web scraping college project, data science project dataset, Python web scraping project, BeautifulSoup web scraping project, ecommerce data science project, product price analysis project, web scraping project using Python, ecommerce dataset for data science students, BeautifulSoup practice website, BeautifulSoup web scraping dataset, Python web scraping practice, Python ecommerce scraping, learn web scraping with Python, web scraping with BeautifulSoup, BeautifulSoup ecommerce data, Python scraping project for beginners, web scraping practice for beginners, product price analysis dataset, ecommerce price dataset, product price comparison dataset, product reviews dataset, product ratings dataset, ecommerce sales dataset, product analytics dataset, product information dataset, price tracking dataset, ecommerce product analysis">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{BASE_URL}/">
    <meta property="og:title" content="E-commerce Product Scraping Project | Practice Dataset Store">
    <meta property="og:description" content="A comprehensive e-commerce product dataset and mock store designed for students and developers practicing web scraping projects.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{BASE_URL}/">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "ScrapeStore - E-commerce Product Scraping Project",
        "url": "{BASE_URL}",
        "description": "A comprehensive e-commerce product dataset and mock store with {total_products} products designed for students and developers practicing web scraping projects."
    }}
    </script>"""
    else:
        seo_block = f"""
    <meta name="description" content="Page {page_num} of {total_pages} - Browse products for web scraping practice.">
    <meta name="robots" content="index, follow">"""

    title = "E-commerce Product Scraping Project | Practice Dataset Store" if page_num == 1 else f"E-Commerce Data Store - Page {page_num} | E-Commerce Scraping Project Practice"

    # Build pagination links
    if is_root:
        # Root index.html links to site/page_X.html
        prev_link = f'<a href="site/page_{page_num - 1}.html" class="page-btn page-btn-inactive">&larr; Previous</a>' if page_num > 1 else '<span class="page-btn page-btn-disabled">Previous</span>'
        next_link = f'<a href="site/page_{page_num + 1}.html" class="page-btn page-btn-inactive">Next &rarr;</a>' if page_num < total_pages else '<span class="page-btn page-btn-disabled">Next</span>'
    else:
        # site/ pages link to sibling pages
        if page_num == 2:
            prev_href = "../index.html"
        else:
            prev_href = f"page_{page_num - 1}.html"
        prev_link = f'<a href="{prev_href}" class="page-btn page-btn-inactive">&larr; Previous</a>' if page_num > 1 else '<span class="page-btn page-btn-disabled">Previous</span>'
        next_link = f'<a href="page_{page_num + 1}.html" class="page-btn page-btn-inactive">Next &rarr;</a>' if page_num < total_pages else '<span class="page-btn page-btn-disabled">Next</span>'

    # Build page number links
    page_links = ""
    pages_to_show = set()
    pages_to_show.add(1)
    pages_to_show.add(total_pages)
    for i in range(max(1, page_num - 2), min(total_pages + 1, page_num + 3)):
        pages_to_show.add(i)
    
    last_shown = 0
    for p in sorted(pages_to_show):
        if last_shown and p > last_shown + 1:
            page_links += '            <span class="page-btn page-btn-disabled">...</span>\n'
        if p == page_num:
            page_links += f'            <span class="page-btn page-btn-active">{p}</span>\n'
        else:
            if is_root:
                href = "index.html" if p == 1 else f"site/page_{p}.html"
            else:
                href = "../index.html" if p == 1 else f"page_{p}.html"
            page_links += f'            <a href="{href}" class="page-btn page-btn-inactive">{p}</a>\n'
        last_shown = p

    products_html = ""
    for p in products:
        products_html += build_product_card(p)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>{seo_block}
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background-color: #f3f4f6;
            font-family: 'Inter', sans-serif;
        }}
        .glass-header {{
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        }}
        .product-card {{
            transition: all 0.3s ease;
        }}
        .product-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }}
        .line-clamp-2 {{
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .page-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 40px;
            height: 40px;
            padding: 0 12px;
            border-radius: 8px;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.2s;
        }}
        .page-btn-active {{
            background: #2563eb;
            color: white;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
        }}
        .page-btn-inactive {{
            background: white;
            color: #374151;
            border: 1px solid #e5e7eb;
        }}
        .page-btn-inactive:hover {{
            background: #f3f4f6;
            border-color: #d1d5db;
        }}
        .page-btn-disabled {{
            background: #f3f4f6;
            color: #9ca3af;
            cursor: not-allowed;
            border: 1px solid #e5e7eb;
        }}
    </style>
</head>
<body class="text-gray-800 antialiased">
    <header class="glass-header sticky top-0 z-50 p-4 shadow-sm">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                ScrapeStore
            </h1>
            <nav class="text-sm font-medium text-gray-600">
                Page {page_num} of {total_pages} | Total Products: {total_products}
            </nav>
        </div>
    </header>

    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6" id="product-list">
{products_html}
        </div>
        
        <!-- Pagination -->
        <div class="mt-12 flex justify-center items-center gap-2 flex-wrap">
            {prev_link}
{page_links}            {next_link}
        </div>
    </main>
    <footer class="mt-16 bg-white border-t border-gray-200 py-8 text-center text-gray-500 text-sm">
        <p>Created for web scraping practice with BeautifulSoup.</p>
    </footer>
</body>
</html>
"""


def build_site():
    dataset_path = 'dataset.csv'

    # Read all products
    products = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)

    total_products = len(products)
    total_pages = math.ceil(total_products / PRODUCTS_PER_PAGE)
    print(f"Total products: {total_products}")
    print(f"Total pages: {total_pages}")
    print(f"Products per page: {PRODUCTS_PER_PAGE}")

    # Clear and recreate site directory
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR)

    # Generate page 1 as root index.html
    page_products = products[0:PRODUCTS_PER_PAGE]
    page_html = build_page_html(page_products, 1, total_pages, total_products, is_root=True)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"  Generated index.html (page 1, {len(page_products)} products)")

    # Generate remaining pages in site/ directory
    for page_num in range(2, total_pages + 1):
        start = (page_num - 1) * PRODUCTS_PER_PAGE
        end = start + PRODUCTS_PER_PAGE
        page_products = products[start:end]

        page_html = build_page_html(page_products, page_num, total_pages, total_products, is_root=False)
        filepath = os.path.join(SITE_DIR, f'page_{page_num}.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_html)

        if page_num % 50 == 0 or page_num == total_pages:
            print(f"  Generated page_{page_num}.html ({len(page_products)} products)")

    # Generate robots.txt
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/site/sitemap.xml
"""
    with open(os.path.join(SITE_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(robots_content)
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)

    # Generate sitemap.xml
    today = datetime.now().strftime('%Y-%m-%d')
    sitemap_urls = [f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""]
    
    for page_num in range(2, total_pages + 1):
        sitemap_urls.append(f"""  <url>
    <loc>{BASE_URL}/site/page_{page_num}.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>
"""
    with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

    print(f"\nSite built successfully!")
    print(f"  Root: index.html")
    print(f"  Pages: {SITE_DIR}/page_2.html to {SITE_DIR}/page_{total_pages}.html")
    print(f"  Sitemap: {SITE_DIR}/sitemap.xml")
    print(f"  Robots: robots.txt + {SITE_DIR}/robots.txt")


if __name__ == '__main__':
    build_site()
