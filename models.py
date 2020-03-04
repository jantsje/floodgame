from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)

import random  # necessary for random risk_high
from django import forms  # necessary for final survey
from django.forms import widgets

author = 'Jantsje Mol'

doc = """
Basic flood investment game (including earnings task)
"""


class Constants(BaseConstants):
    name_in_url = 'floodgame'
    players_per_group = None
    scenarios = ["LH", "LL", "HH", "HL", "LxL", "HxL"]
    scenarios_no_insurance = ["risk1", "risk2", "risk3", "risk4", "risk5", "risk6"]
    num_test_rounds = 1
    minyears = 1  # minimum nr of years per scenario
    maxyears = 1  # maximum nr of years per scenario. if they minyears = maxyears there is no randomness in nr of years
    useless_rounds = 0  # only necessary in case of random number of years
    num_rounds = maxyears*len(scenarios)+num_test_rounds  # 99 could be set very high if it is variable
    num_installments = 10
    risk_high = 15  # high flood risk_high on a scale from 1 to 100
    risk_low = 3  # low flood risk_high on a scale from 1 to 100
    # extra flood risks to test in no_insurance treatment
    risk_1 = 1
    risk_6 = 20
    risk_3 = 5
    risk_4 = 10
    deductible_xtra_low = float(0.05)  # extra small deductible - OBVIOUSLY INTEGER GIVES ERRORS IF YOU USE DECIMALS
    deductible_low = float(0.15)  # small deductible
    deductible_high = float(0.2)  # large deductible
    damage = c(50000)  # size of damage in case of a flood
    scaling_lossfunction = -0.00008
    house_value = c(240000)
    initial_endowment = c(75000)
    total_earnings = house_value + initial_endowment
    income = c(4000)
    interest = 1  # in percent, for loan treatment

    ''' houses for flood risk '''
    itemss = list(range(1, 51))
    items = ["{0:0=3d}".format(value) for value in itemss]
    itemss2 = list(range(51, 101))
    items2 = ["{0:0=3d}".format(value) for value in itemss2]

    ''' risk and time preferences '''

    willingness_values = list(range(0, 11))  # I don't think these are used at the moment
    # TIME PRICE LIST
    right_side_amounts_time = [100.0, 103.0, 106.10, 109.2, 112.4, 115.6, 118.8, 122.1, 125.4, 128.8, 132.3,
                               135.7, 139.2, 142.8, 146.4, 150.1, 153.8, 157.5, 161.3, 165.1, 169.0, 172.9, 176.9,
                               180.9, 185.0]
    # from Falk et al working paper 2016, cannot be constructed by math due to random term
    max_time_payment = '{0:.2f}'.format(max(right_side_amounts_time))
    # RISK GAIN PRICE LIST
    left_side_riskA = [1.68, 1.76, 1.84, 1.92, 2.00, 2.08, 2.16, 2.24, 2.32, 2.4]  # from Drichoutis & Lusk 2016
    left_side_riskB = [2.01, 2.17, 2.32, 2.48, 2.65, 2.86, 3.14, 3.54, 4.50, 4.70]
    right_side_riskA = len(left_side_riskA)*[1.60]
    right_side_riskB = len(left_side_riskA)*[1.00]
    # RISK LOSS PRICE LIST
    left_side_riskC = [i * (-1) for i in reversed(left_side_riskA)]
    left_side_riskD = [i * (-1) for i in reversed(left_side_riskB)]
    right_side_riskC = [i * (-1) for i in reversed(right_side_riskA)]
    right_side_riskD = [i * (-1) for i in reversed(right_side_riskB)]
    endowment_loss = 4.70  # endowment for the risk price list of the loss domain
    endowment_loss_str = str('{0:.2f}'.format(endowment_loss))

    ''' earnings task '''

    box_value = c(10500)
    num_rows = 5
    num_cols = 20
    num_bombs = 50  # = money
    boxes_required = 30
    box_height = '30px'
    box_width = '30px'
    devils_game = True

    ''' Bomb risk elicitation task (BRET) '''

    box_value_BRET = 0.05
    num_rows_BRET = 5
    num_cols_BRET = 20
    box_height_BRET = '30px'
    box_width_BRET = '30px'
    num_rounds_BRET = 1
    feedback_BRET = True
    dynamic_BRET = False
    random_BRET = True
    devils_game_BRET = False
    undoable_BRET = True
    time_interval_BRET = 1.00


