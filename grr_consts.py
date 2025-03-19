# File: grr_consts.py
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
GRR_ERR_SERVER_CONNECTION = "Connection failed"
GRR_ERR_FROM_SERVER = "API failed, Status code: {status}, Detail: {detail}"
GRR_ERR_JSON_PARSE = "Unable to parse the fields parameter into a dictionary"
GRR_ERR_VALIDATE_FAILED = "Failed to validate connection"

GRR_JSON_USERNAME = "username"
GRR_JSON_PASSWORD = "password"  # pragma: allowlist secret
GRR_JSON_SERVER = "server"
GRR_JSON_CLIENT_ID = "client_id"
GRR_JSON_FILE_PATH = "file_path"
GRR_JSON_BROWSER_CACHE_REGEX = "browser_cache_regex"
GRR_JSON_USERS = "users"
GRR_JSON_VERIFY_SERVER_CERT = "verify_server_cert"
GRR_INVALID_COUNT_MSG = "Please provide a non-zero positive integer in the {param_name} parameter"
GRR_INVALID_OFFSET_MSG = "Please provide a non-negative integer in the {param_name} parameter"
DEFAULT_REQUEST_TIMEOUT = 30  # in seconds
