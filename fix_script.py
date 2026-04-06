import os
import re

files = [
    'frontend/advaith_industries_home/code.html',
    'frontend/advaith_product_catalog/code.html',
    'frontend/about_advaith_industries/code.html',
    'frontend/contact_advaith_industries/code.html'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Logo div with a
    content = re.sub(
        r'<div([^>]*class="[^"]*text-xl font-bold tracking-tight text-\[#00327d\][^"]*"[^>]*)>(.*?)</div>',
        r'<a href="/"\1>\2</a>',
        content,
        flags=re.DOTALL
    )

    # Remove Mobile Menu Icon
    content = re.sub(
        r'<!-- Mobile Menu Icon.*?<div class="md:hidden text-primary">\s*<span class="material-symbols-outlined">menu</span>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # Fix Blob Z-index
    content = content.replace('-z-10 transition-transform', 'z-[9999] opacity-30 mix-blend-multiply transition-transform')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
