from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.UI.Selection import ObjectType
def selectAllElementsInView():
    elements = []
    # Get the active view
    active_view = doc.ActiveView
    # Create a filter to collect all elements in the active view
    collector = DB.FilteredElementCollector(doc, active_view.Id).WhereElementIsNotElementType().ToElements()
    for i in collector: elements.append(i)
    return elements
