from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re
import time

user_url = str(input('[+] Enter Target URL To Scan: '))
urls = deque([user_url])

scraped_urls = set()
emails = set()
count = 0

# Regex pattern for email matching with improved detection
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Base domain to limit crawling to the starting domain
base_domain = urllib.parse.urlparse(user_url).netloc

try:
    while len(urls):
        count += 1
        if count == 100:  # Limit to first 100 pages to avoid long run times
            break

        url = urls.popleft()
        scraped_urls.add(url)

        print(f'[{count}] Processing {url}')

        # Adding a User-Agent header for the request
        try:
            with requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                if response.status_code != 200:
                    continue
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema) as e:
            print(f'[!] Error: {e} - skipping URL')
            continue

        # Extract emails from the current page and add to the set
        new_emails = set(email_pattern.findall(response.text))
        emails.update(new_emails)

        # Parse the page content
        soup = BeautifulSoup(response.text, features="lxml")

        # Extract all anchor links and process them
        for anchor in soup.find_all("a"):
            link = anchor.get('href', '')
            
            # Convert relative URLs to absolute and filter for HTTP/HTTPS links only
            link = urllib.parse.urljoin(url, link)
            if not link.startswith(('http://', 'https://')):
                continue

            # Only add links within the same domain
            link_domain = urllib.parse.urlparse(link).netloc
            if link not in urls and link not in scraped_urls and link_domain == base_domain:
                urls.append(link)

        # Respectful delay to avoid overwhelming the server
        time.sleep(1)

except KeyboardInterrupt:
    print('[-] Interrupted by user! Closing.')

# Output all found email addresses
print("\n[+] Email Addresses Found:")
for mail in emails:
    print(mail)
