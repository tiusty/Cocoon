import json
import math

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from Unicorn.settings.Global_Config import survey_types, Hybrid_weighted_max, \
    Hybrid_weighted_min, hybrid_question_weight, approximate_commute_range, \
    default_rent_survey_name, gmaps, number_of_exact_commutes_computed, commute_question_weight, \
    price_question_weight
from houseDatabase.models import RentDatabase, ZipCodeDictionary, ZipCodeDictionaryChild
from survey.models import RentingSurveyModel, CommutePrecision
from userAuth.models import UserProfile
from survey.forms import RentSurvey, DestinationForm, RentSurveyMini


# Create your views here.
@login_required
def renting_survey(request):
    # Create the two forms,
    # RentSurvey contains everything except for destinations
    form = RentSurvey()

    # DestinationFrom contains the destination
    # The reason why this is split is because the destination form can be made into a form factory
    # So that multiple destinations can be entered, it is kinda working but I removed the ability to do
    # Multiple Destinations on the frontend
    form_destination = DestinationForm()

    # Retrieve the current profile or return a 404
    current_profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'error_message': [],
    }

    if request.method == 'POST':

        # first validating Destination form
        form_destination = DestinationForm(request.POST)
        # create a form instance and populate it with data from the request:
        form = RentSurvey(request.POST)

        # Check to see if the designations are valid
        if form_destination.is_valid():
            # check whether it is valid
            if form.is_valid():
                # process the data in form.cleaned_data as required
                rent_survey = form.save(commit=False)
                # Need to retrieve the current userProfile to link the survey to

                # Add the current user to the survey
                rent_survey.user_profile = current_profile

                # Given the enumeration, set the survey to either rent or buy
                # This can probably be removed after testing it
                rent_survey.survey_type = survey_types.rent.value

                # Try seeing if there is already a recent survey and if there is
                # Then delete it. We only want to keep one "recent" survey
                # The user has the option to change the name of it to save it permanently
                RentingSurveyModel.objects.filter(user_profile=current_profile).filter(
                    name=default_rent_survey_name).delete()
                rent_survey.save()

                # Since commit=False in the save, need to save the many to many fields
                # After saving the form
                form.save_m2m()

                # Save the destination forms
                destinations = form_destination.save(commit=False)
                # Set the foreign field from the destination to the corresponding survey
                destinations.survey = rent_survey
                destinations.save()

                # redirect to survey result on success:
                return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                    kwargs={"survey_id": rent_survey.id}))
            else:
                context['error_message'].append("The survey form is not valid")
        else:
            # If the destination form is not valid, also do a quick test of the survey field to
            # Inform the user if the survey is also invalid
            if not form.is_valid():
                context['error_message'].append("The normal form is also not valid")
            context['error_message'].append("Destination form is not valid")
    return render(request, 'survey/rentingSurvey.html', {'form': form, 'formDest': form_destination})


# Function is not implemented, it will basically be the same as the rent survey but for buying instead
# @login_required
# def buying_survey(request):
#     form = BuySurvey()
#     return render(request, 'survey/buyingSurvey.html', {'form': form})


