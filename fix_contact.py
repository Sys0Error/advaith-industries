import os
import re

files = [
    'frontend/advaith_industries_home/code.html',
    'frontend/advaith_product_catalog/code.html',
    'frontend/about_advaith_industries/code.html',
    'frontend/contact_advaith_industries/code.html'
]

# 1. Shrink Get Started button across ALL pages.
# Target: px-6 py-2 -> px-4 py-1.5, text-xs
navbar_old = r'px-6 py-2 rounded-lg font-semibold hover:scale-105 active:scale-95 transition-all duration-300'
navbar_new = r'px-4 py-1.5 rounded-md font-bold text-xs hover:scale-105 active:scale-95 transition-all duration-300'

# Also handle the variant in About page
navbar_old_about = r'px-5 py-2 rounded-lg font-semibold text-sm shadow-lg'
navbar_new_about = r'px-4 py-1.5 rounded-md font-bold text-xs shadow-lg'

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(navbar_old, navbar_new)
    content = content.replace(navbar_old_about, navbar_new_about)
    content = content.replace('advaithindustries167@gmail.com', 'advaithindustries167@gmail.com') # already done maybe?
    
    # Update Email universally
    # Regex to catch older email if any placeholder existed
    content = re.sub(r'[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]{2,}', 'advaithindustries167@gmail.com', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Fix Homepage "Contact Us Today" mobile centering
home_path = 'frontend/advaith_industries_home/code.html'
with open(home_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target: the contact section on home. Search for "Contact Us Today"
# Looking for the div containing the button
content = content.replace(
    'class="bg-surface-container-lowest text-primary px-10 py-5 rounded-lg font-black text-xl hover:scale-105 transition-transform duration-300 shadow-xl whitespace-nowrap inline-block"',
    'class="bg-surface-container-lowest text-primary px-10 py-5 rounded-xl font-black text-xl hover:scale-105 transition-transform duration-300 shadow-xl whitespace-nowrap inline-block mx-auto md:mx-0"'
)
# Ensure its parent container is centered on mobile
content = content.replace(
    '<div class="flex flex-wrap gap-4">',
    '<div class="flex flex-wrap justify-center md:justify-start gap-4">'
)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Update Contact Page Logic & UI
contact_path = 'frontend/contact_advaith_industries/code.html'
with open(contact_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Phone Number Field
phone_field = """
<div>
<label class="block text-sm font-bold text-secondary mb-2" for="phone">Phone Number</label>
<input class="w-full bg-surface-container-low border-none rounded-xl px-6 py-4 focus:ring-2 focus:ring-primary/20 transition-all" id="phone" placeholder="+91 00000 00000" type="tel"/>
</div>
"""
if 'id="phone"' not in content:
    # Inject it before the message textarea
    content = content.replace('<label class="block text-sm font-bold text-secondary mb-2" for="message">', phone_field + '\n<label class="block text-sm font-bold text-secondary mb-2" for="message">')

# Update Map Iframe to a more "proper" location (Peenya, Bangalore)
new_map = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15549.336495147576!2d77.5029315809756!3d13.01438903333333!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae3d8438289569%3A0xcf7ba9c28690f055!2sPeenya%20Industrial%20Area%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1712398000000!5m2!1sen!2sin'
content = re.sub(r'src="https://www\.google\.com/maps/embed[^"]+"', f'src="{new_map}"', content)

# WhatsApp Submit Logic
wa_script = """
    function submitInquiry(event) {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const message = document.getElementById('message').value;
        
        const text = `*New Inquiry | Advaith Industries*%0A%0A*Name:* ${name}%0A*Email:* ${email}%0A*Phone:* ${phone}%0A*Message:* ${message}`;
        const whatsappUrl = `https://wa.me/919980164673?text=${text}`; // Using placeholder number, modify if needed
        
        window.open(whatsappUrl, '_blank');
    }
"""

content = re.sub(r'async function loadData\(\) \{.*?\}', wa_script, content, flags=re.DOTALL)
content = content.replace('<form class="space-y-6">', '<form class="space-y-6" onsubmit="submitInquiry(event)">')

# Remove support phone number
content = re.sub(r'\+1\s*\(555\)\s*000-0000', '', content)
content = content.replace('Secondary Support', '')
content = content.replace('Emergency: +1 (555) 999-9999', '')

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(content)
