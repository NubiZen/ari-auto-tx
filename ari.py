import requests
import random
import time  # Untuk jeda waktu
from colorama import Fore, Style, init

init()

ANDROID_USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
]

# Fungsi log
def log(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

# Fungsi login
def login(email, password, headers, proxy=None):
    url = "https://arichain.io/api/account/signin_mobile"
    payload = {
        'blockchain': "testnet",
        'email': email,
        'pw': password,
        'lang': "en",
        'device': "app",
        'is_mobile': "Y"
    }
    
    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxies)
        response.raise_for_status()
        result = response.json()
        return result.get("status") == "success"
    except requests.RequestException:
        return False

# Fungsi auto transfer
def auto_transfer(email, password, to_address, headers, proxy=None):
    url = "https://arichain.io/api/wallet/transfer_mobile"
    payload = {
        'blockchain': "testnet",
        'symbol': "ARI",
        'email': email,
        'to_address': to_address,
        'pw': password,
        'amount': "1",
        'memo': "",
        'valid_code': "",
        'lang': "en",
        'device': "app",
        'is_mobile': "Y"
    }

    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxies)
        response.raise_for_status()
        result = response.json()
        if result.get("status") == "success" and result.get("result") == "success":
            log(f"[SUCCESS] Tx berhasil ke {to_address}.", Fore.GREEN)
            return True
        else:
            log(f"[FAILED] Tx gagal ke {to_address}.", Fore.RED)
            return False
    except requests.RequestException:
        log(f"[ERROR] Gagal mengirim Tx ke {to_address}.", Fore.RED)
        return False

# Fungsi auto check-in
def auto_checkin(address, headers, proxy=None):
    url = "https://arichain.io/api/event/checkin"
    payload = {
        'blockchain': "testnet",
        'address': address,
        'lang': "en",
        'device': "app",
        'is_mobile': "Y"
    }

    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxies)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            log("[SUCCESS] Check-in berhasil.", Fore.GREEN)
            return True
        elif data.get("status") == "already":
            log("[INFO] Sudah check-in sebelumnya.", Fore.YELLOW)
            return True
        else:
            log("[FAILED] Check-in sudah di lakukan.", Fore.RED)
            return False
    except requests.RequestException:
        log("[ERROR] Gagal melakukan check-in.", Fore.RED)
        return False

# Fungsi utama
def main():
    print(Fore.CYAN + "\n=== Ari Wallet Auto Transfer ===" + Style.RESET_ALL)

    # Memuat akun dari file
    try:
        with open("accounts.txt", "r") as file:
            accounts = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        log("[ERROR] File 'accounts.txt' tidak ditemukan!", Fore.RED)
        return

    if not accounts:
        log("[ERROR] File 'accounts.txt' kosong!", Fore.RED)
        return

    # Memeriksa format akun
    formatted_accounts = []
    for account in accounts:
        try:
            email, password, address, private_key = account.split("|")
            formatted_accounts.append((email, password, address, private_key))
        except ValueError:
            log(f"[ERROR] Format salah: {account}", Fore.RED)

    if len(formatted_accounts) < 2:
        log("[ERROR] Jumlah akun di 'accounts.txt' harus lebih dari satu untuk transfer!", Fore.RED)
        return

    # Memuat proxy
    try:
        with open("proxy.txt", "r") as proxy_file:
            proxies = [line.strip() for line in proxy_file if line.strip()]
    except FileNotFoundError:
        proxies = []

    # Header untuk permintaan HTTP
    headers = {
        'Accept': "application/json",
        'Accept-Encoding': "gzip",
        'User-Agent': random.choice(ANDROID_USER_AGENTS)
    }

    # Loop utama
    while True:
        for i, (email, password, address, _) in enumerate(formatted_accounts):
            # Login
            if not login(email, password, headers, proxy=random.choice(proxies) if proxies else None):
                log(f"[FAILED] Login gagal untuk akun {email}.", Fore.RED)
                continue

            # Check-in
            auto_checkin(address, headers, proxy=random.choice(proxies) if proxies else None)

            # Transfer ke semua akun berikutnya
            for j, (_, _, to_address, _) in enumerate(formatted_accounts[i + 1:], start=1):
                auto_transfer(email, password, to_address, headers, proxy=random.choice(proxies) if proxies else None)

            time.sleep(50)  # Jeda 50 detik setiap akun

        time.sleep(86400)  # Jeda 24 jam

if __name__ == "__main__":
    main()