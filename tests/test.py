# import mongoengine
# from app import create_app
#
#
# def create_app():
#     return create_app_base(
#         MONGODB_SETTINGS={'DB': 'testing'},
#         TESTING=True,
#         CSRF_ENABLED=False,
#     )
#
#
# def test_create_app():
#     app = create_app()
#     assert app.config['TESTING']
#     assert mongoengine.connection.get_db().name == 'testing'

import unittest

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
