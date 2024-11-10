import requests
import time


serc_proxy = ""

def get_proxy_list(show_msg=True, http_mode="all"):
    if show_msg: print("[i] Setting up session...")
    req_session = requests.Session()
    req_session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
    })
    if show_msg: print("[i] Requesting list...")
    req_response = req_session.get("https://free-proxy-list.net/")
    raw_site = req_response.text
    req_session.close()
    
    if show_msg: print("[i] Processing data...")
    raw_table = raw_site[
        raw_site.index("<table class=\"table table-striped table-bordered") :
        raw_site.index("</table>", raw_site.index("table table-striped table-bordered")) + 8
    ]
    raw_table = raw_table[
        raw_table.index("<tbody>") + 7 :
        raw_table.index("</tbody>")
    ]
    
    rt_processed = raw_table.split("<tr>")[1::]
    for i in range(len(rt_processed)):
        raw_data = rt_processed[i]
        rd_processed = raw_data.split("</td>")[0:-1]
        for j in range(len(rd_processed)):
            rd_processed[j] = rd_processed[j][rd_processed[j].index(">") + 1::]
        rt_processed[i] = rd_processed
    
    if show_msg: print("[i] Process complete")
    
    if http_mode == "http":
        return [each for each in rt_processed if each[6] == "no"]
    elif http_mode == "https":
        return [each for each in rt_processed if each[6] == "yes"]
    else:
        return rt_processed

def fetch_with_proxies(target_url, proxies):
    for proxy in proxies:
        proxy_dict = {
            "http": f"http://{proxy[0]}:{proxy[1]}",
            "https": f"http://{proxy[0]}:{proxy[1]}"
        }
        
        try:
            response = requests.get(target_url, proxies=proxy_dict, timeout=5)
            if response.status_code == 200:
                print(f"Success with proxy {proxy_dict['http']}")
                return proxy_dict['http']
                
            else:
                print(f"Parsing Proxy...")
        except requests.exceptions.RequestException as e:
            print(f"Parsing Proxy...")
    
    print("All proxies failed.")
    return proxy_dict

proxies = get_proxy_list(show_msg=False)
target_url = "https://api.ipify.org?format=json"
def get_proxy_dict():
    result = fetch_with_proxies(target_url, proxies)
    if result:
        return result
    return