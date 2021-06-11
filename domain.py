import requests
import re
import urllib3
import threading
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# output file
domain_file = "domain.txt"

def banner():
    print("""
Domain Grabber
Github: @ceritarommy
Instagram: @rommymaul
    """)

def grabDomain(url):

    global domain_file

    try:
        response = requests.get(url, timeout=5, verify=False)
        grab_domain = re.findall('<td class=special style="width: 10px;padding:0 5px;"><td>(.*?)<td>', response.text)

        for domain in grab_domain:
            domain = domain.split("/")
            save = open(domain_file, "a")
            save.write(f"{domain[0]}\n")
            save.close()
            print(domain[0])
    except:
        pass

banner()

total_pages = int(input("Total pages: "))
print("\n")

threads = []
for x in range(0, total_pages):
    url = f"https://zone-d.org/mirror/archive/{x}"
    grab = threading.Thread(target=grabDomain, args=(url,))
    threads.append(grab)

for grab in threads:
    grab.start()

time.sleep(3)

for grab in threads:
    grab.join()

print("\n")