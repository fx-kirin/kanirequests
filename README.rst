kanirequests
============

.. image:: https://img.shields.io/pypi/v/kanirequests.svg
    :target: https://pypi.python.org/pypi/kanirequests
    :alt: Latest PyPI version

``requests`` と ``requests_html`` を組み合わせたラッパーです。
デフォルトのタイムアウトやリトライ設定、HTML セッションの共有を簡単にします。

.. image:: https://img.shields.io/pypi/v/kanirequests.svg
    :target: https://pypi.python.org/pypi/kanirequests
    :alt: Latest PyPI version

特徴
-----

* ``requests_html.HTMLSession`` を利用したスクレイピング向けセッション。
* すべてのリクエストにデフォルトタイムアウトを適用可能。
* 簡易的なエラーメール通知のフックを提供。
* Cookie を辞書で取り出し・追加できるユーティリティを提供。

Usage
-----

基本的な使い方::

    from kanirequests import KaniRequests

    client = KaniRequests(
        headers={"User-Agent": "KaniRequests/0.1.5"},
        default_timeout=5,
        max_retries=3,
    )
    response = client.get("https://www.python.org")
    print(response.status_code)

プロキシと Cookie の操作::

    proxy = {"http": "http://localhost:8080", "https": "http://localhost:8080"}
    client = KaniRequests(proxy=proxy, default_timeout=5)
    client.add_cookies({"sessionid": "abc123"})
    print(client.cookies_to_dict())

HTML をブラウザで一時表示::

    from kanirequests import open_html_in_browser
    open_html_in_browser("<html><body>Hello</body></html>")

Installation
------------

pip でインストールします::

    pip install kanirequests

Requirements
^^^^^^^^^^^^

* requests
* requests-html
* urllib3

Compatibility
-------------

Python 3.7 以降での利用を想定しています。

Licence
-------

MIT License

Authors
-------

`kanirequests` was written by `fx-kirin <ono.kirin@gmail.com>`_.
