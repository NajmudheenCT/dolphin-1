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

"""
Client side of the task manager RPC API.
"""

import oslo_messaging as messaging
from oslo_config import cfg

from delfin import rpc

CONF = cfg.CONF


class TaskAPI(object):
    """Client side of the task rpc API.

    API version history:

        1.0 - Initial version.
    """

    RPC_API_VERSION = '1.0'

    def __init__(self):
        super(TaskAPI, self).__init__()
        self.target = messaging.Target(topic='2',
                                       version=self.RPC_API_VERSION)
        self.client = rpc.get_client(self.target, version_cap=self.RPC_API_VERSION)

    def get_client(self, topic):
        target = messaging.Target(topic=topic,
                                       version=self.RPC_API_VERSION)
        return rpc.get_client(target, version_cap=self.RPC_API_VERSION)
    def addJob1(self, context, message, task_id, storage_id):
        print("Naju inside rpcapi")
        print("target  is", self.target)
        rpc_client = self.get_client(str(task_id))
        call_context = rpc_client.prepare(topic=str(task_id), version='1.0', fanout=True)
        print("Naju client prepare done")
        return call_context.cast(context, 'addJob1',
                                 msg=message, task_id=task_id)
