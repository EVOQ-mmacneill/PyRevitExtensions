from Autodesk.Revit.DB import *
from selection import filter_select
from Autodesk.Revit.UI.Selection import Selection, ObjectType, ISelectionFilter

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
selected_viewports = filter_select("Viewports")

if selected_viewports:
    override = OverrideGraphicSettings().SetProjectionLineWeight(8)
    # override = OverrideGraphicSettings()
    with TransactionGroup(doc, "Viewport Outline"):
        for viewport in selected_viewports:
            view = doc.GetElement(viewport.ViewId)
            with Transaction(doc, "Viewport Outline") as t:
                t.Start()
                view.CropBoxVisible = False
                t.Commit()


            collector = FilteredElementCollector(doc, view.Id)
            shownElems = collector.ToElementIds()


            with Transaction(doc, "Viewport Outline") as t:
                t.Start()
                view.CropBoxVisible = True
                t.Commit()
            collector = FilteredElementCollector(doc, view.Id)
            collector.Excluding(shownElems)

            cropBoxElement = collector.FirstElement()

            if cropBoxElement:
                with Transaction(doc, "Viewport Outline") as t:
                    t.Start()
                    view.SetElementOverrides(cropBoxElement.Id, override)
                    t.Commit()

