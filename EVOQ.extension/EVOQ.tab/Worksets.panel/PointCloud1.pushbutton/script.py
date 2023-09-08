# Point Clouds On/Off
"""To Do:
    - Failsafe for when more than one workset name interpreted as pointcloud workset.
    - Revert to "Use Global Setting" if initialy set to neither show nor hide at end of session.
    - 
"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction
import csv
import os
from rpw.ui.forms import TextInput, Alert

os.chdir(os.path.dirname(__file__))
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
t = Transaction(doc, 'Change Workset Visibility')
view = doc.ActiveView

with open('WorksetKeys.csv') as csvfile:
    SearchKeys = [line.strip() for line in csvfile if len(line) >3]

workset_collector = FilteredWorksetCollector(doc)
worksets = workset_collector.OfKind(WorksetKind.UserWorkset).ToWorksets()

def WorksetsSearch(worksets, SearchKeys):
    for workset in worksets:
        for SearchKey in SearchKeys:        
            if SearchKey in workset.Name:
                workset_id = workset.Id
                return workset_id

def WorksetSearch(worksets, SearchKey):
    for workset in worksets:      
        if SearchKey in workset.Name:
            workset_id = workset.Id
            return workset_id
          

def hide_workset(doc, view, workset_id):
    if workset_id:
        # Get the current visibility
        visibility = view.GetWorksetVisibility(workset_id)

        # Set it to 'Hidden' if it is not hidden yet
        if visibility != WorksetVisibility.Hidden:
            view.SetWorksetVisibility(workset_id, WorksetVisibility.Hidden)
        else:
            view.SetWorksetVisibility(workset_id, WorksetVisibility.Visible)
            # Get the workset's default visibility
            # default_visibility = WorksetDefaultVisibilitySettings.GetWorksetDefaultVisibilitySettings(doc)

            # Make sure it is set to 'False'
            # if default_visibility.IsWorksetVisible(workset_id):
                # default_visibility.SetWorksetVisibility(workset_id, False)

 
workset_id = WorksetsSearch(worksets, SearchKeys)

if not workset_id:
    NewKey = TextInput('Workset Name',description='"PointCloud" not found in any Worksets.', default='PointClouds')
    workset_id = WorksetSearch(worksets, NewKey)
    if workset_id:
        SearchKeys.append(NewKey)
        with open('WorksetKeys.csv', "wb") as csvfile:
            writer = csv.writer(csvfile)
            for Key in SearchKeys:
                writer.writerow([Key])
    else:
        Alert('A Workset could not be found. Please review your Workset names and try again.', title='Point Clouds On/Off', header='Workset Not Found', exit=True)

if workset_id:
    t.Start()
    hide_workset(doc, view, workset_id)
    t.Commit()