class ScoringStruct:
    """
    Class that stores one home and the corresponding information for that home
    This is used to rank homes and eliminate them if necessary
    This also makes sure that the scores are easily associated with the home
    Contains functions to easily extract information for the given home
    """

    def __init__(self, new_house):
        self.house = new_house
        self.score = 0
        self.scorePossible = 0
        self.commuteTime = []
        self.approxCommuteTime = []
        self.eliminated = False

    def __str__(self):
        return self.house.get_full_address()

    def get_score(self):
        """
        Generates the actual score based on the possible score and current score.
        This makes sure that the divide by zero case is handled.
        :return:
            Returns the score. If it was eliminated then it returns -1 to indicate that
                The house should not be used
        """
        # Takes care of divide by 0, also if it is eliminated the score should be -1
        if self.scorePossible != 0 and self.eliminated is False:
            return (self.score / self.scorePossible) * 100
        elif self.eliminated:
            # If eliminated return negative one so it is sorted to the back
            return -1
        else:
            return 0

    def get_final_score(self):
        """
        Returns the score but rounds to the nearest integer to make it human friendly
        :return: the score rounded to the nearest integer
        """
        return round(self.get_score())

    def get_user_score(self):
        """
        Function: get_user_score()
        Description:
        Returns a human readable score. Therefore, the user will not see
            a long float which is meaningless
        Comments:
        Currently the scale is to large. Will define to +/- later.
        """
        current_score = self.get_score()
        if current_score >= 90:
            return "A"
        elif current_score >= 80:
            return "B"
        elif current_score >= 70:
            return "C"
        elif current_score >= 60:
            return "D"
        else:
            return "F"

    def get_commute_times(self, commute_precision):
        """
        Get commute times gets the commute for the house depending on the argument
        It will either return the exact or the approximate commute times
        :param commute_precision: Enum type commutePrecision
        :return: An array of ints which are all the commute times associated with that house
        """
        if commute_precision is CommutePrecision.exact:
            return self.get_commute_times_exact()
        else:
            return self.get_commute_times_approx()

    def get_commute_times_exact(self):
        """
        Returns all the commute times for that home as a list
        :return: A list with all the commute times
        """
        commutes = []
        for commute in self.commuteTime:
            commutes.append(commute)
        return commutes

    def get_commute_times_approx(self):
        """
        Returns all the approximate commute times for that home as a list
        :return: A list with all the approximate commute times
        """
        approx_commutes = []
        for commute in self.approxCommuteTime:
            approx_commutes.append(commute)
        return approx_commutes

    def get_commute_times_str(self):
        """
        Returns a formatted string that returns all the commute times for a given home
        Example output:
        27 Minutes, 27 Minutes, 27 Minutes
        :return:
        string -> Formatted to display nicely to the user
        """
        end_result = ""
        counter = 0
        for commute in self.commuteTime:
            if commute > 60:
                max_output = str(int(math.floor(commute / 60))) + " hours " + str(int(commute % 60)) + " Minutes"
            else:
                max_output = str(int(commute)) + " Minutes"
            if counter != 0:
                end_result = end_result + ", " + max_output
            else:
                end_result = max_output
            counter = 1

        return end_result

    def get_approx_commute_times_str(self):
        """
        Returns a formatted string that returns all the commute times for a given home
        Example output:
        27 Minutes, 27 Minutes, 27 Minutes
        :return:
        string -> Formatted to display nicely to the user
        """
        end_result = ""
        counter = 0
        for commute in self.approxCommuteTime:
            if commute > 60:
                max_output = str(int(math.floor(commute / 60))) + " hours " + str(int(commute % 60)) + " Minutes"
            else:
                max_output = str(int(commute)) + " Minutes"
            if counter != 0:
                end_result = end_result + ", " + max_output
            else:
                end_result = max_output
            counter = 1

        return end_result

    def eliminate_home(self):
        """
        Sets the eliminated flag on a home
        :return:
        """
        self.eliminated = True


