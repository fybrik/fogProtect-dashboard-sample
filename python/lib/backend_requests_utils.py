import requests
import curlify
import re
import urllib.parse
import logging
from .log_utils import init_root_logger
from .configs import *

init_root_logger()
logger = logging.getLogger(__name__)


def send_query_backend(query_string, passed_headers, method, values, args):
    query_strings_less_blanks = re.sub(' +', ' ', query_string)
    query_backend_url = get_backend_url()
    request_url = query_backend_url + decode_query(query_strings_less_blanks)

    logger.info(f"request_url: {request_url}")

    try:
        if method == 'POST':
            response = requests.post(request_url, headers=passed_headers, data=values, params=args)
        else:
            response = requests.get(request_url, headers=passed_headers, data=values, params=args)

        logger.debug(f"curl_request: {curlify.to_curl(response.request)}")
    except Exception as e:
        logger.error(f"could not send request to backend server. request_url: {request_url}, method: {method}, "
                     f"passed_headers: {str(passed_headers)}, values: {str(values)}. Error: {e.message}, {e.args}")
        return None

    if response.status_code == 404:
        logger.info("empty return from backend server")
        return None
    else:
        try:
            return_content = response.json()  # decodes the response in json
        except:
            logger.warning("response is not in JSON format, returning as binary")
            return_content = response.content

    return return_content, response.headers


def decode_query(query_string):
    return urllib.parse.unquote_plus(query_string)


def get_backend_url():
    return "http://" + ServerConfig.backend_address + ":" + str(ServerConfig.backend_port) + "/"
