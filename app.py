from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
import os

app = Flask(__name__, static_folder='static')

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Sofia, a warm and professional AI assistant for Bella Tavola, a premium restaurant. You help customers with:

1. MENU QUESTIONS - We serve Italian-inspired cuisine. Starters: Bruschetta (₦3,500), Calamari (₦5,000), Soup of the day (₦3,000). Mains: Grilled Salmon (₦12,000), Pasta Carbonara (₦8,500), Ribeye Steak (₦18,000), Margherita Pizza (₦7,000). Desserts: Tiramisu (₦4,000), Chocolate Lava Cake (₦4,500). Drinks: Fresh Juice (₦2,000), Wine (₦6,000), Water (₦500).

2. RESERVATIONS - Collect the customer's name, date, time, and number of guests. Operating hours: Mon-Sun 11am - 11pm.

3. ORDERS - Help customers place takeaway or delivery orders. Collect their name, phone number, address, and order details.

4. GENERAL INQUIRIES - Address, opening hours, parking, special events.

Always be warm, elegant and professional. Keep responses concise. If collecting info for a reservation or order, ask one question at a time. End every interaction by asking if there's anything else you can help with."""

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        max_tokens=500,
        temperature=0.7
    )
    
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
