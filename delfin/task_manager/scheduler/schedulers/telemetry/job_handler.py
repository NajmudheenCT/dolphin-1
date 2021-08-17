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

from datetime import datetime

import six
from oslo_log import log
from oslo_utils import uuidutils

from delfin import db
from delfin.task_manager import rpcapi as task_rpcapi
from delfin.task_manager.scheduler import schedule_manager
from delfin.task_manager.scheduler.schedulers.telemetry.performance_collection_handler import \
    PerformanceCollectionHandler

LOG = log.getLogger(__name__)


class JobHandler(object):
    def __init__(self, ctx, task_id, storage_id, args, interval):
        self.ctx = ctx
        self.task_id = task_id
        self.storage_id = storage_id
        self.args = args
        self.interval = interval
        self.task_rpcapi = task_rpcapi.TaskAPI()
        # schedule_manager.SchedulerManager().start()
        self.scheduler = schedule_manager.SchedulerManager().get_scheduler()

    @staticmethod
    def get_instance(ctx, task_id):
        LOG.info('Naju Get PerformanceCollectionHandler instance')
        task = db.task_get(ctx, task_id)
        return JobHandler(ctx, task_id, task['storage_id'],
                                            task['args'], task['interval'])



    def addJob1(self):
        LOG.info(" NAju recieved add Job 1 new job handler")
        instance = PerformanceCollectionHandler.get_instance(self.ctx, self.task_id)
        current_time = int(datetime.now().timestamp())
        last_run_time = current_time
        next_collection_time = last_run_time + 120
        job_id = uuidutils.generate_uuid()
        next_collection_time = datetime \
            .fromtimestamp(next_collection_time) \
            .strftime('%Y-%m-%d %H:%M:%S')
        self.scheduler.add_job(
            instance, 'interval', seconds=120,
            next_run_time=next_collection_time, id=job_id,
            misfire_grace_time=60)
        # jobs book keeping
        # self.job_ids.add(job_id)

        update_task_dict = {'job_id': job_id,
                            'last_run_time': last_run_time}
        db.task_update(self.ctx, self.task_id, update_task_dict)
        LOG.info('Periodic collection task triggered for for task id: '
                 '%s ' % self.task_id)





