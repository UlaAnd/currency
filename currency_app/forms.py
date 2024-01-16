from django import forms


class ColumnVisibilityForm(forms.Form):
    eur_to_pln = forms.BooleanField(required=False, initial=False)
    usd_to_pln = forms.BooleanField(required=False, initial=False)
    chf_to_pln = forms.BooleanField(required=False, initial=False)
    eur_to_usd = forms.BooleanField(required=False, initial=False)
    chf_to_usd = forms.BooleanField(required=False, initial=False)
