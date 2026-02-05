kanirequests
============

.. image:: https://img.shields.io/pypi/v/kanirequests.svg
    :target: https://pypi.python.org/pypi/kanirequests
    :alt: Latest PyPI version

A thin wrapper around ``requests`` and ``requests_html``.
It makes default timeout/retry configuration and shared HTML sessions easier to use.

Features
--------

* Scraping-friendly session built on ``requests_html.HTMLSession``.
* Configurable default timeout for all requests.
* Simple hook for sending error notification emails.
* Utilities to read/write cookies as dictionaries.

Usage
-----

Basic usage::

    from kanirequests import KaniRequests

    client = KaniRequests(
        headers={"User-Agent": "KaniRequests/0.1.5"},
        default_timeout=5,
        max_retries=3,
    )
    response = client.get("https://www.python.org")
    print(response.status_code)

Proxy and cookie handling::

    proxy = {"http": "http://localhost:8080", "https": "http://localhost:8080"}
    client = KaniRequests(proxy=proxy, default_timeout=5)
    client.add_cookies({"sessionid": "abc123"})
    print(client.cookies_to_dict())

Temporarily open HTML in your browser::

    from kanirequests import open_html_in_browser
    open_html_in_browser("<html><body>Hello</body></html>")

Installation
------------

Install via pip::

    pip install kanirequests

Requirements
^^^^^^^^^^^^

* requests
* requests-html
* urllib3

Compatibility
-------------

Intended for Python 3.7+.

Licence
-------

MIT License

Authors
-------

`kanirequests` was written by `fx-kirin <ono.kirin@gmail.com>`_.
