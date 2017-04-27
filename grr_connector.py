# --
# File: grr/grr_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2016
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Phantom imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Local imports
from grr_consts import *

import requests
import simplejson as json
import time


class GrrConnector(BaseConnector):

    ACTION_ID_LIST_ENDPOINTS = "list_endpoints"
    ACTION_ID_GET_FILE_INFO = "get_file_info"

    def __init__(self):
        super(GrrConnector, self).__init__()
        return

    def _make_rest_call(self, endpoint, action_result, params=None, body=None, method="get"):
        """ Function to make REST call to GRR Rapid Response server
        """

        resp_json = None
        request_func = getattr(requests, method)

        config = self.get_config()
        base = self.get_config()[GRR_JSON_SERVER]
        base = base[:-1] if base[-1] == "/" else base
        auth = (config[GRR_JSON_USERNAME], config[GRR_JSON_PASSWORD])

        try:
            r = request_func(base + endpoint, params=params, auth=auth, body=None)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e), None

        if (r.status_code < 200 and r.status_code > 399):
            return action_result.set_status(phantom.APP_ERROR, r.text), None

        # The first line of the resp is garbage which needs to be stripped away
        try:
            resp_json = json.loads(r.text.splitlines()[1])
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_JSON_PARSE, e), None

        return phantom.APP_SUCCESS, resp_json

    def _flow_rest_call(self, endpoint, action_result, body=None):
        """ To do a flow you need to make the call then poll for the action to finish """
        """ You also need to get the csrf cookie in order to send a post request """
        """ endpoint should be /api/clients/{cid}/flows """

        resp_json = None

        config = self.get_config()
        base = self.get_config()[GRR_JSON_SERVER]
        base = base[:-1] if base[-1] == "/" else base
        auth = (config[GRR_JSON_USERNAME], config[GRR_JSON_PASSWORD])
        s = requests.Session()
        s.auth = auth

        try:
            csrf = s.get(base).cookies['csrftoken']
            headers = {'X-CSRFToken': csrf, 'Referer': base}
            r2 = s.post(base + endpoint, json=body, headers=headers)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e), None

        ret_val, resp_json = self._verify_response(r2, action_result)
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        if 'message' in resp_json:
            return action_result.set_status(phantom.APP_ERROR, "Error starting flow"), None
        
        # Now we need to wait for the flow to finish
        value = resp_json['value']['urn']['value']
        flow_id = value.split('/')[-1]
        ret_val = self._wait_for_flow(base + endpoint + "/{0}".format(flow_id), s, action_result)
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        try:
            r = s.get(base + endpoint + "/{0}/results".format(flow_id))
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e), None

        ret_val, resp_json = self._verify_response(r, action_result)
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        return phantom.APP_SUCCESS, resp_json

    def _verify_response(self, r, action_result):
        if (r.status_code < 200 and r.status_code > 399):
            return action_result.set_status(phantom.APP_ERROR, r.text), None

        try:
            resp_json = json.loads(r.text.splitlines()[1])
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_JSON_PARSE, e), None

        return phantom.APP_SUCCESS, resp_json
    
    def _wait_for_flow(self, address, s, action_result):
        while True:
            try:
                r = s.get(address)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e), None
            ret_val, resp_json = self._verify_response(r, action_result)
            if (phantom.is_fail(ret_val)):
                return action_result.get_status()
            if resp_json['value']['state']['value'] != "RUNNING":
                # Flow has finished
                break
            time.sleep(1)
        return phantom.APP_SUCCESS


    def _test_connectivity(self, param):
        """ Test connectivity by retrieving 1 client """

        endpoint = "/api/clients"
        params = {'count': 1}

        action_result = ActionResult()

        ret_val, json_resp = self._make_rest_call(endpoint, action_result, params=params)
        if (phantom.is_fail(ret_val)):
            return self.set_status_save_progress(phantom.APP_ERROR, "Connectivity test failed")
        return self.set_status_save_progress(phantom.APP_SUCCESS, "Connectivity test succeeded")

    def _list_endpoints(self, param):

        action_result = self.add_action_result(ActionResult(param))
        endpoint = "/api/clients"
        params = {'count': 0}

        ret_val, json_resp = self._make_rest_call(endpoint, action_result, params=params)
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        action_result.add_data(json_resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved endpoints")

    def _get_file_info(self, param):

        action_result = self.add_action_result(ActionResult(param))
        client_id = param[GRR_JSON_CLIENT_ID]
        file_path = param[GRR_JSON_FILE_PATH]
        endpoint = "/api/clients/{0}/flows".format(client_id)

        # Request body to start a FileFinder flow
        body = { 
                "flow": {
                    "args": {
                        "paths": [ file_path ]
                        },
                    "name": "FileFinder",
                    "runner_args": {
                        "notify_to_user": False,
                        "output_plugins": [],
                        "priority": "HIGH_PRIORITY"
                        }
                    }
                }

        ret_val, json_resp = self._flow_rest_call(endpoint, action_result, body=body)
        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        action_result.add_data(json_resp)
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved file information")

    def handle_action(self, param):

        action = self.get_action_identifier()
        ret_val = phantom.APP_SUCCESS
        if (action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            ret_val = self._test_connectivity(param)
        elif (action == self.ACTION_ID_LIST_ENDPOINTS):
            ret_val = self._list_endpoints(param)
        elif (action == self.ACTION_ID_GET_FILE_INFO):
            ret_val = self._get_file_info(param)

        return ret_val

if __name__ == '__main__':
    # Imports
    import sys
    import pudb

    # Breakpoint at runtime
    pudb.set_trace()

    # The first param is the input json file
    with open(sys.argv[1]) as f:

        # Load the input json file
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=' ' * 4))

        # Create the connector class object
        connector = GrrConnector()

        # Se the member vars
        connector.print_progress_message = True

        # Call BaseConnector::_handle_action(...) to kickoff action handling.
        ret_val = connector._handle_action(json.dumps(in_json), None)

        # Dump the return value
        print ret_val

    exit(0)
