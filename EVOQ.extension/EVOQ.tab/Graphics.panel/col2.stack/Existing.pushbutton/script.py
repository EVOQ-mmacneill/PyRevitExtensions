from Autodesk.Revit.DB import *
from selection import filter_select

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
elements = filter_select("Detail Items")

reset_override = OverrideGraphicSettings()
override_settings = OverrideGraphicSettings()
color = Color(192, 192, 192)
override_settings.SetSurfaceBackgroundPatternColor(color)
all_patterns = FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements()
solid_pattern = [i for i in all_patterns if i.GetFillPattern().IsSolidFill][0]
override_settings.SetSurfaceBackgroundPatternId(solid_pattern.Id)
 
transaction_name = "Graphic Override"
if elements:
    with Transaction(doc, transaction_name) as t:
        t.Start()
        for element in elements:
            id = element.Id
            view.SetElementOverrides(element.Id, reset_override)
            view.SetElementOverrides(element.Id, override_settings)
        t.Commit()

