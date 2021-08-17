# Copyright 2021 The SODA Authors.
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


import six

from oslo_log import log

from delfin import utils


LOG = log.getLogger(__name__)


@six.add_metaclass(utils.Singleton)
class Distributor(object):

    def __init__(self, scheduler=None):
        self.scheduler=None
        LOG.info("NAju Init distributor")

    def start(self):
        LOG.info("NAju Tooz callback recieved on becoming leader")

    def stop(self):
        """Cleanup periodic jobs"""
        LOG.info("NAju Tooz callback recieved on loosing leader")

