# -*- coding: utf-8 -*-
import pprint
from collections import OrderedDict
from io import BytesIO

import six
import werkzeug.urls
from requests.structures import CaseInsensitiveDict
from six.moves import http_cookies as Cookie

if six.PY3:
    from urllib.parse import urlparse
elif six.PY2:
    from urlparse import urlparse


def format_url(url):
    """if url not contains schema, add shema
    eg. httpbin.org -> http://httpbin.org"""
    if not (url.startswith("//") or url.startswith("http")):
        url = "http://" + url
    return url


def is_json(mimetype):
    if mimetype == "application/json":
        return True
    if mimetype.startswith("application/") and mimetype.endswith("+json"):
        return True
    return False


def parse_url_and_params(origin_url):
    """:return: tuple. type is (str, MultiDict)"""
    origin_url = format_url(origin_url)
    parse_result = urlparse(origin_url)
    url = "{0}://{1}{2}".format(
        parse_result.scheme or "http", parse_result.netloc, parse_result.path
    )

    query = parse_result.query
    params = None
    if query:
        params = werkzeug.urls.url_decode(query)
    return url, params


def parse_cookies_and_headers(origin_headers):
    """:return: tuple. type is (OrderedDict(), OrderedDict())"""
    cookies = OrderedDict()
    headers = CaseInsensitiveDict()
    for curl_header in origin_headers:
        header_key, header_value = curl_header.split(":", 1)

        if header_key.lower() == "cookie":
            cookie = Cookie.SimpleCookie(header_value)
            for key in cookie:
                cookies[key] = cookie[key].value
        else:
            headers[header_key] = header_value.strip()
    return cookies, headers


def parse_formdata(body, content_type):
    data = body.encode("utf-8")

    content_length = len(data)
    mimetype, options = werkzeug.http.parse_options_header(content_type)

    stream = BytesIO(data)
    parser = werkzeug.formparser.FormDataParser()

    data, form, files = parser.parse(stream, mimetype, content_length, options)
    return data.getvalue(), form, files


def dict_to_pretty_string(the_dict):
    if not the_dict:
        return "{}"
    return pprint.pformat(the_dict)
