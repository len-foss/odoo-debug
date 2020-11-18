# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from pprint import pformat as pf

from odoo import _, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class Base(models.AbstractModel):

    _inherit = "base"

    def pprint(self, limit=300):
        """Equivalent to read, but slightly better suited to debugging.
           The main feature is to remove the binary fields that are unreadable
           in a debugger session.
           Other text fields that could be very long are also truncated up to limit.
        :param limit: Optional[int] the length at which text fields are truncated.
        :return: List[Dict]
        """
        result = self.read()
        fields = self._fields
        for field_name in self._fields:
            field_type = fields[field_name].type
            for record, read in zip(self, result):
                value = record[field_name]
                if field_type == "binary" and value:
                    read[field_name] = "Binary: {}".format(len(value))
                elif field_type in ["char", "text", "html"]:
                    if value and limit and len(value) > limit:
                        read[field_name] = value[:limit] + "...[{}]".format(len(value))
                elif field_type == "date" and value:
                    read[field_name] = value.strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif field_type == "datetime" and value:
                    read[field_name] = value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return result

    def pwrite(self, name=None, root="/tmp"):
        """Write the pretty-printed recordset to a file (by default in /tmp).
           This makes it easy to use diff between to compare records
           (e.g. to investigate how a record changed before/after some action).
        :param name: the name of the file
        :param root: the destination folder. Defaults to /tmp
        :return: None (side-effect only)
        """
        result = self.pprint()
        if not name:
            if len(self) > 10:
                suffix = "{}_records".format(len(self))
            else:
                suffix = ",".join(map(str, self.ids))
            name = self._name.replace(".", "_") + ":" + suffix
        full_name = os.path.join(root, name)
        with open(full_name, 'w') as f:
            f.write(pf(result))
