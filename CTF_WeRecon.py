import requests
import dns.resolver
import threading
from queue import Queue
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
import time
import os
from colorama import init, Fore, Style
import sys

# Colorama başlat
init()

# Default wordlist’ler (dosya yoksa bunları kullanır ve kaydeder)
DEFAULT_SUBDOMAINS = [
    "www", "mail", "ftp", "api", "admin", "dev", "test", "staging",
    "login", "shop", "blog", "app", "portal", "secure"
]

DEFAULT_WORDLIST = [
    "admin", "login", "config", "backup", "uploads", "files", "images",
    "css", "js", "api", "test", "dashboard", "panel", "user", "index.php", "index.html"
]

def banner():
    print(Fore.RED + """
    ╔══════════════════════════════════════╗
    ║       CTF-WebRecon - Türkçe Tool     ║
    ║   Pentesting ve CTF için Efsane Araç  ║
    ╚══════════════════════════════════════╝
    """ + Style.RESET_ALL)
    print("ReDIIN \n")

def load_wordlist(wordlist_file, default_list=None):
    if not os.path.exists(wordlist_file) and default_list:
        print(Fore.YELLOW + f"[*] {wordlist_file} bulunamadı, varsayılan liste oluşturuluyor..." + Style.RESET_ALL)
        try:
            with open(wordlist_file, "w") as f:
                f.write("\n".join(default_list))
            print(Fore.GREEN + f"[+] {wordlist_file} oluşturuldu!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Hata: {wordlist_file} oluşturulamadı: {e}" + Style.RESET_ALL)
            return default_list
    try:
        with open(wordlist_file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[!] Hata: {wordlist_file} bulunamadı!" + Style.RESET_ALL)
        return default_list or []

def save_results(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(Fore.GREEN + f"[+] Sonuçlar {filename} dosyasına kaydedildi!" + Style.RESET_ALL)

def subdomain_enum(domain):
    print(Fore.CYAN + "[*] Subdomain tarama başlıyor..." + Style.RESET_ALL)
    subdomains = load_wordlist("subdomains.txt", DEFAULT_SUBDOMAINS)
    found_subdomains = []
    resolver = dns.resolver.Resolver()

    for sub in subdomains:
        try:
            target = f"{sub}.{domain}"
            answers = resolver.resolve(target, "A")
            for rdata in answers:
                print(Fore.GREEN + f"[+] Bulundu: {target} ({rdata})" + Style.RESET_ALL)
                found_subdomains.append({"subdomain": target, "ip": str(rdata)})
        except:
            pass

    if found_subdomains:
        save_results(f"subdomains_{domain}.json", found_subdomains)
    else:
        print(Fore.YELLOW + "[!] Subdomain bulunamadı." + Style.RESET_ALL)

def dir_bruteforce(base_url, wordlist, queue, found_paths):
    while not queue.empty():
        path = queue.get()
        url = urljoin(base_url, path.strip())
        try:
            response = requests.get(url, timeout=3)
            if response.status_code != 404:
                print(Fore.GREEN + f"[+] Bulundu: {url} (Status: {response.status_code})" + Style.RESET_ALL)
                headers = {k: v for k, v in response.headers.items() if k in ["Server", "X-Powered-By"]}
                found_paths.append({"url": url, "status": response.status_code, "headers": headers})
        except requests.RequestException:
            pass
        queue.task_done()

def directory_bruteforce(url):
    print(Fore.CYAN + "[*] Directory bruteforce başlıyor..." + Style.RESET_ALL)
    wordlist = load_wordlist("wordlist.txt", DEFAULT_WORDLIST)
    if not wordlist:
        return

    queue = Queue()
    found_paths = []
    threads = 10

    for path in wordlist:
        queue.put(path)

    for _ in range(threads):
        t = threading.Thread(target=dir_bruteforce, args=(url, wordlist, queue, found_paths))
        t.daemon = True
        t.start()

    queue.join()

    if found_paths:
        save_results(f"dirs_{url.replace('http://', '').replace('https://', '')}.json", found_paths)
    else:
        print(Fore.YELLOW + "[!] Hiçbir dizin bulunamadı." + Style.RESET_ALL)

def basic_vuln_check(url):
    print(Fore.CYAN + "[*] Zafiyet tarama başlıyor..." + Style.RESET_ALL)
    payloads = {
        "XSS": ["<script>alert('xss')</script>", "'';!--\"<XSS>=&{()}"],
        "SQLi": ["' OR '1'='1", "1; DROP TABLE users --"]
    }
    results = []

    for vuln_type, payload_list in payloads.items():
        for payload in payload_list:
            try:
                test_url = f"{url}?test={payload}"
                response = requests.get(test_url, timeout=3)
                soup = BeautifulSoup(response.text, "html.parser")
                if payload in response.text or response.status_code != 404:
                    print(Fore.RED + f"[!] Potansiyel {vuln_type}: {test_url}" + Style.RESET_ALL)
                    results.append({"type": vuln_type, "url": test_url, "payload": payload})
            except requests.RequestException:
                pass

    if results:
        save_results(f"vulns_{url.replace('http://', '').replace('https://', '')}.json", results)
    else:
        print(Fore.YELLOW + "[!] Zafiyet bulunamadı." + Style.RESET_ALL)

def response_analyzer(url):
    print(Fore.CYAN + "[*] Response analizi başlıyor..." + Style.RESET_ALL)
    try:
        response = requests.get(url, timeout=3)
        headers = dict(response.headers)
        interesting_headers = {k: v for k, v in headers.items() if k in ["Server", "X-Powered-By", "Content-Type"]}
        result = {
            "url": url,
            "status_code": response.status_code,
            "headers": interesting_headers
        }
        print(Fore.GREEN + f"[+] Status: {response.status_code}" + Style.RESET_ALL)
        for k, v in interesting_headers.items():
            print(Fore.GREEN + f"    {k}: {v}" + Style.RESET_ALL)
        save_results(f"response_{url.replace('http://', '').replace('https://', '')}.json", result)
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Hata: {e}" + Style.RESET_ALL)

def main():
    banner()
    while True:
        print(Fore.YELLOW + "\n=== CTF-WebRecon Menü ===" + Style.RESET_ALL)
        print("1. Subdomain Tarama")
        print("2. Directory Bruteforce")
        print("3. Zafiyet Kontrolü (XSS, SQLi)")
        print("4. Response Analizi")
        print("5. Çıkış")
        secim = input(Fore.CYAN + "Seçiminiz (1-5): " + Style.RESET_ALL)

        if secim == "5":
            print(Fore.RED + "[*] Çıkılıyor... Görüşürüz kanka!" + Style.RESET_ALL)
            sys.exit(0)

        if secim in ["1", "2", "3", "4"]:
            hedef = input(Fore.CYAN + "Hedef (örn: example.com veya http://example.com): " + Style.RESET_ALL)
            if secim == "1":
                if not hedef.startswith("http"):
                    subdomain_enum(hedef)
                else:
                    print(Fore.RED + "[!] Subdomain tarama için sadece domain girin (örn: example.com)" + Style.RESET_ALL)
            elif secim == "2":
                if hedef.startswith("http"):
                    directory_bruteforce(hedef)
                else:
                    print(Fore.RED + "[!] Directory bruteforce için tam URL girin (örn: http://example.com)" + Style.RESET_ALL)
            elif secim == "3":
                if hedef.startswith("http"):
                    basic_vuln_check(hedef)
                else:
                    print(Fore.RED + "[!] Zafiyet kontrolü için tam URL girin (örn: http://example.com)" + Style.RESET_ALL)
            elif secim == "4":
                if hedef.startswith("http"):
                    response_analyzer(hedef)
                else:
                    print(Fore.RED + "[!] Response analizi için tam URL girin (örn: http://example.com)" + Style.RESET_ALL)
        else:
            print(Fore.RED + "[!] Geçersiz seçim, 1-5 arası bi’ sayı gir!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
