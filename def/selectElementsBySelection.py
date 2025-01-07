from Autodesk.Revit.UI.Selection import ObjectType
def selectElementsBySelection():
    elements = []
    try:
        # Prompt user to select elements using the mouse
        selection = uidoc.Selection.PickObjects(ObjectType.Element, "Select elements in the view")
        for ref in selection:
            element = doc.GetElement(ref.ElementId)
            elements.append(element)
        return elements
    except Exception as e: return None
