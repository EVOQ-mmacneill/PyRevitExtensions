from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI.Selection import Selection, ObjectType, ISelectionFilter

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

class CustomISelectionFilter(ISelectionFilter):
    def __init__(self, nom_category):
        self.nom_category = nom_category
    def AllowElement(self, e):
        if e.Category.Name in self.nom_category:
            return True
        else:
            return False

def select():
    element = [doc.GetElement(uidoc.Selection.PickObject(ObjectType.Element, "Select Element").ElementId)]
    return element

def multi_select():
    elements = uidoc.Selection.PickElementsByRectangle("Select Elements")  # add filter
    return elements

def filter_select(category):
    sel_filter = CustomISelectionFilter(category)
    try:
        elements = uidoc.Selection.PickElementsByRectangle(sel_filter, "Select Elements.")
    except:
        elements = None
    return elements

def select_symbol():
    symbols = []
    sel = [doc.GetElement(uidoc.Selection.PickObject(ObjectType.Element, "Select Element").ElementId)]
    for item in sel:
        symbol = item.Symbol
        symbols.append(symbol)
    return symbols

def multi_select_symbol():
    symbols = []
    sel = uidoc.Selection.PickElementsByRectangle("Select Elements")  # add filter
    for item in sel:
        symbol = item.Symbol
        symbols.append(symbol)
    return symbols
