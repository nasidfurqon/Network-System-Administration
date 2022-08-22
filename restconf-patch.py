import requests
import json

def printBytesAsJSON(bytes):
    print(json.dumps(json.loads(bytes), indent=2))

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

response = requests.patch(
    url = 'https://{ip}/restconf/data/Cisco-IOS-XE-native:native/interfaces/GigabitEthernet=1',
    auth = ('admin', 'admin'),
    headers = {
        'Account': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json'
    },
    data = json.dumps({
            'Cisco-IOS-XE-native:GigabitEthernet': {
                'ip': {
                    'address': {
                        'primary': {
                            'address': '{new_ip}',
                            'mask': '{new_mask}'
                        }
                    }
                }
            }
    }),
    verify = False
)

print('Response Code: ' + str(response.status_code))