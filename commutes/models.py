# Django Imports
from django.db import models
from django.utils import timezone


class CommuteTypeModel(models.Model):
    """
    Class stores all the different commute types
    This generates a choice field in the survey
    If another commute type gets added, it should get added to the COMMUTE_TYPES field
    """

    COMMUTE_TYPES = (
        ('Driving', 'Driving'),
        ('Transit', 'Transit'),
        ('Walking', 'Walking'),
        ('Biking', 'Biking'),
    )
    commute_type_field = models.CharField(
        unique=True,
        choices=COMMUTE_TYPES,
        max_length=200,
    )

    def __str__(self):
        return self.commute_type

    @property
    def commute_type(self):
        return self.commute_type_field


class ZipCodeDictionaryParentModel(models.Model):
    """
    The base Zip Code, aka 02476, for each base zip_code, there will be
    a bunch of associated zip codes via foreign key from ZipCodeDictionaryParentModel model.
     The Base model should not have a commute_time_minutes or Commute_distance since it is in
     relation to nothing. Instead the child zip code identifies the relation
    """
    zip_code_parent = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.zip_code

    @property
    def zip_code(self):
        return self.zip_code_parent


class ZipCodeDictionaryChildModel(models.Model):
    """
    This model class serves as an approximation for commute time/distance associated with
    zip_codes. This ZipCodeDictionaryParentModel should be precomputed or should be populated periodically.
    """
    zip_code_child = models.CharField(max_length=20)
    parent_zip_code_child = models.ForeignKey('ZipCodeDictionaryParentModel', on_delete=models.CASCADE)
    commute_time_seconds_child = models.IntegerField(default=-1)
    commute_distance_meters_child = models.IntegerField(default=-1)
    last_date_updated_child = models.DateField(default=timezone.now)
    commute_type_child = models.ForeignKey('CommuteTypeModel', on_delete=models.PROTECT)

    def __str__(self):
        return self.zip_code

    @property
    def zip_code(self):
        return self.zip_code_child

    @property
    def parent_zip_code(self):
        return self.parent_zip_code_child

    @property
    def zip_code_parent(self):
        return self.parent_zip_code_child

    @property
    def commute_time_minutes(self):
        return self.commute_time_seconds / 60

    @property
    def commute_time_seconds(self):
        return self.commute_time_seconds_child

    @property
    def commute_distance_miles(self):
        return self.commute_distance_meters * 0.000621371

    @property
    def commute_distance_meters(self):
        return self.commute_distance_meters_child

    @property
    def last_date_updated(self):
        return self.last_date_updated_child

    @last_date_updated.setter
    def last_date_updated(self, new_last_date_updated):
        self.last_date_updated_child = new_last_date_updated

    @property
    def commute_type(self):
        return self.commute_type_child

    def zip_code_cache_still_valid(self):
        """
        This function tests whether or not the zip code should be recalculated
        Currently, the zip_code should be recomputed if it is older than 2 months old
        :return: Boolean: True -> The cache is still valid, False -> The cache is no longer valid
        """
        if timezone.now().date() > self.last_date_updated + timezone.timedelta(days=ZIP_CODE_TIMEDELTA_VALUE):
            return False
        else:
            return True
