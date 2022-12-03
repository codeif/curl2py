# -*- coding: utf-8 -*-
import json

import werkzeug.http

from .curl_parser import parser
from .utils import (
    dict_to_pretty_string,
    is_json,
    parse_cookies_and_headers,
    parse_formdata,
    parse_url_and_params,
)


def format_requests_code(method, url, **kwargs):
    keys = [
        "params",
        "data",
        "headers",
        "cookies",
        "files",
        "auth",
        "timeout",
        "allow_redirects",
        "proxies",
        "hooks",
        "stream",
        "verify",
        "cert",
        "json",
    ]
    keys_alias = {"json": "json_data"}
    kw = []
    variables = []
    for k in keys:
        key_alias = keys_alias.get(k, k)
        v = kwargs.get(k)
        if not v:
            continue
        if isinstance(v, dict):
            v = dict_to_pretty_string(v)
            variables.append("\n{0} = {1}\n".format(key_alias, v))
        else:
            variables.append("\n{0} = {1}\n".format(key_alias, repr(v)))
        kw.append(", {0}={1}".format(k, key_alias))

    result = """import requests

url = "{url}"
{variables}
r = requests.{method}(url{kwargs})

print(r.text)""".format(
        method=method.lower(), url=url, variables="".join(variables), kwargs="".join(kw)
    )
    return result


def main():
    parsed_args = parser.parse_args()

    kwargs = {}

    body = parsed_args.data or parsed_args.data_binary or parsed_args.data_raw

    # method
    method = parsed_args.request
    if not method:
        if body:
            method = "POST"
        else:
            method = "GET"

    url, params = parse_url_and_params(parsed_args.url)
    if params:
        kwargs["params"] = params

    cookies, headers = parse_cookies_and_headers(parsed_args.header)
    kwargs["cookies"], kwargs["headers"] = cookies, dict(headers)

    content_type = headers.get("Content-Type")
    if not content_type and parsed_args.data:
        content_type = "application/x-www-form-urlencoded"

    if body:
        mimetype, options = werkzeug.http.parse_options_header(content_type)
        if is_json(mimetype):
            kwargs["json"] = json.loads(body)
        else:
            data, forms, kwargs["files"] = parse_formdata(body, content_type)
            if forms:
                kwargs["data"] = forms
            else:
                kwargs["data"] = data

    code = format_requests_code(method, url, **kwargs)
    print(code)
