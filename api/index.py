import os
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "6LcOPqksAAAAAL8MMC6rb4PDYnir3Uti_knPO4GS")
WHATSAPP_NUMBER = "919949190246"

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/data?table=<name>
# General-purpose table fetch used by all frontend pages on load.
# Allowed tables are explicitly whitelisted for security.
# ─────────────────────────────────────────────────────────────────────────────

ALLOWED_TABLES = {"products", "contacts", "categories", "inquiries"}


@app.route("/api/data", methods=["GET", "POST"])
def manage_data():
    if not supabase:
        return jsonify({"error": "Supabase client not configured."}), 503

    if request.method == "POST":
        # Check payload size (limit to 100KB to prevent DDoS/Memory issues)
        if request.content_length and request.content_length > 102400:
            return jsonify({"error": "Payload too large"}), 413
            
        try:
            data = request.get_json(silent=False)
            if data is None:
                return jsonify({"error": "Invalid or empty JSON payload"}), 400
        except Exception:
            return jsonify({"error": "Malformed JSON in request body"}), 400

        # Validate that we have some data
        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400

        table_name = request.args.get("table", "inquiries")
        if table_name not in ALLOWED_TABLES:
            return jsonify({"error": f"Table '{table_name}' is not writable."}), 400

        # Basic type validation for common fields
        for key, value in data.items():
            if not isinstance(value, str) and value is not None:
                return jsonify({"error": f"Field '{key}' must be a string."}), 400
            if isinstance(value, str) and len(value) > 5000:
                return jsonify({"error": f"Field '{key}' exceeds maximum length."}), 400

        try:
            response = supabase.table(table_name).insert(data).execute()
            return jsonify({"success": True, "data": response.data}), 201
        except Exception as e:
            # Handle duplicates or other DB errors
            error_msg = str(e)
            if "duplicate key" in error_msg.lower():
                return jsonify({"error": "Duplicate entry detected"}), 409
            return jsonify({"error": error_msg}), 500

    # GET logic
    table_name = request.args.get("table", "products")
    if table_name not in ALLOWED_TABLES:
        return jsonify({"error": f"Table '{table_name}' is not accessible."}), 400

    try:
        response = supabase.table(table_name).select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/products
# Fetch products, with optional ?category=<name> filter.
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/products")
def get_products():
    if not supabase:
        return jsonify({"error": "Supabase client not configured."}), 503

    try:
        category = request.args.get("category")
        query = supabase.table("products").select("*").order("created_at", desc=True)
        if category:
            query = query.eq("category", category)
        response = query.execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/contact
# Save a contact form submission to the `contacts` Supabase table.
# Expected JSON body: { name, company, email, message }
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    company = data.get("company", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "name, email, and message are required."}), 400

    if not supabase:
        return jsonify({
            "success": True,
            "note": "Supabase not configured — message not persisted."
        })

    try:
        response = supabase.table("contacts").insert({
            "name": name,
            "company": company,
            "email": email,
            "message": message,
        }).execute()

        record_id = response.data[0].get("id") if response.data else None
        return jsonify({"success": True, "id": record_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/verify-recaptcha", methods=["POST"])
def verify_recaptcha():
    data = request.get_json(silent=True) or {}
    token = data.get("token")
    
    if not token:
        return jsonify({"success": False, "error": "No token provided"}), 400
        
    try:
        verify_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": RECAPTCHA_SECRET_KEY,
                "response": token
            }
        )
        result = verify_response.json()
        
        if result.get("success"):
            # Construct WA URL on backend to hide number from frontend
            # We assume form data is sent along or we just return the template
            result["whatsapp_base"] = f"https://wa.me/{WHATSAPP_NUMBER}?text="
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/healthz
# Simple health check — useful for Vercel deployment verification.
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/healthz")
def healthz():
    return jsonify({
        "status": "ok",
        "supabase_connected": supabase is not None,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Local dev entrypoint (not used by Vercel — Vercel imports `app` directly)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
