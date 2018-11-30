"""KaniRequests - ''"""

__version__ = '0.1.0'
__author__ = 'fx-kirin <ono.kirin@gmail.com>'
__all__ = ['KaniRequests', 'open_html_in_browser']

import os
import requests
import requests.packages.urllib3
import tempfile
import time
from requests.utils import add_dict_to_cookiejar, dict_from_cookiejar
from requests_html import HTMLSession
requests.packages.urllib3.disable_warnings()

from requests.adapters import TimeoutSauce

class KaniRequests(object):
    def __init__(self, headers={}, proxy={}, default_timeout=None):
        self.headers = headers
        self.proxy = proxy
        self.session = HTMLSession()
        self.session.headers.update(headers)
        if proxy != {}:
            self.session.proxies = proxy
            #self.session.verify = os.path.join(os.path.dirname(__file__), "FiddlerRoot.pem")
            self.session.verify = None
        self.adapters = requests.adapters.HTTPAdapter(max_retries=3)
        self.default_timeout = default_timeout
        self.session.mount("http://", self.adapters)
        self.session.mount("https://", self.adapters)
    
    def get(self, url, *args, **kwargs):
        if 'timeout' not in kwargs:
            if self.default_timeout:
                kwargs['timeout'] = self.default_timeout
        return self.session.get(url, cookies=self.session.cookies, *args, **kwargs)
        
    def post(self, url, *args, **kwargs):
        if 'timeout' not in kwargs:
            if self.default_timeout:
                kwargs['timeout'] = self.default_timeout
        return self.session.post(url, cookies=self.session.cookies, *args, **kwargs)
        
    def put(self, url, *args, **kwargs):
        if 'timeout' not in kwargs:
            if self.default_timeout:
                kwargs['timeout'] = self.default_timeout
        return self.session.put(url, cookies=self.session.cookies, *args, **kwargs)
        
    def delete(self, url, *args, **kwargs):
        if 'timeout' not in kwargs:
            if self.default_timeout:
                kwargs['timeout'] = self.default_timeout
        return self.session.delete(url, cookies=self.session.cookies, *args, **kwargs)
    
    def close(self):
        self.session.close()
    
    def cookies_to_dict(self):
        return dict_from_cookiejar(self.session.cookies)
    
    def add_cookies(self, cookies):
        add_dict_to_cookiejar(self.session.cookies, cookies)
        
def open_html_in_browser(html_text):
    with tempfile.NamedTemporaryFile(suffix='.html') as f:
        filename = f.name
        f.write(html_text)
        f.flush()
        os.system('xdg-open %s > /dev/null 2>&1'%(filename))
        time.sleep(1)
        
if __name__ == "__main__":
    client = Pyhttp({"User-Agent" : "Java/1.6.0_34"})
    client.get("https://www.python.org")