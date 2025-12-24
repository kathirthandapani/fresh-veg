import os
import re

# Configuration
base_dir = r"c:\Users\Boobalan\OneDrive\Desktop\kathir\stitch_the_interactive_soil_shop"
output_file = os.path.join(base_dir, "index.html")

pages = [
    {"folder": "the__living__homepage", "id": "home", "title": "Home"},
    {"folder": "the__interactive_soil__shop", "id": "shop", "title": "Shop"},
    {"folder": "impact_dashboard", "id": "impact", "title": "Impact"},
    {"folder": "root-to-table_traceability_page", "id": "traceability", "title": "Traceability"},
    {"folder": "seasonal_flavor_cycles", "id": "seasonal", "title": "Seasonal"},
    {"folder": "the_anatomy_of_a_veggie", "id": "anatomy", "title": "Anatomy"},
    {"folder": "the_chef’s_canvas", "id": "chef", "title": "Chef"},
    {"folder": "the_kitchen_laboratory", "id": "kitchen", "title": "Kitchen Lab"},
    {"folder": "the_smart-bin_subscription_manager", "id": "subscription", "title": "Subscription"},
    {"folder": "zero-waste_bulk_shop", "id": "bulk", "title": "Bulk Shop"},
]

# Common Head Content
head_content = set()
head_section = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stitch Soil Shop - Unified Experience</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#0df259",
                        "background-light": "#f5f8f6",
                        "background-dark": "#102216",
                        "surface-dark": "#1A2C20",
                        "text-secondary": "#9cbaa6",
                    },
                    fontFamily: {
                        "display": ["Manrope", "sans-serif"]
                    },
                    borderRadius: {"DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "full": "9999px"},
                },
            },
        }
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
    <style>
        /* Global Navigation Styles */
        #global-nav {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 2147483647; /* Maximum Z-Index */
            background: rgba(16, 34, 22, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 12px 24px;
            border-radius: 50px;
            display: flex;
            gap: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            max-width: 90vw;
            overflow-x: auto;
        }
        #global-nav button {
            color: rgba(255,255,255,0.7);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            transition: all 0.2s;
            font-family: 'Manrope', sans-serif;
            cursor: pointer;
        }
        #global-nav button:hover {
            color: white;
            background: rgba(255,255,255,0.1);
        }
        #global-nav button.active {
            background: #0df259;
            color: #102216;
        }
        .page-section {
            display: none;
            min-height: 100vh;
            animation: fadeIn 0.5s ease;
        }
        .page-section.active {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
"""

# Extract body content
page_sections = []

for page in pages:
    file_path = os.path.join(base_dir, page["folder"], "code.html")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
        # Extract Style tags to add to head (simple regex)
        styles = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
        for style in styles:
            head_content.add(f"<style>{style}</style>")

        # Extract Body content
        # We assume body tag exists.
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if body_match:
            body_inner = body_match.group(1)
            # Remove scripts that might conflict (tailwind)
            body_inner = re.sub(r'<script.*?tailwind.*?</script>', '', body_inner, flags=re.DOTALL)
            
            section_html = f"""
            <section id="{page['id']}" class="page-section {'active' if page['id'] == 'home' else ''}">
                {body_inner}
            </section>
            """
            page_sections.append(section_html)

# Build Navigation
nav_html = '<div id="global-nav">'
for page in pages:
    active_class = "active" if page["id"] == "home" else ""
    nav_html += f'<button class="{active_class}" onclick="switchPage(\'{page["id"]}\')">{page["title"]}</button>'
nav_html += '</div>'


# Build Script for switching
script_html = """
<script>
    // Page ID Mapping for Internal Links
    const pageMap = {
        'home': 'home',
        'living': 'home',
        'shop': 'shop',
        'market': 'shop',
        'impact': 'impact',
        'dashboard': 'impact',
        'sustainability': 'impact', // Mapped Sustainability to Impact
        'traceability': 'traceability',
        'farm': 'traceability',
        'farms': 'traceability', // Mapped Farms to Traceability
        'seasonal': 'seasonal',
        'anatomy': 'anatomy',
        'chef': 'chef',
        'canvas': 'chef',
        'kitchen': 'kitchen',
        'lab': 'kitchen',
        'my kitchen': 'kitchen', // Mapped My Kitchen to Kitchen Lab
        'subscription': 'subscription',
        'smart-bin': 'subscription',
        'bulk': 'bulk',
        'zero-waste': 'bulk'
    };

    function switchPage(pageId) {
        // Hide all sections
        document.querySelectorAll('.page-section').forEach(el => {
            el.classList.remove('active');
        });
        // Show target section
        const target = document.getElementById(pageId);
        if (target) {
            target.classList.add('active');
        }
        
        // Update nav
        document.querySelectorAll('#global-nav button').forEach(el => {
            el.classList.remove('active');
            if (el.getAttribute('onclick').includes(pageId)) {
                el.classList.add('active');
            }
        });
        
        window.scrollTo(0,0);
    }

    // Auto-Rectify Navigation: Intercept all link clicks
    document.addEventListener('click', function(e) {
        // Find closest anchor tag
        const link = e.target.closest('a');
        if (link) {
            // Get text content recursively
            const text = link.innerText.toLowerCase().trim();
            const href = link.getAttribute('href');
            
            // Allow default if it's an external link
            if (href && href.startsWith('http') && !href.includes(window.location.hostname)) return;

            // Prevent default behavior (especially jumping to top)
            e.preventDefault();
            
            // Try to match text to a page
            let foundId = null;
            // Check exact text matches first
            for (const [key, id] of Object.entries(pageMap)) {
                if (text === key || text.includes(key)) {
                    foundId = id;
                    break;
                }
            }
            
            // Fallback: Check if href implies a page
            if (!foundId && href) {
                if (href.includes('shop')) foundId = 'shop';
                else if (href.includes('home')) foundId = 'home';
            }

            if (foundId) {
                console.log("Auto-Rectifying Navigation to: " + foundId);
                switchPage(foundId);
            } else {
                console.log("No navigation mapping found for: " + text);
                // Optional: Provide feedback or route to home
            }
        }
    });
</script>
"""

# Assemble Final HTML
final_html = head_section + "\n".join(head_content) + "</head>\n<body class='bg-background-dark text-white'>\n" + nav_html + "\n<div id='app-container'>\n" + "\n".join(page_sections) + "\n</div>\n" + script_html + "\n</body>\n</html>"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Successfully created {output_file}")