# It will take in the houseMatrix score
# It will commute the score based on the commute times to the destinations
# The score is multiplied by the scale factor which is user determined
# This factor determines how much the factor will affect the overall weight
def create_commute_score(scored_house_list, survey, commute_precision):
    """
    Evaluates a score based on the commute times.
    This function assumes that commutes have been already eliminated due to being out of range
    Therefore, if the commute value is out of range, then it will force the value into the range
    Out of range values should only occur for approximate commutes

    The User can define a commute weight. If the commute weight is 0, then the scaling factor is 0 so all
    homes are weighted the same as long as they are within the range. As the scaling factor increases, it
    gives a large weight to homes that are closer.

    Note: The commute score is calculated for either the approx commute or exact dependent
        on commute_precision argument
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The Survey is passed, but is only really needed to find the max and min commute times
    :param commute_precision: Enum of commutePrecision
    :return:
        Returns the ScoringStruct but with the housing scores updated with the commute times and
            appropriate homes eliminated
    """
    # Currently only scores based on commute times
    # It supports having multiple destinations
    max_commute = survey.get_max_commute()
    min_commute = survey.get_min_commute()
    scale_factor = survey.get_commute_weight()
    for house in scored_house_list:
        # It needs to be made clear that the scale factor only effects the homes that are under the
        # Commute time. For example, if the max commute is 12 minutes, then anything over 12 is removed.
        # If the scale factor is 0, then all the homes under 12 are weighted equally at 0. Likewise if
        # the scale factor is 5, then a home with a commute time of 6 minutes will have a much higher score then
        # a commute of 9 minutes even though in reality it isn't that much.
        for commute in house.get_commute_times(commute_precision):
            if commute:
                if commute < min_commute:
                    commute = min_commute
                elif commute > max_commute:
                    commute = max_commute
                # Minimum range is always 10
                if max_commute > 11:
                    range_com = max_commute
                else:
                    # Make sure that the minimum is 11, so that when it subtracts 10, it doesn't do
                    # a divide by zero
                    range_com = 11
                # First check to see if the commute is less then the minimum commute, if it is then remove it
                # Second check if the commute time is less than 10 minutes, because if it is it is a perfect score
                # Third If the commute is less than the max commute time compute a score
                # Forth if the commute is more than the maxCommute then remove the house
                if commute <= 10:
                    house.score += (commute_question_weight * scale_factor)
                    house.scorePossible += (commute_question_weight * scale_factor)
                else:
                    house.score += (((1 - (commute - 10) / (range_com - 10)) * commute_question_weight) * scale_factor)
                    house.scorePossible += (commute_question_weight * scale_factor)
    return scored_house_list


def create_price_score(scored_house_list, survey):
    """
    Generates the score according to the price of the home
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The survey that the homes are being filtered by
    :return:
    """

    # Retrieve all the constant values
    max_price = survey.get_max_price()
    min_price = survey.get_min_price()
    scale_factor = survey.get_price_weight()

    # Apply price scoring for all the houses
    for house in scored_house_list:
        house_price = house.house.get_price()
        house_price_normalized = house_price - min_price
        # Guarantee that the house normalized price is not negative, (score should never decrease)
        if house_price_normalized >= 0:
            house_range = max_price - min_price
            # Make sure that the house range is never negative (score should never decrease)
            if house_range > 0:
                house.score += ((1 - house_price_normalized / house_range) * price_question_weight) * scale_factor
                house.scorePossible += (price_question_weight * scale_factor)
            # This takes care of the divide by zero case
            # If the range is zero, then the max and min price should be the same
            # Therefore assuming that the static filter worked before, the house price
            # Needs to be between the max and minimum price and therefore, in this case,
            # The house price should be equal to the min price. Therefore, if this case occurs
            # Do an extra validation to make sure that the min_price equals the house price to
            # Prevent an error
            elif house_range == 0 and house_price == min_price:
                house.score += price_question_weight * scale_factor
                house.scorePossible += price_question_weight * scale_factor


def weighted_question_scoring(home, contains_item, scale_factor):
    """
    This is the function that determines the weight of a given weight question
    This allows a constant method of determining the score and thus makes it
    Easier to change later
    :param home: This is a home given as a single house structure
    :param contains_item: This is a boolean that says whether or not the given home
        has the item that is being tested for, i.e does it have an airconditioning?
    :param scale_factor: This is an integer which is the weighted value that the user
        gave the question. Therefore, the higher the scale factor, the more the question
        affects the weight
    """

    # First remove the factor if the user marked it as must have, or must not have.
    if scale_factor == Hybrid_weighted_max and contains_item is False:
        home.eliminate_home()
    elif scale_factor == Hybrid_weighted_min and contains_item is True:
        home.eliminate_home()
    # If the item is desired and the item is present the score will go up, or if the
    # item is not desired and it doesn't have the item, then the score will go up.
    # Otherwise the score will go down
    home.score += (1 if contains_item else -1) * scale_factor * hybrid_question_weight
    # Regardless of anything else, always increment the possible points depending on the
    # Scale factor. The factor is added by the absolute value because the maximum value
    # needs to be added
    home.scorePossible += abs(scale_factor) * hybrid_question_weight


