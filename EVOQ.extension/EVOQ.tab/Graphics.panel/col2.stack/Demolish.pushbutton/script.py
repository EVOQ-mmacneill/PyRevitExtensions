from Autodesk.Revit.DB import *
from selection import filter_select

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
elements = filter_select("Detail Items")

reset_override = OverrideGraphicSettings()
override_settings = OverrideGraphicSettings()
override_settings.SetSurfaceTransparency(100)
override_settings.SetSurfaceBackgroundPatternVisible(False)
override_settings.SetSurfaceForegroundPatternVisible(False)
all_patterns = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()
object_style = "Demolished"
demo_pattern = [i for i in all_patterns if i.Name == object_style][0]
override_settings.SetProjectionLinePatternId(demo_pattern.Id)

transaction_name = "Graphic Override"
if elements:
    with Transaction(doc, transaction_name) as t:
        t.Start()
        for element in elements:
            id = element.Id
            view.SetElementOverrides(element.Id, reset_override)
            view.SetElementOverrides(element.Id, override_settings)
        t.Commit()

