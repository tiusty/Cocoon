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
        for polygon in polygons:
            if len(polygon['vertices']) >= 3:
                polygon_model = survey.polygons.create()
                for vertex in polygon['vertices']:
                    lat = None
                    lng = None
                    for key, value in vertex.items():
                        if key == 'lat':
                            lat = value
                        elif key == 'lng':
                            lng = value
                    if lat is not None or lng is not None:
                        polygon_model.vertices.create(lat=lat, lng=lng)
