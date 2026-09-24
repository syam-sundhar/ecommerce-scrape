import csv
import os
import html

def escape(text):
    if not text:
        return ""
    return html.escape(str(text))

def build_site():
    dataset_path = 'dataset.csv'
    
    products = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
            
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-commerce Product Scraping Project | Practice Dataset Store</title>
    <meta name="description" content="A comprehensive e-commerce product dataset and mock store designed for students and developers practicing web scraping projects, BeautifulSoup, and data extraction.">
    <meta name="keywords" content="ecommerce website designed for web scraping students, dummy ecommerce website for college project, ecommerce scraping website no anti bot, fake ecommerce site product data web scraping, practice website for BeautifulSoup ecommerce scraping, ecommerce product catalog scraping practice, dummy ecommerce website for web scraping, fake ecommerce website for scraping practice, ecommerce website dummy data scraping, test ecommerce website for students, ecommerce scraping practice website, mock ecommerce website products, sample ecommerce product website, fake online store for web scraping, ecommerce dataset website for scraping, product catalog website for web scraping, BeautifulSoup ecommerce scraping practice website, BeautifulSoup fake ecommerce website, Python web scraping practice ecommerce site, web scraping sandbox ecommerce products, static ecommerce website for web scraping">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="E-commerce Product Scraping Project | Practice Dataset Store">
    <meta property="og:description" content="A comprehensive e-commerce product dataset and mock store designed for students and developers practicing web scraping projects.">
    <meta property="og:type" content="website">
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
            content-visibility: auto;
            contain-intrinsic-size: 1px 300px;
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
    </style>
</head>
<body class="text-gray-800 antialiased">
    <header class="glass-header sticky top-0 z-50 p-4 shadow-sm">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                ScrapeStore
            </h1>
            <nav class="text-sm font-medium text-gray-600">
                Total Products: {len(products)}
            </nav>
        </div>
    </header>

    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6" id="product-list">
"""

    for p in products:
        img_url = p.get('image_links', '')
        if ',' in img_url:
            img_url = img_url.split(',')[0].strip()
        
        title = escape(p.get('title', ''))
        selling_price = escape(p.get('selling_price', ''))
        mrp = escape(p.get('mrp', ''))
        cat1 = escape(p.get('category_1', ''))
        cat2 = escape(p.get('category_2', ''))
        rating = escape(p.get('product_rating', ''))
        seller = escape(p.get('seller_name', ''))
        
        html_content += f"""
        <div class="product-card bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 flex flex-col">
            <div class="relative pt-[100%] bg-gray-50">
                <img src="{img_url}" alt="{title}" class="absolute top-0 left-0 w-full h-full object-contain p-4" loading="lazy">
                <span class="absolute top-2 right-2 bg-white/80 backdrop-blur text-xs font-semibold px-2 py-1 rounded-full text-blue-600 border border-blue-100">
                    ★ {rating if rating else 'N/A'}
                </span>
            </div>
            <div class="p-4 flex-1 flex flex-col">
                <p class="text-xs text-indigo-500 font-medium mb-1 truncate">{cat1} > {cat2}</p>
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

    html_content += """
        </div>
    </main>
    <footer class="mt-16 bg-white border-t border-gray-200 py-8 text-center text-gray-500 text-sm">
        <p>Created for web scraping practice with BeautifulSoup.</p>
    </footer>
</body>
</html>
"""
    filepath = 'index.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Successfully generated single '{filepath}' file in the root directory.")

if __name__ == '__main__':
    build_site()
