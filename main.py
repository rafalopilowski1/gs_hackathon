import time
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from zapv2 import ZAPv2
from collections import defaultdict
import functools
import operator

# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'ug1a3ikituq8i8m0od65hss3kl'
zap = ZAPv2(apikey=apiKey, proxies={
            'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

app = FastAPI()

api_router = APIRouter(prefix="/api")

templates = Jinja2Templates(directory="templates")

@api_router.get("/process")
async def process_data(request: Request, url: str, apikey: str | None = None, response_class=HTMLResponse):
    try:
        activeScan = False
        r = requests.get(url)
        openapi = r.json()
        urls = list(map(lambda x: x['url'], openapi['servers']))            
        errors = zap.openapi.import_url(url, apikey=apikey)
        if errors:
            return templates.TemplateResponse(request=request, name="error.html")
        loaded_urls = zap.core.urls()

        while int(zap.pscan.records_to_scan) > 0:
            # Loop until the passive scan has finished
            print('Records to passive scan : ' + zap.pscan.records_to_scan)
            time.sleep(2)

        if activeScan:
            zap.context.new_context(url)
            context_id = zap.context.context(url)
            for url in loaded_urls:            
                found = any(map(lambda u: u.startswith(url), urls))
                if found:
                    zap.context.include_in_context(url)
            scanID = zap.ascan.scan(contextid=context_id)
            while int(zap.ascan.status(scanID)) < 100:
                # Loop until the scanner has finished
                progress = zap.ascan.status(scanID)
                print('Scan progress %: ' + progress)
                time.sleep(5)
        
        output = functools.reduce(operator.iconcat, [zap.core.alerts(baseurl=u) for u in urls], [])

        # Zmienna do przechowywania zgrupowanych alertów
        grouped_alerts = defaultdict(lambda: {
            'confidence': '',
            'risk': '',
            'description': '',
            'solution': '',
            'reference': '',
            'urls': set()
        })

        # Grupowanie alertów
        for alert in output:
            alert_name = alert['alert']
            grouped_alerts[alert_name]['confidence'] = alert['confidence']
            grouped_alerts[alert_name]['risk'] = alert['risk']
            grouped_alerts[alert_name]['description'] = alert['description']
            grouped_alerts[alert_name]['solution'] = alert['solution']
            grouped_alerts[alert_name]['reference'] = alert['reference']
            grouped_alerts[alert_name]['urls'].add(alert['url'])

        return templates.TemplateResponse(request=request, name="raport.html", context={'alerts': grouped_alerts})
    except Exception as e:
        return templates.TemplateResponse(request=request, name="error.html", context={'error': e})


app.include_router(api_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