def create_interior_amenities_score(scored_house_list, survey):
    """
    Updates the house scores based on the interior amenities questions
    Homes are passed by reference
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The user survey that is being used to evaluate the homes
    """
    # Loop throuh all the homes and score each one
    for home in scored_house_list:
        weighted_question_scoring(home, home.house.get_air_conditioning(), survey.get_air_conditioning())
        weighted_question_scoring(home, home.house.get_wash_dryer_in_home(), survey.get_wash_dryer_in_home())
        weighted_question_scoring(home, home.house.get_dish_washer(), survey.get_dish_washer())
        weighted_question_scoring(home, home.house.get_bath(), survey.get_bath())


def create_exterior_amenities_score(scored_house_list, survey):
    """
    Updates the house scores based on the exterior amenities questions.
    Homes are passed by reference
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The user survey that is being used to evaluate the homes
    """
    for home in scored_house_list:
        weighted_question_scoring(home, home.house.get_parking_spot(), survey.get_parking_spot())
        weighted_question_scoring(home, home.house.get_washer_dryer_in_building(),
                                  survey.get_washer_dryer_in_building())
        weighted_question_scoring(home, home.house.get_elevator(), survey.get_elevator())
        weighted_question_scoring(home, home.house.get_handicap_access(), survey.get_handicap_access())
        weighted_question_scoring(home, home.house.get_pool_hot_tub(), survey.get_pool_hot_tub())
        weighted_question_scoring(home, home.house.get_fitness_center(), survey.get_fitness_center())
        weighted_question_scoring(home, home.house.get_storage_unit(), survey.get_storage_unit())


# Given the houseScore and the survey generate and add the score based
# On the commute times to the destinations
def create_house_score(house_list_scored, survey):
    """
    All the functions that perform dynamic scoring will be listed here
    :param house_list_scored: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The current survey, since the scoring is based on the result of the survey
    :return: The house structure with the homes scored
    """
    # Creates score based on commute
    create_commute_score(house_list_scored, survey, CommutePrecision.approx)
    create_price_score(house_list_scored, survey)
    create_interior_amenities_score(house_list_scored, survey)
    create_exterior_amenities_score(house_list_scored, survey)
    return house_list_scored


# Function takes in the ScoringStruct and returns the sorted list
def order_by_house_score(scored_house_list):
    """
    Orders the homes based on the current score
    The high scored home will be put at the front of the list
    Homes that are eliminated have no order
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :return: The house structure but sorted based on the home score
    """
    # Simple insertion sort to sort houses by score
    for index in range(1, len(scored_house_list)):
        current_value = scored_house_list[index]
        position = index

        while position > 0 and scored_house_list[position - 1].get_score() < current_value.get_score():
            scored_house_list[position] = scored_house_list[position - 1]
            position -= 1

        scored_house_list[position] = current_value

    return scored_house_list


def compute_approximate_commute_times(destinations, scored_list, commute_type):

    #TODO: Pass the town along with the zip code

    """
    This function takes each home and tries to find the approximate commute times for all the destinations
    The zip code combination will be checked in the database for the value and if it doesn't exist, it will
    add the zip code combination to the failed_zip_codes list. That list will eventually be passed to another
    function which will compute all the zipcode combinations and add them to the database. After the zip codes are
    added to the database, the commute times will be recomputed
    :param destinations: A list of all the destinations desired by the user
    :param scored_list: Array of ScoringStruct that contains all the origins and associated values
    :param commute_type: String, one of driving, walking, transit, bicycling
    """
    # If the home failed to find an associated zip code cached, mark it as failed
    # and then we will dynamically get that zip code and store it
    # Format of dictionary:
    # { 'destination zip code 1' : [ 'origin zip code 1', 'origin zip code 2' ],
    #   'destination zip code 2' : [ 'origin zip code 1', 'origin zip code 3' ]}
    failed_zip_codes = {}

    for house in scored_list:
        # Only populate the commute time if the array is empty
        # This is important when this function is called again after all the failed
        # zip codes are computed. Then homes with a commute already should not have the
        # value recomputed
        if not house.get_commute_times_approx():
            for destination in destinations:
                # This searches for the zip code combination and then if it can't find it, it will
                # add the combination to the failed_zip_code dictionary
                try:
                    zip_code_dictionary = ZipCodeDictionary.objects.get(
                        zip_code=house.house.get_zip_code(),
                    )
                    try:
                        zip_code_dictionary_child = zip_code_dictionary.zipcodedictionarychild_set.get(
                            zip_code=destination.get_zip_code(),
                            commute_type=commute_type,
                        )
                        # If the zip code needs to be refreshed, then delete the zip code
                        # and add it to the failed list
                        if zip_code_dictionary_child.test_recompute_date():
                            zip_code_dictionary_child.delete()
                            add_home_to_failed_list(failed_zip_codes, destination, house)
                            # If all the conditions pass, then store the commute time stored for that combination
                        else:
                            house.approxCommuteTime.append(zip_code_dictionary_child.get_commute_time())
                    except ZipCodeDictionaryChild.DoesNotExist:
                        add_home_to_failed_list(failed_zip_codes, destination, house)
                except ZipCodeDictionary.DoesNotExist:
                    add_home_to_failed_list(failed_zip_codes, destination, house)

    # If there are failed zip codes, compute the commute for the zip code and add it to the database
    if failed_zip_codes:
        add_zip_codes_to_database(failed_zip_codes, commute_type)
        # Call the function again to recompute the commute times for the failed homes
        compute_approximate_commute_times(destinations, scored_list, commute_type)


