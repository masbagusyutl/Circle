import requests
import json
import time
import datetime
import os
from colorama import Fore, Back, Style, init

# Menginisialisasi colorama
init(autoreset=True)

def print_welcome_message():
    print(Fore.WHITE + r"""
_  _ _   _ ____ ____ _    ____ _ ____ ___  ____ ____ ___ 
|\ |  \_/  |__| |__/ |    |__| | |__/ |  \ |__/ |  | |__]
| \|   |   |  | |  \ |    |  | | |  \ |__/ |  \ |__| |         
          """)
    print(Fore.GREEN + Style.BRIGHT + "Nyari Airdrop")
    print(Fore.YELLOW + Style.BRIGHT + "Telegram: https://t.me/nyariairdrop")

def baca_data():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    
    accounts = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            accounts.append({
                'c': lines[i].strip(),
                'authorization': lines[i + 1].strip()
            })
    return accounts

def kirim_request(url, method, headers, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Terjadi kesalahan saat mengirim request: {e}")
        return None

def proses_akun(account, index, total):
    print(Fore.CYAN + f"\nMemproses akun {index + 1} dari {total}")
    
    headers = {
        'authorization': account['authorization'],
        'content-type': 'application/json'
    }

    # Profile
    profile_url = f"https://api.toncircle.org/user/profile?c={account['c']}"
    profile_data = kirim_request(profile_url, 'GET', headers)
    if profile_data:
        print(Fore.GREEN + "Informasi Profil:")
        print(f"  Nama: {profile_data['firstName']} {profile_data['lastName']}")
        print(f"  Jumlah Referral: {profile_data['referralsAmount']}")
        print(f"  Saldo Poin: {profile_data['pointsBalance']}")
        print(f"  Saldo Bintang: {profile_data['starsBalance']}")
        print(f"  Total Permainan: {profile_data['totalGames']}")
        print(f"  Total Kemenangan: {profile_data['totalGamesWin']}")
        print(f"  Rata-rata Peluang: {profile_data['avgChance']}")
        print(f"  Streak: {profile_data['streak']}")
        print(f"  TON yang Dimenangkan: {profile_data['wonTon']}")
        print(f"  Dompet: {profile_data['wallet'] if profile_data['wallet'] else 'Tidak ada'}")
        print(f"  Login Pertama: {'Ya' if profile_data['isFirstLogin'] else 'Tidak'}")
        print(f"  Hari Bonus: {profile_data['bonusDay']}")
        print(f"  Tanggal Klaim Bonus: {profile_data['bonusClaimDate']}")
        print(f"  Promo: {profile_data['promo'] if profile_data['promo'] else 'Tidak ada'}")

    # Daily Bonus
    bonus_url = f"https://api.toncircle.org/user/bonus/daily?c={account['c']}"
    bonus_data = kirim_request(bonus_url, 'POST', headers, {"withMultiplier": False})
    if bonus_data:
        print(Fore.GREEN + "Bonus harian berhasil diklaim")


    # Tasks
    tasks_url = f"https://api.toncircle.org/user/tasks/list?c={account['c']}"
    tasks_data = kirim_request(tasks_url, 'GET', headers)
    if tasks_data:
        for task in tasks_data['tasks']:
            if not task['completed']:
                start_url = f"https://api.toncircle.org/user/tasks/start?c={account['c']}"
                start_data = kirim_request(start_url, 'POST', headers, {"id": task['id']})
                if start_data and start_data['success']:
                    print(Fore.YELLOW + f"Memulai tugas: {task['data']['title']}")
                    time.sleep(2)  # Simulasi pengerjaan tugas
                    finalize_url = f"https://api.toncircle.org/user/tasks/finalize?c={account['c']}"
                    finalize_data = kirim_request(finalize_url, 'POST', headers, {"id": task['id']})
                    if finalize_data and finalize_data['success']:
                        print(Fore.GREEN + f"Tugas selesai: {task['data']['title']}")


    # One-time Tasks
    one_time_tasks_url = f"https://api.toncircle.org/user/tasks/one-time/list?c={account['c']}"
    one_time_tasks_data = kirim_request(one_time_tasks_url, 'GET', headers)
    if one_time_tasks_data:
        for task in one_time_tasks_data['tasks']:
            if not task['completed']:
                start_url = f"https://api.toncircle.org/user/tasks/one-time/start?c={account['c']}"
                start_data = kirim_request(start_url, 'POST', headers, {"id": task['id']})
                if start_data and start_data['success']:
                    print(Fore.YELLOW + f"Memulai tugas one-time: {task['data']['title']}")
                    time.sleep(2)  # Simulasi pengerjaan tugas
                    finalize_url = f"https://api.toncircle.org/user/tasks/one-time/finalize?c={account['c']}"
                    finalize_data = kirim_request(finalize_url, 'POST', headers, {"id": task['id']})
                    if finalize_data and finalize_data['success']:
                        print(Fore.GREEN + f"Tugas one-time selesai: {task['data']['title']}")

def hitung_mundur(durasi):
    end_time = datetime.datetime.now() + datetime.timedelta(days=1)
    while datetime.datetime.now() < end_time:
        remaining = end_time - datetime.datetime.now()
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\rWaktu tersisa: {remaining.days} hari {hours:02d}:{minutes:02d}:{seconds:02d}", end="", flush=True)
        time.sleep(1)
    print("\nWaktu habis! Memulai ulang proses...")

def main():
    print_welcome_message()  # Menampilkan banner saat program dimulai
    while True:
        accounts = baca_data()
        print(Fore.CYAN + f"Total akun: {len(accounts)}")

        for i, account in enumerate(accounts):
            proses_akun(account, i, len(accounts))
            if i < len(accounts) - 1:
                print(Fore.YELLOW + "Menunggu 5 detik sebelum memproses akun berikutnya...")
                time.sleep(5)

        print(Fore.MAGENTA + "\nSemua akun telah diproses. Memulai hitung mundur 1 hari...")
        hitung_mundur(1)

if __name__ == "__main__":
    main()
