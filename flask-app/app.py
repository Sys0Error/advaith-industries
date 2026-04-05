import os
from flask import Flask, jsonify, request, send_file, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="frontend", static_url_path="/frontend")
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully.")
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not set. Supabase features will be unavailable.")


# ─────────────────────────────────────────────────────────────────────────────
# Frontend routes — serve the HTML pages
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return send_file("frontend/advaith_industries_home/code.html")


@app.route("/about")
def about():
    return send_file("frontend/about_advaith_industries/code.html")


@app.route("/products")
def products():
    return send_file("frontend/advaith_product_catalog/code.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        company = request.form.get("company", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            return render_template_string(
                "<p>Missing required fields. Please go back and fill in all fields.</p>"
            ), 400

        if supabase:
            try:
                supabase.table("contacts").insert({
                    "name": name,
                    "company": company,
                    "email": email,
                    "message": message,
                }).execute()
            except Exception as e:
                print(f"Error saving contact: {e}")

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Thank You | Advaith Industries</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet"/>
            <style>body { font-family: 'Manrope', sans-serif; }</style>
        </head>
        <body class="bg-[#f7f9fb] flex items-center justify-center min-h-screen">
            <div class="text-center max-w-lg px-6">
                <div class="text-5xl mb-6">✅</div>
                <h1 class="text-3xl font-bold text-[#00327d] mb-4">Inquiry Received</h1>
                <p class="text-[#515f74] text-lg mb-8">Thank you, {{ name }}. We've received your message and will respond within 24 hours.</p>
                <a href="/" class="bg-[#00327d] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#0047ab] transition-all">Back to Home</a>
            </div>
        </body>
        </html>
        """, name=name)

    return send_file("frontend/contact_advaith_industries/code.html")


# ─────────────────────────────────────────────────────────────────────────────
# API routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/data")
def get_data():
    if not supabase:
        return jsonify({"error": "Supabase client not configured. Set SUPABASE_URL and SUPABASE_KEY."}), 503

    table_name = request.args.get("table", "products")
    allowed_tables = {"products", "contacts", "categories", "inquiries"}
    if table_name not in allowed_tables:
        return jsonify({"error": f"Table '{table_name}' is not accessible."}), 400

    try:
        response = supabase.table(table_name).select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/products")
def get_products():
    if not supabase:
        return jsonify({"error": "Supabase client not configured."}), 503
    try:
        category = request.args.get("category")
        query = supabase.table("products").select("*")
        if category:
            query = query.eq("category", category)
        response = query.execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    company = data.get("company", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "name, email, and message are required."}), 400

    if supabase:
        try:
            response = supabase.table("contacts").insert({
                "name": name,
                "company": company,
                "email": email,
                "message": message,
            }).execute()
            return jsonify({"success": True, "id": response.data[0].get("id") if response.data else None})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"success": True, "note": "Supabase not configured — message not persisted."})


@app.route("/api/healthz")
def healthz():
    return jsonify({
        "status": "ok",
        "supabase_connected": supabase is not None,
    })


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