def add_home_to_failed_list(failed_zip_codes, destination, house):
    """
    This function adds a failed home combination to the failed_zip_codes array
    It is passed the house and the destination that is is supposed to go to
    :param failed_zip_codes: A dictionary of failed zip code combination
    :param destination: The destination stored as a RentDatabase model
    :param house: The house (origin), stored as a scoring structure
    """
    if destination.get_zip_code() in failed_zip_codes:
        # Only add the zip code if the combination is not already in the list
        if house.house.get_zip_code() not in failed_zip_codes[destination.get_zip_code()]:
            failed_zip_codes[destination.get_zip_code()].append(house.house.get_zip_code())
    else:
        failed_zip_codes[destination.get_zip_code()] = [house.house.get_zip_code()]


def add_zip_codes_to_database(failed_zip_codes, commute_type):
    """
    This function takes in a dictionary of failed zip code combination and computes
    the distance and saves it to the database.
    :param failed_zip_codes: A dictionary of zip code combinations:
        i.e: {'02474': ['02476', '02474'], '02476': ['02474', '02476']} or {'destination': ['origin1', origin2]}
    :param commute_type: String, one of driving, walking, bicycling, transit
    """
    print("adding new zip codes")

    # Can add things to the arguments, like traffic_model, avoid things, depature_time etc
    # Each row contains the origin with each corresponding destination
    # The value field of duration is in seconds
    measure_units = "imperial"

    for destination_zip_code in failed_zip_codes:
        origins = []
        if len(destination_zip_code) >= 5:
            for origins_zip_code in failed_zip_codes.get(destination_zip_code):
                print(origins_zip_code)
                print(destination_zip_code)
                if len(origins_zip_code) >= 5:
                    origins.append(origins_zip_code[:5])

        print(origins)
        print(destination_zip_code)

        matrix = gmaps.distance_matrix(
            origins,
            destination_zip_code,
            mode=commute_type,
            units=measure_units,
        )

        if matrix:
            counter = 0
            for origin in origins:
                for commute in matrix["rows"][counter]["elements"]:
                    # Divide by 60 to get minutes
                    if commute['status'] == 'OK':
                        if ZipCodeDictionary.objects.filter(zip_code=origin).exists():
                            zip_code_dictionary = ZipCodeDictionary.objects.get(zip_code=origin)
                            if zip_code_dictionary.zipcodedictionarychild_set.filter(
                                    zip_code=destination_zip_code,
                                    commute_type=commute_type).exists():
                                print("The combination that was computed already exists")
                            else:
                                zip_code_dictionary.zipcodedictionarychild_set.create(
                                    zip_code=destination_zip_code,
                                    commute_type=commute_type,
                                    commute_distance=commute['distance']['value'],
                                    commute_time=commute['duration']['value'],
                                )
                        else:
                            ZipCodeDictionary.objects.create(zip_code=origin) \
                                .zipcodedictionarychild_set.create(
                                zip_code=destination_zip_code,
                                commute_type=commute_type,
                                commute_distance=commute['distance']['value'],
                                commute_time=commute['duration']['value'],
                            )
                    else:
                        print("distance not found")
                    counter += 1
        else:
            print("something went wrong with zip code matrix")


