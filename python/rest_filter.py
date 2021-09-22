import json
import jwt
import os
import time
import logging
import kofiko
from flask import Flask, request
from flask_cors import cross_origin
from lib.log_utils import init_root_logger
from lib.backend_requests_utils import send_query_backend, get_backend_url
from lib.opa_requests_utils import opa_get_actions, configmap_to_policy
from lib.filter_utils import filter_data
from lib.configs import *

logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_info_jwt(encrypted_payload):
    def get_decrypted_value(key):
        try:
            decrypted_value = decrypt_jwt(encrypted_payload, key)
        except:
            logger.warning(f"could not decrypt {key} in JWT")
            decrypted_value = None
        return decrypted_value

    # TODO: change this into a list of keys and not only 2 keys of role and organization, this is specific for
    #  this usecase
    role = get_decrypted_value(ServerConfig.jwt_role_key)
    organization = get_decrypted_value(ServerConfig.jwt_organization_key)

    return role, organization


# Catch anything
@app.route('/<path:query_string>', methods=['GET', 'POST', 'PUT'])
@cross_origin()
def get_all(query_string=None):

    logger.info(f"received query: {query_string}. Request URL: {request.url}")

    # Support JWT token for OAuth 2.1
    organization = None
    role = None

    encrypted_payload = request.headers.get('Authorization')
    if encrypted_payload is not None:
        role, organization = get_info_jwt(encrypted_payload)
    else:
        role = request.headers.get('role')   # testing only

    logger.info(f"role: {role}, organization: {organization}")

    # Get the filter constraints from OPA, the requester might not have access to this URL
    logger.info("getting filter constraints from OPA")
    filter_actions = opa_get_actions(role, OPAConfig.filter_endpoint, query_string)  # queryString not needed here
    logger.debug(f"filter actions: {str(filter_actions)}")

    actions = filter_actions['result']

    # return 500 in case the requester has no access (if BLOCK_URL_ACTION is specified in one of the actions)
    if any(filter_action['action'] == FilterAction.BLOCK_URL or filter_action['action'] == FilterAction.DENY
           for filter_action in actions):
        return "Access denied!", ResponseCode.ACCESS_DENIED_CODE

    # Go out to the actual destination webserver
    logger.info("sending query the the backend data service")

    logger.info(f"query gateway URL: {get_backend_url()}, request.method: {request.method}")
    data, return_headers = send_query_backend(query_string, request.headers, request.method, request.form, request.args)
    if data is None:
        logger.warning("no results returned from the backend data service")
        return "No results returned", ResponseCode.VALID_RETURN

    logger.info("filtering received data")
    response = filter_data(data, return_headers, filter_actions)
    return response


def decrypt_jwt(encrypted_token, flat_key):
    # String with "Bearer <token>".  Strip out "Bearer"...
    prefix = 'Bearer'
    if not encrypted_token.startswith(prefix):
        error_message = f'\"Bearer\" not found in token: {encrypted_token}'
        logger.error(error_message)
        raise Exception(error_message)

    stripped_token = encrypted_token[len(prefix):].strip()
    algorithms = ["HS256"]  # using the default, if it is changed then it should also be changed in the frontend code
    secret = "temp"
    decoded_jwt = jwt.api_jwt.decode(stripped_token, secret, algorithms)

    logger.debug(f"decoded_jwt: {decoded_jwt}")

    # We might have a nested key in JWT (dict within dict).  In that case, flatKey will express the hierarchy and so we
    # will iteratively chunk through it.
    decoded_key = None
    while type(decoded_jwt) is dict:
        for s in flat_key.split('.'):
            if s in decoded_jwt:
                decoded_jwt = decoded_jwt[s]
                decoded_key = decoded_jwt
            else:
                logger.warning(f"{s} not found in decoded_key")
                return decoded_key
    return decoded_key


if __name__ == "__main__":
    overrides = kofiko.configure()
    init_root_logger()

    logger.info(f"configuration overrides:\n{json.dumps(overrides, indent=2)}")

    opa_wait_seconds = 30
    logger.info(f"waiting {opa_wait_seconds} seconds for the OPA sidecar")
    time.sleep(opa_wait_seconds)  # waiting for the opa sidecar to run

    logger.info("sending the policy to the OPA sidecar")
    configmap_to_policy()

    logger.info(f"starting flask server, listening on port number: {ServerConfig.port}")
    app.run(port=ServerConfig.port, host='0.0.0.0')
