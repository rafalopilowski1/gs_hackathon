import time
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from zapv2 import ZAPv2
from collections import defaultdict

# Change to match the API key set in ZAP, or use None if the API key is disabled
apiKey = 'ug1a3ikituq8i8m0od65hss3kl'
zap = ZAPv2(apikey=apiKey, proxies={
            'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

app = FastAPI()

api_router = APIRouter(prefix="/api")

templates = Jinja2Templates(directory="templates")


@api_router.get("/process")
async def process_data(request: Request, url: str, response_class=HTMLResponse):
    zap.core.new_session(name="blablabla", overwrite=True)
    r = requests.get(url)
    openapi = r.json()
    urls = list(map(lambda x: x['url'], openapi['servers']))

    errors = zap.openapi.import_url(url)

    loaded_urls = zap.core.urls()
    for url in loaded_urls:            
        found = any(map(lambda u: u.startswith(url), urls))
        if not found:
            zap.core.delete_site_node(url)

    while int(zap.pscan.records_to_scan) > 0:
        # Loop until the passive scan has finished
        print('Records to passive scan : ' + zap.pscan.records_to_scan)
        time.sleep(2)

    output = zap.core.alerts()

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


app.include_router(api_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
