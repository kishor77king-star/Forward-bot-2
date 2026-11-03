import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters

# --- RENDER 24/7 DUMMY SERVER ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Userbot is active and watching for deals!")
        
    # HEAD requests valla vache '501 Unsupported method' error fix
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# --------------------------------

# --- USERBOT SETTINGS ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")

source_env = os.environ.get("SOURCE_CHANNEL", "").strip()
SOURCE_CHANNELS = [ch.strip() for ch in source_env.split(",") if ch.strip()]

CONVERTER_BOT = os.environ.get("CONVERTER_BOT", "").strip()

app = Client("affiliate_userbot", session_string=SESSION, api_id=API_ID, api_hash=API_HASH)

# Multiple photos (albums) ni track cheyadaniki chinna memory list
processed_groups = []

@app.on_message(filters.chat(SOURCE_CHANNELS))
async def send_to_converter(client, message):
    try:
        # Message lo multiple photos unte...
        if message.media_group_id:
            if message.media_group_id in processed_groups:
                return # Already pampisina group aithe aapeyali
            
            processed_groups.append(message.media_group_id)
            if len(processed_groups) > 50:
                processed_groups.pop(0) # Memory full avvakunda pathavi delete chestham
                
            # Album mottanni okesari copy chestundi
            await client.copy_media_group(CONVERTER_BOT, message.chat.id, message.id)
            print(f"Album deal successfully copied to {CONVERTER_BOT}")
            
        # Normal single photo leda text message aithe...
        else:
            await message.copy(CONVERTER_BOT)
            print(f"Single deal successfully copied to {CONVERTER_BOT}")
            
    except Exception as e:
        print(f"Error copying message: {e}")

print(f"Userbot is watching channels: {SOURCE_CHANNELS}")

# Auto-reconnect loop (Connection Lost error fix)
while True:
    try:
        app.run()
    except Exception as e:
        print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
        time.sleep(5)
