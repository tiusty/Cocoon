from django.test import TestCase

from houseDatabase.models import ZipCodeDictionary, ZipCodeDictionaryChild
from django.db import IntegrityError

# defaults for the ZipCodeDictionary
default_ZipCodeDictionary_zip_code = "02476"
default_ZipCodeDictionaryChild_zip_code = "02474"
default_ZipCodeDictionaryChild_commute_time_seconds = 1200
default_ZipCodeDictionaryChild_commute_distance_meters = 25
default_ZipCodeDictionaryChild_commute_type = "driving"


def create_zip_code_dictionary(
        zip_code=default_ZipCodeDictionary_zip_code
        ):
    return ZipCodeDictionary.objects.create(
        _zip_code=zip_code
    )


def create_zip_code_dictionary_with_child(
        zip_code=default_ZipCodeDictionaryChild_zip_code,
        commute_time=default_ZipCodeDictionaryChild_commute_time_seconds,
        commute_distance=default_ZipCodeDictionaryChild_commute_distance_meters,
        commute_type=default_ZipCodeDictionaryChild_commute_type
    ):
    zip_code_dictionary = create_zip_code_dictionary()
    zip_code_dictionary.zipcodedictionarychild_set.create(
        _zip_code=zip_code,
        _commute_time=commute_time,
        _commute_distance=commute_distance,
        _commute_type=commute_type,
    )
    return zip_code_dictionary


class ZipCodeDictionaryTestCase(TestCase):
    @staticmethod
    def test_zip_code_dictionary_unique_attribute_same():
            create_zip_code_dictionary()
            try:
                create_zip_code_dictionary()
                raise Exception("ZipCodeDictionary should be unique")
            except IntegrityError:
                pass

    @staticmethod
    def test_zip_code_dictionary_unique_attribute_different():
        create_zip_code_dictionary()
        try:
            create_zip_code_dictionary(zip_code="02474")
        except IntegrityError:
            raise Exception("Integrity Error should not have been raised")


