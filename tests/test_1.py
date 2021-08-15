from .models import User, Truck, Garbage
# from backyard import Env
# from dotenv import dotenv_values
import json

# config = dotenv_values(".env")
# env = Env(config)
#
# for m in (User, Garbage, Truck):
#     m.bind(env)


class TestCase:

    def test_user_read(self):
        u = User.get().fields(['id', 'first_name', 'uid']
                              ).order('id asc').limit(10)
        assert u

    def test_assign_first_name(self):
        u = User.find(2)
        u.first_name = 'sadasdasd'
        assert u.first_name == 'sadasdasd'

    def test_load_related_data(self):
        u = User.find(1).load('garbages')
        q = u.json()
        assert 'garbages' in q
        q = json.loads(q)
        assert len(q['garbages']) > 0

    def test_update_related_object(self):
        u = User.find(1).load('garbages')
        for g in u.garbages:
            g.scoops = 99
            g.save()
        j = Garbage.get().where(" scoops = 99  ").all()
        assert len(j) > 0

    def test_create(self):
        g = Garbage.new()
        g.scoops = 10
        g.boops = 'xlxlxlxlxlxlxlxlxlxl'
        g.save()
        assert g.id > 0

    def test_delete(self):
        Garbage.delete(where=" boops = 'xlxlxlxlxlxlxlxlxlxl' ")
        g = Garbage.get().where(" boops = 'xlxlxlxlxlxlxlxlxlxl' ").all()
        assert len(g) == 0

    def test_show_fields(self):
        u = User.new()
        assert len(u.show_fields()) > 0

    def test_shadow(self):
        u = User.new()
        assert u.check_state()[0] == 'CLEAN'
        u.first_name = 'asdasdasd'
        assert 'first_name' in u.check_state()[1].keys()
        assert u.dump_shadow()['first_name'] is None

    def test_state_dirty(self):
        u = User.new()
        u.first_name = 'asdasdasd'
        assert u.check_state()[0] == 'DIRTY'

    def test_json_format(self):
        assert '"id": null,' in User.new().json()

    def test_xml_format(self):
        assert '<User>' in User.new().xml()