def filter_homes_based_on_approximate_commute(survey, scored_list):
    """
    This function computes the approximate commute filter
    This eliminates any home with an approximate commute that is over the
    user's max_commute + approximate_commute_range, or user's min - approximate_commute_range
    The reason why there is a buffer is because the approximate commute range is based off of the
    zip_code. Within a zip_code the commute time can vary by say 20 minutes.
    This function only eliminates homes out of range, it does not score
    :param survey: Passed the user's survey
    :param scored_list: Array of scoringStruct
    """
    for home in scored_list:
        for commute in home.get_commute_times_approx():
            if (commute >= survey.get_max_commute() + approximate_commute_range) \
                    or (commute <= survey.get_min_commute() - approximate_commute_range):
                home.eliminate_home()


def compute_exact_commute(destinations, scored_list, commute_type):
    """
    Computes the exact commute for the first so many homes
    :param destinations: The list of destinations as RentingDestination objects
    :param scored_list: A list containing ScoreStruct objects.
    :param commute_type: The commute type the user desires
    :return:
    """

    # Can add things to the arguments, like traffic_model, avoid things, departure_time etc
    # Each row contains the origin with each corresponding destination
    # The value field of duration is in seconds
    measure_units = "imperial"
    destinations_full_address = []
    # Retrieve only the full address to give to the distance matrix
    for destination in destinations:
        destinations_full_address.append(destination.get_full_address())

    origins = []
    counter = 0
    for home in scored_list:
        origins.append(home.house.get_full_address())
        counter += 1
        if counter is number_of_exact_commutes_computed:
            break

    matrix = gmaps.distance_matrix(origins, destinations_full_address,
                                   mode=commute_type,
                                   units=measure_units,
                                   )
    # Only if the matrix is defined should the calculations occur, otherwise throw an error
    if matrix:
        # Try to think of a better way than a simple counter
        counter = 0
        for house in scored_list[:number_of_exact_commutes_computed]:
            for commute in matrix["rows"][counter]["elements"]:
                # Divide by 60 to get minutes
                if commute['status'] == 'OK':
                    house.commuteTime.append(commute['duration']["value"] / 60)
                else:
                    # Eliminate houses that can't have a commute value
                    house.eliminate_home()
            counter += 1
            # Only Add the context if the commute is able to be processed
    else:
        print("Couldn't calculate distances, something went wrong")

    return scored_list