class Subsession(BaseSubsession):

    def creating_session(self):

        for p in self.get_players():

            if self.round_number == 1:
                p.participant.vars["opened_instructions"] = 0
                p.participant.vars["selected_scenario"] = random.randint(1, 6)
                p.participant.vars["selected_pref"] = random.randint(1, 7)
                p.participant.vars["selected_additional"] = random.randint(1, 3)
                p.participant.vars["payoff_small"] = 0
                p.participant.vars["selected_row_time"] = random.randint(0, len(Constants.right_side_amounts_time)-1)
                p.participant.vars["left_selected"] = random.choice([True, False])
                p.participant.vars["left_selected2"] = random.choice([True, False])
                p.participant.vars["switching_point_time"] = 0
                p.participant.vars["switching_point_risk"] = 0
                p.participant.vars["selected_row_risk"] = random.randint(1, len(Constants.left_side_riskB))
                p.participant.vars["selected_row_risk2"] = random.randint(1, len(Constants.left_side_riskB))
                p.participant.vars["selected_scenario_time"] = \
                    Constants.right_side_amounts_time[p.participant.vars["selected_row_time"]]
                p.participant.vars["cumulative_payoff"] = 0
                p.participant.vars["mitigate_more"] = 0
                p.participant.vars["payoff_scenario1"] = 0
                p.participant.vars["payoff_scenario2"] = 0
                p.participant.vars["payoff_scenario3"] = 0
                p.participant.vars["payoff_scenario4"] = 0
                p.participant.vars["payoff_scenario5"] = 0
                p.participant.vars["payoff_scenario6"] = 0
                p.participant.vars["payoff_time_str"] = ""
                p.participant.vars["payoff_time_str"] = ""
                p.participant.vars["payoff_time"] = 0
                p.participant.vars["payoff_additional"] = 0
                p.participant.vars["payoff_risk"] = 0  # for the gain domain
                p.participant.vars["payoff_risk2"] = 0  # for the loss domain
                p.participant.vars["payoff_BRET"] = 0
                p.participant.vars["payoff_risk_str"] = 0
                p.participant.vars["payoff_risk_str2"] = 0
                p.participant.vars["payoff_time_str"] = 0
                p.participant.vars["page_title"] = "empty"
                p.participant.vars["premium"] = 999999  # set initial value
                p.participant.vars["premium_discounted"] = [c(0), c(0), c(0), c(0), c(0)]
                p.participant.vars["reduced_damage"] = [c(0), c(0), c(0), c(0), c(0)]
                p.participant.vars["reduced_deductible"] = [c(0), c(0), c(0), c(0), c(0)]
                p.participant.vars["mitigation_cost"] = ([c(0), c(1000), c(5000), c(10000), c(15000)])
                p.participant.vars["reduced_damage"] = (c(50000), c(46156), c(33516), c(22466), c(15060))
                p.participant.vars["mitigated_before"] = 0
                p.participant.vars["in_scenario"] = False
                p.participant.vars["mitigated_this_scenario"] = 999
                p.participant.vars["mitigation_cost_this_scenario"] = 999
                p.participant.vars["deductible_ecu_this_scenario"] = 999
                p.participant.vars["deductible_ecu_this_scenario"] = 999
                p.participant.vars["deductible_percent"] = 999
                p.participant.vars["previous_floodrisk"] = 999
                p.participant.vars["previous_deductible"] = 999
                p.participant.vars["floodrisk_percent"] = 999
                p.participant.vars["reduced_damage_this_scenario"] = Constants.damage
                p.participant.vars["installment"] = 0
                p.participant.vars["installment+interest"] = 0
                p.participant.vars["loan"] = c(0)
                p.mitigation_cost = 0  # fixme why not 999?

                p.set_treatment()
                p.set_has_treatment()
                p.set_scenarios()

            if self.round_number < len(p.participant.vars["scenarios_list"]) - Constants.useless_rounds + 1:
                p.year = p.participant.vars["years"][self.round_number - 1]
                p.scenario_nr = p.participant.vars["scenarios_list"][self.round_number - 1]
                if p.scenario_nr == 0:
                    p.scenario = p.participant.vars["scenarios"][0]
                else:
                    p.scenario = p.participant.vars["scenarios"][p.scenario_nr - 1]
                    # -1 is to correct for python list index that starts at 0

            p.set_has_treatment()

            if p.scenario == "HH":
                p.high_risk = True
                p.level_deductible = 2
                p.risk = Constants.risk_high
                p.deductible = Constants.deductible_high
            elif p.scenario == "HL":
                p.high_risk = True
                p.level_deductible = 1
                p.risk = Constants.risk_high
                p.deductible = Constants.deductible_low
            elif p.scenario == "LL":
                p.high_risk = False
                p.level_deductible = 1
                p.risk = Constants.risk_low
                p.deductible = Constants.deductible_low
            elif p.scenario == "LH":
                p.high_risk = False
                p.level_deductible = 2
                p.risk = Constants.risk_low
                p.deductible = Constants.deductible_high
            elif p.scenario == "LxL":
                p.high_risk = False
                p.level_deductible = 0
                p.risk = Constants.risk_low
                p.deductible = Constants.deductible_xtra_low
            elif p.scenario == "HxL":
                p.high_risk = True
                p.level_deductible = 0
                p.risk = Constants.risk_high
                p.deductible = Constants.deductible_xtra_low
            elif p.scenario == "risk1":
                p.risk = Constants.risk_1
                p.deductible = 0
            elif p.scenario == "risk2":
                p.risk = Constants.risk_low
                p.deductible = 0
            elif p.scenario == "risk3":
                p.risk = Constants.risk_3
                p.deductible = 0
            elif p.scenario == "risk4":
                p.risk = Constants.risk_4
                p.deductible = 0
            elif p.scenario == "risk5":
                p.risk = Constants.risk_high
                p.deductible = 0
            elif p.scenario == "risk6":
                p.risk = Constants.risk_6
                p.deductible = 0
            else:
                p.risk = 0
                p.deductible = 0

            floodnrs = str(list(random.sample(range(1, 101), p.risk)))
            p.floodnrs = str(["{0:0=3d}".format(value) for value in eval(floodnrs)])

            if "012" in eval(p.floodnrs):
                p.flooded = True
            else:
                p.flooded = False

    def vars_for_admin_report(self):
        vars_admin_list = [[p.participant.code,
                            p.participant.vars["treatment"],
                            p.participant.vars["payoff_scenario1"],
                            p.participant.vars["payoff_scenario2"],
                            p.participant.vars["payoff_scenario3"],
                            p.participant.vars["payoff_scenario4"],
                            p.participant.vars["payoff_scenario5"],
                            p.participant.vars["payoff_scenario6"],
                            p.participant.vars["payoff_time_str"],
                            p.participant.vars["payoff_risk_str"],
                            p.participant.vars["payoff_BRET"],
                            "€" + str('{0:.2f}'.format(p.total_payoff)),
                            p.bigprize]
                           for p in self.get_players()]
        return {'vars_admin_list': vars_admin_list}


class Group(BaseGroup):  # it is an individual decision making game
    pass


