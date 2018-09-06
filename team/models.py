from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.db.models import Sum

from match.models import Match


class Team(models.Model):
    """ Teams are Season-based
    -> every season there are new values
    -> values are calculated from the matches
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    teamname = models.CharField(
        max_length=50, verbose_name="Teamname",
        blank=True,
    )
    players = models.ManyToManyField('player.Player')

    frm = datetime(2000, 1, 1).date()
    to = datetime(3000, 1, 1).date()

    @classmethod
    def set_from_to(cls, frm, to):
        def to_date(date_x):
            """ date_x may be date, datetime or string object 
            returns date object
            """
            return {
                datetime: lambda: date_x.date(),
                date: lambda: date_x,
                str: lambda: datetime.strptime(date_x, '%Y-%m-%d').date(),
                }.get(type(date_x))()

        cls.frm = to_date(frm)
        cls.to = to_date(to) + timedelta(days=1)

    @property
    def is_player_team(self):
        return len(self.players.all()) is 1

    @property
    def name(self):
        name = self.teamname
        return name if name else False

    @property
    def team_score(self):
        ''' calculate based on matches '''
        results = self.get_win_draw_lose()
        return len(results[0]) * 2 + len(results[1]) * 1

    @property
    def team_rating(self):
        """ Calculates the team strength out of the Player Elo """
        if not len(self.players.all()):
            return 0.0
        else:
            return sum([x.player_rating() for x in self.players.all()]) / \
                len(self.players.all())

    @property
    def verbose_name(self):
        return str("%s (TeamScore: %s; TeamRating: %s Members: %s)" % (
            self.get_team_name_or_members(),
            int(self.team_score + 0.5),
            int(self.team_rating + 0.5),
            ", ".join([x.nick for x in self.players.all()])
        ))

    @property
    def team_rating_as_int(self):
        return int(self.team_rating + 0.5)

    def get_team_name_or_members(self):
        if self.is_player_team:
            return self.teamname
        else:
            return '%s <%s>' % (
                self.teamname,
                ', '.join([x.nick for x in self.players.all()])
            )

    def get_win_draw_lose(self):
        win, draw, lose = [], [], []
        matches = Match.objects.filter(
            firstteam_id=self.pk,
            date_time__range=(self.frm, self.to)
        )
        for match in matches:
            result = match.firstteam_goals - match.secondteam_goals
            if result > 0:
                win.append(match)
            elif result is 0:
                draw.append(match)
            elif result < 0:
                lose.append(match)

        matches = Match.objects.filter(
            secondteam_id=self.pk,
            date_time__range=(self.frm, self.to)
        )
        for match in matches:
            result = match.secondteam_goals - match.firstteam_goals
            if result > 0:
                win.append(match)
            elif result is 0:
                draw.append(match)
            elif result < 0:
                lose.append(match)
        return win, draw, lose

    @property
    def team_win(self):
        return self.get_win_draw_lose()[0]

    @property
    def team_draw(self):
        return self.get_win_draw_lose()[1]

    @property
    def team_lose(self):
        return self.get_win_draw_lose()[2]

    @property
    def close_win_lose(self):
        close_win, close_lose = [], []
        for match in Match.objects.filter(
            firstteam=self,
            date_time__range=(self.frm, self.to)
        ):
            if match.goal_difference is 1:
                close_win.append(match)
            elif match.goal_difference is -1:
                close_lose.append(match)

        for match in Match.objects.filter(
            secondteam=self,
            date_time__range=(self.frm, self.to)
        ):
            if match.goal_difference is 1:
                close_lose.append(match)
            elif match.goal_difference is -1:
                close_win.append(match)

        return (close_win, close_lose)

    @property
    def close_win(self):
        return self.close_win_lose[0]

    @property
    def close_lose(self):
        return self.close_win_lose[1]

    @property
    def close_wl_factor(self):
        return len(self.close_win) - len(self.close_lose)

    @property
    def goal_own_foreign(self):
        own, foreign = 0, 0
        sum_ = Match.objects.filter(
            firstteam_id=self.pk,
            date_time__range=(self.frm, self.to)
        ).aggregate(Sum('firstteam_goals'))['firstteam_goals__sum']
        own += sum_ if sum_ else 0

        sum_ = Match.objects.filter(
            secondteam_id=self.pk,
            date_time__range=(self.frm, self.to)
        ).aggregate(Sum('secondteam_goals'))['secondteam_goals__sum']
        own += sum_ if sum_ else 0

        sum_ = Match.objects.filter(
            firstteam_id=self.pk,
            date_time__range=(self.frm, self.to)
        ).aggregate(Sum('secondteam_goals'))['secondteam_goals__sum']
        foreign += sum_ if sum_ else 0

        sum_ = Match.objects.filter(
            secondteam_id=self.pk,
            date_time__range=(self.frm, self.to)
        ).aggregate(Sum('firstteam_goals'))['firstteam_goals__sum']

        foreign += sum_ if sum_ else 0
        return own, foreign

    @property
    def goal_own(self):
        return self.goal_own_foreign[0]

    @property
    def goal_foreign(self):
        return self.goal_own_foreign[1]

    @property
    def goal_factor(self):
        if self.goal_own == 0 and self.goal_foreign == 0:
            return -1000
        return self.goal_own - self.goal_foreign

    @classmethod
    def players_have_team(cls, player_obj_lst):
        for team in cls.objects.all():
            if sorted(player_obj_lst, key=lambda x: x.pk) \
                    == sorted(team.players.all(), key=lambda x: x.pk):
                return team
        # return None  # no more possible

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s (%s)' % (
            self.get_team_name_or_members(),
            self.team_rating_as_int
        )
