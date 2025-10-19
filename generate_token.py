import requests

import json

import base64

class DiscordLogin:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

        })

    

    def login_and_get_token(self, email, password, twofa_code=None):

        """Login và lấy token từ Discord"""

        print("🔐 Đang đăng nhập...")

        

        # Lấy fingerprint trước

        fingerprint = self.get_fingerprint()

        if not fingerprint:

            print("❌ Không thể lấy fingerprint")

            return None

        

        # Tạo payload login

        payload = {

            'login': email,

            'password': password,

            'undelete': False,

            'captcha_key': None,

            'login_source': None,

            'gift_code_sku_id': None

        }

        

        headers = {

            'Content-Type': 'application/json',

            'X-Fingerprint': fingerprint

        }

        

        try:

            # Gửi request login

            response = self.session.post(

                'https://discord.com/api/v9/auth/login',

                json=payload,

                headers=headers

            )

            

            print(f"📡 Login response: {response.status_code}")

            

            if response.status_code == 200:

                # Login thành công

                data = response.json()

                token = data.get('token')

                if token:

                    print(f"✅ Login thành công!")

                    print(f"🔑 Token: {token}")

                    return token

                    

            elif response.status_code == 400:

                data = response.json()

                if data.get('captcha_key'):

                    print("❌ Cần giải captcha")

                elif data.get('email'):

                    print("❌ Email không hợp lệ")

                else:

                    print(f"❌ Lỗi: {data}")

                    

            elif response.status_code == 401:

                print("❌ Sai email hoặc mật khẩu")

                

            else:

                print(f"❌ Lỗi {response.status_code}: {response.text}")

                

        except Exception as e:

            print(f"❌ Lỗi kết nối: {e}")

            

        return None

    

    def get_fingerprint(self):

        """Lấy fingerprint từ Discord"""

        try:

            response = self.session.get('https://discord.com/api/v9/experiments')

            if response.status_code == 200:

                data = response.json()

                return data.get('fingerprint')

        except Exception as e:

            print(f"❌ Lỗi lấy fingerprint: {e}")

        return None

    

    def get_user_info(self, token):

        """Lấy thông tin user từ token"""

        headers = {'Authorization': token}

        

        try:

            response = self.session.get('https://discord.com/api/v9/users/@me', headers=headers)

            if response.status_code == 200:

                return response.json()

            else:

                print(f"❌ Token không hợp lệ: {response.status_code}")

                return None

        except Exception as e:

            print(f"❌ Lỗi: {e}")

            return None

# Sử dụng

def manual_login():

    login = DiscordLogin()

    

    print("=== ĐĂNG NHẬP DISCORD ===")

    email = input("📧 Email: ")

    password = input("🔒 Password: ")

    

    token = login.login_and_get_token(email, password)

    

    if token:

        print("\n✅ ĐĂNG NHẬP THÀNH CÔNG!")

        user_info = login.get_user_info(token)

        if user_info:

            print(f"👤 User: {user_info['username']}#{user_info['discriminator']}")

            print(f"🆔 ID: {user_info['id']}")

            print(f"📧 Email: {user_info.get('email', 'N/A')}")

        

        # Lưu token (tùy chọn)

        save = input("\n💾 Lưu token? (y/n): ")

        if save.lower() == 'y':

            with open('token.txt', 'w') as f:

                f.write(token)

            print("✅ Đã lưu token vào token.txt")

    

    return token

if __name__ == "__main__":

    manual_login()