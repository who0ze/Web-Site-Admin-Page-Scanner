import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract
import time
import sys
import itertools
import webbrowser

def is_cdn_cgi_url(url):
    """Checks if the URL contains cdn-cgi."""
    return 'cdn-cgi' in urlparse(url).path

def is_fragment_url(url):
    """Checks if the URL contains a fragment."""
    return bool(urlparse(url).fragment)

def get_redirected_pages(base_url, visited, base_domain):
    redirected_pages = set()
    all_links = set()
    queue = [base_url]
    
    while queue:
        url = queue.pop(0)
        if url not in visited and not is_cdn_cgi_url(url) and not is_fragment_url(url):
            visited.add(url)
            try:
                print(f"Visiting: {url}")
                response = requests.get(url, allow_redirects=True)
                
                final_url = response.url
                if response.status_code == 200 and urlparse(final_url).netloc.endswith(base_domain):
                    if final_url != url:
                        redirected_pages.add(final_url)
                        print(f"Found Redirect: {final_url}")
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(final_url, href)
                        parsed_url = urlparse(full_url)
                        
                        if parsed_url.netloc and parsed_url.netloc.endswith(base_domain) and not is_cdn_cgi_url(full_url) and not is_fragment_url(full_url):
                            if full_url not in visited:
                                queue.append(full_url)
                        
                        all_links.add(full_url)
                
                time.sleep(0.01)
            except requests.RequestException as e:
                print(f"Error: {url} - {e}")
                continue

    return redirected_pages, all_links

def print_with_delay(items, delay=0.05):
    """Prints each item in the list with the specified delay."""
    for item in items:
        print(item)
        time.sleep(delay)
        sys.stdout.flush()

def display_language_selection():
    """Displays the language selection prompt and returns the selected language."""
    print("Please select your language / Lütfen dilinizi seçin:")
    print("1. English")
    print("2. Türkçe")
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        return 'en'
    elif choice == '2':
        return 'tr'
    else:
        print("Invalid choice, defaulting to English.")
        return 'en'

def loading_animation(duration=5):
    """Shows a loading animation for a given duration."""
    end_time = time.time() + duration
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while time.time() < end_time:
        sys.stdout.write(f'\rLoading... {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)

def main(domain, language):
    global base_domain
    extracted = tldextract.extract(domain)
    base_domain = f"{extracted.domain}.{extracted.suffix}"
    
    if language == 'en':
        print(f"Scanning started: {domain}")
    elif language == 'tr':
        print(f"Tarama başlatılıyor: {domain}")

    visited = set()
    
    start_time = time.time()
    
    redirected_pages, _ = get_redirected_pages(f"http://{domain}", visited, base_domain)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    with open("site_page.txt", "w", encoding="utf-8") as file:
        for page in redirected_pages:
            file.write(f"{page}\n")

    if language == 'en':
        print(f"\nScan completed. Results saved in 'site_page.txt'.")
    elif language == 'tr':
        print(f"\nTarama tamamlandı. Sonuçlar 'site_page.txt' dosyasına kaydedildi.")

    print(f"Scan duration: {elapsed_time:.2f} seconds")

    webbrowser.open("https://github.com/who0ze")

def search_pages_with_wordlist(pages_file, wordlist_file, output_file):
    """Searches for words from a wordlist in the pages listed in the pages_file and saves results to a new file."""
    with open(pages_file, "r", encoding="utf-8") as file:
        pages = file.readlines()
    
    with open(wordlist_file, "r", encoding="utf-8") as file:
        words = file.readlines()
    
    pages = [page.strip() for page in pages]
    words = [word.strip() for word in words]
    
    results = set()  
    for page in pages:
        for word in words:
            test_url = f"{page.rstrip('/')}/{word}"
            try:
                print(f"Testing: {test_url}")
                response = requests.get(test_url)
                if response.status_code == 200:
                    results.add(test_url)  # Add to set
                    print(f"Found: {test_url}")
            except requests.RequestException as e:
                print(f"Error fetching {test_url}: {e}")
                continue
    
    with open(output_file, "w", encoding="utf-8") as file:
        for result in sorted(results):  
            file.write(f"{result}\n")
    
    print(f"Search results saved to {output_file}")

if __name__ == "__main__":
    print(r"      _       ______   ____    ____  _____  ____  _____     _______     _        ______  ________  ")
    print(r"     / \     |_   _ `.|_   \  /   _||_   _||_   \|_   _|   |_   __ \   / \     .' ___  ||_   __  | ")
    print(r"    / _ \      | | `. \ |   \/   |    | |    |   \ | |       | |__) | / _ \   / .'   \_|  | |_ \_| ")
    print(r"   / ___ \     | |  | | | |\  /| |    | |    | |\ \| |       |  ___/ / ___ \  | |   ____  |  _| _  ")
    print(r" _/ /   \ \_  _| |_.' /_| |_\/_| |_  _| |_  _| |_\   |_     _| |_  _/ /   \ \_\ `.___]  |_| |__/ | ")
    print(r"|____| |____||______.'|_____||_____||_____||_____|\____|   |_____||____| |____|`._____.'|________| ")
    print(r" ________  _____  ____  _____  ______   ________  _______                                          ")
    print(r"|_   __  ||_   _||_   \|_   _||_   _ `.|_   __  ||_   __ \                                         ")
    print(r"  | |_ \_|  | |    |   \ | |    | | `. \ | |_ \_|  | |__) |                                        ")
    print(r"  |  _|     | |    | |\ \| |    | |  | | |  _| _   |  __ /                Created by who0ze        ")
    print(r" _| |_     _| |_  _| |_\   |_  _| |_.' /_| |__/ | _| |  \ \_              https://github.com/who0ze")
    print(r"|_____|   |_____||_____|\____||______.'|________||____| |___|                                      ")
    print(r"                                                                                                   ")
    language = display_language_selection()
    domain = input("Enter the domain to scan (e.g., example.com): ").strip()
    main(domain, language)
    
    wordlist_file = input("Enter the path to the wordlist file (e.g., wordlist.txt): ").strip()
    output_file = "found_admin_pages.txt"
    search_pages_with_wordlist("site_page.txt", wordlist_file, output_file)
