# To use this module first install the following packages:
# pip install python-owasp-zap-v2.4
# to run a sap server sh use the following comand:
# zap.bat -daemon -port <custom_port> -config api.key=ulooo57b6aagv44m4j0mns2mg7
# or docker
# docker run -u zap -p 8080:8080 -i owasp/zap2docker-stable zap-webswing.sh

import time
import requests
import json
from zapv2 import ZAPv2

apiKey = 'ug1a3ikituq8i8m0od65hss3kl'


zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

url = 'https://api.apis.guru/v2/specs/ably.net/control/1.0.14/openapi.json'
print('Importing OpenAPI definition from {}'.format(url))
# result = zap.openapi.import_file(file=f)
result = zap.openapi.import_url(url)
print('Import result: {}'.format(result))

headers = {
  'Accept': 'application/json'
}

r = requests.get(f'http://127.0.0.1:8080/JSON/httpSessions/view/sites/?apikey={apiKey}', headers = headers)

# TODO : explore the app (Spider, etc) before using the Passive Scan API, Refer the explore section for details
while int(zap.pscan.records_to_scan) > 0:
    # Loop until the passive scan has finished
    print('Records to passive scan : ' + zap.pscan.records_to_scan)
    time.sleep(2)

print('Passive Scan completed')

# Print Passive scan results/alerts
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
# Save the alerts to a JSON file
with open('alerts.json', 'w') as json_file:
    json.dump(zap.core.alerts(), json_file, indent=4)
# TODO
