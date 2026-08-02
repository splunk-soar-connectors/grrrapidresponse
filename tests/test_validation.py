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
import unittest

from grr_validation import validate_client_id


class ValidateClientIdTest(unittest.TestCase):
    def test_accepts_grr_grammar(self):
        for value in ("C.0123456789abcdef", "C.ABCDEF0123456789"):
            with self.subTest(value=value):
                self.assertEqual(validate_client_id(value), value)

    def test_rejects_non_grr_values(self):
        invalid_values = (".", "..", "../config", "C.0123456789abcde", "C.0123456789abcdef0", "c.0123456789abcdef", "C.0123456789abcdeg")
        for value in invalid_values:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_client_id(value)
