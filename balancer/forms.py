""" forms for balancer views """
from django import forms

from player.models import Player


class BalancerForm(forms.Form):
    """ form for balancer """

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = sorted(Player.objects.filter())
        c = ((x.pk, x) for x in choices)
        choices = tuple(c)
        self.fields['players'] = forms.MultipleChoiceField(
            choices=choices,
            widget=forms.CheckboxSelectMultiple,
        )
        self.fields['count'] = forms.ChoiceField(
            label="Constellation",
            choices=[
                [2, '1 vs 1'],
                [3, '2 vs 1'],
                [4, '2 vs 2'],
                [5, '3 vs 2'],
                [6, '3 vs 3'],
            ],
            widget=forms.RadioSelect(attrs={}),
        )