def start_algorithm(survey, context):
    # Creates an array with all the home types indicated by the survey
    current_home_types = []
    for home in survey.home_type.all():
        current_home_types.append(home.homeType)

    """
    STEP 1: Compute Static Elements
    The item that will filter the list the most should be first to narrow down the number of iterations
    The database needs to be searched
    (Right now it isn't order by efficiency but instead by when it was added. Later it can be switched around

    Current order:
    1. Filter by price range. The House must be in the correct range to be accepted
    2. Filter by Home Type. The home must be the correct home type to be accepted
    3. Filter by Move In day. The two move in days create the range that is allowed. The range is inclusive
        If the house is outside the range it is eliminated
    4. Filter by the number of bed rooms. It must be the correct number of bed rooms to work.
    4. Filter by the number of bathrooms
    """
    filtered_house_list = RentDatabase.objects \
        .filter(price__range=(survey.get_min_price(), survey.get_max_price())) \
        .filter(home_type__in=current_home_types) \
        .filter(move_in_day__range=(survey.get_move_in_date_start(), survey.get_move_in_date_end())) \
        .filter(num_bedrooms=survey.get_num_bedrooms()) \
        .filter(num_bathrooms__range=(survey.get_min_bathrooms(), survey.get_max_bathrooms()))

    # Retrieves all the destinations that the user recorded
    destination_set = survey.rentingdestinations_set.all()

    # Origins are defined as all the homes that the person would originate from.
    # This means where they would live, aka the house
    origins = []
    for house in filtered_house_list:
        origins.append(house.address)

    # The destination is defined as a location the user would commute to.
    # Aka their job, school etc. Therefore this is the destination they wish to be at
    # This just stores the list of destinations as a Survey.RentingDestination object
    destinations = []
    for location in destination_set:
        destinations.append(location)

    # This puts all the homes into a scored list
    scored_house_list = []
    for house in filtered_house_list:
        scored_house_list.append(ScoringStruct(house))

    commute_type = survey.get_commute_type()
    context['commuteType'] = commute_type

    """
    STEP 2: Compute the approximate distance using zip codes.
    This serves as a secondary static filer to eliminate homes that are far away.
    This also will store how long the commute will take which will be used later for
    Dynamic filtering/scoring
    """
    # If there are no destinations or no homes, then don't bother with algorithm
    if not destinations or not scored_house_list:
        context['error_message'].append("No Destination or origin")
    else:
        # Computes the approximate commute times for the homes in the score_house_list
        compute_approximate_commute_times(destinations, scored_house_list, commute_type)

        # Filters the houses based on the approximate commutes
        filter_homes_based_on_approximate_commute(survey, scored_house_list)

        # Generate scores for the homes based on the survey results
        create_house_score(scored_house_list, survey)

        # Order the homes based off the score
        order_by_house_score(scored_house_list)

        """
        STEP 3:
        Compute the exact commutes and change the score based on the exact commute.
        """
        # Compute the exact commute for the top homes in the list and reorder only the top homes
        compute_exact_commute(destinations, scored_house_list, commute_type)

        # Now generate the score based on the exact commute
        create_commute_score(scored_house_list, survey, CommutePrecision.exact)

        # Now reorder all the homes with the new information
        order_by_house_score(scored_house_list)

    # Contains destinations of the user
    context['locations'] = destination_set
    # House list either comes from the scored homes or from the database static list if something went wrong
    # Only put up to 200 house on the list
    context['houseList'] = scored_house_list[:200]


# Assumes the survey_id will be passed by the URL if not, then it grabs the most recent survey.
# If it can't find the most recent survey it redirects back to the survey
@login_required
def survey_result_rent(request, survey_id="recent"):
    """
    Survey result rent is the heart of the website where the survey is grabbed and the housing list is created
    Based on the results of the survey. This is specifically for the rent survey
    :param request: Http Request
    :param survey_id:  This is the survey id that corresponds to the survey that is desired
        If no id is specified then the latest survey is used
    :return: HttpResponse if everything goes well. It returns a lot of context variables like the housingList
        etc. If something goes wrong then it may redirect back to the survey homePage

    To Do:
    1. Set a limit on the number of homes that are used for commute times. I would say 50 max, then
        only return the top 20-30 homes to the user
    """
    context = {
        'error_message': [],
    }

    user_profile = get_object_or_404(UserProfile, user=request.user)
    # If no id is specified in the URL, then it attempts to load the recent survey
    # The recent survey is the last survey to be created
    if survey_id == "recent":
        # Try to retrieve the most recent survey, but if there are no surveys, then
        # Redirect back to the homepage
        try:
            survey = RentingSurveyModel.objects.filter(user_profile=user_profile).order_by('-created').first()
        except RentingSurveyModel.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Could not find Survey')
            return HttpResponseRedirect(reverse('homePage:index'))
    else:
        # If the user did not choose recent, then try to grab the survey by it's id
        # If it can't find it or it is not associated with the user, just grab the
        # Recent Survey. If that fails, then redirect back to the home page.
        try:
            survey = RentingSurveyModel.objects.filter(user_profile=user_profile).get(id=survey_id)
        # If the survey ID, does not exist/is not for that user, then return the most recent survey
        except RentingSurveyModel.DoesNotExist:
            context['error_message'].append("Could not find survey id, getting recent survey")
            try:
                survey = RentingSurveyModel.objects.filter(user_profile=user_profile).order_by('-created').first()
            except RentingSurveyModel.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Could not find Survey')
                return HttpResponseRedirect(reverse('homePage:index'))

    # Populate form with stored data
    form = RentSurveyMini(instance=survey)

    # If a POST message occurs (They submit the mini form) then process it
    # If it fails then keep loading survey result and pass the error messages
    if request.method == 'POST':
        # If a POST occurs, update the form. In the case of an error, then the survey
        # Should be populated by the POST data.
        form = RentSurveyMini(request.POST, instance=survey)
        # If the survey is valid then redirect back to the page to reload the changes
        # This will also update the house list
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                kwargs={"survey_id": survey.id}))
        else:
            context['error_message'].append("There are form errors")
            try:
                survey = RentingSurveyModel.objects.get(id=survey.id)
                # Think of better solution for problem
            except RentingSurveyModel.DoesNotExist:
                print("Something really went wrong")
                messages.add_message(request, messages.ERROR, 'Could not find Survey')
                return HttpResponseRedirect(reverse('survey:rentSurveyResult'))

    # Now start executing the Algorithm
    start_algorithm(survey, context)
    context['survey'] = survey
    context['form'] = form
    return render(request, 'survey/surveyResultRent.html', context)


