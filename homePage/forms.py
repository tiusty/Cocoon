from django import forms


class SurveyType(forms.Form):
    SURVEY_TYPES = [
        ('rent', 'Rent'),
        ('buy', 'Buy'),
    ]
    survey_type = forms.ChoiceField(
        choices=SURVEY_TYPES,
        widget=forms.RadioSelect()
    )

