from django.db import models


class Trackers(models.Model):
    SURVEY_RESULT_TRACKER = 'sr'
    TRACKER_TYPES = (
        (SURVEY_RESULT_TRACKER, 'Survey Results Tracker'),
    )

    tracker_type = models.CharField(
        unique=True,
        choices=TRACKER_TYPES,
        max_length=2,
    )

    @staticmethod
    def get_survey_results_tracker():
        (tracker, created) = Trackers.objects.get_or_create(tracker_type=Trackers.SURVEY_RESULT_TRACKER)
        return tracker

    def __str__(self):
        return self.get_tracker_type_display()


class SurveyResultsIteration(models.Model):
    tracker = models.ForeignKey(Trackers, related_name="iterations")
    user_email = models.CharField(default="", max_length=200)
    user_full_name = models.CharField(default="", max_length=200)
    number_of_tenants = models.IntegerField(default=-1)

    def __str__(self):
        return self.user_email


class HomeTracker(models.Model):
    iteration = models.ForeignKey(SurveyResultsIteration, related_name="homes")
    score = models.IntegerField(default=-1)



