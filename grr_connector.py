# File: grr_connector.py
#
# Copyright (c) 2018-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Phantom App imports
import json
import sys
import time

import phantom.app as phantom
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

# Usage of the consts file is recommended
from grr_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class GrrConnector(BaseConnector):
    ACTION_ID_GET_FILE_INFO = "get_file_info"
    ACTION_ID_GET_BROWSER_CACHE = "get_browser_cache"
    ACTION_ID_GET_HUNTS = "get_hunts"

    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _process_empty_reponse(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = f"Status Code: {status_code}. Data from server:\n{error_text}\n"

        message = message.replace("{", "{{").replace("}", "}}")

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.text.lstrip(")]}'\n")
            resp_json = json.loads(resp_json)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Unable to parse JSON response. Error: {e!s}"), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {} Data from server: {}".format(
            r.status_code, resp_json.get("message", r.text.replace("{", "{{").replace("}", "}}"))
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if "json" in r.headers.get("Content-Type", ""):
            return self._process_json_response(r, action_result)

        # Process an HTML resonse, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {} Data from server: {}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, method="get"):
        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), resp_json)

        # Create a URL to connect to
        url = self._base_url + endpoint + "?strip_type_info=1"

        try:
            r = request_func(
                url,
                auth=(config[GRR_JSON_USERNAME], config[GRR_JSON_PASSWORD]),  # basic authentication
                data=data,
                headers=headers,
                verify=config.get(GRR_JSON_VERIFY_SERVER_CERT, False),
                params=params,
            )
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Error Connecting to server. Details: {e!s}"), resp_json)

        return self._process_response(r, action_result)

    def _make_flow_rest_call(self, endpoint, action_result, body=None):
        """To do a flow you need to make the call then poll for the action to finish"""
        """ You also need to get the csrf cookie in order to send a post request """
        """ endpoint should be /api/v2/clients/{cid}/flows """

        self.save_progress("Making flow rest call")

        resp_json = None

        config = self.get_config()
        url = self._base_url + endpoint
        auth = (config[GRR_JSON_USERNAME], config[GRR_JSON_PASSWORD])
        verify_cert = config.get(GRR_JSON_VERIFY_SERVER_CERT, False)
        s = requests.Session()
        s.auth = auth

        try:
            csrf = s.get(self._base_url, verify=verify_cert).cookies["csrftoken"]
            headers = {"X-CSRFToken": csrf, "Referer": self._base_url}
            r2 = s.post(url + "?strip_type_info=1", json=body, headers=headers, verify=verify_cert, timeout=DEFAULT_REQUEST_TIMEOUT)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e), None

        ret_val, resp_json = self._verify_response(r2, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        if "message" in resp_json:
            return action_result.set_status(phantom.APP_ERROR, "Error starting flow"), None

        # Now we need to wait for the flow to finish
        flow_id = resp_json["flowId"]
        ret_val = self._wait_for_flow(url + f"/{flow_id}?strip_type_info=1", s, action_result, verify_cert)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        try:
            r = s.get(url + f"/{flow_id}", verify=verify_cert, timeout=DEFAULT_REQUEST_TIMEOUT)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e), None

        ret_val, resp_json = self._verify_response(r, action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        return phantom.APP_SUCCESS, resp_json

    def _verify_response(self, r, action_result):
        self.save_progress("Verifying response")

        if not r.ok:
            message = "Can't process response from server. Status Code: {0} Message: {1}"
            try:
                resp_json = r.text.lstrip(")]}'\n")
                resp_json = json.loads(resp_json)
                message = message.format(r.status_code, resp_json.get("message", r.reason))
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, GRR_ERR_JSON_PARSE, e), None

            return action_result.set_status(phantom.APP_ERROR, message), None

        try:
            resp_json = json.loads(r.text.splitlines()[1])
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, GRR_ERR_JSON_PARSE, e), None

        return phantom.APP_SUCCESS, resp_json

    def _wait_for_flow(self, address, s, action_result, verify_cert=False):
        self.save_progress("Waiting for flow to complete")

        while True:
            try:
                r = s.get(address, verify=verify_cert, timeout=DEFAULT_REQUEST_TIMEOUT)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, GRR_ERR_SERVER_CONNECTION, e)
            ret_val, resp_json = self._verify_response(r, action_result)
            if phantom.is_fail(ret_val):
                return action_result.get_status()
            if resp_json["state"] != "RUNNING":
                # Flow has finished
                break
            time.sleep(1)
        return phantom.APP_SUCCESS

    def _get_flow_result(self, endpoint, action_result):
        self.save_progress("Retrieving flow results")

        result_endpoint = endpoint + "/results"

        # make rest call
        ret_val, response = self._make_rest_call(result_endpoint, action_result)

        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        return phantom.APP_SUCCESS, response

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress("Testing by sending request to /api/v2/clients")

        # make rest call
        ret_val, response = self._make_rest_call("/api/v2/clients", action_result)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_cron_jobs(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary
        offset = param.get("offset", "")
        count = param.get("count", "")

        if count != "" and (str(count).isdigit() is False or int(count) == 0):
            return action_result.set_status(phantom.APP_ERROR, GRR_INVALID_COUNT_MSG.format(param_name="count"))

        if offset != "" and str(offset).isdigit() is False:
            return action_result.set_status(phantom.APP_ERROR, GRR_INVALID_OFFSET_MSG.format(param_name="offset"))

        params = {"offset": offset, "count": count}

        # make rest call
        ret_val, response = self._make_rest_call("/api/v2/cron-jobs", action_result, params=params, headers=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        for item in response.get("items", {}):
            action_result.add_data(item)

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.save_progress(f"Action: {self.get_action_identifier()} - Status: {phantom.APP_SUCCESS}")
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved cron jobs")

    def _handle_list_endpoints(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        params = {"count": 0}

        # make rest call
        ret_val, response = self._make_rest_call("/api/v2/clients", action_result, params=params, headers=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        for item in response.get("items", {}):
            action_result.add_data(item)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary["num_endpoints"] = len(response["items"])

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.save_progress(f"Action: {self.get_action_identifier()} - Status: {phantom.APP_SUCCESS}")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_connections(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        client_id = requests.compat.quote(param[GRR_JSON_CLIENT_ID])

        endpoint = f"/api/v2/clients/{client_id}/flows"

        # Request body to start a FileFinder flow
        body = {
            "flow": {
                "args": {"@type": "type.googleapis.com/EmptyMessage"},
                "name": "Netstat",
                "runner_args": {"notify_to_user": False, "output_plugins": [], "priority": "HIGH_PRIORITY"},
            }
        }

        # make rest call
        ret_val, response = self._make_flow_rest_call(endpoint, action_result, body=body)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary["status"] = response.get("context", {}).get("status")
        summary["flow_id"] = response.get("flowId", {})

        # make rest call to get results
        ret_val, response = self._get_flow_result(endpoint + "/{}".format(response.get("flowId", {})), action_result)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Add the response into the data section
        for item in response.get("items", {}):
            action_result.add_data(item)

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved netstat information")

    def _handle_get_hunts(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary
        offset = param.get("offset", "")
        count = param.get("count", "")
        created_by = param.get("created_by", "")
        description_contains = param.get("description_contains", "")
        active_within = param.get("active_within", "")

        if count != "" and (not str(count).isdigit() or int(count) == 0):
            return action_result.set_status(phantom.APP_ERROR, GRR_INVALID_COUNT_MSG.format(param_name="count"))

        if offset != "" and not str(offset).isdigit():
            return action_result.set_status(phantom.APP_ERROR, GRR_INVALID_OFFSET_MSG.format(param_name="offset"))

        params = {
            "offset": offset,
            "count": count,
            "created_by": created_by,
            "description_contains": description_contains,
            "active_within": active_within,
        }

        # make rest call
        ret_val, response = self._make_rest_call("/api/v2/hunts", action_result, params=params, headers=None)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        for item in response.get("items", {}):
            action_result.add_data(item)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary["total_hunts"] = len(response.get("items", {}))

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.save_progress(f"Action: {self.get_action_identifier()} - Status: {phantom.APP_SUCCESS}")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_system_info(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        # Required values can be accessed directly
        client_id = requests.compat.quote(param[GRR_JSON_CLIENT_ID])

        if client_id is None:
            return action_result.set_status(phantom.APP_ERROR, "Please specify client id")

        endpoint = f"/api/v2/clients/{client_id}"

        # make rest call
        ret_val, response = self._make_rest_call(endpoint, action_result)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary["num_users"] = len(response["users"])

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        self.save_progress(f"Action: {self.get_action_identifier()} - Status: {phantom.APP_SUCCESS}")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_file_info(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        # Required values can be accessed directly
        client_id = requests.compat.quote(param[GRR_JSON_CLIENT_ID])
        file_path = param[GRR_JSON_FILE_PATH]

        endpoint = f"/api/v2/clients/{client_id}/flows"

        # Request body to start a FileFinder flow
        body = {
            "flow": {
                "args": {"paths": [file_path], "@type": "type.googleapis.com/FileFinderArgs"},
                "name": "FileFinder",
                "runner_args": {"notify_to_user": False, "output_plugins": [], "priority": "HIGH_PRIORITY"},
            }
        }

        # make rest call
        ret_val, response = self._make_flow_rest_call(endpoint, action_result, body=body)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        if response.get("context", {}).get("status") == "Found and processed 0 files.":
            return action_result.set_status(phantom.APP_SUCCESS, "Found and processed 0 files")

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary["flow_id"] = response.get("flowId", {})

        # make rest call to get results
        ret_val, response = self._get_flow_result(endpoint + "/{}".format(response.get("flowId", {})), action_result)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Add the response into the data section
        for item in response.get("items", {}):
            action_result.add_data(item)

        summary["total_count"] = response.get("totalCount", {})

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved file information")

    def _handle_get_browser_cache(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        # Required values can be accessed directly
        client_id = requests.compat.quote(param[GRR_JSON_CLIENT_ID])
        regex = param[GRR_JSON_BROWSER_CACHE_REGEX]
        users = [x.strip() for x in str(param[GRR_JSON_USERS]).split(",") if x.strip()]  # might need to format if multiple users

        check_chrome = str(param.get("check_chrome", True)).lower() == "true"
        check_firefox = str(param.get("check_firefox", True)).lower() == "true"
        check_ie = str(param.get("check_ie", True)).lower() == "true"

        endpoint = f"/api/v2/clients/{client_id}/flows"

        # Request body to start a FileFinder flow
        body = {
            "flow": {
                "args": {
                    "grepUsers": users,
                    "checkChrome": check_chrome,
                    "checkIe": check_ie,
                    "dataRegex": regex,
                    "@type": "type.googleapis.com/CacheGrepArgs",
                    "checkFirefox": check_firefox,
                },
                "name": "CacheGrep",
            }
        }

        # make rest call
        ret_val, response = self._make_flow_rest_call(endpoint, action_result, body=body)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary["flow_id"] = response.get("flowId", {})

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved browser cache information")

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)

        elif action_id == "get_cron_jobs":
            ret_val = self._handle_get_cron_jobs(param)

        elif action_id == self.ACTION_ID_GET_HUNTS:
            ret_val = self._handle_get_hunts(param)

        elif action_id == "get_system_info":
            ret_val = self._handle_get_system_info(param)

        elif action_id == "list_endpoints":
            ret_val = self._handle_list_endpoints(param)

        elif action_id == "list_connections":
            ret_val = self._handle_list_connections(param)

        elif action_id == self.ACTION_ID_GET_FILE_INFO:
            ret_val = self._handle_get_file_info(param)

        elif action_id == self.ACTION_ID_GET_BROWSER_CACHE:
            ret_val = self._handle_get_browser_cache(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        self._base_url = config.get("server").rstrip("/")

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == "__main__":
    import argparse

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)
    argparser.add_argument("-v", "--verify", action="store_true", help="verify", required=False, default=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password
    verify = args.verify

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = GrrConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, verify=verify, timeout=DEFAULT_REQUEST_TIMEOUT)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=verify, data=data, headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print(f"Unable to get session id from the platform. Error: {e}")
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = GrrConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
