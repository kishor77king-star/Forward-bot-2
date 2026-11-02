import os
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

# Multiple channels support
source_env = os.environ.get("SOURCE_CHANNEL", "").strip()
SOURCE_CHANNELS = [ch.strip() for ch in source_env.split(",") if ch.strip()]

CONVERTER_BOT = os.environ.get("CONVERTER_BOT", "").strip()

app = Client("affiliate_userbot", session_string=SESSION, api_id=API_ID, api_hash=API_HASH)

# Ikkada 'async' mariyu 'await' add chesam
@app.on_message(filters.chat(SOURCE_CHANNELS))
async def send_to_converter(client, message):
    try:
        await message.copy(CONVERTER_BOT)
        print(f"Deal successfully copied to {CONVERTER_BOT}")
    except Exception as e:
        print(f"Error copying message: {e}")

print(f"Userbot is watching channels: {SOURCE_CHANNELS}")
app.run()
