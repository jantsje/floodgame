# floodgame

This application is the first version of the **Floodgame**. Participants first face a real effort task (*Earnings*) to earn ECU. From this starting capital, they buy a virtual house, that is prone to flood risk. Participants play 6 scenarios of 12 rounds each, with different flood probabilities and deductibles per scenario. At the start of each scenario, the starting capital is reset. In each round, participants are informed about the risk and the damage of the previous round. The *Invest* page offers five discrete investment levels with accompanying benefits. 

The **Floodgame** allows for a test scenario to familiarize participants with the game, followed by understanding questions (based on [otreeutils](https://github.com/WZBSocialScienceCenter/otreeutils)), conditional on treatment. The instructions are available throughout the game in a pop-up screen [Bootstrap modal](https://getbootstrap.com/docs/4.0/components/modal/). A JavaScript counter tracks the number of times the instructions are opened, to correct for inattentive subjects. 

After the **Floodgame**, several extra tasks are implemented to gather data on risk preferences, time preferences and other behavioral characteristics. Risk preferences are measured with price lists in the gain and loss domain (Drichoutis and Lusk, 2016) and a static version of the [Bomb Risk Elicitation Task](https://github.com/felixholzmeister/bret). Time preferences are measured with a price list (Falk et al, 2016). The final pages of the game implement a short survey. 

The experiment was conducted in the CREED lab of the University of Amsterdam in November 2017 with 361 subjects.

## Published paper
Mol, J. M., Botzen, W. J. W., & Blasch, J. E. (2020). Risk reduction in compulsory disaster insurance: Experimental evidence on moral hazard and financial incentives. Journal of Behavioral and Experimental Economics, 84(February), 101500. https://doi.org/10.1016/j.socec.2019.101500

## Installation
To install the app to your local oTree directory, copy the folder 'floodgame' to your oTree Django project and extend the session configuraations in your ```settings.py``` at the root of the oTree directory:
```
SESSION_CONFIGS = [

    dict(
        name= 'floodgame',
        display_name="Floodgame lab",
        num_demo_participants=1,
        app_sequence=['floodgame'],
)
]
```
## Treatments
* No Insurance
* Insurance Baseline
* Discount (offers discount on insurance premium)
* Loan (offers loan  with 10 installments to spread investment costs)
* Loan + Discount (combination of loan and discount treatments)

## Issues
Note that this is a modified version. The original experiment was  conducted using oTree v1. Issues after updating to v2:
* progressbar does not account for the pages of the final survey
* *Bomb Risk Elicitation Task* does not work if *Earnings* task is enabled. 
* *AdminReport* calls for old variables, leading to an error.
