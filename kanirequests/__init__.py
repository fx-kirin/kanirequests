"""KaniRequests - requests/requests-html thin wrapper."""
import logging
import os
import sys
import tempfile
import time
import traceback

import requests
import urllib3
from requests.adapters import TimeoutSauce
from requests.utils import add_dict_to_cookiejar, dict_from_cookiejar
from requests_html import HTMLSession

__version__ = "0.1.5"
__author__ = "fx-kirin <ono.kirin@gmail.com>"
__all__ = ["KaniRequests", "open_html_in_browser"]



urllib3.disable_warnings()


class KaniRequests(object):
    """Wrapper around HTMLSession with default timeouts and helpers."""

    def __init__(self, headers={}, proxy={}, default_timeout=None, max_retries=3):
        # Provide a custom TimeoutSauce that falls back to default_timeout.
        def __init__(self, *args, **kwargs):
            if kwargs["connect"] is None:
                kwargs["connect"] = default_timeout
            if kwargs["read"] is None:
                kwargs["read"] = default_timeout
            return TimeoutSauce.__init__(self, *args, **kwargs)

        DefaultTimeout = type("DefaultTimeout", (TimeoutSauce,), {"__init__": __init__})

        self.headers = headers
        self.proxy = proxy
        self.session = HTMLSession()
        self.session.headers.update(headers)
        if proxy != {}:
            self.session.proxies = proxy
            # Disable TLS verification when proxying (e.g. Fiddler/mitm).
            self.session.verify = None
        # Apply retry and timeout defaults to the session adapters.
        self.adapters = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.adapters.TimeoutSauce = DefaultTimeout
        requests.adapters.TimeoutSauce = DefaultTimeout
        self.session.mount("http://", self.adapters)
        self.session.mount("https://", self.adapters)
        # Optional error-mailer configuration.
        self.yag = None
        self.mail_to = None
        self.subject = None
        self.log = logging.getLogger(self.__class__.__name__)

    def set_error_mailer(self, yag, mail_to, subject):
        """Configure a mailer to send errors when requests fail."""
        self.yag = yag
        self.mail_to = mail_to
        self.subject = subject

    def mount(self, prefix, adapters):
        """Expose adapter mounting for custom protocols."""
        self.session.mount(prefix, adapters)
        self.session.mount(prefix, adapters)

    def get(self, url, *args, **kwargs):
        """GET request with cookie sharing and optional error notifications."""
        try:
            kwargs["cookies"] = self.session.cookies
            result = self.session.get(url, *args, **kwargs)
            if self.yag is not None:
                if result.status_code != 200:
                    status_code = result.status_code
                    body = f"status_code is not 200 on Get {url=} {args=} {kwargs=}\n"
                    body += f"{status_code=}"
                    self.yag.send(
                        to=self.mail_to,
                        subject=self.subject,
                        contents=body,
                    )
                    self.log.error("Sending error email because of status_code=%s.", status_code)
            return result
        except Exception as e:
            if self.yag is not None:
                body = f"Error on Get {url=} {args=} {kwargs=}"
                body += "\n[sys.exe_info]\n"
                body += str(sys.exc_info())
                body = "\n[traceback.format_exc]\n"
                body += traceback.format_exc()
                self.yag.send(
                    to=self.mail_to,
                    subject=self.subject,
                    contents=body,
                )
                self.log.error("Sending error email because of Exception=%s.", e)
            raise

    def post(self, url, *args, **kwargs):
        """POST request with cookie sharing and optional error notifications."""
        try:
            kwargs["cookies"] = self.session.cookies
            result = self.session.post(url, *args, **kwargs)
            if self.yag is not None:
                if result.status_code != 200:
                    status_code = result.status_code
                    body = f"status_code is not 200 on Get {url=} {args=} {kwargs=}\n"
                    body += f"{status_code=}"
                    self.yag.send(
                        to=self.mail_to,
                        subject=self.subject,
                        contents=body,
                    )
                    self.log.error("Sending error email because of status_code=%s.", status_code)
            return result
        except Exception as e:
            if self.yag is not None:
                body = f"Error on Get {url=} {args=} {kwargs=}\n"
                body += "\n[sys.exe_info]\n"
                body += sys.exc_info()
                body = "\n[traceback.format_exc]\n"
                body += traceback.format_exc()
                self.yag.send(
                    to=self.mail_to,
                    subject=self.subject,
                    contents=body,
                )
                self.log.error("Sending error email because of Exception=%s.", e)
            raise

    def put(self, url, *args, **kwargs):
        """PUT request with cookie sharing."""
        kwargs["cookies"] = self.session.cookies
        return self.session.put(url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        """DELETE request with cookie sharing."""
        kwargs["cookies"] = self.session.cookies
        return self.session.delete(url, *args, **kwargs)

    def close(self):
        """Close the underlying HTML session."""
        self.session.close()

    def cookies_to_dict(self):
        """Return the current cookies as a dict."""
        return dict_from_cookiejar(self.session.cookies)

    def add_cookies(self, cookies):
        """Add cookies from a dict to the current session."""
        add_dict_to_cookiejar(self.session.cookies, cookies)


def open_html_in_browser(html_text):
    """Write HTML to a temp file and open it in the default browser."""
    with tempfile.NamedTemporaryFile(suffix=".html") as f:
        filename = f.name
        f.write(html_text)
        f.flush()
        os.system("xdg-open %s > /dev/null 2>&1" % (filename))
        time.sleep(5)


if __name__ == "__main__":
    client = KaniRequests({"User-Agent": "Java/1.6.0_34"}, default_timeout=1)
    client.get("https://www.python.org")
