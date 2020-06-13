from autoticket import *
import unittest


class TestTicket(unittest.TestCase):
    def test_ticket_gettemplates(self):
        self.assertIn('testtemplate.txt', gettemplates())

    def test_ticket_existing_getfieldsfordescriptiontemplate(self):
        template = 'testtemplate'
        fields = getfieldsfordescriptiontemplate(template)
        expected = ['ip', 'subject', 'alert']
        self.assertEqual(fields, expected)

    def test_ticket_fake_getfieldsfordescriptiontemplate(self):
        template = 'faketemplate'
        with self.assertRaises(BadTemplateException):
            getfieldsfordescriptiontemplate(template)

    def test_ticket_empty_getfieldsfordescriptiontemplate(self):
        template = ''
        with self.assertRaises(BadTemplateException):
            getfieldsfordescriptiontemplate(template)

    def test_ticket_existing_ticketexists(self):
        ticketnumber = '2391426'
        exists = ticketexists(ticketnumber)
        self.assertTrue(exists)

    def test_ticket_fake_ticketexists(self):
        ticketnumber = '2983913'
        exists = ticketexists(ticketnumber)
        self.assertFalse(exists)

    def test_ticket_empty_ticketexists(self):
        ticketnumber = ''
        exists = ticketexists(ticketnumber)
        self.assertFalse(exists)

    def test_ticket_none_ticketexists(self):
        ticketnumber = None
        exists = ticketexists(ticketnumber)
        self.assertFalse(exists)


unittest.main()
