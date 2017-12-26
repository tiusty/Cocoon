# Django modules
from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

# House Database models
from houseDatabase.models import ZipCodeDictionaryParentModel

# Import Global Config
from Unicorn.settings.Global_Config import ZIP_CODE_TIMEDELTA_VALUE


class ZipCodeDictionaryTest(TestCase):

    def setUp(self):
        self.zip_code = "02476"
        self.zip_code1 = "02474"
        self.zip_code2 = "02467"
        self.commute_time = 4500
        self.commute_distance = 700
        self.commute_type = "driving"
        self.commute_type1 = "transit"

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        """
        Creates a parent zip_code_dictionary object
        :param zip_code: String -> Zip code for parent zip_code
        :return: ZipCodeDictionaryParentModel -> An object instance
        """
        return ZipCodeDictionaryParentModel.objects.create(zip_code_parent=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time,
                                         commute_distance, commute_type):
        """
        Creates a child zip code dictionary for the parent zip code object
        :param parent_zip_code_dictionary: ZipCodeDictionaryParentModel -> An object instance
        :param zip_code: String -> zip_code for the child dictionary
        :param commute_time: Int -> The commute time for the child dictionary in seconds
        :param commute_distance: Int -> The commute distance for the child dictionary in meters
        :param commute_type: Commute Type Enum -> Enum for the different commute types
        :return:
        """
        parent_zip_code_dictionary.zipcodedictionarychildmodel_set.create(
            zip_code_child=zip_code,
            commute_time_seconds_child=commute_time,
            commute_distance_meters_child=commute_distance,
            commute_type_child=commute_type,
        )

    def test_zip_code_dictionary_parent_working(self):
        # Arrange/ Act
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Assert
        self.assertEqual(self.zip_code, parent_zip_code.zip_code)

    def test_zip_code_dictionary_parent_all_working_child(self):
        # Arrange/ Act / Assert // not really following methodology
        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code1)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code2)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # All the adding should pass and finish successfully
        self.assertTrue(True)

    def test_zip_code_dictionary_parent_error_adding_duplicate_error_child(self):
        # Arrange/ Act / Assert // not really following methodology
        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Act
        try:
            self.create_zip_code_dictionary(self.zip_code)
            self.assertTrue(False, "Integrity exception should have been raised")
        except IntegrityError:
            self.assertTrue(True)

    def test_zip_code_dictionary_parent_error_adding_duplicate_third_child(self):
        # Arrange/ Act / Assert // not really following methodology

        # Adding zip code 1
        try:
            self.create_zip_code_dictionary(self.zip_code)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 2
        try:
            self.create_zip_code_dictionary(self.zip_code1)
        except IntegrityError:
            self.assertTrue(False, "Integrity exception should not have been raised")

        # Adding zip code 3, should fail
        try:
            self.create_zip_code_dictionary(self.zip_code)
            self.assertTrue(False, "Integrity exception should have been raised")
        except IntegrityError:
            self.assertTrue(True)

    def test_zip_code_dictionary_child_two_child_with_different_commute_types(self):
        # Arrange
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type1)

        # Assert
        self.assertEqual(2, parent_zip_code.zipcodedictionarychildmodel_set.filter(zip_code_child=self.zip_code).count())
        self.assertEqual(self.zip_code, parent_zip_code.zipcodedictionarychildmodel_set
                         .get(zip_code_child=self.zip_code, commute_type_child=self.commute_type).zip_code)
        self.assertEqual(self.commute_type, parent_zip_code.zipcodedictionarychildmodel_set
                         .get(zip_code_child=self.zip_code, commute_type_child=self.commute_type).commute_type)
        self.assertEqual(self.commute_type1, parent_zip_code.zipcodedictionarychildmodel_set
                         .get(zip_code_child=self.zip_code, commute_type_child=self.commute_type1).commute_type)

    def test_zip_code_dictionary_child_cache_still_valid(self):
        # Arrange
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Assert
        self.assertTrue(parent_zip_code.zipcodedictionarychildmodel_set.first().zip_code_cache_still_valid())

    def test_zip_code_dictionary_child_cache_still_valid_on_day(self):
        # Arrange
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Set the last_date_updated in the past to simulate an old zip_code entry
        time = timezone.now().date() + timezone.timedelta(days=-ZIP_CODE_TIMEDELTA_VALUE)
        child_zip_code = parent_zip_code.zipcodedictionarychildmodel_set.first()
        child_zip_code.last_date_updated = time
        child_zip_code.save()

        # Assert
        self.assertTrue(parent_zip_code.zipcodedictionarychildmodel_set.first().zip_code_cache_still_valid())

    def test_zip_code_dictionary_child_cache_not_still_valid(self):
        # Arrange
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Set the last_date_updated in the past to simulate an old zip_code entry
        time = timezone.now().date() + timezone.timedelta(days=-ZIP_CODE_TIMEDELTA_VALUE-1)
        child_zip_code = parent_zip_code.zipcodedictionarychildmodel_set.first()
        child_zip_code.last_date_updated = time
        child_zip_code.save()

        # Assert
        self.assertFalse(parent_zip_code.zipcodedictionarychildmodel_set.first().zip_code_cache_still_valid())

    def test_zip_code_dictionary_child_name(self):
        # Arrange
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Assert
        self.assertEqual(parent_zip_code, parent_zip_code.zipcodedictionarychildmodel_set.first().base_zip_code)
        self.assertEqual(self.zip_code, parent_zip_code.zipcodedictionarychildmodel_set.first().zip_code)
        self.assertEqual(self.commute_time, parent_zip_code.zipcodedictionarychildmodel_set.first()
                         .commute_time_seconds)
        self.assertEqual(self.commute_time/60, parent_zip_code.zipcodedictionarychildmodel_set.first()
                         .commute_time_minutes)
        self.assertEqual(self.commute_distance, parent_zip_code.zipcodedictionarychildmodel_set.first()
                         .commute_distance_meters)
        self.assertEqual(self.commute_distance * 0.000621371, parent_zip_code.zipcodedictionarychildmodel_set.first()
                         .commute_distance_miles)
        self.assertEqual(self.commute_type, parent_zip_code.zipcodedictionarychildmodel_set.first().commute_type)
