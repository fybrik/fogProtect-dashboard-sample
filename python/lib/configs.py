import os
import kofiko
from kofiko import config_section


@config_section
class ServerConfig:
    # the port on which the server listens, all rest requests from the user should be sent to this port
    port = 5559

    # the address of the backend server, the backend server is the server that actually retrieves
    # the data and returns it.
    backend_address = 'localhost'

    # the address on which the backend server listens.
    backend_port = 9005

    # the string that will be used for columns in the returned data that need to be redacted.
    redaction_statement = 'XXX'

    # TODO: turn the following keys into one list (for future additions of keys) and change the relevant places
    #  in the whole code.
    # the role key in case the user is using JWT and wants to specify a role
    jwt_role_key = 'role'

    # the role key in case the user is using JWT and wants to specify an organization
    jwt_organization_key = 'organization'


@config_section
class OPAConfig:
    # the port on which the OPA server listens
    port = 8181

    # the address of the OPA server
    address = 'localhost'

    # the endpoint to send to in order to get the list of filters from the OPA server
    filter_endpoint = '/v1/data/katalog/example/filters'

    # the endpoint to send to in order to get the list of blocks from the OPA server
    block_endpoint = '/v1/data/katalog/example/blockList'

    # TODO: add documentation about this endpoint
    query_endpoint = '/v1/data/localEval/block'

    # the enpoint to send to in order to update the policy in the OPA server.
    set_policy_endpoint = '/v1/policies/localEval'

    # the namespace in the cluster in which the assets reside.
    asset_namespace = 'default'

    # TODO: change this to the actual path of the configmap (mounted in the container)
    # the path for the configmap file created by the fybrik-manager whenever a new policy is applied
    configmap_path = 'fogprotect-policy.yaml'


class FilterAction:
    BLOCK_URL = 'BlockURL'
    REDACT_COLUMN = 'RedactColumn'
    BLOCK_COLUMN = 'BlockColumn'
    FILTER = 'Filter'
    ALLOW = 'Allow'
    DENY = 'Deny'


class ResponseCode:
    ACCESS_DENIED_CODE = 403
    ERROR_CODE = 406
    VALID_RETURN = 200
