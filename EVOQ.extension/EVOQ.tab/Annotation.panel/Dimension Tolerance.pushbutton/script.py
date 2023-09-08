# -*- coding=utf-8 -*-

"""Dimension Tolerance
To Do:
    - 
    - 
"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.UI.Selection import Selection, ObjectType, ISelectionFilter
import csv
import os
from rpw.ui.forms import FlexForm, Label, TextBox, Separator, TextInput, Alert, Button, ComboBox

os.chdir(os.path.dirname(__file__))
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
t = Transaction(doc, 'Dimension Tolerance')
view = doc.ActiveView

class CustomISelectionFilter(ISelectionFilter):
    def __init__(self, nom_category):
        self.nom_category = nom_category
    def AllowElement(self, e):
        if e.Category.Name in self.nom_category:
            return True
        else:
            return False

 # Load previous dimension tolerance values
with open('DefaultText.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        #row = [entry.decode("utf-8") for entry in row]
        row = [entry for entry in row]
        prefix = row[0]
        suffix = row[1]
        break

 # Select elements
sel_filter = CustomISelectionFilter("Dimensions")

sel = uidoc.Selection.PickElementsByRectangle(sel_filter, "Select Elements.")

 # UI to enter dimension tolerance values
components = [Label('Enter Prefix/Suffix:'),
    Label('Prefix:'),
    TextBox('textbox1', Text=prefix),
    Label('Suffix:'),
    TextBox('textbox2', Text=suffix),
    Separator(),
    Button('Enter')]
form = FlexForm('Dimension Tolerance', components)
form.show()

 # Update default values to current values
if form.values['textbox1'] != prefix or form.values['textbox2'] != suffix:
    prefix = form.values['textbox1']
    suffix = form.values['textbox2']
    with open('DefaultText.csv', "wb") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([prefix, suffix])

 # Transaction to update text elemenets
if sel:
    t.Start()
    for i in sel:
        i.Prefix = prefix
        i.Suffix = suffix
    t.Commit()
