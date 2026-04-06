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
    html = html.replace('object-contain p-6', 'max-h-full max-w-full object-contain p-6 transition-all duration-500 group-hover:scale-105')
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
        content = f.read()
    
    # Extract the header part (everything before the grid)
    header_part = re.split(r'<div class="grid grid-cols-1 md:grid-cols-12 gap-8">', content)[0]
    if len(header_part) == len(content): # fallback if class differs
        header_part = re.split(r'<div class="grid grid-cols-1 md:grid-cols-12 gap-6">', content)[0]
    
    # Reconstruct grid
    grid_start = '<div class="grid grid-cols-1 md:grid-cols-12 gap-8 justify-center">'
    
    new_cards = []
    for name, link in assets.items():
        card = f"""
<!-- Product: {name} -->
<div class="md:col-span-4 group bg-surface-container-lowest/90 rounded-2xl transition-all duration-500 hover:shadow-2xl border border-outline/5 hover:border-primary/20 flex flex-col overflow-hidden">
    <div class="h-64 bg-surface-container-highest/10 overflow-hidden w-full flex items-center justify-center p-8 group-hover:bg-primary/5 transition-colors">
        <img alt="{name}" class="max-h-full max-w-full object-contain drop-shadow-2xl transition-all duration-700 group-hover:scale-110" src="{link}"/>
    </div>
    <div class="p-8">
        <span class="text-[10px] font-bold uppercase tracking-[0.25em] text-primary mb-3 block opacity-60">Industrial Component</span>
        <h3 class="text-xl font-bold text-on-background mb-3 group-hover:text-primary transition-colors leading-tight">{name}</h3>
        <p class="text-secondary text-sm leading-relaxed line-clamp-2 opacity-80">Precision-engineered high-performance component manufactured to exacting industrial standards.</p>
        <a href="/contact" class="mt-8 inline-flex items-center gap-2 text-xs font-extra-bold text-primary hover:gap-4 transition-all uppercase tracking-widest">
            Inquire Now <span class="material-symbols-outlined text-sm">arrow_forward</span>
        </a>
    </div>
</div>
"""
        new_cards.append(card)

    footer = """
</main>
<!-- Footer -->
<footer class="w-full border-t border-[#c3c6d5]/15 bg-[#f7f9fb] dark:bg-slate-950 font-['Manrope'] text-sm tracking-wide">
<div class="flex flex-col md:flex-row justify-between items-center py-12 px-8 max-w-7xl mx-auto gap-6">
<div class="text-lg font-black text-[#00327d] dark:text-blue-400">
                Advaith Industries
            </div>
<div class="flex flex-wrap justify-center gap-8 text-[#515f74]">
<a class="hover:text-[#00327d] hover:underline" href="#">Privacy Policy</a>
<a class="hover:text-[#00327d] hover:underline" href="#">Terms of Service</a>
</div>
<div class="text-[#515f74]">
                © 2024 Advaith Industries. All rights reserved.
            </div>
</div>
</footer>
<!-- Mobile Navigation Shell -->
<div id="mobile-bottom-nav" class="md:hidden fixed bottom-6 left-1/2 -translate-x-1/2 w-[90%] bg-surface/90 backdrop-blur-xl shadow-2xl rounded-full px-6 py-3 flex justify-around items-center border border-outline-variant/10 z-[60]">
<a class="flex flex-col items-center gap-1 text-secondary" href="/"><span class="material-symbols-outlined">home</span><span class="text-[10px] font-bold uppercase">Home</span></a>
<a class="flex flex-col items-center gap-1 text-[#00327d]" href="/products"><span class="material-symbols-outlined">inventory_2</span><span class="text-[10px] font-bold uppercase">Products</span></a>
<a class="flex flex-col items-center gap-1 text-secondary" href="/about"><span class="material-symbols-outlined">factory</span><span class="text-[10px] font-bold uppercase">Facility</span></a>
<a class="flex flex-col items-center gap-1 text-secondary" href="/contact"><span class="material-symbols-outlined">mail</span><span class="text-[10px] font-bold uppercase">Contact</span></a>
</div>
<div id="blob" class="hidden md:block pointer-events-none fixed top-0 left-0 w-[400px] h-[400px] bg-primary/20 rounded-full blur-[100px] z-[9999] opacity-30 mix-blend-multiply transition-transform duration-[50ms] ease-out will-change-transform"></div>
<style>
    #mobile-bottom-nav { transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
</style>
<script>
  let lastScrollY = window.scrollY;
  const mobileNav = document.getElementById('mobile-bottom-nav');
  if (mobileNav) {
    window.addEventListener('scroll', () => {
      const currentScrollY = window.scrollY;
      if (currentScrollY > lastScrollY && currentScrollY > 100) {
        mobileNav.style.transform = 'translate(-50%, 150%)'; 
      } else {
        mobileNav.style.transform = 'translate(-50%, 0)'; 
      }
      lastScrollY = currentScrollY;
    });
  }
  const blob = document.getElementById('blob');
  if (blob) {
    window.addEventListener('mousemove', (e) => {
      requestAnimationFrame(() => blob.style.transform = `translate(${e.clientX - 200}px, ${e.clientY - 200}px)`);
    });
  }
</script>
</body></html>
"""
    final_html = header_part + grid_start + "".join(new_cards) + "</div>" + footer
    with open('frontend/advaith_product_catalog/code.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

update_home()
update_catalog()
