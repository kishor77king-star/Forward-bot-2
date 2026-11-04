import os
import time
import threading
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters

# --- RENDER 24/7 DUMMY SERVER ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Userbot is active and watching for deals!")
        
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

processed_groups = []

@app.on_message(filters.chat(SOURCE_CHANNELS))
async def send_to_converter(client, message):
    try:
        # Message lo multiple photos unte (Album)
        if message.media_group_id:
            if message.media_group_id in processed_groups:
                return 
            
            processed_groups.append(message.media_group_id)
            if len(processed_groups) > 50:
                processed_groups.pop(0) 
                
            await client.copy_media_group(CONVERTER_BOT, message.chat.id, message.id)
            print(f"Album deal successfully copied to {CONVERTER_BOT}")
            
        # Normal single photo leda text message
        else:
            await message.copy(CONVERTER_BOT)
            print(f"Single deal successfully copied to {CONVERTER_BOT}")
            
    except Exception as e:
        print(f"Error copying message: {e}")

# --- PERMANENT FIX: AUTO-HEALTH CHECKER ---
async def main():
    await app.start()
    print(f"Userbot is watching channels: {SOURCE_CHANNELS}")
    
    while True:
        try:
            # Prathi 5 minutes ki connection check chestundi
            await asyncio.sleep(300)
            await app.get_me() 
        except Exception as e:
            print(f"Telegram Connection Frozen: {e}. Auto-Restarting Server...")
            # Connection cut ayithe idi process ni kill chestundi, Render malli automatic ga kotha server start chestundi.
            os._exit(1)

# Bot ni start chestundi
app.run(main())
