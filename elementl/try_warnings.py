import warnings
import sys
import requests

warnings.filterwarnings('once')

if len(sys.argv) == 2:
    _, URL = sys.argv
    if 'http://' in URL:
        warnings.warn('The connection is insecure')
    # raise a repeated warning
    warnings.warn('The connection is insecure')
    Response = requests.get(url=URL)
else:
    warnings.warn('You need to provide me a url')
