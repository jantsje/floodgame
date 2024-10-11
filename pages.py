from . import models
from ._builtin import Page
from .models import Constants
from floodgame.extrapages import UnderstandingQuestionsPage
from django import forms


def vars_for_all_templates(self):
    player = self.player
    participant = self.participant
    deductible_percent = '{0:.0f}'.format(player.deductible * 100)
    vars_for_all = {'progress': progress(self), 'cumulative_payoff': participant.vars["cumulative_payoff"],
                    'income': Constants.income, 'loan': participant.vars["loan"],
                    'risk': player.risk,
                    'deductible_percent': deductible_percent}
    if player.has_loan:
        vars_for_all['interest'] = Constants.interest
        vars_for_all['installments'] = Constants.num_installments
    if player.in_scenarios():
        vars_for_all.update(self.player.vars_for_scenarios())
    return vars_for_all


class Page(Page):
    def get_form_fields(self):
        return self.form_fields + ['opened']


def progress(p):
    progressrel = p.round_number/p.participant.vars["total_rounds"]*100
    return progressrel


class Welcome(Page):
    form_model = 'player'

    def vars_for_template(self):
        return {'demo_treatment': self.participant.vars["demo_treatment"],
                'page_title': "Welcome"}

    def before_next_page(self):
        self.player.set_treatment()

    def is_displayed(self):
        return self.round_number == 1


class Overview(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'page_title': "Overview"}


