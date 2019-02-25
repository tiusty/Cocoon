from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from celery import shared_task
from cocoon.survey.models import RentingSurveyModel
from cocoon.survey.cocoon_algorithm.rent_algorithm import RentAlgorithm

@shared_task
def notify_user_survey_updates():
    """
    Checks all the surveys and any survey that is marked to send updates to the user
        the survey results are computed and then if the user requirements are met
        then an email is sent to the user
    """
    for survey in RentingSurveyModel.objects.all():
        # Check if the user wants updates about the survey
        if survey.wants_update:
            # Determine if the survey is ready to be updated
            if survey.ready_to_update_user():
                # Since the survey is being updated save the update timestamp
                survey.last_updated = timezone.now()
                survey.save()

                # Compute the algorithm
                rent_algorithm = RentAlgorithm()
                rent_algorithm.run(survey)

                # Determine if there is enough homes over the score threshold determined
                #   by the client
                homes_over_threshold = True
                for home in rent_algorithm.homes[:survey.num_home_threshold]:
                    if home.percent_match < survey.score_threshold:
                        homes_over_threshold = False
                        break

                # If there is then email the client!
                if homes_over_threshold:
                    print('yes!')
                else:
                    print('no...not yet')


