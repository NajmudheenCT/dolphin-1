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

from webob import exc

from dolphin import db, cryptor
from dolphin import exception
from dolphin.api.common import wsgi, LOG
from dolphin.api.views import access_info as access_info_viewer
from dolphin.drivers import api as driverapi
from dolphin.api.views import storages as storage_view
from dolphin.i18n import _

def update_access_info(access_info, body):
    access_info_dict=access_info.to_dict()
    for key in access_info_dict:
        if key in body:
            access_info_dict[key] = body[key]
    del access_info_dict['created_at']
    del access_info_dict['updated_at']
    return access_info_dict


class AccessInfoController(wsgi.Controller):

    def __init__(self):
        super(AccessInfoController, self).__init__()
        self._view_builder = access_info_viewer.ViewBuilder()
        self.driver_api = driverapi.API()

    def show(self, req, id):
        """Show access information by storage id."""
        ctxt = req.environ['dolphin.context']

        try:
            access_info = db.access_info_get(ctxt, id)
        except exception.AccessInfoNotFound as e:
            raise exc.HTTPNotFound(explanation=e.msg)

        return self._view_builder.show(access_info)
    def update(self, req, id, body):
        """Update storage access information."""
        ctx = req.environ.get('dolphin.context')

        # Get existing access_info from DB and merge modified attributes
        access_info_present = db.access_info_get(ctx, id)
        access_info_updated_dict = update_access_info(access_info_present, body)
        # update access_info first
        try:
            access_info_updated_dict['password'] = cryptor.encode(access_info_updated_dict['password'])
            db.access_info_update(ctx, id, access_info_updated_dict)
        except Exception as e:
            msg = _('Failed to update storage access info: {0}'.format(e))
            LOG.error(msg)
            raise exc.HTTPBadRequest(explanation=msg)

        try:
            # Discover Storage with new access info
            storage = self.driver_api.discover_storage(ctx, access_info_updated_dict)
            # check whether new stora.serilnu == oldstorage==serilno
            if storage:
                db.storage_update(ctx, id, storage)
                return storage_view.build_storage(storage)
            else:
                raise exception.StorageNotFound()
        except (exception.InvalidCredential,
                exception.StorageDriverNotFound,
                exception.AccessInfoNotFound,
                exception.StorageNotFound) as e:
            # roll back access info
            LOG.error("Failed to get storage with new access_info, reverting access_info")
            # roll_back access_info
            db.access_info_update(ctx, id, access_info_present)
            raise exc.HTTPBadRequest(explanation=e.message)
        except Exception as e:
            msg = _('Failed to update storage access info: {0}'.format(e))
            LOG.error(msg)
            # roll_back access_info
            db.access_info_update(ctx, id, access_info_present)
            raise exc.HTTPBadRequest(explanation=msg)


def create_resource():
    return wsgi.Resource(AccessInfoController())