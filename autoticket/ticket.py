import os
import re

from autoticket import calls


class BadTemplateException(Exception):
    pass


class Ticket:

    def __init__(self, template: str):
        self.tickettemplate = calls.gettemplate()['fields']  # ticket fields to be filled in
        self.descriptiontemplatetype = template  # type of ticket
        self.record = None  # once created -> id and record number
        self.errors = None  # only has a value if the ticket cannot be created
        self.attachmentpath = None

        template = template.strip().lower()
        if template + '.txt' not in gettemplates():
            raise BadTemplateException("The template: " + template + " does not exist.")

        with open(os.path.dirname(os.path.realpath(__file__)) + "\\templates\\" + template + ".txt") as templateFile:
            temp = templateFile.read()
            self.descriptiontemplate = temp  # always unfilled ticket description
            self.description = temp  # description that gets updated

        self.setticketfields({"Description": self.description})

    def setdescriptionfields(self, fields: dict):
        for key in fields.keys():
            if "{" + key + "}" in self.description:
                self.description = self.description.replace("{" + key + "}", fields.get(key))

        self.setticketfields({"Description": self.description})

    def setticketfields(self, ticketfields: dict):
        for key in ticketfields.keys():
            for i in range(0, len(self.tickettemplate)):
                if self.tickettemplate[i]["name"].strip().lower() == key.strip().lower():
                    self.tickettemplate[i]["value"] = ticketfields[key]
                    self.tickettemplate[i]["dirty"] = True

    def createticket(self) -> dict:
        data = calls.createticket(self.tickettemplate)
        if data["hasError"]:
            self.errors = {
                "errorCode": data["errorCode"],
                "errorMessage": data["errorMessage"],
                "fieldValidationErrors": data["fieldValidationErrors"]
            }
            print("A ticket has not been created -> ErrorMessage: " + data["errorMessage"])
            return self.errors
        else:
            self.record = {
                "ticketnumber": data["busObPublicId"],
                "recordnumber": data["busObRecId"]
            }

            if self.attachmentpath is not None:
                addattachment(self.attachmentpath, data["busObPublicId"])

            print("A ticket has been created -> TicketNumber: " + data["busObPublicId"])
            return self.record

    def setattachment(self, filepath: str):
        self.attachmentpath = filepath

    def getalldescriptionfields(self) -> list:
        return re.findall("{(.*?)}", self.descriptiontemplate)

    def getunsetdescriptionfields(self) -> list:
        return re.findall("{(.*?)}", self.description)

    def getcreatedticketfield(self, name: str) -> str:
        fields = getcreatedticketfields(self.record["ticketnumber"])
        for field in fields:
            if field["name"] == name:
                return field["value"]

    def created(self) -> bool:
        if self.record is None:
            return False
        else:
            return True


def addattachment(filepath: str, ticketnumber: str):
    filesize = os.path.getsize(filepath)

    with open(filepath, "rb") as attachment:
        calls.addattachment(attachment.read(), filepath, ticketnumber, filesize)


def getallfieldnames() -> list:
    fields = calls.gettemplate()['fields']
    names = []
    for field in fields:
        names.append(field["name"])

    return names


def getfullcreatedticket(ticketnumber: str) -> dict:
    if not ticketnumber or ticketnumber is None:
        return {'busObId': None, 'fields': []}
    return calls.getticket(ticketnumber)


def getcreatedticketfields(ticketnumber: str) -> list:
    ticketfields = getfullcreatedticket(ticketnumber)["fields"]
    fields = []
    for i in range(len(ticketfields)):
        if ticketfields[i]['value']:
            fields.append(ticketfields[i])

    return fields


def ticketexists(ticketnumber: str) -> bool:
    response = getfullcreatedticket(ticketnumber)
    if response['busObId'] is not None:
        return True
    else:
        return False


def gettemplates() -> list:
    return os.listdir(os.path.dirname(os.path.realpath(__file__)) + "\\templates")


def getfieldsfordescriptiontemplate(template: str) -> list:
    template = template.strip().lower()
    if template + '.txt' not in gettemplates():
        raise BadTemplateException("The template: " + template + " does not exist.")

    with open(os.path.dirname(os.path.realpath(__file__)) + "\\templates\\" + template + ".txt") as templateFile:
        fields = re.findall("{(.*?)}", templateFile.read())
        return fields

# ticketfields = {
#         'Owner': 'Security-BADGIRT',
#         'Customer': 'nwiltzius',
#         'Service': 'Security',
#         'Category': 'Suspicious Activity Report',
#         'Subcategory': 'Submit Incident',
#         'CustomerRecID': 'nwiltzius',
#         'CustomerDisplayName': 'nwiltzius',
#         'ShortDescription': 'test short description'
#     }