@login_required
def visit_list(request):
    context = {
        'error_message': []
    }

    print("Got here")

    return render(request, 'survey/visitList.html', context)


#######################################################
# Ajax Requests below
#############################################################

# This is used for ajax request to set house favorites
@login_required
def set_favorite(request):
    """
    Ajax request that sets a home as a favorite. This function just toggles the homes.
    Therefore, if the home is requested, if it already existed in the database as a favorite
    Then it unfavorites it. If it was not in the database as a favorite then it favorites it. The return
    value is the current state of the house after toggling the home. It returns a 0 if the home is
    not in the home and returns a 1 if the home is a favorite
    :param request: The HTTP request
    :return: An HTTP response which returns a JSON
        0- house not in favorites
        1- house in favorites
        else:
            - the error message
    """
    if request.method == 'POST':
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            house_id = request.POST.get('fav')
            # Retrieve the house associated with that id
            try:
                house = RentDatabase.objects.get(id=house_id)
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    # If the house is already in the database then remove it and return 0
                    # Which means that it is no longer in the favorites
                    if user_profile.favorites.filter(id=house_id).exists():
                        user_profile.favorites.remove(house)
                        return HttpResponse(json.dumps({"result": "0"}),
                                            content_type="application/json",
                                            )
                    # If the  house is not in the Many to Many then add it and
                    # return 1 which means it is currently in the favorites
                    else:
                        user_profile.favorites.add(house)
                        return HttpResponse(json.dumps({"result": "1"}),
                                            content_type="application/json",
                                            )
                except UserProfile.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                        content_type="application/json",
                                        )
            # Return an error is the house cannot be found
            except RentDatabase.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve house"}),
                                    content_type="application/json",
                                    )


@login_required
def delete_survey(request):
    """
    Deletes the given Survey passed by the User.
    It only deletes the survey if the survey corresponds to the given user.
    Always returns to the profile page of the renting survey
    :param request: HTTP request object
    :return:
        0 if the survey was successfully deleted
        error message if the survey was not successfully deleted
    """
    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            survey_id = request.POST.get('survey')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    survey_delete = user_profile.rentingsurveymodel_set.get(id=survey_id)
                    survey_delete.delete()
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json",
                                        )

                except RentingSurveyModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Survey"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )


@login_required
def set_visit_house(request):
    """
    This ajax function adds a house to the users visit list
    :param request: Http request
    :return: 1 means the home has successfully added
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            home_id = request.POST.get('visit_id')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    home = RentDatabase.objects.get(id=home_id)
                    user_profile.visit_list.add(home)
                    return HttpResponse(json.dumps({"result": "1",
                                                    "homeId": home_id}),
                                        content_type="application/json", )
                except RentDatabase.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )


@login_required
def delete_visit_house(request):
    """
    This ajax function removes a house from the users visit list
    :param request: Http request
    :return: 0 means the home was successfully removed
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            home_id = request.POST.get('visit_id')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    home = RentDatabase.objects.get(id=home_id)
                    user_profile.visit_list.remove(home)
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json", )
                except RentDatabase.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )
