import requests
import random
import time
from colorama import Fore, Style, init

init()

ANDROID_USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
]

def log(message, color=Fore.WHITE, prefix="INFO"):
    print(f"{color}[{prefix}] {message}{Style.RESET_ALL}")

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
        if result.get("status") == "success":
            log(f"Berhasil login ke akun {email}.", Fore.GREEN, "LOGIN SUCCESS")
            return True
        else:
            log(f"Gagal login ke akun {email}.", Fore.RED, "LOGIN FAILED")
            return False
    except requests.RequestException:
        log(f"Terjadi kesalahan saat login ke akun {email}.", Fore.RED, "LOGIN ERROR")
        return False

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
            log(f"Send berhasil 1 ke {to_address}.", Fore.GREEN, "TRANSFER SUCCESS")
            return True
        else:
            log(f"Send gagal ke {to_address}.", Fore.RED, "TRANSFER FAILED")
            return False
    except requests.RequestException:
        log(f"Kesalahan saat mengirim Tx ke {to_address}.", Fore.RED, "TRANSFER ERROR")
        return False

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
            log("Check-in berhasil.", Fore.GREEN, "CHECK-IN SUCCESS")
            return True
        elif data.get("status") == "already":
            log("Sudah check-in sebelumnya.", Fore.YELLOW, "CHECK-IN INFO")
            return True
        else:
            log("Check-in gagal dilakukan.", Fore.RED, "CHECK-IN FAILED")
            return False
    except requests.RequestException:
        log("Kesalahan saat check-in.", Fore.RED, "CHECK-IN ERROR")
        return False

def main():
    print(Fore.CYAN + "\n=== Ari Wallet Auto Transfer ===\n" + Style.RESET_ALL)

    try:
        with open("accounts.txt", "r") as file:
            accounts = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        log("File 'accounts.txt' tidak ditemukan!", Fore.RED, "ERROR")
        return

    if not accounts:
        log("File 'accounts.txt' kosong!", Fore.RED, "ERROR")
        return

    log(f"Total akun yang ditemukan: {len(accounts)}", Fore.BLUE, "INFO")

    formatted_accounts = []
    for account in accounts:
        try:
            email, password, address, private_key = account.split("|")
            formatted_accounts.append((email, password, address, private_key))
        except ValueError:
            log(f"Format salah: {account}", Fore.RED, "ERROR")

    if len(formatted_accounts) < 2:
        log("Jumlah akun di 'accounts.txt' harus lebih dari satu untuk transfer!", Fore.RED, "ERROR")
        return

    try:
        with open("proxy.txt", "r") as proxy_file:
            proxies = [line.strip() for line in proxy_file if line.strip()]
    except FileNotFoundError:
        proxies = []

    headers = {
        'Accept': "application/json",
        'Accept-Encoding': "gzip",
        'User-Agent': random.choice(ANDROID_USER_AGENTS)
    }

    while True:
        for i, (email, password, address, _) in enumerate(formatted_accounts):
            log(f"Memproses akun {i + 1}/{len(formatted_accounts)}: {email}", Fore.CYAN, "PROCESSING")
            
            if not login(email, password, headers, proxy=random.choice(proxies) if proxies else None):
                continue

            auto_checkin(address, headers, proxy=random.choice(proxies) if proxies else None)

            for j, (_, _, to_address, _) in enumerate(formatted_accounts[i + 1:], start=1):
                auto_transfer(email, password, to_address, headers, proxy=random.choice(proxies) if proxies else None)

            time.sleep(50)

        log("Menunggu 24 jam untuk siklus berikutnya...", Fore.MAGENTA, "WAIT")
        time.sleep(86400)

if __name__ == "__main__":
    main()