import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertNotEqual(True, False)  # add assertion here


class TodoTest(unittest.TestCase):

    def test_stub(self):
        # pytest will fail if zero tests are present
        # this is a stub that should be removed once
        # the unittest branch is merged in
        self.assertEqual(1, 1)
