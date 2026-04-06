import json
import re

assets = {
    "HV Bushing Clamps": "/assets/HV Bushing Clamps.jpeg",
    "LV Epoxy Bushings": "/assets/LV Epoxy Bushings.jpeg",
    "Air Release Plug": "/assets/Air Release Plug.jpeg",
    "Arching Horns": "/assets/Arching Horns.jpeg",
    "Bi-Metallic Connectors": "/assets/Bi-Metallic Connectors.jpeg",
    "Bi-Metallic Connectors (Alt Angle)": "/assets/Bi-Metallic Connecters 2.jpeg",
    "Bushing Clamp and Aluminum Members": "/assets/Bushing Clamp and Aluminum Members.jpeg",
    "Oil Filling Caps": "/assets/Oil Filling Caps.jpeg",
    "Secondary Terminals": "/assets/Secondary Terminals.jpeg"
}

def fix_image_classes(html):
    html = html.replace('object-cover', 'object-contain p-6')
    return html

def update_home():
    with open('frontend/advaith_industries_home/code.html', 'r', encoding='utf-8') as f:
        html = f.read()
Port 5000 is default; make sure it doesn't conflict? No, frontend is static.
        
    html = fix_image_classes(html)
    
    # Replace HV Bushing Clamps image
    html = re.sub(
        r'(<img alt="HV Bushing Clamps"[^>]*)src="[^"]+"',
        rf'\1src="{assets["HV Bushing Clamps"]}"',
        html
    )
    
    # Replace LV Epoxy Bushings image
    html = re.sub(
        r'(<img alt="LV Epoxy Bushings"[^>]*)src="[^"]+"',
        rf'\1src="{assets["LV Epoxy Bushings"]}"',
        html
    )
    
    # Add view all button
    view_all_html = """
<div class="flex justify-center mt-12 mb-12">
    <a href="/products" class="border-2 border-primary text-primary px-10 py-4 rounded-lg font-bold text-lg hover:bg-primary hover:text-on-primary transition-all duration-300">View All Products</a>
</div>
    """
    if "View All Products" not in html:
        html = html.replace('<!-- Values / Facility Section -->', view_all_html + '\n<!-- Values / Facility Section -->')
        
    with open('frontend/advaith_industries_home/code.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_catalog():
    with open('frontend/advaith_product_catalog/code.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    html = fix_image_classes(html)
    
    # Replace standard images
    # HV Bushing Clamps (First featured product)
    html = re.sub(
        r'(<h2 class="text-3xl font-bold text-on-background mb-4">Hv bushing clamps</h2>.*?<img alt="Industrial Metal Components"[^>]*)src="[^"]+"',
        rf'\1src="{assets["HV Bushing Clamps"]}"',
        html,
        flags=re.DOTALL
    )
    
    # LV Epoxy Bushings
    html = re.sub(
        r'(<img alt="Electrical Bushings"[^>]*)src="[^"]+"(.*Lv Epoxy bushings</h3>)',
        rf'\1src="{assets["LV Epoxy Bushings"]}"\2',
        html,
        flags=re.DOTALL
    )
    
    # Check if catalog has already been updated to avoid duplicates
    if "Ancillary Services" in html and "Air Release Plug" not in html:
        # Create new product cards
        new_cards = []
        new_items = ["Air Release Plug", "Arching Horns", "Bi-Metallic Connectors", "Bi-Metallic Connectors (Alt Angle)", "Bushing Clamp and Aluminum Members", "Oil Filling Caps", "Secondary Terminals"]
        
        for name in new_items:
            img_src = assets[name]
            card = f"""
<!-- Product: {name} -->
<div class="md:col-span-4 group bg-surface-container-lowest rounded transition-all duration-500 hover:shadow-[0px_20px_40px_rgba(0,50,125,0.06)] flex flex-col items-center">
<div class="aspect-square bg-surface-container-highest overflow-hidden w-full">
<img alt="{name}" class="w-full h-full object-contain p-6 transition-slow group-hover:scale-110" src="{img_src}"/>
</div>
<div class="p-8 w-full">
<span class="text-[10px] font-bold uppercase tracking-widest text-secondary mb-2 block">Industrial Assorted</span>
<h3 class="text-xl font-bold text-on-background mb-2">{name}</h3>
<p class="text-secondary text-sm line-clamp-2">High-quality precision-engineered component designed to meet robust industrial standards.</p>
</div>
</div>
"""
            new_cards.append(card)
        
        html = html.replace('<!-- Capability Statement -->', ''.join(new_cards) + '\n<!-- Capability Statement -->')

    with open('frontend/advaith_product_catalog/code.html', 'w', encoding='utf-8') as f:
        f.write(html)

update_home()
update_catalog()
