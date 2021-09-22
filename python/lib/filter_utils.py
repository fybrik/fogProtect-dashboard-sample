import json
import logging
from .log_utils import init_root_logger
from .configs import *

init_root_logger()
logger = logging.getLogger(__name__)


def _can_filter(data, headers):
    # The input can actually be a list, a string (JSON), or interpreted by Python to be a dict
    if type(data) is dict:
        return True

    if type(data) is list and len(data) > 0 and type(data[0]) is dict:
        return True

    if type(data) is str:
        if headers['Content-Type'] != 'video/mp4':
            return True

        # check if the data is a JSON string
        try:
            json.loads(data)
        except:
            return False

        return True

    return False


# create a list of dicts of the data in order to be able to filter it
def _prepare_for_filter(data):
    prepared_data = [data]
    if type(data) is str:
        try:
            # the following call should succeed as we checked if we can turn the data into JSON in previous calls
            prepared_data = [json.loads(data)]
        except:
            logger.error("could not convert string data to JSON")

    if type(data) is list:
        # remove elements of types other than dict
        prepared_data = [element for element in data if type(element) is dict]

    return prepared_data


def _apply_action(data, key_search, action):
    try:
        i = key_search.pop(0)
    except:
        logger.error(f"on key_search.pop, key_search: {str(key_search)}")
        return data

    while i in data:
        last = data[i]
        if not key_search:
            if action == FilterAction.REDACT_COLUMN:
                data[i] = ServerConfig.redaction_statement
            else:
                del data[i]
            return data
        else:
            _apply_action(data[i], key_search, action)
            return data


def filter_data(data, headers, filter_actions):

    if not _can_filter(data, headers):
        logger.info(f"can't filter this type of data: {type(data)} - returning data with no filter")
        return data, ResponseCode.VALID_RETURN

    prefiltered_data = _prepare_for_filter(data)
    filtered_data = ''

    for data_element in prefiltered_data:
        for result_dict in filter_actions['result']:
            action = result_dict['action']

            # Handle the filtering here
            if action == FilterAction.ALLOW:
                return json.dumps(data), ResponseCode.VALID_RETURN
            # Note: can have both "RedactColumn" and "BlockColumn" actions in line
            if action == FilterAction.REDACT_COLUMN or action == FilterAction.BLOCK_COLUMN:
                columns = result_dict['columns']
                for key_search in columns:
                    _apply_action(data_element, key_search.split('.'), action)
            if action == FilterAction.FILTER:
                # TODO: add support for filter predicates
                logger.warning("filter predicates is not supported yet")
                filter_pred = result_dict['filterPredicate']

        filtered_data += json.dumps(data_element)
        logger.debug(f"filtered line: {filtered_data}")
        return filtered_data, ResponseCode.VALID_RETURN
