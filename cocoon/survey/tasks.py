# Import Django Modules
from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Import Python Modules
from celery import shared_task

# Import App Modules
from .models import RentingSurveyModel
from .constants import NUMBER_OF_HOMES_RETURNED

# Import Cocoon Modules
from cocoon.dataAnalysis.models import Trackers, SurveyResultsIteration
from cocoon.userAuth.models import UserProfile
from cocoon.survey.cocoon_algorithm.rent_algorithm import RentAlgorithm

# Load the logger
import logging
logger = logging.getLogger(__name__)


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

                if len(rent_algorithm.homes) >= survey.num_home_threshold:
                    for home in rent_algorithm.homes[:survey.num_home_threshold]:
                        if home.percent_match < survey.score_threshold:
                            homes_over_threshold = False
                            break

                    # If there is then email the client!
                    if homes_over_threshold:
                        email_user(survey)


def email_user(survey):

    if hasattr(settings, 'DEFAULT_DOMAIN'):
        domain = settings.DEFAULT_DOMAIN
    else:
        domain = "https://bostoncocoon.com/"

    mail_subject = 'We found homes that match your Requirements!'
    text_message = render_to_string(
        'survey/emails/survey_notification.html', {
            'user': survey.user_profile.user,
            'num_homes': survey.num_home_threshold,
            'score_threshold': survey.score_threshold,
            'surveyUrl': survey.url,
            'domain': domain,
        }
    )
    html_message = render_to_string(
        'survey/emails/survey_notification.html', {
            'user': survey.user_profile.user,
            'num_homes': survey.num_home_threshold,
            'score_threshold': survey.score_threshold,
            'surveyUrl': survey.url,
            'domain': domain,
        }
    )
    from_email = 'devteam@bostoncocoon.com'
    to_email = survey.user_profile.user.email
    email = EmailMultiAlternatives(mail_subject, text_message, from_email, to=[to_email])
    email.attach_alternative(html_message, "text/html")

    # Send the email to the user
    email.send()


@shared_task
def compute_survey_result_iteration_task(survey_id, user_profile_id, home_scores):
    """
    Given a list of scores for the homes, populates the data regarding the survey iteration
    :param survey_id: (int) -> The survey id for the survey taken
    :param user_profile_id: (int) -> The user profile id for the user
    :param home_scores: (list(ints)) -> The scores of the homes from the survey
    """
    # Store data for tracking data
    survey_results_tracker = Trackers.get_survey_results_tracker()
    user_profile = UserProfile.objects.get(id=user_profile_id)
    survey = RentingSurveyModel.objects.get(id=survey_id)
    survey_results_tracker.iterations.create(
        user_email=user_profile.user.email,
        user_full_name=user_profile.user.full_name,
        number_of_tenants=survey.number_of_tenants,
        survey_id=survey_id,
        avg_home_score=SurveyResultsIteration.compute_average(home_scores),
        avg_home_score_returned=SurveyResultsIteration.compute_average(home_scores[:NUMBER_OF_HOMES_RETURNED]),
        standard_deviation_homes=SurveyResultsIteration.compute_standard_deviation(home_scores),
        standard_deviation_homes_returned=SurveyResultsIteration.compute_standard_deviation(home_scores[:NUMBER_OF_HOMES_RETURNED]),
        max_score_home=max(home_scores),
        max_score_home_returned=max(home_scores[:NUMBER_OF_HOMES_RETURNED]),
        min_score_home=min(home_scores),
        min_score_home_returned=min(home_scores[:NUMBER_OF_HOMES_RETURNED]),
        num_homes=len(home_scores)
    )
