from Autodesk.Revit.DB import StorageType
def getParamValue(element, param_name):
    param = element.LookupParameter(param_name)
    if param:
        if param.StorageType == StorageType.String:
            return param.AsString()
        elif param.StorageType == StorageType.Double:
            return param.AsDouble()
        elif param.StorageType == StorageType.Integer:
            return param.AsInteger()
        elif param.StorageType == StorageType.ElementId:
            return param.AsElementId().IntegerValue
    return None
