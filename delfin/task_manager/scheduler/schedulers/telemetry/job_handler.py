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
from oslo_config import cfg
from oslo_log import log
from oslo_utils import uuidutils

from delfin import db
from delfin.task_manager import rpcapi as task_rpcapi
from delfin.task_manager.scheduler import schedule_manager
from delfin.task_manager.scheduler.schedulers.telemetry.performance_collection_handler import \
    PerformanceCollectionHandler

CONF = cfg.CONF
LOG = log.getLogger(__name__)


class JobHandler(object):
    def __init__(self, ctx, task_id, storage_id, args, interval):
        self.ctx = ctx
        self.task_id = task_id
        self.storage_id = storage_id
        self.args = args
        self.interval = interval
        self.task_rpcapi = task_rpcapi.TaskAPI()
        self.scheduler = schedule_manager.SchedulerManager().get_scheduler()
        self.stopped = False
        self.job_ids = set()

    @staticmethod
    def get_instance(ctx, task_id):
        task = db.task_get(ctx, task_id)
        return JobHandler(ctx, task_id, task['storage_id'],
                          task['args'], task['interval'])

    def schedule_job(self, job):

        if self.stopped:
            """If Job is stopped return immediately"""
            return

        LOG.info("........... JobHandler received A job %s to schedule.............. " % job['id'])
        instance = PerformanceCollectionHandler.get_instance(self.ctx, self.task_id)
        current_time = int(datetime.now().timestamp())
        last_run_time = current_time
        next_collection_time = last_run_time + job['interval']
        job_id = uuidutils.generate_uuid()
        next_collection_time = datetime \
            .fromtimestamp(next_collection_time) \
            .strftime('%Y-%m-%d %H:%M:%S')
        # is job already there for this task in scheduler

        existing_job_id = job['job_id']

        scheduler_job = self.scheduler.get_job(existing_job_id)

        if not (existing_job_id and scheduler_job):
            LOG.info('.......... JobHandler scheduling a new job')
            self.scheduler.add_job(
                instance, 'interval', seconds=job['interval'],
                next_run_time=next_collection_time, id=job_id,
                misfire_grace_time=int(
                        CONF.telemetry.performance_collection_interval / 2))

            update_task_dict = {'job_id': job_id,
                                'last_run_time': last_run_time}
            db.task_update(self.ctx, self.task_id, update_task_dict)
            LOG.info('............Periodic collection task triggered for for job id: '
                     '%s ' % self.task_id)
        else:
            LOG.info('.......... Job already exists with this scheduler')

    def stop(self):
        self.stopped = True
        for job_id in self.job_ids.copy():
            self.remove_scheduled_job(job_id)
        LOG.info("Stopping telemetry jobs")

    def remove_scheduled_job(self, job_id):
        if job_id in self.job_ids:
            self.job_ids.remove(job_id)
        if job_id and self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)

    def remove_job(self, job):
        try:
            LOG.info("........received job %s to remove", job['id'])
            job_id = job['job_id']
            self.remove_scheduled_job(job_id)
            db.task_delete(self.ctx, job['id'])
            LOG.info("...........removed job %s ", job['id'])
        except Exception as e:
            LOG.error("Failed to remove periodic scheduling job , reason: %s.",
                      six.text_type(e))
