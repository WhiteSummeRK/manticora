from unittest import TestCase
from manticora.models import tables


class TestUserModel(TestCase):
    def test_User_should_return_correct_types(self):
        result_table = tables.User(
            name='Jow',
            pwd='Jowzinho123',
            bill=10.11
        )
        self.assertIsInstance(result_table.name, str)
        self.assertIsInstance(result_table.pwd, str)
        self.assertIsInstance(result_table.bill, float)
        self.assertEqual(
            result_table.__repr__(),
            "User(name=Jow, pwd=Jowzinho123, bill=10.11)"
        )
