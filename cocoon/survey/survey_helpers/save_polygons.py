from ..models import PolygonModel, VertexModel


def save_polygons(survey, polygons, filter_type):
    """
    Saves the polygons that the user draws from the google maps
    :param survey: (RentingSurveyModel) -> The survey that is being created
    :param polygons: (Dict()) -> Dictionary containing all the polygons and their vertices
    :param filter_type: (int) -> The type of filter that is being used
                                    1 -> The user is drawing the polygons manually
                                    0 -> The polygons should not be saved

    !!!!!! TODO: Fix saving mechanism
    Once the survey results page gets edited change the method so it can update polygons/
    not add polygons that already exist
    """

    if filter_type is 1:
        # Right now we just delete all the polygons saved before re-adding them
        #   this needs to get fixed with the new survey results page
        survey.polygons.all().delete()

        # Save all the new polygons
        for new_polygon in polygons:

            # Only allow polygons with 3 or more vertices to be saved and needs to be less than 200
            #   Make a arbitrarily big number to prevent getting spammed
            if 3 <= len(new_polygon['vertices']) <= 200:
                vertices_new = []

                # Create the model. It needs to be saved to allow saving foreign keys to it
                polygon_model = survey.polygons.create()
                errors = False

                # retrieve all the new vertices
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

                # If there were no errors then save the vertices
                if not errors:
                    for vertex in vertices_new:
                        vertex.save()
                # If something happened then delete the polygon
                else:
                    polygon_model.delete()

