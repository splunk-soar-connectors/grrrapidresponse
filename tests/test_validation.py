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
import pytest

from grr_validation import validate_client_id


@pytest.mark.parametrize("value", ["C.0123456789abcdef", "C.ABCDEF0123456789"])
def test_validate_client_id_accepts_grr_grammar(value):
    assert validate_client_id(value) == value


@pytest.mark.parametrize(
    "value",
    [".", "..", "../config", "C.0123456789abcde", "C.0123456789abcdef0", "c.0123456789abcdef", "C.0123456789abcdeg"],
)
def test_validate_client_id_rejects_non_grr_values(value):
    with pytest.raises(ValueError):
        validate_client_id(value)
