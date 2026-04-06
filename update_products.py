import json
import re

def get_direct_link(drive_id):
    # Using the google drive thumbnail API which is reliable for direct image display
    return f"https://drive.google.com/thumbnail?id={drive_id}&sz=w1000"

assets = {
    "Air Release Plug": get_direct_link("1ef7xBbJofnii6jOGWOGfxRPBreuInAHl"),
    "Arching Horns": get_direct_link("1xO_l96rEqo7-QP_DJbhrsy4oBDIoChgb"),
    "Bi-Metallic Connectors": get_direct_link("1fuCxHI3pFvgSa-h2BCNe8BmUcNSGGKQZ"),
    "Bi-Metallic Connectors (Alt Angle)": get_direct_link("10uGSsyQwaTiNi59xhd4-7M5eenJSXZa3"),
    "Bushing Clamps and Aluminum Members": get_direct_link("1caip8wJ3v44J0JniK0oIkf46Ats-E4BH"),
    "HV Bushing Clamps": get_direct_link("1WD57Hwa2PYy_NTghKHPZPRToVcIwvo4i"),
    "LV Epoxy Bushing": get_direct_link("10rQIVDA6qg9ToU-fN3jaEsrjddLNehe6"),
    "Oil Filling Clamps": get_direct_link("17goOvhqbxsE6VhsH44bkXWczndxlUXiF"),
    "Secondary Terminals": get_direct_link("1yxRDao1CKewdBam_MuzqXS5fIsEhyiGS"),
}

def fix_image_classes(html):
    # Fix the main product cards to not be huge. Use a fixed height for consistency.
    # Replace aspect-square with a fixed max height container
    # Before: <div class="aspect-square bg-surface-container-highest overflow-hidden w-full">
    # After: <div class="h-64 bg-surface-container-highest/20 overflow-hidden w-full flex items-center justify-center p-4">
    html = html.replace('aspect-square bg-surface-container-highest overflow-hidden w-full', 'h-72 bg-surface-container-highest/30 overflow-hidden w-full flex items-center justify-center p-4 rounded-t-xl group')
    html = html.replace('object-contain p-6', 'max-h-full max-w-full object-contain transition-all duration-500 group-hover:scale-105')
    
    # Fix homepage large card (HV Bushing Clamps)
    # The homepage featured product can still be bigger but needs containment.
    return html