class Earnings(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_earnings()
        vars_for_this_template.update({'page_title': "Collect your money"})
        return vars_for_this_template

    def before_next_page(self):
        self.player.earn_money()


class BuyHouse(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['buy_house']

    def before_next_page(self):
        self.player.buy_house_method()

    def vars_for_template(self):
        return {'page_title': "Buy a house"}


class Instructions(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'page_title': "Instructions page 1"}


class Instructions2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_instructions()
        vars_for_this_template.update({'page_title': "Instructions page 2"})
        return vars_for_this_template


class Instructions2a(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1 and self.player.has_loan

    def vars_for_template(self):
        return {'page_title': "Instructions page 3"}


class Instructions3(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'page_title': "Instructions last page"}


class WaitForNewScenario(Page):
    form_model = 'player'
    timeout_seconds = 0.00001

    def is_displayed(self):
        return self.player.is_new_scenario()

    def before_next_page(self):
        if self.player.year == 1:
            self.player.new_scenario_method()


class NewScenario(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.is_new_scenario()

    def before_next_page(self):
        self.player.get_income()
        self.player.opened_instructions()

    def vars_for_template(self):
        return {'page_title': self.participant.vars['page_title']}


class UnderstandingQuestions(UnderstandingQuestionsPage):
    page_title = 'Comprehension questions'
    set_correct_answers = False  # do not fill out the correct answers (this is for fast skipping through pages)
    form_model = 'player'
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'
    form_fields = ['opened']

    def get_questions(self):
        return self.player.get_questions_method()

    def before_next_page(self):
        self.player.opened_instructions()

    def is_displayed(self):
        return self.round_number == Constants.num_test_rounds


class Premium(Page):
    form_model = 'player'
    form_fields = ['pay_premium']

    def is_displayed(self):
        if not self.player.has_insurance:
            return False
        elif self.player.in_scenarios():
            return True

    def before_next_page(self):
        self.player.pay_premium_method()
        self.player.opened_instructions()

    def vars_for_template(self):
        return {'page_title': "Please pay your premium"}


class Invest(Page):
    form_model = 'player'
    form_fields = ['mitigate']

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_invest()
        vars_for_this_template.update({'page_title': "Flood protection investment decision"})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_scenarios() and self.player.year == 1

    def before_next_page(self):
        print(id(self.player))
        self.player.set_payoff()
        self.player.pay_mitigation_method()
        self.player.opened_instructions()


class Invest2(Page):
    form_model = 'player'
    form_fields = ['mitigate']

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_invest2()
        vars_for_this_template.update({'page_title': "Flood protection investment decision"})
        return vars_for_this_template

    def is_displayed(self):
        if self.player.in_scenarios() and self.player.year > 1:
            return True
        else:
            return False

    def before_next_page(self):
        self.player.set_payoff()
        self.player.pay_mitigation_more()
        self.player.opened_instructions()


class PayInstallment(Page):
    form_model = 'player'
    form_fields = ['pay_installment']

    def vars_for_template(self):
        return {'loan_cost': self.participant.vars["installment+interest"],
                'page_title': 'Please pay your loan cost'}

    def is_displayed(self):
        return self.player.should_pay_installment()

    def before_next_page(self):
        self.player.pay_installment_method()
        self.player.opened_instructions()


class PayFinalInstallment(Page):
    form_model = 'player'
    form_fields = ['repay_loan']

    def is_displayed(self):
        return self.player.should_pay_final_installment()

    def before_next_page(self):
        self.player.pay_final_installment_method()
        self.player.opened_instructions()

    def vars_for_template(self):
        return {'page_title': 'Please repay your loan'}


class Floodrisk(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.flooded and self.player.has_insurance:
            # only show button to pay deductible if player is flooded and has insurance
            return ['pay_deductible', 'opened']
        elif self.player.mitigate == 0 and self.player.flooded and not self.player.has_insurance:
            # only show button to pay damage if player is flooded and no insurance was offered
            return ['pay_damage', 'opened']
        else:
            return['opened']

    def vars_for_template(self):
        player = self.player
        return {'floodnrs': player.floodnrs,
                'items': models.Constants.items,
                'items2': models.Constants.items2,
                'page_title': 'Floodrisk'}

    def is_displayed(self):
        return self.player.in_scenarios()

    def before_next_page(self):
        self.player.pay_after_flood()
        self.player.save_payoff()
        self.player.opened_instructions()

        if self.player.year != Constants.maxyears:
            self.player.get_income()


class Payment(Page):
    form_model = 'player'
    form_fields = ['selected']

    def is_displayed(self):
        return self.player.in_last_year()

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_payment()
        vars_for_this_template.update({'page_title': "Select scenario for payment"})
        return vars_for_this_template


class Payment2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.in_last_year()

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_payment()
        vars_for_this_template.update({'page_title': "Select scenario for payment"})
        return vars_for_this_template


'''Class bomb risk elicitation task (BRET)'''


class BRET(Page):
    form_model = 'player'
    form_fields = [
        'bomb_BRET',
        'boxes_collected_BRET',
        'bomb_row_BRET',
        'bomb_col_BRET',
    ]

    def is_displayed(self):
        return self.player.in_last_year()

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_BRET()
        vars_for_this_template.update({'page_title': "Additional task 3/3"})
        return vars_for_this_template

    def before_next_page(self):
        self.player.save_payoff_bret()


class BRET_2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.in_last_year() and self.participant.vars["selected_additional"] == 3

    def vars_for_template(self):
        return {
            'box_value_BRET':              Constants.box_value_BRET,
            'boxes_total_BRET':            Constants.num_rows_BRET * Constants.num_cols_BRET,
            'boxes_collected_BRET':        self.player.boxes_collected_BRET,
            'bomb_BRET':                   self.player.bomb_BRET,
            'bomb_row_BRET':               self.player.bomb_row_BRET,
            'bomb_col_BRET':               self.player.bomb_col_BRET,
            'payoff_BRET':                 '{0:.2f}'.format(self.player.payoff_BRET),
            'page_title':                  'Additional task 3 - results'

        }


'''Risk preferences choice lists'''


class List_R(Page):
    form_model = 'player'
    form_fields = ['switching_point_risk']

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_risk()
        vars_for_this_template.update({'page_title': "Additional task 2/3"})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_last_year()

    def before_next_page(self):
        self.player.save_payoff_risk()


class List_R2(Page):
    form_model = 'player'

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_risk()  # should this be risk2?
        vars_for_this_template.update({'page_title': "Additional task 2 - results"})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_last_year() and self.participant.vars["selected_additional"] == 2


class List_R3(Page):
    form_model = 'player'
    form_fields = ['switching_point_risk2']

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_risk3()  # should this be risk2?
        vars_for_this_template.update({'page_title': "Additional task 1/3"})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_last_year()

    def before_next_page(self):
        self.player.save_payoff_risk2()


class List_R4(Page):
    form_model = 'player'

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_risk3()  # should this be risk2?
        vars_for_this_template.update({'page_title': "Additional task 1 - results"})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_last_year() and self.participant.vars["selected_additional"] == 1


'''Time preferences choice lists'''


class List_T(Page):
    form_model = 'player'
    form_fields = ['switching_point_time']

    def vars_for_template(self):
        return {'max_time_payment': Constants.max_time_payment,
                'page_title': "Time preferences"}

    def is_displayed(self):
        return self.player.in_last_year()

    def before_next_page(self):
        self.player.save_payoff_time()


class List_T2(Page):
    form_model = 'player'

    def vars_for_template(self):
        return {'selected_scenario': self.participant.vars["selected_scenario_time"],
                'payoff_time': self.participant.vars["payoff_time"],
                'page_title': "Time preferences"}

    def is_displayed(self):
        return self.player.in_last_year()


'''Payment pages'''


class PaymentAdditional(Page):
    form_model = 'player'

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_additional_payment()
        vars_for_this_template.update({'page_title': "Select additional task for payment", 'selected': None})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_last_year()


class PaymentAdditional2(Page):
    form_model = 'player'

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_additional_payment()
        vars_for_this_template.update({'page_title': "Additional tasks - payment selected"})
        return vars_for_this_template

    def is_displayed(self):
        return self.player.in_last_year()


class PaymentPrize(Page):
    form_model = 'player'
    form_fields = ['selected_button']

    def is_displayed(self):
        return self.player.in_last_year()

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_payment_prize()
        vars_for_this_template.update({'page_title': "Select winning scenario"})
        # vars_for_this_template.update(self.player())
        return vars_for_this_template


class PaymentPrize2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.in_last_year()

    def before_next_page(self):
        self.player.save_final_payoffs()

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_payment_prize()
        vars_for_this_template.update({'page_title': "Winning scenario selected"})
        # vars_for_this_template.update(self.player())
        return vars_for_this_template


class TotalPayment(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.in_last_year()

    def before_next_page(self):
        self.player.save_final_payoffs()

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_payment_prize()
        vars_for_this_template.update({'page_title': "Overview of payments"})
        return vars_for_this_template


page_sequence = [
    Welcome,
    Overview,
    Earnings,
    BuyHouse,
    Instructions,
    Instructions2,
    Instructions2a,
    Instructions3,
    WaitForNewScenario,
    NewScenario,
    Invest,
    Invest2,
    PayInstallment,
    PayFinalInstallment,
    Premium,
    Floodrisk,
    UnderstandingQuestions,
    Payment,
    Payment2,
    List_R3,
    List_R,
    BRET,
    PaymentAdditional,
    PaymentAdditional2,
    List_R4,
    List_R2,
    BRET_2,
    List_T,
    List_T2,
    PaymentPrize,
    PaymentPrize2,
    TotalPayment]
