from ..models import PolygonModel, VertexModel


def save_polygons(survey, polygons, filter_type):
    """
    Saves the polygons that the user draws from the google maps
    :param survey: (RentingSurveyModel) -> The survey that is being created
    :param polygons: (Dict()) -> Dictionary containing all the polygons and their vertices
    :param filter_type: (int) -> The type of filter that is being used
                                    1 -> The user is drawing the polygons manually
                                    0 -> The polygons should not be saved
    :return:
    """

    if filter_type is 1:
        for new_polygon in polygons:
            if len(new_polygon['vertices']) >= 3:
                vertices_new = []
                polygon_model = survey.polygons.create()
                errors = False
                for vertex in new_polygon['vertices']:
                    lat = None
                    lng = None
                    for key, value in vertex.items():
                        if key == 'lat':
                            lat = value
                        elif key == 'lng':
                            lng = value
                    if lat is not None or lng is not None:
                        vertices_new.append(VertexModel(polygon=polygon_model, lat=round(lat, 6), lng=round(lng, 6)))
                    else:
                        errors = True

                # Check to see if this polygon already exists
                polygon_exist = False
                for polygon_saved in PolygonModel.objects.filter(survey=survey):
                    if check_matching_vertices(polygon_saved, vertices_new):
                        polygon_exist = True
                        break

                if not errors and not polygon_exist:
                    for vertex in vertices_new:
                        vertex.save()
                else:
                    polygon_model.delete()


def check_matching_vertices(polygon_saved, vertices_new):
    """
    Given a polygon model and a list of vertices, checks to see if the polygon has identical vertices to the new polygon

    To be equivelent, all the vertices must exists in the polygon
    :param polygon_saved: (PolygonModel) -> The polygon to compare against
    :param vertices_new: (list(VertexModels)) -> THe list of vertices to check in the polygon
    :return: (Boolean) -> True: The polygon has identical vertices to the passed in vertices
                          False: The polygon is different
    """
    if polygon_saved.vertices.count() == len(vertices_new):
        for vertex_new in vertices_new:
            if not polygon_saved.vertices.filter(lat=vertex_new.lat, lng=vertex_new.lng):
                return False
    return True
