import requests
import json

def printBytesAsJSON(bytes):
    print(json.dumps(json.loads(bytes), indent=2))

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

response = requests.put(
    url = 'https://{ip}/restconf/data/ietf-interfaces/interface=GigabitEthernet2',
    auth = ('admin', 'admin'),
    headers = {
        'Account': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json'
    },
    data = json.dumps({
        'ietf-interfaces: interface': {
            'name': 'GigabitEthernet2',
            'type': 'iana-if-type:ethernetCsmacd',
            'enabled': 'true',
            'ietf-ip:ipv4': [
                {
                    'ip': '{new_ip}',
                    'netmask': '{new_mask}'
                }
            ]
        }
    }),
    verify = False
)

print('Response Code: ' + str(response.status_code))