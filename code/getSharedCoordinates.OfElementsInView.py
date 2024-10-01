#Yamoh Rasa
#yrasa@geobimetric.com
#https://github.com/geobimetric

from Autodesk.Revit.DB import FilteredElementCollector, LocationPoint, LocationCurve, Line, Transform, UnitUtils, UnitTypeId, XYZ
doc = __revit__.ActiveUIDocument.Document  # type: ignore

def invertTransform(transform):
    """Manually invert the transformation matrix."""
    # Invert the basis vectors (rotation)
    basisX = transform.BasisX.Normalize() * -1  # Reverse the X basis vector
    basisY = transform.BasisY.Normalize() * -1  # Reverse the Y basis vector
    basisZ = transform.BasisZ.Normalize() * -1  # Reverse the Z basis vector

    # Invert the translation (origin)
    origin = transform.Origin
    inverted_origin = XYZ(
        -(origin.DotProduct(basisX)),  # Reverse translation along X-axis
        -(origin.DotProduct(basisY)),  # Reverse translation along Y-axis
        -(origin.DotProduct(basisZ))   # Reverse translation along Z-axis
    )

    # Create a new Transform object with the inverted basis vectors and origin
    inverted_transform = Transform.Identity
    inverted_transform.BasisX = basisX
    inverted_transform.BasisY = basisY
    inverted_transform.BasisZ = basisZ
    inverted_transform.Origin = inverted_origin

    return inverted_transform
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

activeView = doc.ActiveView
collector = FilteredElementCollector(doc, activeView.Id)
elemInView = collector.ToElements()

""" Variables """
paramname = "ParameterName"
output = list()

for element in elemInView:
    elementid = element.Id
    points = list()
    param = element.LookupParameter(paramname)
    if param:
        location = element.Location
        if location is None:
            print(f"Element {element.Name} has no location")
        else:
            if isinstance(location, LocationPoint):
                pt = location.Point
                points.append(pt)
            elif isinstance(location, LocationCurve):
                curve = location.Curve
                if isinstance(curve, Line):
                    startpt = curve.GetEndPoint(0)
                    endpt = curve.GetEndPoint(1)
                    points.append(startpt)
                    points.append(endpt)

            projectLocation = doc.ActiveProjectLocation
            transform = projectLocation.GetTotalTransform()
            transform_inverse = invertTransform(transform)

            # Apply the inverse transformation to the points
            sharedpoints = [transform_inverse.OfPoint(pt) for pt in points]

            # Convert points to meters
            pointinmeters = [
                XYZ(
                    UnitUtils.ConvertFromInternalUnits(pt.X, UnitTypeId.Meters)*(-1),
                    UnitUtils.ConvertFromInternalUnits(pt.Y, UnitTypeId.Meters)*(-1),
                    UnitUtils.ConvertFromInternalUnits(pt.Z, UnitTypeId.Meters)*(-1)
                ) for pt in sharedpoints
            ]
            paramvalue = getParamValue(element, paramname)
            coordinates = [("{} {} {}".format(pt.X, pt.Y, pt.Z)) for pt in pointinmeters]
            output.append([elementid, paramvalue, coordinates])
for item in output: print(item)
