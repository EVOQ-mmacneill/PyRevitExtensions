from Autodesk.Revit.DB import *
from selection import filter_select
from Autodesk.Revit.UI.Selection import Selection, ObjectType, ISelectionFilter

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
elements = filter_select("Detail Items")

override_settings = OverrideGraphicSettings()
override_settings.SetProjectionLineWeight(6)

transaction_name = "Graphic Override"
if elements:
    with Transaction(doc, transaction_name) as t:
        t.Start()
        for element in elements:
            id = element.Id
            view.SetElementOverrides(element.Id, override_settings)
        t.Commit()