class Player(BasePlayer):
    """you first need to set up fields for the variables,
    they are later changed in the set_payoffs and before_session_starts methods"""

    has_insurance = models.BooleanField()
    has_loan = models.BooleanField()
    has_discount = models.BooleanField()

    high_risk = models.BooleanField()
    level_deductible = models.IntegerField()

    reduced_damage_this_scenario = models.CurrencyField()

    understanding_questions_wrong_attempts = models.PositiveIntegerField()
    # number of wrong attempts on understanding questions page

    bomb = models.IntegerField()
    # location of bomb with row/col info
    bomb_row = models.PositiveIntegerField()
    bomb_col = models.PositiveIntegerField()
    # number of collected boxes
    boxes_collected = models.IntegerField()
    # set/scheme of collected boxes
    boxes_scheme = models.LongStringField()

    pay_premium = models.StringField()
    mitigate = models.IntegerField(initial=0)  # is necessary for numpy to have an initial value
    mitigation_cost = models.CurrencyField()
    pay_deductible = models.StringField()
    pay_damage = models.StringField()
    floodnr = models.IntegerField()
    flooded = models.BooleanField()
    buy_house = models.StringField()
    scenario = models.StringField()
    scenario_nr = models.IntegerField()
    year = models.IntegerField()
    pay_installment = models.StringField()
    opened = models.IntegerField(initial=0)
    total_opened = models.IntegerField()
    repay_loan = models.StringField()
    risk = models.IntegerField()
    deductible = models.FloatField()  # because it has decimals
    premium = models.CurrencyField()
    floodnrs = models.LongStringField()
    selected = models.StringField()
    selected2 = models.StringField()
    selected_button = models.StringField()
    bigprize = models.StringField()

    ''' saving payoffs for results '''
    payoff_scenario1 = models.FloatField()
    payoff_scenario2 = models.FloatField()
    payoff_scenario3 = models.FloatField()
    payoff_scenario4 = models.FloatField()
    payoff_scenario5 = models.FloatField()
    payoff_scenario6 = models.FloatField()
    payoff_scenario_risk = models.FloatField()
    payoff_scenario_risk2 = models.FloatField()
    payoff_scenario_time = models.FloatField()
    total_payoff = models.FloatField()

    ''' risk price list '''
    left_side_risk = models.StringField(initial="300")
    right_side_risk = models.StringField()
    switching_point_risk = models.IntegerField()
    left_side_risk2 = models.StringField(initial="-300")
    right_side_risk2 = models.StringField()
    switching_point_risk2 = models.IntegerField()

    ''' time price list '''
    left_side_time = models.StringField(initial="100")
    switching_point_time = models.FloatField()
    # right_side_amounts_time is in Constants

    ''' Bomb risk elicitation task (BRET) '''
    # whether bomb is collected or not
    # store as integer because it's easier for JS
    bomb_BRET = models.IntegerField()

    # location of bomb
    bomb_row_BRET = models.PositiveIntegerField()
    bomb_col_BRET = models.PositiveIntegerField()

    # number of collected boxes
    boxes_collected_BRET = models.IntegerField()

    payoff_BRET = models.FloatField()

    difficult = models.CharField(
        verbose_name="How easy or difficult did you find it to make a choice in the investment game presented to you?",
        choices=["Very easy", "Easy", "Not easy/not difficult", "Difficult", "Very difficult"],
        widget=widgets.RadioSelect,
        default="",
        # note: without this default option, an empty checkbox will be displayed that is initially selected
    )
    explain_strategy = models.TextField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}),
        verbose_name="Could you briefly explain how you made your decisions in the investment game?"
    )
    difficult_text = models.TextField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}),
        verbose_name="Could you describe what made the investment game difficult for you?")
    flood_prone = models.CharField(
        verbose_name="In real life, do you live in a flood-prone area?",
        choices=["Yes, I am certain that I live in a flood-prone area",
                 "I think that I live in a flood-prone area, but I am not sure",
                 "No, I am certain that I do not live in a flood-prone area", "Don't know"],
        widget=widgets.RadioSelect,
        default="")
    climate_change = models.CharField(
        verbose_name="What consequences of climate change for flood risk do you expect at your current residence?",
        choices=["Flood risk will increase", "Flood risk will remain constant",
                 "Flood risk will decrease", "Don't know"],
        widget=widgets.RadioSelect,
        default="")
    availability = models.CharField(
        verbose_name="Do you recall any situations of exceptionally "
                     "high water levels in rivers close to your residence?",
        choices=["Yes, I can recall high water levels", "No, I cannot recall high water levels"],
        widget=widgets.RadioSelect,
        default="")

    think_flooded = models.PositiveIntegerField(
        verbose_name="How many times do you think you were flooded during the game?")

    worry = models.CharField(
        verbose_name="I am worried about the danger of flooding at my current residence")
    flood_risk_perception = models.CharField(
        verbose_name="I expect that I will never experience a flood near my residence")
    trust = models.CharField(
        verbose_name="I am confident that the dikes in the Netherlands are maintained well")
    concern = models.CharField(
        verbose_name="The probability of flooding at my current residence is too low to be concerned about")

    regret1 = models.CharField(
        verbose_name="I felt regret about not investing in protection when a flood occurred in the game")
    regret2 = models.CharField(
        verbose_name="When in a certain year in the game no flood occurred, I felt regret about paying for protection")

    control = models.CharField(
        verbose_name="When I get what I want, it is usually because I am lucky")
    control2 = models.CharField(
        verbose_name="It is not always wise for me to plan too far ahead "
                     "because many things turn out to be a matter of good or bad fortune")
    control3 = models.CharField(
        verbose_name="I believe that there are a number of measures that people can take to reduce their risk")
    control4 = models.CharField(
        verbose_name="I can pretty much determine what will happen in my life")

    #  ###### RISK & TIME PREFERENCES QUALITATIVE ###############
    time_qualitative = models.CharField()
    risk_qualitative = models.CharField()
    perceived_efficacy = models.IntegerField()

    #  ###### DEMOGRAPHICS ###############
    age = models.PositiveIntegerField(verbose_name="How old are you?")
    gender = models.CharField(
        verbose_name="Are you male or female?",
        choices=["Male", "Female"], widget=widgets.RadioSelect,
        default="")
    income = models.CharField(verbose_name="What is your household monthly income (after taxes)?",
                              choices=["Less than €499", "Between  €500 and €999", "Between €1000 and €1499",
                                       "Between €1500 and €1999", "Between €2000 and €2499", "Between €2500 and €2999",
                                       "Between €3000 and €3499", "Between €3500 and €3999", "Between €4000 and €4499",
                                       "Between €4500 and €4999", "€5000 or more", "Don't know", "Rather not say"])
    floor = models.CharField(verbose_name="Please indicate in what kind of property you live:",
                             choices=["House", "Ground floor apartment", "Apartment on 1st floor or higher", "Other"])
    edu = models.CharField(verbose_name="What is the highest level of education you have completed?",
                           choices=["No diploma", "Primary school", "Lower vocational education (VBO, LBO)",
                                    "Lower general secondary education (ULO, MULO, VMBO, MAVO)",
                                    "Lower vocational secondary education (MBO)",
                                    "Higher general secondary education or pre-university education (HAVO, VWO, HBS)",
                                    "Higher vocational and university education (HBO, WO Bachelor)",
                                    "Master's degree (WO Master)", "Doctorate, PhD (Promotie-onderzoek)", "Other"])
    edu_text = models.CharField(verbose_name="In which subject did you major?")
    nationality = models.CharField(verbose_name="What is your nationality?")
    postcode = models.CharField(
        verbose_name="What is your postcode in numbers and letters?",
        blank=True)
    insurance = models.CharField(
        verbose_name="In your Dutch health insurance, what do you think was your deductible (eigen risico) in 2016?",
        choices=["385 euro, the minimum set by the Dutch government",
                 "485 euro, I raised it by 100 euro", "585 euro, I raised it by 200 euro",
                 "685 euro, I raised it by 300 euro", "785 euro, I raised it by 400 euro",
                 "885 euro, I raised it by 500 euro (the maximum)", "I do not know",
                 'I do not have Dutch health insurance'])
    feedback = models.TextField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 130}),
                                verbose_name="This is the end of the survey. "
                                             "If you have comments, you can write them below.",
                                blank=True)
    email = models.CharField(widget=widgets.EmailInput(),
                             verbose_name="In case you are selected for large payment, "
                                          "we will contact you by email to arrange the payment. "
                                          "Please fill in your email address here.",
                             blank=True)
    understand = models.BooleanField(widget=forms.CheckboxInput(),
                                     verbose_name="I understand that submitting no (working) "
                                                  "email address excludes me from the large payment")

    def set_treatment(self):
        sconfig = self.session.config
        combinations = []
        combinations.extend(1 * [[False, False, False, "no insurance"]])
        combinations.extend(1 * [[True, False, False, "baseline"]])
        combinations.extend(1 * [[True, True, True, "loan+discount"]])
        combinations.extend(1 * [[True, True, False, "loan"]])
        combinations.extend(1 * [[True, False, True, "discount"]])

        p = self
        if 'has_insurance' in sconfig:
            p.participant.vars["treatment"] = sconfig.get('treatment')
        else:
            p.participant.vars["combination"] = random.choice(combinations)
            p.participant.vars["treatment"] = p.participant.vars["combination"][3]

    def set_has_treatment(self):
        p = self
        if p.participant.vars["treatment"] == 'no insurance':
            p.has_insurance = False
        else:
            p.has_insurance = True
        if p.participant.vars["treatment"] == "loan" or p.participant.vars["treatment"] == "loan+discount":
            p.has_loan = True
        else:
            p.has_loan = False
        if p.participant.vars["treatment"] == "discount" or p.participant.vars["treatment"] == "loan+discount":
            p.has_discount = True
        else:
            p.has_discount = False

    def set_scenarios(self):
        p = self

        p.participant.vars["years"] = []
        for l in range(1, Constants.num_test_rounds + 1):  # add test scenario years
            p.participant.vars["years"].extend([l])

        p.participant.vars["scenarios_list"] = []
        for l in range(1, Constants.num_test_rounds + 1):  # add nr 0 to signal test scenario years
            p.participant.vars["scenarios_list"].extend([0])

        p.participant.vars["rounds_per_scenario_random"] = []
        for k in range(1, (len(Constants.scenarios) + 1)):
            p.participant.vars["rounds_per_scenario_random"].append(random.randint(Constants.minyears,
                                                                                   Constants.maxyears))
            # set number of years for each scenario

        for i in range(0, len(Constants.scenarios)):
            for j in range(1, (int(p.participant.vars["rounds_per_scenario_random"][i])) + 1):
                p.participant.vars["scenarios_list"].extend([i + 1])  # list of scenario numbers
                p.participant.vars["years"].extend([j])  # list of year numbers

        for l in range(1,
                       Constants.useless_rounds + 1):  # add nr 99 to extend list, prevent out of range
            p.participant.vars["years"].extend([99])
            p.participant.vars["scenarios_list"].extend({99})

        p.participant.vars["total_rounds"] = len(p.participant.vars["scenarios_list"]) - \
                                             Constants.useless_rounds

        if p.has_insurance:
            p.participant.vars["scenarios"] = Constants.scenarios.copy()
            random.shuffle(p.participant.vars["scenarios"])
        else:
            p.participant.vars["scenarios"] = Constants.scenarios_no_insurance.copy()
            random.shuffle(p.participant.vars["scenarios"])

    def save_payoff_bret(self):

        if self.bomb_BRET:
            self.payoff_BRET = 0
        else:
            self.payoff_BRET = float(self.boxes_collected_BRET) * Constants.box_value_BRET

    def set_page_title(self):
        if self.scenario_nr == "0":
            page_title = 'Test scenario'
        elif self.scenario_nr == "1":
            page_title = 'First scenario'
        else:
            page_title = 'New scenario'
        return page_title

    def in_game(self):
        return self.round_number <= len(self.participant.vars["scenarios_list"]) - Constants.useless_rounds

    def in_scenarios(self):
        return self.in_game() and self.participant.vars["in_scenario"]

    def is_new_scenario(self):
        return self.in_game() and self.participant.vars["scenarios_list"][self.round_number - 1] != \
               self.participant.vars["scenarios_list"][self.round_number - 2]

    def in_last_year(self):
        return self.round_number == len(self.participant.vars["years"]) - Constants.useless_rounds

    def _choices_for_field(opts, add_empty=True):
        """Create a list of tuples for choices in a form field."""
        if add_empty:
            choices = [('', '---')]
        else:
            choices = []
        choices.extend([(o, str(o)) for o in opts])
        return choices

    def get_questions_method(self):

        questions = [
            {
                'question': 'What was the flood risk in the test scenario?',
                'options': [str(Constants.risk_1) + " percent",
                            str(Constants.risk_low) + " percent",
                            str(Constants.risk_3) + " percent",
                            str(Constants.risk_4) + " percent",
                            str(Constants.risk_high) + " percent",
                            str(Constants.risk_6) + " percent"],
                'correct': str(self.risk) + " percent",
                'hint': "It is the number of houses that was flooded each year, please check the instructions"
            },
            {
                'question': 'If you are flooded in year 1, what is the flood risk in year 2?',
                'options': ["Less than in year 1", "Flood risk does not change", "More than in year 1"],
                'correct': "Flood risk does not change",
                'hint': 'A flood does not influence the probability of flooding in the next year, '
                        'please check the instructions'
            },
            {
                'question': 'How long are protective investments effective?',
                'options': ['From the moment you implement to the end of the experiment',
                            'From the moment you implement to the end of the scenario',
                            'From the start of the scenario to the end of the scenario',
                            'For one year only'],
                'correct': 'From the moment you implement to the end of the scenario',
                'hint': "The investments are effective in the next years, but the scenarios are independent"

            }
        ]

        if self.has_insurance:
            questions.append(
                {
                    'question': 'What was your deductible (eigen risico) in the test scenario?',
                    'options': [str('{0:.0f}'.format(Constants.deductible_xtra_low*100)) + " percent",
                                str('{0:.0f}'.format(Constants.deductible_low*100)) + " percent",
                                str('{0:.0f}'.format(Constants.deductible_high*100)) + " percent",
                                '50 percent'],
                    'correct': str(self.participant.vars["deductible_percent"]) + " percent",
                    'hint':
                    "It is the part of damage you have to pay yourself, please check the pie-chart in the instructions"

                },
            )
        else:
            questions.append(
                {
                    'question': 'What happens if you are flooded and you did not take protective investments?',
                    'options': ['I have to pay the full damage: ' + str(Constants.damage),
                                'I have to pay a small fee',
                                'I will cry'],
                    'correct': 'I have to pay the full damage: ' + str(Constants.damage),
                    'hint': "Please check the instructions"

                },
            )

        if self.has_discount:
            questions.append(
                {
                    'question': 'What is the benefit of a protective investment?',
                    'options': ["A reduced damage in case of a flood",
                                "A lower premium",
                                "Both reduced damage and a lower premium",
                                "None of the above"],
                    'correct': "Both reduced damage and a lower premium",
                    'hint': "Please check the instructions"

                },
            )

        if self.has_loan:
            questions.append(
                {
                    'question': 'Should you always repay your loan?',
                    'options': ["No, I can refuse to pay the loan cost",
                                "No, if the loan is not fully repaid in the last year, I am lucky",
                                "Yes, I will pay the loan cost in the first 5 years",
                                "Yes, if the loan is not fully repaid in the last year, I will pay the remainder"],
                    'correct': "Yes, if the loan is not fully repaid in the last year, I will pay the remainder",
                    'hint': "Please check the instructions"

                },
            )

        return questions

    def should_pay_installment(self):
        scenarios_list = self.participant.vars["scenarios_list"]
        mitigated_this_scenario = self.participant.vars["mitigated_this_scenario"]
        if not self.has_loan:  # only display in loan
            return False
        elif self.round_number > len(scenarios_list) - Constants.useless_rounds:  # end of game
            return False
        elif self.participant.vars["loan"] >= 0:
            return False
        elif 0 < mitigated_this_scenario < 999 and int(self.year) <= Constants.minyears \
                and self.participant.vars["loan"] < 0:
            # only show if mitigation measures were taken and not in the last year
            return True
        else:
            return False

    def should_pay_final_installment(self):
        if not self.has_loan:  # only display in loan
            return False
        # for test years
        elif self.scenario_nr == '0' and int(self.year) == \
                Constants.num_test_rounds and self.participant.vars["loan"] < 0:
            return True
        # for normal years
        elif int(self.year) == Constants.minyears and self.participant.vars["loan"] < 0:
            # only show if mitigation measures were taken and you are in the last year and if there is still a loan open
            return True
        else:
            return False

    def vars_for_instructions(self):
        deductible_percent = '{0:.0f}'.format(self.deductible*100)
        return{'deductible_percent': deductible_percent}

    def vars_for_risk(self):  # for the gain domain
        vars_for_risk = []
        for i in range(0, len(Constants.left_side_riskA)):
            vars_for_risk.append(['{0:.2f}'.format(Constants.left_side_riskA[i]),
                                  '{0:.2f}'.format(Constants.right_side_riskA[i]),
                                  '{0:.2f}'.format(Constants.left_side_riskB[i]),
                                  '{0:.2f}'.format(Constants.right_side_riskB[i])])
        vars_for_risk2 = [Constants.left_side_riskA, Constants.left_side_riskB,
                          Constants.right_side_riskA, Constants.right_side_riskB]
        return {'vars_for_risk': vars_for_risk, 'vars_for_risk2': vars_for_risk2,
                'left_selected': self.participant.vars["left_selected"],
                'selected_row': self.participant.vars["selected_row_risk"],
                'payoff_risk': self.participant.vars["payoff_risk"]}

    def vars_for_risk3(self):  # for the loss domain
        vars_for_risk3 = []
        for i in range(0, len(Constants.left_side_riskC)):
            vars_for_risk3.append(['{0:.2f}'.format(Constants.left_side_riskC[i]),
                                   '{0:.2f}'.format(Constants.right_side_riskC[i]),
                                  '{0:.2f}'.format(Constants.left_side_riskD[i]),
                                   '{0:.2f}'.format(Constants.right_side_riskD[i])])
        vars_for_risk4 = [Constants.left_side_riskC, Constants.left_side_riskD,
                          Constants.right_side_riskC, Constants.right_side_riskD]
        return {'vars_for_risk3': vars_for_risk3, 'vars_for_risk4': vars_for_risk4,
                'left_selected2': self.participant.vars["left_selected2"],
                'selected_row2': self.participant.vars["selected_row_risk2"],
                'payoff_risk2': self.participant.vars["payoff_risk2"]}

    def vars_for_earnings(self):
        input = False
        return {
            'input':            input,
            'reset':            True,
            'num_rows':         Constants.num_rows,
            'num_cols':         Constants.num_cols,
            'box_width':        Constants.box_width,
            'box_height':       Constants.box_height,
            'box_value':        Constants.box_value,
            'total_earnings':   Constants.total_earnings,
            'boxes_total':      Constants.num_rows * Constants.num_cols,
            'boxes_collected':  self.boxes_collected,
        }

    def vars_for_BRET(self):
        input_BRET = not Constants.devils_game_BRET if not Constants.dynamic_BRET else False
        return {
            'input': input_BRET,
            'reset': False,
            'random': Constants.random_BRET,
            'dynamic': Constants.dynamic_BRET,
            'num_rows': Constants.num_rows_BRET,
            'num_cols': Constants.num_cols_BRET,
            'feedback': Constants.feedback_BRET,
            'undoable': Constants.undoable_BRET,
            'box_width': Constants.box_width_BRET,
            'box_height': Constants.box_height_BRET,
            'time_interval': Constants.time_interval_BRET,
            'box_value_BRET': Constants.box_value_BRET
        }

    def vars_for_scenarios(self):
        participant = self.participant
        return {'opened': self.opened, 'scenario_nr': self.scenario_nr, 'year': self.year,
                'mitigate': self.mitigate, 'mitigated_before': participant.vars["mitigated_before"],
                'mitigated_this_scenario': participant.vars["mitigated_this_scenario"],
                'premium': participant.vars['premium'], 'insurance': self.has_insurance,
                'deductible': self.deductible,
                'deductible_ecu_this_scenario': participant.vars["deductible_ecu_this_scenario"],
                'deductible_percent': participant.vars["deductible_percent"],
                'previous_deductible': participant.vars["previous_deductible"],
                'previous_floodrisk': participant.vars["previous_floodrisk"],
                'premium_discounted': participant.vars["premium_discounted"],
                'the_year': participant.vars["years"][self.round_number - 1],
                'opened_total': self.participant.vars["opened_instructions"],
                'years_list': participant.vars["years"],
                'magiclist': participant.vars["rounds_per_scenario_random"],
                'scenarios_list': participant.vars["scenarios_list"],
                'scenario': self.scenario,
                'reduced_damage_this_scenario': participant.vars["reduced_damage_this_scenario"],
                'loan': self.participant.vars["loan"]
                }

    def vars_for_invest(self):
        participant = self.participant
        installment1 = participant.vars["mitigation_cost"][1] / Constants.num_installments
        installment2 = participant.vars["mitigation_cost"][2] / Constants.num_installments
        installment3 = participant.vars["mitigation_cost"][3] / Constants.num_installments
        installment4 = participant.vars["mitigation_cost"][4] / Constants.num_installments
        return {'treatment': participant.vars["treatment"],
                'installment1': installment1, 'installment2': installment2,
                'installment3': installment3,  'installment4': installment4,
                'mitigation_cost0': participant.vars["mitigation_cost"][0],
                'mitigation_cost1': participant.vars["mitigation_cost"][1],
                'mitigation_cost2': participant.vars["mitigation_cost"][2],
                'mitigation_cost3': participant.vars["mitigation_cost"][3],
                'mitigation_cost4': participant.vars["mitigation_cost"][4],
                'loan': participant.vars["loan"],
                'premium_discounted0': participant.vars["premium_discounted"][0],
                'premium_discounted1': participant.vars["premium_discounted"][1],
                'premium_discounted2': participant.vars["premium_discounted"][2],
                'premium_discounted3': participant.vars["premium_discounted"][3],
                'premium_discounted4': participant.vars["premium_discounted"][4],
                'reduced_deductible0': participant.vars["reduced_deductible"][0],
                'reduced_deductible1': participant.vars["reduced_deductible"][1],
                'reduced_deductible2': participant.vars["reduced_deductible"][2],
                'reduced_deductible3': participant.vars["reduced_deductible"][3],
                'reduced_deductible4': participant.vars["reduced_deductible"][4],
                'mitigation_cost_this_scenario': participant.vars["mitigation_cost_this_scenario"],
                'reduced_damage0': participant.vars["reduced_damage"][0],
                'reduced_damage1': participant.vars["reduced_damage"][1],
                'reduced_damage2': participant.vars["reduced_damage"][2],
                'reduced_damage3': participant.vars["reduced_damage"][3],
                'reduced_damage4': participant.vars["reduced_damage"][4],
                'reduced_damage_this_scenario': participant.vars["reduced_damage_this_scenario"],
                'installment': participant.vars["installment"], 'income': Constants.income
                }

    def vars_for_invest2(self):
        vars_for_template = self.vars_for_invest()
        difference1 = self.participant.vars["mitigation_cost"][1] - \
            self.participant.vars["mitigation_cost_this_scenario"]
        difference2 = self.participant.vars["mitigation_cost"][2] - \
            self.participant.vars["mitigation_cost_this_scenario"]
        difference3 = self.participant.vars["mitigation_cost"][3] - \
            self.participant.vars["mitigation_cost_this_scenario"]
        difference4 = self.participant.vars["mitigation_cost"][4] - \
            self.participant.vars["mitigation_cost_this_scenario"]
        vars_for_template.update({'difference1': difference1,
                                  'difference2': difference2,
                                  'difference3': difference3,
                                  'difference4': difference4})
        return vars_for_template

    def vars_for_additional_payment(self):
        participant = self.participant
        payoff_additional = 0
        if self.participant.vars["selected_additional"] == 2:
            payoff_additional = participant.vars["payoff_risk"]
        elif self.participant.vars["selected_additional"] == 1:
            payoff_additional = participant.vars["payoff_risk2"]
        elif self.participant.vars["selected_additional"] == 3:
            payoff_additional = self.payoff_BRET

        self.participant.vars["payoff_additional"] = payoff_additional
        payoff_risk = "€" + str(participant.vars["payoff_risk"])
        payoff_risk2 = "€" + str(participant.vars["payoff_risk2"])
        payoff_BRET = "€" + str(self.payoff_BRET)

        return {'payoff_additional': payoff_additional, 'payoff_risk': payoff_risk,
                'payoff_risk2': payoff_risk2, 'payoff_BRET': payoff_BRET,
                'selected_additional': self.participant.vars["selected_additional"]
                }

    def vars_for_payment(self):
        participant = self.participant
        payoff1 = max(c(participant.vars["payoff_scenario1"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff2 = max(c(participant.vars["payoff_scenario2"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff3 = max(c(participant.vars["payoff_scenario3"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff4 = max(c(participant.vars["payoff_scenario4"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff5 = max(c(participant.vars["payoff_scenario5"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff6 = max(c(participant.vars["payoff_scenario6"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff_time = c(participant.vars["payoff_time"]).to_real_world_currency(self.session)*100
        payoff_small_1 = payoff1*0.01
        payoff_small_2 = payoff2*0.01
        payoff_small_3 = payoff3*0.01
        payoff_small_4 = payoff4*0.01
        payoff_small_5 = payoff5*0.01
        payoff_small_6 = payoff6*0.01
        if float(participant.vars["selected_scenario_time"]) >= float(participant.vars["switching_point_time"]):
            payoff_time = str(payoff_time) + " in 12 months"

        return {'payoff_small_1': payoff_small_1, 'payoff_small_2': payoff_small_2, 'payoff_small_3': payoff_small_3,
                'payoff_small_4': payoff_small_4, 'payoff_small_5': payoff_small_5, 'payoff_small_6': payoff_small_6,
                'payoff1': payoff1, 'payoff2': payoff2, 'payoff3': payoff3, 'payoff4': payoff4,
                'payoff_scenario1': participant.vars["payoff_scenario1"],
                'payoff_scenario2': participant.vars["payoff_scenario2"],
                'payoff_scenario3': participant.vars["payoff_scenario3"],
                'payoff_scenario4': participant.vars["payoff_scenario4"],
                'payoff_scenario5': participant.vars["payoff_scenario5"],
                'payoff_scenario6': participant.vars["payoff_scenario6"],
                'participation_fee': self.session.config['participation_fee'],
                'selected_scenario': self.participant.vars["selected_scenario"],
                'selected': self.selected
                }

    def vars_for_payment_prize(self):
        participant = self.participant
        # max to make sure participants do not get a negative payment
        payoff1 = max(c(participant.vars["payoff_scenario1"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff2 = max(c(participant.vars["payoff_scenario2"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff3 = max(c(participant.vars["payoff_scenario3"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff4 = max(c(participant.vars["payoff_scenario4"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff5 = max(c(participant.vars["payoff_scenario5"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff6 = max(c(participant.vars["payoff_scenario6"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff_time = "€" + str(participant.vars["payoff_time"])
        payoff_BRET = "€" + str(self.payoff_BRET)
        participant.vars["payoff_BRET"] = payoff_BRET
        payoff_risk = "€" + str(participant.vars["payoff_risk"])
        payoff_risk2 = "€" + str(participant.vars["payoff_risk2"])

        if float(participant.vars["selected_scenario_time"]) >= float(participant.vars["switching_point_time"]):
            payoff_time += " in 12 months"
        else:
            payoff_time += " now"

        if self.participant.vars["selected_pref"] == 1:
            payoff_if_selected = payoff1
        elif self.participant.vars["selected_pref"] == 2:
            payoff_if_selected = payoff2
        elif self.participant.vars["selected_pref"] == 3:
            payoff_if_selected = payoff3
        elif self.participant.vars["selected_pref"] == 4:
            payoff_if_selected = payoff4
        elif self.participant.vars["selected_pref"] == 5:
            payoff_if_selected = payoff5
        elif self.participant.vars["selected_pref"] == 6:
            payoff_if_selected = payoff6
        elif self.participant.vars["selected_pref"] == 7:
            payoff_if_selected = payoff_time
        else:
            payoff_if_selected = 0
        self.bigprize = str(payoff_if_selected)
        self.total_payoff = float(participant.vars["payoff_small"] + \
            self.session.config["participation_fee"] + participant.vars["payoff_additional"])
        payoff_small = participant.vars["payoff_small"]
        payoff_additional = "€" + str(participant.vars["payoff_additional"])

        return {'participation_fee': self.session.config['participation_fee'],
                'selected_pref': self.participant.vars["selected_pref"],
                'payoff1': str(payoff1) + " now",
                'payoff2': str(payoff2) + " now",
                'payoff3': str(payoff3) + " now",
                'payoff4': str(payoff4) + " now",
                'payoff5': str(payoff5) + " now",
                'payoff6': str(payoff6) + " now",
                'payoff_small': payoff_small,
                'payoff_time': payoff_time,
                'selected_button': self.selected_button,
                'total_payoff': "€" + str('{0:.2f}'.format(self.total_payoff)),
                'payoff_if_selected': payoff_if_selected,
                'bigprize': self.bigprize,
                'payoff_additional': payoff_additional
                }

    def opened_instructions(self):
        self.participant.vars["opened_instructions"] += self.opened

    def buy_house_method(self):
        if self.buy_house == "bought":
            self.participant.vars["cumulative_payoff"] -= Constants.house_value
            self.buy_house = "done"

    def earn_money(self):
        self.participant.vars["cumulative_payoff"] = c(Constants.boxes_required * Constants.box_value)

    def get_income(self):
        self.participant.vars["cumulative_payoff"] += Constants.income

    def pay_installment_method(self):
        if self.pay_installment == "paid_installment":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["installment+interest"]
            self.participant.vars["loan"] += self.participant.vars["installment"]

    def pay_final_installment_method(self):
        if self.repay_loan == "repaid_loan":
            self.participant.vars["cumulative_payoff"] += self.participant.vars["loan"]
            self.participant.vars["loan"] = 0

    def pay_premium_method(self):
        if self.pay_premium == "paid_premium":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["premium"]

    def pay_after_flood(self):
        if self.pay_damage == "paid_damage":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["reduced_damage_this_scenario"]
        elif self.pay_deductible == "paid_deductible":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["deductible_ecu_this_scenario"]

    def pay_mitigation_method(self):
        if 0 < self.mitigate < 999:
            self.participant.vars["mitigation_cost_this_scenario"] = \
                self.participant.vars["mitigation_cost"][self.mitigate]
            self.participant.vars["mitigated_before"] = self.year
            if not self.has_loan:
                self.participant.vars["cumulative_payoff"] -= self.participant.vars["mitigation_cost_this_scenario"]
            elif self.has_loan:
                self.participant.vars["loan"] = - self.participant.vars["mitigation_cost_this_scenario"]
                self.participant.vars["installment"] = \
                    self.participant.vars["mitigation_cost_this_scenario"]/Constants.num_installments
                self.participant.vars["installment+interest"] = \
                    self.participant.vars["installment"]*(1+Constants.interest/100)
            self.participant.vars["mitigated_this_scenario"] = self.mitigate
        elif self.mitigate == 0:
            self.participant.vars["mitigation_cost_this_scenario"] = \
                self.participant.vars["mitigation_cost"][self.mitigate]  # is zero
            self.participant.vars["mitigated_this_scenario"] = 0

    def pay_mitigation_more(self):
        if 0 < self.mitigate < 999:
            old_mitigation_cost = self.participant.vars["mitigation_cost_this_scenario"]
            self.participant.vars["mitigation_cost_this_scenario"] = \
                self.participant.vars["mitigation_cost"][self.mitigate]
            self.participant.vars["mitigated_before"] = self.year
            self.participant.vars["mitigate_more"] = \
                self.participant.vars["mitigation_cost_this_scenario"] - old_mitigation_cost
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["mitigate_more"]

            if self.has_loan and self.mitigate > self.participant.vars["mitigated_this_scenario"]:
                self.participant.vars["loan"] -= self.participant.vars["mitigate_more"]
                self.participant.vars["installment"] = (-self.participant.vars["loan"])/Constants.num_installments
                self.participant.vars["installment+interest"] = \
                    self.participant.vars["installment"]*(1+Constants.interest/100)

            self.participant.vars["mitigated_this_scenario"] = self.mitigate

        elif self.mitigate == 0:
            self.participant.vars["mitigation_cost_this_scenario"] = \
                self.participant.vars["mitigation_cost"][self.mitigate]  # is zero

    def new_scenario_method(self):
        for m in range(0, 5):
            self.participant.vars["premium_discounted"][m] = c(
                (1 - self.deductible) * float(self.risk) * 0.01 * self.participant.vars["reduced_damage"][m])
            self.participant.vars["reduced_deductible"][m] = \
                self.participant.vars["reduced_damage"][m] * self.deductible
        # after start of new scenario set premium to premium with 0 discount, did not work in reset payoffs
        self.participant.vars["premium"] = self.participant.vars["premium_discounted"][0]
        self.participant.vars["previous_deductible"] = self.participant.vars["deductible_percent"]
        self.participant.vars["deductible_percent"] = int(100 * self.deductible)
        # int to get rid of the decimals of the float that is p.deductible
        self.participant.vars["deductible_ecu_this_scenario"] = Constants.damage * self.deductible  # initially
        self.participant.vars["previous_floodrisk"] = self.participant.vars["floodrisk_percent"]
        self.participant.vars["floodrisk_percent"] = self.risk
        self.participant.vars["cumulative_payoff"] = Constants.initial_endowment
        # resetting cumulative payoff to initial endowment
        self.participant.vars["mitigated_this_scenario"] = 999  # new scenario
        self.participant.vars["in_scenario"] = True
        self.participant.vars["mitigated_before"] = 0
        self.participant.vars["loan"] = 0
        self.participant.vars["installment"] = 0
        self.participant.vars["installment+interest"] = 0
        self.participant.vars["reduced_damage_this_scenario"] = Constants.damage
        # set page title:
        self.participant.vars["page_title"] = self.set_page_title()

    def set_payoff(self):

        if not self.mitigate:  # set premium for first year
            self.participant.vars["premium"] = c((1 - self.deductible) * float(self.risk) * 0.01 * Constants.damage)
        elif self.mitigate > 0:  # mitigated this scenario
            if not self.has_discount:
                self.participant.vars["premium"] = c((1 - self.deductible) * float(self.risk) * 0.01 * Constants.damage)
            elif self.has_discount:
                self.participant.vars["premium"] = self.participant.vars["premium_discounted"][self.mitigate]

        ''' set mitigation cost and reduced damage '''
        if 0 < self.mitigate <= 4:
            self.participant.vars["reduced_damage_this_scenario"] = \
                self.participant.vars["reduced_damage"][self.mitigate]
            self.reduced_damage_this_scenario = self.participant.vars["reduced_damage"][self.mitigate]
            self.mitigation_cost = self.participant.vars["mitigation_cost"][self.mitigate]
        else:
            self.mitigation_cost = 0  # initially
            self.participant.vars["reduced_damage_this_scenario"] = Constants.damage
            self.reduced_damage_this_scenario = Constants.damage
        self.participant.vars["deductible_ecu_this_scenario"] = \
            self.participant.vars["reduced_damage_this_scenario"] * self.deductible

    def save_payoff(self):
        if self.year == Constants.maxyears and self.scenario_nr != "4":
            self.participant.vars["payoff_scenario{}".format(self.scenario_nr)] = \
                self.participant.vars["cumulative_payoff"]
        elif self.year == Constants.maxyears and self.scenario_nr == "4":  # save last scenario
            self.participant.vars["payoff_scenario{}".format(self.scenario_nr)] = \
                self.participant.vars["cumulative_payoff"]

    def save_payoff_risk(self):
        self.participant.vars["switching_point_risk"] = self.switching_point_risk
        if self.participant.vars["selected_row_risk"] >= self.switching_point_risk:  # option B
            if self.participant.vars["left_selected"]:  # left B
                self.participant.vars["payoff_risk"] = \
                    '{0:.2f}'.format(Constants.left_side_riskB[self.participant.vars["selected_row_risk"]-1])
            else:  # right B
                self.participant.vars["payoff_risk"] = \
                    '{0:.2f}'.format(Constants.right_side_riskB[self.participant.vars["selected_row_risk"]-1])
        else:  # option A
            if self.participant.vars["left_selected"]:  # left A
                self.participant.vars["payoff_risk"] = \
                    '{0:.2f}'.format(Constants.left_side_riskA[self.participant.vars["selected_row_risk"]-1])
            else:  # right A
                self.participant.vars["payoff_risk"] = \
                    '{0:.2f}'.format(Constants.right_side_riskA[self.participant.vars["selected_row_risk"]-1])

    def save_payoff_risk2(self):
        self.participant.vars["switching_point_risk2"] = self.switching_point_risk2
        if self.participant.vars["selected_row_risk2"] >= self.switching_point_risk2:  # option D
            if self.participant.vars["left_selected2"]:  # left D
                self.participant.vars["payoff_risk2"] = '{0:.2f}'.format(Constants.left_side_riskD
                                                                         [self.participant.vars["selected_row_risk2"]-1]
                                                                         + Constants.endowment_loss)
            else:  # right D
                self.participant.vars["payoff_risk2"] = '{0:.2f}'.format(Constants.right_side_riskD
                                                                         [self.participant.vars["selected_row_risk2"]-1]
                                                                         + Constants.endowment_loss)
        else:  # option C
            if self.participant.vars["left_selected2"]:  # left C
                self.participant.vars["payoff_risk2"] = '{0:.2f}'.format(Constants.left_side_riskC
                                                                         [self.participant.vars["selected_row_risk2"]-1]
                                                                         + Constants.endowment_loss)
            else:  # right C
                self.participant.vars["payoff_risk2"] = '{0:.2f}'.format(Constants.right_side_riskC
                                                                         [self.participant.vars["selected_row_risk2"]-1]
                                                                         + Constants.endowment_loss)

    def save_payoff_time(self):

        if self.participant.vars["selected_scenario_time"] < self.switching_point_time:  # left side
            self.participant.vars["payoff_time"] = self.left_side_time
        else:
            self.participant.vars["payoff_time"] = self.participant.vars["selected_scenario_time"]
        self.participant.vars["switching_point_time"] = self.switching_point_time

    def save_final_payoffs(self):

        self.payoff_scenario1 = float(self.participant.vars["payoff_scenario1"])
        self.payoff_scenario2 = float(self.participant.vars["payoff_scenario2"])
        self.payoff_scenario3 = float(self.participant.vars["payoff_scenario3"])
        self.payoff_scenario4 = float(self.participant.vars["payoff_scenario4"])
        self.payoff_scenario5 = float(self.participant.vars["payoff_scenario6"])
        self.payoff_scenario6 = float(self.participant.vars["payoff_scenario6"])
        self.payoff_scenario_risk = float(self.participant.vars["payoff_risk"])
        self.payoff_scenario_risk2 = float(self.participant.vars["payoff_risk2"])
        self.payoff_scenario_time = float(self.participant.vars["payoff_time"])

        if self.participant.vars["selected_scenario"] == 1:
            self.participant.payoff = self.payoff_scenario1*0.01
            self.participant.vars["payoff_small"] = max(c(self.payoff_scenario1).to_real_world_currency(self.session)*0.01,
                                                        c(0).to_real_world_currency(self.session))
        elif self.participant.vars["selected_scenario"] == 2:
            self.participant.payoff = self.payoff_scenario2*0.01
            self.participant.vars["payoff_small"] = max(c(self.payoff_scenario2).to_real_world_currency(self.session)*0.01,
                                                        c(0).to_real_world_currency(self.session))
        elif self.participant.vars["selected_scenario"] == 3:
            self.participant.payoff = self.payoff_scenario3*0.01
            self.participant.vars["payoff_small"] = max(c(self.payoff_scenario3).to_real_world_currency(self.session)*0.01,
                                                        c(0).to_real_world_currency(self.session))
        elif self.participant.vars["selected_scenario"] == 4:
            self.participant.payoff = self.payoff_scenario4*0.01
            self.participant.vars["payoff_small"] = max(c(self.payoff_scenario4).to_real_world_currency(self.session)*0.01,
                                                        c(0).to_real_world_currency(self.session))
        elif self.participant.vars["selected_scenario"] == 5:
            self.participant.payoff = self.payoff_scenario5*0.01
            self.participant.vars["payoff_small"] = max(c(self.payoff_scenario5).to_real_world_currency(self.session)*0.01,
                                                        c(0).to_real_world_currency(self.session))
        elif self.participant.vars["selected_scenario"] == 6:
            self.participant.payoff = self.payoff_scenario6*0.01
            self.participant.vars["payoff_small"] = max(c(self.payoff_scenario6).to_real_world_currency(self.session)*0.01,
                                                        c(0).to_real_world_currency(self.session))
