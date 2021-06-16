import os
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

def checkOutput():

    global domain_file

    # remove old output if exist
    if os.path.exists(domain_file):
        os.remove(domain_file)

def grabDomain(pages):

    global domain_file

    try:
        
        # mirror list
        mirror_list = [
            "https://mirror-h.org/archive/page/",
            "https://zone-xsec.com/archive/page=",
            "https://zone-d.org/mirror/archive/"
        ]

        for mirror in mirror_list:

            # requests
            page = pages + 1
            url = f"{mirror}{page}"
            header = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
            response = requests.get(url, headers=header, timeout=20, verify=False)

            # grab domain
            if "zone-d" in url:
                grab_domain = re.findall('<td class=special style="width: 10px;padding:0 5px;"><td>(.*?)<td>', response.text)

                for domain in grab_domain:
                    domain = domain.split("/")
                    save = open(domain_file, "a")
                    save.write(f"{domain[0]}\n")
                    save.close()
                    print(domain[0])

            elif "mirror-h" in url:
                grab_domain = re.findall('<td style="word-break: break-word;white-space: normal;min-width: 300px;"><?a?.+\>(.*?)</a></td>', response.text)
                
                for domain in grab_domain:
                    domain = domain.split("/")
                    save = open(domain_file, "a")
                    save.write(f"{domain[2]}\n")
                    save.close()
                    print(domain[2])

            elif "zone-xsec" in url:
                grab_domain = re.findall('''            <td></td>
                <td>(.*?)</td>''', response.text)
                
                if "For Archive Security" in response.text:
                    pass
                else:
                    for domain in grab_domain:
                        domain = domain.split("/")
                        save = open(domain_file, "a")
                        save.write(f"{domain[0]}\n")
                        save.close()
                        print(domain[0])
            else:
                pass

    except:
        pass

banner()
checkOutput()

total_pages = int(input("Total pages: "))
print("\n")

threads = []
for x in range(0, total_pages):
    pages = x
    grab = threading.Thread(target=grabDomain, args=(pages,))
    threads.append(grab)

for grab in threads:
    grab.start()

time.sleep(20)

for grab in threads:
    grab.join()

print("\n")