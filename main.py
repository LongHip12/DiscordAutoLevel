import discord
import asyncio
import datetime
import threading
from colorama import init, Fore, Style
from dotenv import load_dotenv
import os
import time
from flask import Flask

# Khởi tạo colorama và load env
init()
load_dotenv()

# Tạo Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Discord Auto Level Bot is Running! 🚀"

@app.route('/status')
def status():
    return {
        "status": "online",
        "service": "Discord Auto Level Bot",
        "timestamp": datetime.datetime.now().isoformat()
    }

def run_flask():
    """Chạy Flask server trong thread riêng"""
    print(f"{Fore.CYAN}[Flask]{Style.RESET_ALL} Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

class FixedAutoLevelBot:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.channel_id = 1409791680864850001
        
        # FIX: Thêm intents đơn giản
        intents = discord.Intents.default()
        self.client = discord.Client(intents=intents)
        self.is_running = False

    async def on_ready(self):
        print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã đăng nhập thành công: {self.client.user}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} User: {self.client.user.name}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} ID: {self.client.user.id}")
        
        # Đặt status
        try:
            activity = discord.Game(name="Lonely Hub")
            await self.client.change_presence(activity=activity)
            print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã đặt status")
        except Exception as e:
            print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Lỗi khi đặt status: {e}")
        
        # Bắt đầu auto level
        await self.start_auto_level()
    
    async def on_disconnect(self):
        print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Đã ngắt kết nối")
        
    async def start_auto_level(self):
        """Bắt đầu auto gửi !level"""
        self.is_running = True
        print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Bắt đầu auto level...")
        
        count = 0
        while self.is_running:
            try:
                count += 1
                channel = self.client.get_channel(self.channel_id)
                
                if not channel:
                    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Không tìm thấy channel!")
                    await asyncio.sleep(60)
                    continue
                
                print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Lần {count}: Đang gửi tin nhắn...")
                
                # Gửi tin nhắn
                message = await channel.send("　　　　　　　　　　")
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã gửi tin nhắn lúc {current_time}")
                
                # Đợi 5 giây
                await asyncio.sleep(5)
                
                # Xóa tin nhắn
                await message.delete()
                print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã xóa tin nhắn")
                
                # Chờ 55 giây cho lần tiếp theo
                next_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M:%S")
                print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Chờ 60 giây... Lần tiếp theo: {next_time}")
                await asyncio.sleep(60)
                
            except discord.errors.HTTPException as e:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi HTTP: {e}")
                await asyncio.sleep(300)
            except Exception as e:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi khác: {e}")
                await asyncio.sleep(300)
    
    async def run_bot(self):
        """Chạy bot"""
        try:
            print(f"{Fore.CYAN}[Discord]{Style.RESET_ALL} Đang kết nối Discord...")
            await self.client.start(self.token)
        except discord.errors.LoginFailure:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Token không hợp lệ!")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Dừng bot...")
            self.is_running = False
            await self.client.close()
        except Exception as e:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi: {e}")

async def main_discord():
    """Chạy Discord bot"""
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Discord Auto Level Bot - FIXED")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đảm bảo đã thay token mới và channel_id")
    
    # Kiểm tra token
    token = os.getenv("DISCORD_TOKEN")
    if not token or len(token) < 50:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Token không hợp lệ!")
        return
        
    print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Token có vẻ đúng định dạng")
    
    bot = FixedAutoLevelBot()
    await bot.run_bot()

def run_discord_bot():
    """Chạy Discord bot trong thread riêng"""
    asyncio.run(main_discord())

if __name__ == "__main__":
    print(f"{Fore.GREEN}[System]{Style.RESET_ALL} Starting both services...")
    
    # Tạo và start thread cho Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Tạo và start thread cho Discord bot
    discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
    discord_thread.start()
    
    print(f"{Fore.GREEN}[System]{Style.RESET_ALL} Both services started!")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Flask: http://localhost:5000")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Discord: Auto Level Bot Running")
    
    # Giữ chương trình chạy
    try:
        while True:
            # Kiểm tra nếu cả 2 thread đều không chạy thì thoát
            if not flask_thread.is_alive() and not discord_thread.is_alive():
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Both services stopped!")
                break
            time.sleep(10)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Shutting down...")