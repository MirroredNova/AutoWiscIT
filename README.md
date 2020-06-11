# AutoWiscIT

###**Description:**  
Allows for automated created of Cherwell tickets using methods from the ticket class.  
Class Methods: 
1. `__init__(self, template)` - Creates a new Ticket object.
2. `setdescriptionfields(self, fields)` - Fills the description template. `fields` is a dictionary.
3. `setticketfields(self, ticketfields)` - Fills out the ticket template. `ticketfields` is a dictionary.
4. `createticket(self)` - Submits the ticket and creates it in Cherwell.
5. `setattachment(self, filepath)` - Adds the attachment to this ticket. `filepath` is a string.
6. `getalldescriptionfields(self)` - Aets all fields for the description.
7. `getunsetdescriptionfields(self)` - Gets all fields that haven't been set yet for the description
 
Static Methods:
1. `addattachment(filepath, ticketnumber)` - Adds the file to the given `ticketnumber` string
2. `getallfieldnames()` - Gets all available fieldNames for a Cherwell ticket
3. `gettemplates()` - Gets all available templates for a ticket
4. `getfieldsfordescriptiontemplate(template)` - Takes a `template` string and returns the fields


###**Instanciating:**  
To create a new Ticket, you must pass in a template so that the ticket type and template can be loaded

###**Attachments Folder:**  
This folder is where attachments can be put, and then added to a ticket either by calling the static method or adding
the attachment through each object. 

###**Templates Folder:**  
This is where templates will go. The template can be pasted as normal, but any fields that you want to be able to set
must be notated as such: `{'fieldName'}`. This will set the template and description for the ticket. 

To fill the fields in, you must call `Ticket.setdescriptionfields(fields)` and pass in a dictionary where the keys are 
the 'fieldName' and the key is the value to be filled: `fields = {'ip': '1.1.1.1'}`. 
Any field in the template that doesn't get set will remain in brackets.

###**Ticket Fields:**  
In addition to the fields in the description that must be filled out, there are also ticket fields that have to be filled
out in order for the ticket to be valid. Some are required, but I recommend you pass in more. They can be set by
passing in a dictionary where the keys are the 'fieldName's and values are your value. The following fields
are required in order to create a valid ticket:
```
ticketfields = {
         'Owner': 'Security-BADGIRT',
         'Customer': 'nwiltzius',
         'Service': 'Security',
         'Category': 'Suspicious Activity Report',
         'Subcategory': 'Submit Incident',
         'CustomerRecID': 'nwiltzius',
         'CustomerDisplayName': 'nwiltzius',
         'ShortDescription': 'test short description'
     }
```
Note: Description is required, however it **SHOULD NOT** be set through the ticket fields. It should instead be set
through `Ticket.setdescriptionfields(fields)`  
