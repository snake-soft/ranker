""" team forms """
from django import forms

from .models import Team


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices=()):
        forms.CheckboxSelectMultiple.__init__(self, attrs=attrs, choices=choices)

    def id_for_label(self, id_, index=None):
        id_ += '_nav'
        return forms.CheckboxSelectMultiple.id_for_label(self, id_, index=index)


class TeamCreateForm(forms.ModelForm):
    """ Team creation form """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = Team.objects.filter(communities=self.request.user.active_community if self.request.user.is_authenticated else False)

    class Meta:
        model = Team
        fields = ['teamname', 'players']
        widgets = {'players': CheckboxSelectMultiple()}
