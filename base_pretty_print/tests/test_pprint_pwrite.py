# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import functools
import math
from datetime import datetime

from odoo import fields
from odoo.tests.common import SavepointCase

import os

class TestPprint(SavepointCase):

    def test_pprint(self):
        user = self.env.ref("base.user_admin")
        user.name = "".join(map(str, range(10)))

        res = user.pprint(limit=9)[0]

        self.assertEqual(res["image"], "Binary: 6192")
        self.assertEqual(res["name"], "012345678...[10]")
        self.assertEqual(type(res["create_date"]), type(""))


class TestPwrite(SavepointCase):

    def test_zero_records(self):
        no_partner = self.env["res.partner"]
        no_partner.pwrite()

        self.assertTrue(os.path.exists("/tmp/res_partner:"))

    def test_two_records(self):
        partners = self.env["res.partner"].search([], limit=2)
        partners.pwrite()

        ids = partners.ids
        expected_name = "/tmp/res_partner:{},{}".format(ids[0], ids[1])
        self.assertTrue(os.path.exists(expected_name))

    def test_manyrecords(self):
        users = self.env["res.partner"]
        many = 12
        for i in range(many):
            users |= users.create({"name": "apostle {}".format(i)})
        users.pwrite()

        self.assertTrue(os.path.exists("/tmp/res_partner:{}_records".format(many)))