def update_home():
    with open('frontend/advaith_industries_home/code.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = fix_image_classes(html)
    
    # Update src for Home featured images
    html = re.sub(r'(<img alt="HV Bushing Clamps"[^>]*)src="[^"]+"', rf'\1src="{assets["HV Bushing Clamps"]}"', html)
    html = re.sub(r'(<img alt="LV Epoxy Bushings"[^>]*)src="[^"]+"', rf'\1src="{assets["LV Epoxy Bushing"]}"', html)
    
    with open('frontend/advaith_industries_home/code.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_catalog():
    with open('frontend/advaith_product_catalog/code.html', 'r', encoding='utf-8') as f:
        html = f.read()
Port 5000 is default; make sure it doesn't conflict? No, frontend is static.
    
    # Clear previous custom generated cards to start fresh (avoids duplicates)
    html = re.split(r'<!-- Product: ', html)[0]
    if '<!-- Capability Statement -->' not in html:
        # If we split it away, we need to re-add the end tag
        pass 
    
    # Actually, it's safer to just re-read the original "clean" catalog if possible or use a more robust regex
    # Let's just update existing matched text.
    
    # Update HV Bushing Clamps (First featured product in catalog)
    html = re.sub(
        r'(<h2 class="text-3xl font-bold text-on-background mb-4">Hv bushing clamps</h2>.*?<img alt="Industrial Metal Components"[^>]*)src="[^"]+"',
        rf'\1src="{assets["HV Bushing Clamps"]}"',
        html,
        flags=re.DOTALL
    )
    
    # Update manual cards for standard items
    html = re.sub(r'(<img alt="Electrical Bushings"[^>]*)src="[^"]+"', rf'\1src="{assets["LV Epoxy Bushing"]}"', html)

    # Now add all assets as a clean grid
    new_cards = []
    for name, link in assets.items():
        card = f"""
<!-- Product: {name} -->
<div class="md:col-span-4 group bg-surface-container-lowest/80 rounded-xl transition-all duration-500 hover:shadow-[0px_20px_40px_rgba(0,50,125,0.1)] border border-outline/5 hover:border-primary/20 flex flex-col overflow-hidden">
    <div class="h-64 md:h-72 bg-surface-container-highest/20 overflow-hidden w-full flex items-center justify-center p-6 group-hover:bg-primary/5 transition-colors">
        <img alt="{name}" class="max-h-full max-w-full object-contain drop-shadow-xl transition-all duration-700 group-hover:scale-110" src="{link}"/>
    </div>
    <div class="p-8">
        <span class="text-[10px] font-bold uppercase tracking-[0.2em] text-primary mb-3 block opacity-70">Industrial Portfolio</span>
        <h3 class="text-xl font-bold text-on-background mb-3 group-hover:text-primary transition-colors">{name}</h3>
        <p class="text-secondary text-sm leading-relaxed line-clamp-3">Precision machined component built for reliability and high-performance industrial applications. Manufactured to exacting standards.</p>
        <a href="/contact" class="mt-6 inline-flex items-center gap-2 text-xs font-bold text-primary group-hover:gap-4 transition-all">
            Inquire Details <span class="material-symbols-outlined text-sm">arrow_forward</span>
        </a>
    </div>
</div>
"""
        new_cards.append(card)

    # Inject into grid
    # Looking for the main grid container start
    grid_target = '<div class="grid grid-cols-1 md:grid-cols-12 gap-6">'
    final_html = html.split(grid_target)[0] + grid_target + "\n" + "".join(new_cards) + "\n" + '</div>\n<!-- Capability Statement -->'
    
    # Need to keep the footer and end of file
    # For now, I'll just write it back with the footer I know is there.
    
    with open('frontend/advaith_product_catalog/code.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

# Simple check to finish the HTML file since my split might have eaten the rest
def append_footer():
    footer_text = """
</main>
<!-- Footer -->
<footer class="w-full border-t border-[#c3c6d5]/15 bg-[#f7f9fb] dark:bg-slate-950 font-['Manrope'] text-sm tracking-wide">
<div class="flex flex-col md:flex-row justify-between items-center py-12 px-8 max-w-7xl mx-auto gap-6">
<div class="text-lg font-black text-[#00327d] dark:text-blue-400">
                Advaith Industries
            </div>
<div class="flex flex-wrap justify-center gap-8">
<a class="text-[#515f74] hover:text-[#00327d] hover:underline transition-all" href="#">Privacy Policy</a>
<a class="text-[#515f74] hover:text-[#00327d] hover:underline transition-all" href="#">Terms of Service</a>
<a class="text-[#515f74] hover:text-[#00327d] hover:underline transition-all" href="#">Sustainability</a>
<a class="text-[#515f74] hover:text-[#00327d] hover:underline transition-all" href="#">Careers</a>
</div>
<div class="text-[#515f74]">
                © 2024 Advaith Industries. All rights reserved.
            </div>
</div>
</footer>
<!-- Mobile Navigation Shell (Visible only on mobile) -->
<div id="mobile-bottom-nav" class="md:hidden fixed bottom-6 left-1/2 -translate-x-1/2 w-[90%] bg-surface/90 backdrop-blur-xl shadow-2xl rounded-full px-6 py-3 flex justify-around items-center border border-outline-variant/10 z-[60]">
<a class="flex flex-col items-center gap-1 text-secondary" href="/">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">home</span>
<span class="text-[10px] font-bold uppercase">Home</span>
</a>
<a class="flex flex-col items-center gap-1 text-[#00327d]" href="/products">
<span class="material-symbols-outlined">inventory_2</span>
<span class="text-[10px] font-bold uppercase">Products</span>
</a>
<a class="flex flex-col items-center gap-1 text-secondary" href="/about">
<span class="material-symbols-outlined">factory</span>
<span class="text-[10px] font-bold uppercase">Facility</span>
</a>
<a class="flex flex-col items-center gap-1 text-secondary" href="/contact">
<span class="material-symbols-outlined">mail</span>
<span class="text-[10px] font-bold uppercase">Contact</span>
</a>
</div>
<!-- Custom Interactions -->
<div id="blob" class="hidden md:block pointer-events-none fixed top-0 left-0 w-[400px] h-[400px] bg-primary/20 rounded-full blur-[100px] z-[9999] opacity-30 mix-blend-multiply transition-transform duration-[50ms] ease-out will-change-transform"></div>
<style>
    #mobile-bottom-nav { transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
    .btn-interactive { transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    .btn-interactive:active { transform: scale(0.92) !important; }
</style>
<script>
  const blob = document.getElementById('blob');
  if (blob) {
    window.addEventListener('mousemove', (e) => {
      requestAnimationFrame(() => blob.style.transform = `translate(${e.clientX - 200}px, ${e.clientY - 200}px)`);
    });
  }
  let lastScrollY = window.scrollY;
  const mobileNav = document.getElementById('mobile-bottom-nav');
  if (mobileNav) {
    window.addEventListener('scroll', () => {
      const currentScrollY = window.scrollY;
      if (currentScrollY > lastScrollY && currentScrollY > 100) {
        mobileNav.style.transform = 'translate(-50%, 150%)'; // hide
      } else {
        mobileNav.style.transform = 'translate(-50%, 0)'; // show
      }
      lastScrollY = currentScrollY;
    }, { passive: true });
  }
</script>
</body></html>
"""
    with open('frontend/advaith_product_catalog/code.html', 'a', encoding='utf-8') as f:
        f.write(footer_text)

update_home()
update_catalog()
append_footer()
