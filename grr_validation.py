# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re


GRR_CLIENT_ID_PATTERN = re.compile(r"C\.[0-9a-fA-F]{16}\Z")


def validate_client_id(value: object) -> str:
    """Return a GRR client ID after enforcing its complete path-segment grammar."""
    client_id = str(value)
    if not GRR_CLIENT_ID_PATTERN.fullmatch(client_id):
        raise ValueError("Client ID must use the format C. followed by 16 hexadecimal characters")
    return client_id
