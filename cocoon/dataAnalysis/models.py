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
    survey_id = models.IntegerField(default=-1)
    avg_home_score = models.IntegerField(default=-1)
    avg_home_score_returned = models.IntegerField(default=-1)
    standard_deviation_homes = models.IntegerField(default=-1)
    standard_deviation_homes_returned = models.IntegerField(default=-1)
    max_score_home = models.IntegerField(default=-1)
    max_score_home_returned = models.IntegerField(default=-1)
    min_score_home = models.IntegerField(default=-1)
    min_score_home_returned = models.IntegerField(default=-1)
    num_homes = models.IntegerField(default=-1)

    @staticmethod
    def compute_standard_deviation(scores):
        """
        Given a list of scores, returns the standard deviation of the scores
        :param scores: (list(ints)) -> A list of numbers
        :return: (int) -> The standard deviation of the numbers
        """
        if len(scores) > 0:
            avg = SurveyResultsIteration.compute_average(scores)

            score_normalized = []
            for score in scores:
                score_normalized.append((score - avg) ** 2)

            if len(score_normalized) > 0:
                variance = sum(score_normalized)/len(score_normalized)
                return variance ** .5
        return 0

    @staticmethod
    def compute_average(scores):
        """
        Computes the average of a list
        :param scores: (list(int)) -> List of numbers
        :return: (int) -> The average value of the list
        """
        if len(scores) > 0:
            return sum(scores)/len(scores)
        return 0

    def __str__(self):
        return "{0}-{1}".format(self.user_email, self.survey_id)



