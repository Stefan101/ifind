__author__ = 'leif'

from game_models import UserProfile, PlayerAchievement, Achievement
from django.contrib.auth.models import User



class GameAchievement(object):

    def __init__(self, userprofile, highscores, currentgame=None):
        """
        :param userprofile: ifind.models.game_models.UserProfile
        :param highscores: list of highscores for this user
        :return:
        """
        self.userprofile = userprofile
        self.highscores = highscores
        self.currentgame = currentgame


    def check_achievement_criteria(self):
        pass


class AllCat(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, num_of_cats = 2):
        GameAchievement.__init__(self,userprofile, highscores)
        self.num_of_cats = num_of_cats

    def check_achievement_criteria(self):
        """
        the number of highscores is a list of the highest_score in each category
        a highest_score is only recorded once they have played a game.
        but we could also check to make sure they have score points in each category, too
        :return:
        """
        if len(self.highscores) == self.num_of_cats:
            return True
        else:
            return False

    def __str__(self):
        #TODO(leifos): there probably a neat way to return the class name

        return self.__class__.__name__

class HighScorer(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, score_required=10000):
        GameAchievement.__init__(self,userprofile, highscores)
        self.score_required = score_required

    def check_achievement_criteria(self):
        total = 0
        for hs in self.highscores:
            total += hs.high_score

        if total > self.score_required:
            return True
        else:
            return False

    def __str__(self):
        #TODO(leifos): there probably a neat way to return the class name
        return self.__class__.__name__


class GameAchievementChecker(object):
    def __init__(self, user):
        """
        :param user:
        :return:
        """
        self.user=user

    def check_and_set_new_achievements(self, userprofile, highscores, currentgame):

        # get list of the users current player achievements
        cpal = PlayerAchievement.objects.filter(user=self.user)

        # pull out the list of achievements they have obtained.
        pal = []
        for cpa in cpal:
            pal.append(cpa.achievement)


        # get list of possible achievements
        aal = Achievement.objects.all()

        # exclude achievements already obtained
        al = []
        for a in aal:
            if a not in pal:
                al.append(a)


        # create an empty list of new achievements
        nal = []

        # for each achievement, check whether the criteria is met
        for a in al:
            outcome = self._test_achievement(a, userprofile, highscores, currentgame)
            if outcome:
                # if met, create the PlayerAchievement Record
                pa = PlayerAchievement(user=self.user, achievement=a)
                pa.save()
                # add this PlayerAchievement to a list
                nal.append(pa)

        # return list of new achievements
        return nal


    def _test_achievement(self, achievement, userprofile, highscores, currentgame):
        """
        :return: true, if the achievement criteria are met, else false

        """

        #TODO(leifos): use reflection ? or some kind of class inspection to determine if the class has been implemented and then use that class
        # need some reflection in here to inspect whether the achievement class specified exists or not
        outcome = False
        ga =  None
        if achievement.achievement_class == 'HighScorer':
            ga = HighScorer(userprofile, highscores, currentgame)

        if achievement.achievement_class == 'AllCat':
            ga = AllCat(userprofile, highscores, currentgame)

        if ga:
           outcome = ga.check_achievement_crtieria()

        return outcome