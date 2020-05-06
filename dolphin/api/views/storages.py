# Copyright 2020 The SODA Authors.
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
import copy

from dolphin.api.views import common


def build_storages(storages):
    # Build list of storages
    views = [build_storage(storage)
             for storage in storages]
    return dict(storages=views)


def build_storage(storage):
    view = copy.deepcopy(storage)

    # Sql Numeric(Decimal) type is not able to be serialized directly into JSON , Need to convert all numeric fields
    # to float
    numeric_keys = ['total_capacity', 'used_capacity', 'free_capacity']
    common.convert_numeric_to_float(numeric_keys, view)
    return dict(view)
