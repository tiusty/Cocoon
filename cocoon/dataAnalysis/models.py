from django.db import models


class SurveyResultsTracker(models.Model):
    pass


class SurveyResultsIteration(models.Model):
    tracker = models.ForeignKey(SurveyResultsTracker, related_name="iterations")


class HomeTracker(models.Model):
    iteration = models.ForeignKey(SurveyResultsIteration, related_name="homes")
    score = models.IntegerField(default=-1)



