from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants
from otree.common import safe_json

import random


class PlayerBot(Bot):

    def play_round(self):
        scenarios_list = self.participant.vars["scenarios_list"]
        mitigated_this_scenario = self.participant.vars["mitigated_this_scenario"]

        if self.round_number == 1:
            yield (pages.Welcome, {'opened': 0})
            yield (pages.Overview, {'opened': 0})
            yield (pages.Earnings, {'opened': 0})
            yield (pages.BuyHouse, {'opened': 0, 'buy_house': 'bought'})
            yield (pages.Instructions)
            yield (pages.Instructions2)
            if self.player.has_loan:
                yield (pages.Instructions2a)
            yield (pages.Instructions3)


        if self.round_number <= len(self.participant.vars["scenarios_list"]) - Constants.useless_rounds and self.participant.vars["scenarios_list"][self.round_number - 1] != self.participant.vars["scenarios_list"][self.round_number - 2]:
            yield Submission(pages.WaitForNewScenario, {'opened': 0}, timeout_happened=True, check_html=False, )

        if self.round_number <= len(self.participant.vars["scenarios_list"]) - Constants.useless_rounds and \
            self.participant.vars["scenarios_list"][self.round_number - 1] \
            != self.participant.vars["scenarios_list"][self.round_number - 2] :
            yield (pages.NewScenario, {'opened': 2})


        if self.round_number > len(scenarios_list) - Constants.useless_rounds:  # end of game
            pass
        elif self.player.year == 1:
            yield (pages.Invest, {'mitigate': 1, 'opened':0})

        if self.round_number == 1:
            pass
        elif self.round_number > len(scenarios_list) - Constants.useless_rounds:  # end of game
            pass
        elif self.player.year == 1:
            pass
        elif self.player.year > 1:
            yield (pages.Invest2, {'mitigate': 1, 'opened':0})
        else:
            pass

        if self.player.should_pay_installment():
            yield (pages.PayInstallment, {'pay_installment': 'paid_installment', 'opened': 0})

        if self.player.should_pay_final_installment():
            yield (pages.PayFinalInstallment, {'repay_loan': 'repaid_loan', 'opened': 0})

        if not self.player.has_insurance:
            pass
        elif self.round_number > len(scenarios_list) - Constants.useless_rounds:  # end of game
            pass
        elif int(self.player.year) > 0:
            yield (pages.Premium, {'pay_premium': 'paid_premium', 'opened': 0})


        if self.player.flooded and self.player.has_insurance: # only show button to pay deductible if player is flooded and has insurance
            # print("***** deductible should be paid")
            yield (pages.Floodrisk, {'pay_deductible': 'paid_deductible', 'opened':0})
        elif self.player.mitigate == 0 and self.player.flooded and not self.player.has_insurance: # only show button to pay damage if player is flooded and no insurance was offered
            yield (pages.Floodrisk, {'pay_damage': 'paid_damage', 'opened':0})
        else:
            yield (pages.Floodrisk, {'opened':0})

        if self.round_number == Constants.num_test_rounds:
            yield Submission(pages.UnderstandingQuestions, check_html=False)

        if self.round_number == len(self.participant.vars["years"]) - Constants.useless_rounds:
            yield (pages.Payment, {'selected':1, 'opened':0})
            yield (pages.Payment2, {'opened':0})
            yield (pages.List_R3, {'switching_point_risk2': 5})
            yield (pages.List_R, {'switching_point_risk': 6})
            yield (pages.BRET, {'bomb_BRET': 0, 'boxes_collected_BRET': 20, 'bomb_row_BRET': 1,
                                'bomb_col_BRET': 1, 'opened': 0})
            yield (pages.PaymentAdditional)
            yield (pages.PaymentAdditional2)
            if self.participant.vars["selected_additional"] == 1:
                yield(pages.List_R4)
            elif self.participant.vars["selected_additional"] == 2:
                yield(pages.List_R2)
            elif self.participant.vars["selected_additional"] == 3:
                yield(pages.BRET_2)
            yield (pages.List_T, {'switching_point_time': 100.0})
            yield (pages.List_T2)
            yield (pages.PaymentPrize, {'selected_button': 'selected'})
            yield (pages.PaymentPrize2)
            yield (pages.TotalPayment)


