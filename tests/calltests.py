from autoticket import *
import unittest


class TestClass(unittest.TestCase):
    def test_calls_getticket(self):
        publicid = '2391426'
        responsejson = calls.getticket(publicid)['busObRecId']

        self.assertEqual(responsejson, '94609ebfd554f53c2f817a46fba5e519842a52e6c9')

    def test_calls_gettoken(self):
        token = calls.gettoken()
        self.assertNotEqual(token, "")


unittest.main()
