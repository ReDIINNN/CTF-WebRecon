CTF-WebRecon
CTF-WebRecon, web pentesting ve CTF'ler için geliştirilmiş, Türkçe menüye sahip, kullanıcı dostu bir Python aracıdır. Subdomain tarama, directory bruteforce, temel zafiyet kontrolü (XSS, SQLi) ve HTTP response analizi yapar. Tüm özellikler tek bir script üzerinden, kolayca seçilebilir.

Özellikler

Subdomain Tarama: Verilen domain için subdomain'leri bulur (DNS sorguları ile).
Directory Bruteforce: Web sunucusunda gizli dosya ve klasörleri tarar.
Zafiyet Kontrolü: Basit XSS ve SQLi payload'larıyla zafiyet testi yapar.
Response Analizi: HTTP header'larını ve status kodlarını analiz eder.
Türkçe menü, renkli terminal çıktıları ve JSON formatında raporlama.


Kurulum (Türkçe)
Gereksinimler

Python 3.6+
Linux (Kali, Ubuntu vb.) veya başka bir Unix tabanlı sistem
pip ve python3-venv

Adımlar

Repoyu klonlayın:
git clone https://github.com/ReDIINNN/CTF-WebRecon.git
cd CTF-WebRecon


Sanal ortam oluşturun ve aktif edin:
python3 -m venv ctf_webrecon_env
source ctf_webrecon_env/bin/activate


Bağımlılıkları kurun:
pip install -r requirements.txt


Script’i çalıştırın:
python CTF-WebRecon.py



Wordlist’ler

subdomains.txt: Subdomain tarama için (otomatik oluşur).
wordlist.txt: Directory bruteforce için (otomatik oluşur).


Installation (English)
Requirements

Python 3.6+
Linux (Kali, Ubuntu, etc.) or other Unix-based systems
pip and python3-venv

Steps

Clone the repository:
git clone https://github.com/ReDIINNN/CTF-WebRecon.git
cd CTF-WebRecon


Create and activate a virtual environment:
python3 -m venv ctf_webrecon_env
source ctf_webrecon_env/bin/activate


Install dependencies:
pip install -r requirements.txt


Run the script:
python CTF-WebRecon.py



Wordlists

subdomains.txt: For subdomain enumeration (auto-generated if missing).
wordlist.txt: For directory bruteforce (auto-generated if missing).


Kullanım (Türkçe)

Script’i çalıştırın: python CTF-WebRecon.py
Menüden bir seçenek seçin (1-5):
1: Subdomain Tarama (örn: example.com)
2: Directory Bruteforce (örn: http://example.com)
3: Zafiyet Kontrolü (örn: http://example.com/search.php?test=query)
4: Response Analizi (örn: http://example.com)
5: Çıkış


Sonuçlar JSON dosyalarına kaydedilir.


Usage (English)

Run the script: python CTF-WebRecon.py
Select an option from the menu (1-5):
1: Subdomain Enumeration (e.g., example.com)
2: Directory Bruteforce (e.g., http://example.com)
3: Vulnerability Check (e.g., http://example.com/search.php?test=query)
4: Response Analysis (e.g., http://example.com)
5: Exit


Results are saved to JSON files.


Lisans
MIT Lisansı altında dağıtılmaktadır. Detaylar için LICENSE dosyasına bakın.

Katkıda Bulunma
Fikirleriniz, hata raporları veya yeni özellik önerileri için GitHub Issues veya Pull Request açabilirsiniz. Türkçe pentest camiasına katkıda bulunalım! 😎
