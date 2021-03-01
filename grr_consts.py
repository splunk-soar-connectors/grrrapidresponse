# File: grr_consts.py
# Copyright (c) 2018-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

GRR_ERR_SERVER_CONNECTION = "Connection failed"
GRR_ERR_FROM_SERVER = "API failed, Status code: {status}, Detail: {detail}"
GRR_ERR_JSON_PARSE = "Unable to parse the fields parameter into a dictionary"
GRR_ERR_VALIDATE_FAILED = "Failed to validate connection"

GRR_JSON_USERNAME = "username"
GRR_JSON_PASSWORD = "password"
GRR_JSON_SERVER = "server"
GRR_JSON_CLIENT_ID = "client_id"
GRR_JSON_FILE_PATH = "file_path"
GRR_JSON_BROWSER_CACHE_REGEX = "browser_cache_regex"
GRR_JSON_USERS = "users"
GRR_JSON_VERIFY_SERVER_CERT = "verify_server_cert"
GRR_INVALID_COUNT_MSG = "Please provide a non-zero positive integer in {param_name}"
GRR_INVALID_OFFSET_MSG = "Please provide a non-negative integer in {param_name}"
