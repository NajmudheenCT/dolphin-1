# Copyright 2020 The SODA Authors.
# Copyright 2010 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import webob.dec
import webob.request

from dolphin import context
from dolphin.api.common import wsgi as os_wsgi
from dolphin.common import config, constants  # noqa


@webob.dec.wsgify
def fake_wsgi(self, req):
    return self.application


class HTTPRequest(os_wsgi.Request):

    @classmethod
    def blank(cls, *args, **kwargs):
        if not kwargs.get('base_url'):
            kwargs['base_url'] = 'http://localhost/v1'
        use_admin_context = kwargs.pop('use_admin_context', False)
        out = os_wsgi.Request.blank(*args, **kwargs)
        out.environ['dolphin.context'] = context.RequestContext(
            is_admin=use_admin_context)
        return out


def fake_storages_get_all(context, marker=None, limit=None, sort_keys=None,
                          sort_dirs=None, filters=None, offset=None):
    return [
        {
            "id": "12c2d52f-01bc-41f5-b73f-7abf6f38a2a6",
            "created_at": "2020-06-09T08:59:48.710890",
            "free_capacity": 1045449,
            "updated_at": "2020-06-09T08:59:48.769470",
            "name": "fake_driver",
            "location": "HK",
            "firmware_version": "1.0.0",
            "vendor": "fake_vendor",
            "status": "normal",
            "sync_status": constants.SyncStatus.SYNCED,
            "model": "fake_model",
            "description": "it is a fake driver.",
            "serial_number": "2102453JPN12KA0000113",
            "used_capacity": 3126,
            "total_capacity": 1048576
        },
        {
            "id": "277a1d8f-a36e-423e-bdd9-db154f32c289",
            "created_at": "2020-06-09T08:58:23.008821",
            "free_capacity": 1045449,
            "updated_at": "2020-06-09T08:58:23.033601",
            "name": "fake_driver",
            "location": "HK",
            "firmware_version": "1.0.0",
            "vendor": "fake_vendor",
            "status": "normal",
            "sync_status": constants.SyncStatus.SYNCED,
            "model": "fake_model",
            "description": "it is a fake driver.",
            "serial_number": "2102453JPN12KA0000112",
            "used_capacity": 3126,
            "total_capacity": 1048576
        }
    ]


def fake_storages_get_all_with_filter(
        context, marker=None, limit=None,
        sort_keys=None, sort_dirs=None, filters=None, offset=None):
    return [
        {
            "id": "12c2d52f-01bc-41f5-b73f-7abf6f38a2a6",
            "created_at": "2020-06-09T08:59:48.710890",
            "free_capacity": 1045449,
            "updated_at": "2020-06-09T08:59:48.769470",
            "name": "fake_driver",
            "location": "HK",
            "firmware_version": "1.0.0",
            "vendor": "fake_vendor",
            "status": "normal",
            "sync_status": constants.SyncStatus.SYNCED,
            "model": "fake_model",
            "description": "it is a fake driver.",
            "serial_number": "2102453JPN12KA0000113",
            "used_capacity": 3126,
            "total_capacity": 1048576
        }
    ]


def fake_storages_show(context, storage_id):
    return {
        "id": "12c2d52f-01bc-41f5-b73f-7abf6f38a2a6",
        "created_at": "2020-06-09T08:59:48.710890",
        "free_capacity": 1045449,
        "updated_at": "2020-06-09T08:59:48.769470",
        "name": "fake_driver",
        "location": "HK",
        "firmware_version": "1.0.0",
        "vendor": "fake_vendor",
        "status": "normal",
        "sync_status": constants.SyncStatus.SYNCED,
        "model": "fake_model",
        "description": "it is a fake driver.",
        "serial_number": "2102453JPN12KA0000113",
        "used_capacity": 3126,
        "total_capacity": 1048576
    }


def fake_access_info_get_all(context, marker=None, limit=None, sort_keys=None,
                             sort_dirs=None, filters=None, offset=None):
    return [
        {
            'created_at': "2020-06-09T08:59:48.710890",
            'model': 'fake_driver',
            'storage_id': '5f5c806d-2e65-473c-b612-345ef43f0642',
            'host': '10.0.0.76',
            'extra_attributes': {'array_id': '0001234567891'},
            'password': b'YWJjZA==', 'port': '1234',
            'updated_at': None,
            'username': 'admin',
            'vendor': 'fake_storage'
        }
    ]


def fake_sync(self, req, id):
    pass


def fake_storage_pools_get_all(context, marker=None, limit=None, sort_keys=None,
                               sort_dirs=None, filters=None, offset=None):
    return [
        {
            "created_at": "2020-06-10T07:17:08.707356",
            "updated_at": "2020-06-10T07:17:08.707356",
            "id": "14155a1f-f053-4ccb-a846-ed67e4387428",
            "name": "SRP_1",
            "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
            "original_id": "SRP_1",
            "description": "Dell EMC VMAX Pool",
            "status": "normal",
            "storage_type": "block",
            "total_capacity": 26300318136401,
            "used_capacity": 19054536509358,
            "free_capacity": 7245781627043
        }
    ]


def fake_pool_show(context, pool_id):
    return {
        "created_at": "2020-06-10T07:17:08.707356",
        "updated_at": "2020-06-10T07:17:08.707356",
        "id": "14155a1f-f053-4ccb-a846-ed67e4387428",
        "name": "SRP_1",
        "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
        "original_id": "SRP_1",
        "description": "Dell EMC VMAX Pool",
        "status": "normal",
        "storage_type": "block",
        "total_capacity": 26300318136401,
        "used_capacity": 19054536509358,
        "free_capacity": 7245781627043
    }
