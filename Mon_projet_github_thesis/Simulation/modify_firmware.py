from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    if flow.request.path.endswith('/firmware'):
        flow.response.content = b"FAULTY FIRMWARE"