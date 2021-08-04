#import unittest
from .models import User, Workflow, Runpack, PendingStep, Garbage
from tinyorm import Model
from tinyorm import Env
from dotenv import dotenv_values
import pytest

config = dotenv_values(".env")
env = Env(config)

for m in (User, Workflow, Runpack, PendingStep, Garbage):
    m.bind(env)


class TestCase:
    def setUp(self):
        pass

    def test_user_read(self):
        u = User.get().fields(['id', 'first_name', 'uid']
                              ).order('id asc').limit(10)
        assert u

    def test_assign_first_name(self):
        u = User.find(2)
        u().first_name = 'sadasdasd'
        assert u().first_name == 'sadasdasd'

    def test_create(self):
        g = Garbage.new()
        g().scoops = 10
        g().boops = 'xlxlxlxlxlxlxlxlxlxlxlxlxlxl'
        g.save()
        assert g().id > 0

    def test_delete(self):
        Garbage.delete(where=" boops = 'xlxlxlxlxlxlxlxlxlxlxlxlxlxl' ")
        g = Garbage.get().where(" boops = 'xlxlxlxlxlxlxlxlxlxlxlxlxlxl' ").all()
        assert len(g) == 0

    def test_show_fields(self):
        u = User.new()
        assert len(u.show_fields()) > 0

    def test_shadow(self):
        """Class methods are similar to regular functions.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.

        """
        u = User.new()
        assert u.check_state()[0] == 'CLEAN'
        u().first_name = 'asdasdasd'
        assert 'first_name' in u.check_state()[1].keys()
        assert u.dump_shadow()['first_name'] == None

    def test_state_dirty(self):
        u = User.new()
        u().first_name = 'asdasdasd'
        assert u.check_state()[0] == 'DIRTY'

    def test_json_format(self):
        assert '"id": null,' in User.new().json()

    def test_xml_format(self):
        assert '<User>' in User.new().xml()
