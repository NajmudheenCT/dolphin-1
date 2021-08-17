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

**periodical task manager**

"""
from oslo_log import log

from delfin import manager

from delfin.task_manager.scheduler.schedulers.telemetry.job_handler import JobHandler
from delfin.task_manager.tasks import telemetry

LOG = log.getLogger(__name__)


class MetricsTaskManager(manager.Manager):
    """manage periodical tasks"""

    RPC_API_VERSION = '1.0'

    def __init__(self, service_name=None, *args, **kwargs):
        self.telemetry_task = telemetry.TelemetryTask()
        super(MetricsTaskManager, self).__init__(*args, **kwargs)

    def addJob1(self, context, msg, task_id):
        LOG.info('Addd job message:{0}'
                 .format(msg))
        print('target in recieving side', self.target)
        instance = JobHandler.get_instance(context, task_id)

        instance.addJob1()
