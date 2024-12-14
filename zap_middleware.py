import time
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

def passive_scan(zap):
    while int(zap.pscan.records_to_scan) > 0:
        print('Records to passive scan : ' + zap.pscan.records_to_scan)
        time.sleep(2)

def active_scan(zap):
    scanID = zap.ascan.scan()
    while int(zap.ascan.status(scanID)) < 100:
      progress = zap.ascan.status(scanID)
      print('Scan progress %: ' + progress)
      time.sleep(5)
    return scanID

    # def load_api(self, url, apikey=None):
    #     self.zap.core.new_session(name="blablabla", overwrite=True)
    #     r = requests.get(url)
    #     openapi = r.json()
    #     urls = list(map(lambda x: x['url'], openapi['servers']))
    #     errors = self.zap.openapi.import_url(url, apikey=apikey)
    #     if errors:
    #         return False, urls
    #     loaded_urls = self.zap.core.urls()
    #     for url in loaded_urls:
    #         found = any(map(lambda u: u.startswith(url), urls))
    #         if not found:
    #             self.zap.core.delete_site_node(url)
    #     return True, urls