import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import datetime
import sys, os.path

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append('C:\\PythonWorkspace\\Workwiz\\Control')
from Control import Utils as log

logger = log.CreateLogger('Saramin_Crawling')

access_key_sa = [
    'KP7xtZEXslt47atHqRtECeAfTxb6i0dxWF8nZbWGnNRgq8AfLmGC',
    'KQEbnI89RuK9eOgqRYOvukpOqFKDDGu9C8GBelQAyB9SUmeYZ2a'
    'zO2S04ShRmktKDMsxeEO4pWHrSyzg6NB4ISlgDhqEVjv5PV3Ba',
    'JgtMgeO8H9YnQVMxUGRLuE9zvgfuLsrVtD28Yq86GxTCGdnkkC',
    'oABj4P5DPdMeQYOD6MiojOau0V4eO2PGQt8GCRiytoFrpq5vHpOG',
    'tNhJjw8rjeJ02koc0dzYXOHoa2lobdysuVd3wMV9fVmg28WiPBG',
    'apNPeyfia5Er2TWiC14nluj4NnRFz4onHHETo5ANYZyi6MNzhsO',
    'z9e2CRM9ytxHaA2W9FCoOvkP770IDhyVfkY5VZbNczZ8Uv1u0y',
    'qapOoQuojX76OA7WV3qye6Olyw1Q83coUXqnwYCxXpg4kB7Ela',
    'jo7abWobJ9jUElhiCiAcjeY06pN8ClISZpKQPHE5NEztfsniLYG',
]

def set_api(arg, key_no, page_no):
    try:
        getDate = str(datetime.date.today() - datetime.timedelta(1))
        headers = {'Accept': 'application/xml; charset=utf-8'}
        URL = 'https://oapi.saramin.co.kr/job-search' +\
        '?fields=count,keyword-code,posting-date,expiration-date' +\
        '&count=110' +\
        '&' + arg + '=' + getDate +\
        '&access-key=' + access_key_sa[key_no] +\
        '&start=' + str(page_no)
        #print(URL)
    except Exception as e:
        logger.error(f'access_key_sa[key_no] Over:: [Saramin] "{e}"')
        
       
    return URL, headers




