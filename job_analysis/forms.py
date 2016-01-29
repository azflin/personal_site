from django import forms


class JobAnalysisForm(forms.Form):

    search_query = forms.CharField(label='Search Query')
    location = forms.CharField(label='Location', required=False)
    country = forms.ChoiceField(
        label='Country',
        choices=[('ca', 'Canada'), ('us', 'United States')]
    )
    max_jobs = forms.IntegerField(min_value=1, label='Max Number of Jobs', required=False)