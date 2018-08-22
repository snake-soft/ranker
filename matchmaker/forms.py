from django import forms

from player.models import Player


class MatchmakerForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        choices = sorted(
            Player.objects.all(), key=lambda x: x.rating, reverse=True
            )
        choices = tuple((x.pk, "%s (%s)" % (x.nick, x.rating_as_int))
                        for x in (choices))

        initial = request.session['last_players'] \
            if 'last_players' in request.session else ''

        self.fields['players'] = forms.MultipleChoiceField(
            choices=choices, widget=forms.CheckboxSelectMultiple, initial=initial
            )

        initial = int(request.session['last_count']) \
            if 'last_count' in request.session else 2
        self.fields['count'] = forms.IntegerField(min_value=2, initial=initial)

    def clean(self):
        data = self.cleaned_data
        if "players" not in data or len(data["players"]) <= 1:
            self._errors["players"] = ["At least 2 Players are needed"]
        elif len(data["players"]) < data["count"]:
            self._errors["players"] = ["Check Count"]
        return self.cleaned_data