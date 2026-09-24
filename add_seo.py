import os
import glob
import re
from datetime import datetime

site_dir = 'site'
base_url = 'https://ecommerce-scrape-opal.vercel.app' # I will tell them to update this

# SEO Metadata to inject
seo_tags = """
    <!-- SEO Tags -->
    <meta name="google-site-verification" content="V_-grCcQCBGEfc7HZu91aoVMrcVZPCbL73zxPY1z-hQ" />
    <meta name="description" content="A comprehensive e-commerce product dataset and mock store designed for students and developers practicing web scraping projects, BeautifulSoup, and data extraction.">
    <meta name="keywords" content="ecommerce product scraping project, web scraping practice site, ecommerce dataset, python web scraping tutorial, beautifulsoup scraping practice, ecommerce scraper, mock ecommerce site for scraping">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="E-commerce Product Scraping Project | Practice Dataset Store">
    <meta property="og:description" content="A comprehensive e-commerce product dataset and mock store designed for students and developers practicing web scraping projects.">
    <meta property="og:type" content="website">
    <!-- End SEO Tags -->
"""

html_files = glob.glob(os.path.join(site_dir, '*.html'))

print(f"Found {len(html_files)} HTML files. Injecting SEO tags...")

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if we already injected SEO tags to avoid duplicates
    if "<!-- SEO Tags -->" not in content:
        # Inject right after <head>
        content = content.replace('<head>', f'<head>\n{seo_tags}', 1)
        
        # Optionally, improve the title if it's too generic
        content = re.sub(r'<title>(.*?)</title>', r'<title>\1 | E-Commerce Scraping Project Practice</title>', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("SEO tags injected into all HTML files.")

# Generate robots.txt
robots_content = f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""
with open(os.path.join(site_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_content)
print("Generated robots.txt")

# Generate sitemap.xml
today = datetime.now().strftime('%Y-%m-%d')
sitemap_urls = []
for filepath in html_files:
    filename = os.path.basename(filepath)
    # Give index.html a higher priority
    priority = "1.0" if filename == 'index.html' else "0.8"
    sitemap_urls.append(f"""  <url>
    <loc>{base_url}/{filename}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>
"""
with open(os.path.join(site_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_content)
print("Generated sitemap.xml")
