import discord
import asyncio
import datetime
import itertools
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Khởi tạo colorama
init()

colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

ascii_art = r"""
 _                          _          ____          _
| |      ___   _ __    ___ | | _   _  | __ )   ___  | |_
| |     / _ \ | '_ \  / _ \| || | | | |  _ \  / _ \ | __|
| |___ | (_) || | | ||  __/| || |_| | | |_) || (_) || |_
|_____| \___/ |_| |_| \___||_| \__, | |____/  \___/  \__|
                               |___/
"""

def print_chroma(text):
    cycle_colors = itertools.cycle(colors)
    result = ""
    for char in text:
        if char.strip():  # có ký tự
            result += next(cycle_colors) + char + Style.RESET_ALL
        else:  # giữ khoảng trắng
            result += char
    print(result)

print_chroma(ascii_art)

class FixedAutoLevelBot:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.channel_id = os.getenv("DISCORD_CHANNEL_ID")  # Đã thay channel id
        self.client = discord.Client()
        self.is_running = False
        
        self.client.event(self.on_ready)
        self.client.event(self.on_connect)
        self.client.event(self.on_disconnect)
        self.client.event(self.on_error)
        
    async def on_connect(self):
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đã kết nối đến Discord...")
        
    async def on_ready(self):
        print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã đăng nhập thành công: {self.client.user}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} User: {self.client.user.name}")
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} ID: {self.client.user.id}")
        
        # Đặt status "Đang chơi Lonely Hub" với logo từ Imgur
        try:
            # Sử dụng Streaming activity để có thể thêm logo
            activity = discord.Streaming(
                name="Lonely Hub", 
                url="https://dsc.gg/lonelyhub",
                assets={
                    'large_image': 'https://i.imgur.com/TWW22k4.jpeg',  # Thay bằng URL Imgur thật
                    'large_text': 'Lonely Hub Inc',
                    'small_image': 'https://i.imgur.com/W3w50x4.jpeg',   # Logo nhỏ (tùy chọn)
                    'small_text': 'LongHip12'
                }
            )
            await self.client.change_presence(status=discord.Status.online, activity=activity)
            print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã đặt status với logo: Đang chơi Lonely Hub")
        except Exception as e:
            # Fallback nếu streaming không work
            try:
                activity = discord.Game(name="Lonely Hub")
                await self.client.change_presence(status=discord.Status.online, activity=activity)
                print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã đặt status: Đang chơi Lonely Hub")
            except Exception as e2:
                print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Lỗi khi đặt status: {e2}")
        
        # Bắt đầu auto level
        await self.start_auto_level()
    
    async def on_disconnect(self):
        print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Đã ngắt kết nối")
        
    async def on_error(self, event, *args, **kwargs):
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi sự kiện {event}: {args} {kwargs}")
    
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
                    print(f"{Fore.RED}[Error]{Style.RESET_ALL} Không tìm thấy channel! Kiểm tra lại channel_id")
                    await asyncio.sleep(60)
                    continue
                
                print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Lần {count}: Đang gửi text...")
                
                # Gửi !level
                message = await channel.send("hello")
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã gửi text lúc {current_time}")
                
                # Đợi 5 giây
                print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đợi 5 giây...")
                await asyncio.sleep(5)
                
                # Xóa tin nhắn
                await message.delete()
                print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Đã xóa tin nhắn")
                
                # Chờ 1 phút cho lần tiếp theo
                next_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M:%S")
                print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Chờ 1 phút... Lần tiếp theo: {next_time}")
                await asyncio.sleep(60 - 5)
                
            except discord.errors.HTTPException as e:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi HTTP: {e}")
                await asyncio.sleep(300)
            except Exception as e:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi khác: {e}")
                await asyncio.sleep(300)
    
    async def run(self):
        """Chạy bot với xử lý lỗi chi tiết"""
        try:
            print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đang kết nối...")
            await self.client.start(self.token)
            
        except discord.errors.LoginFailure:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} LOGIN FAILED - Token không hợp lệ!")
            print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Hãy dùng token mới từ lần login thành công!")
            
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}[Warn]{Style.RESET_ALL} Dừng bot...")
            self.is_running = False
            await self.client.close()
            
        except Exception as e:
            print(f"{Fore.RED}[Error]{Style.RESET_ALL} Lỗi không xác định: {e}")
            
# Test token trước khi chạy
def test_token():
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Kiểm tra token...")
    token = os.getenv("DISCORD_TOKEN")
    
    if not token or token == "token_của_bạn":
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Chưa thay token mới!")
        return False
        
    if len(token) < 50:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Token quá ngắn, có thể không đúng")
        return False
        
    print(f"{Fore.GREEN}[Info]{Style.RESET_ALL} Token có vẻ đúng định dạng")
    return True

async def main():
    if test_token():
        bot = FixedAutoLevelBot()
        await bot.run()
    else:
        print(f"{Fore.RED}[Error]{Style.RESET_ALL} Chưa thay token mới!")

if __name__ == "__main__":
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Discord Auto Level Bot - FIXED")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đảm bảo đã thay token mới và channel_id")
    asyncio.run(main())
