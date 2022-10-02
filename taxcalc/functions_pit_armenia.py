"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


"Calculation of annual maximum limit for social payment at low rate"
@iterate_jit(nopython=True)
def cal_max_annual_income_lowssc(max_income_pm_low_ssc, max_annual_income_low_ssc):
   max_annual_income_low_ssc = max_income_pm_low_ssc*12
   return (max_annual_income_low_ssc)

"Calculation of monthly cap for social payment - (15 times the minimum wage per pm)"
@iterate_jit(nopython=True)
def cal_max_annual_income_ssc(min_wage_pm, max_annual_income_ssc):
   max_annual_income_ssc = (min_wage_pm*15)
   return (max_annual_income_ssc)

"Calculation of base for payment of social security contribution"
@iterate_jit(nopython=True)
def cal_base_social(salary, civil_contract, base_social):
    base_social=salary + civil_contract
    return (base_social)

"Calculation of Social payments"
@iterate_jit(nopython=True)
def cal_ssc_fun(social_fee, base_social, min_income_for_ssc,max_annual_income_low_ssc,max_annual_income_ssc,rate_sp_1,rate_sp_2, cal_ssc):    
    """ Note:  
            Hint: Please note, that the social security scheme is mandatory for all the taxpayers born after 1974, and it is voluntary for others born before 1974.
            
             1.Base for social payment :
              
              The base for calculation of the social payment is the basic income, which is salary and other payments equal thereto which are subject to taxation by income tax.
              The Employer, as a tax agent, is obliged to withhold the amount of social payment as well as submit monthly personalized reports to the tax authorities on calculated income, amounts of tax and social payments withheld from individuals within the terms established by the RA Tax Code.
              The social payment rates are as follows:
                  
                     Basic monthly Income*             Social payment
             2021   Up to AMD 500,000                   3.5 %
                    More than AMD 500,000              10 % on income above 500000
                     
             2022  Up to AMD 500,000                     4.5 %
                   More than AMD 500,000                10 % on income above 500000     
                     
             2023  Up to AMD 500,000                     5 %
                   More than AMD 500,000                10 % on income above 500000            
                     
              Starting 01.07.2020 the maximum monthly threshold of the calculation basis for social payment is AMD 1,020,000. This means that the maximum amount of the Social Payment in 2021 will be capped at AMD.69,500. (Source https://home.kpmg/xx/en/home/insights/2021/07/armenia-thinking-beyond-borders.html)
                
              
              2.Rule for calculation Social security contributions for 2021 :
               
              Individuals born after 1 January 1974 must make social security payments at a rate of 3.5 % on their salary and equivalent income and income from the provision of services, in a case where the income is less than or equal to AMD 500,000. 
              If the salary and equivalent income or income from the provision of services is between AMD 500,000 and AMD 1,020,000 (the latter amount is calculated as 15 times the minimum monthly salary (AMD 68,000)), 
              the social security contribution is calculated as 10% on the gross income minus AMD 32,500. Where the relevant income is equal to or exceeds AMD 1,020,000, the social security contribution is calculated 
              as 10% on AMD 1,020,000 minus AMD 32,500. Individuals have the right to waive the maximum threshold for social security payments.(Source:https://www2.deloitte.com/content/dam/Deloitte/global/Documents/Tax/dttl-tax-armeniahighlights-2021.pdf)
    
    """
    
    if social_fee ==0 and base_social> 1:
        calc_ssc = 0
    elif base_social <= min_income_for_ssc:
        calc_ssc = 0.
    elif (base_social >=min_income_for_ssc) and (base_social <= max_annual_income_low_ssc):
       calc_ssc = base_social * rate_sp_1  #policy is to pay ssc on entire base if it exceeds threshold
    #elif (base_social >=min_income_for_ssc) and (base_social <= max_annual_income_low_ssc):
        #calc_ssc = (base_social - min_income_for_ssc)  * rate_sp_1  #policy is to pay ssc on portion above min threshold 
    elif (base_social >=max_annual_income_low_ssc) and (base_social <=max_annual_income_ssc): 
       calc_ssc =  (max_annual_income_low_ssc * rate_sp_1) +  max(0., (base_social - max_annual_income_low_ssc)*rate_sp_2)
    elif base_social > max_annual_income_ssc:
       calc_ssc = (max_annual_income_low_ssc * rate_sp_1) +  max(0., (max_annual_income_ssc - max_annual_income_low_ssc)*rate_sp_2)
    return  (cal_ssc)



"Calculation for tax base for income from wages"
@iterate_jit(nopython=True)
def cal_tti_wage(salary, civil_contract,other_income,deduction,tti_wages):
    tti_wages=(salary + civil_contract + other_income) - deduction
    return (tti_wages)

"Calculation for tax base for income from royalty"
@iterate_jit(nopython=True)
def cal_tti_royalty(royalty, tti_royalty):
    tti_royalty=royalty
    return (tti_royalty)

"Calculation for tax base for income from interest"
@iterate_jit(nopython=True)
def cal_tti_interest(interest, tti_interest):
    tti_interest=interest
    return (tti_interest)

"Calculation for tax base for income from rent"
@iterate_jit(nopython=True)
def cal_tti_rent(rent, tti_rent):
    tti_rent=rent
    return (tti_rent)

"Calculation for tax base for income from rent higher than AMD 60 mn"
@iterate_jit(nopython=True)
def cal_tti_rent_high(rent_high, tti_rent_high):
    tti_rent_high=rent_high
    return (tti_rent_high)

"Calculation for tax base for income from sale of property by developer"
@iterate_jit(nopython=True)
def cal_tti_sale_prop_dev(sale_prop_dev, tti_sale_prop_dev):
    tti_sale_prop_dev=sale_prop_dev
    return (tti_sale_prop_dev)

"Calculation for tax base for income from sale of property by other than developer"
@iterate_jit(nopython=True)
def cal_tti_sale_prop(sale_prop, tti_sale_prop):
    tti_sale_prop=sale_prop
    return (tti_sale_prop)

"Calculation for tax base for income from sale of securities"
@iterate_jit(nopython=True)
def cal_tti_stocks(stocks, tti_stocks):
    tti_stocks=stocks
    return (tti_stocks)

"Calculation for tax base for income from dividends"
@iterate_jit(nopython=True)
def cal_tti_dividends(dividends, tti_dividends):
    tti_dividends=dividends
    return (tti_dividends)

"Calculation for total tax base from all income sources (except dividends) taxed at 10%"
@iterate_jit(nopython=True)
def cal_tti_all(tti_wages, tti_royalty, tti_interest, tti_rent, tti_rent_high, tti_sale_prop, tti_sale_prop_dev, tti_stocks):
    tti_all=tti_wages+tti_royalty+tti_interest+tti_rent+tti_rent_high+tti_sale_prop+tti_sale_prop_dev+tti_stocks
    return (tti_all)

"Calculation for gross total income from all income sources before deductions"
@iterate_jit(nopython=True)
def cal_tot_gross_inc(tti_wages, deduction, tti_royalty, tti_interest, tti_rent, tti_rent_high, tti_sale_prop, tti_sale_prop_dev, tti_stocks, tti_dividends, total_gross_income):
    total_gross_income=tti_wages+tti_royalty+tti_interest+tti_rent+tti_rent_high+tti_sale_prop+tti_sale_prop_dev+tti_stocks+tti_dividends+deduction
    return (total_gross_income)

"Calculation for PIT from salaires,civil contracts, other income"
@iterate_jit(nopython=True)
def cal_pit_wages(tti_wages,rate1,rate2,rate3,rate4,tbrk1,tbrk2,tbrk3,pit_wages):
    """
        Note: 
             From 1 January 2020, a FLAT RATE of income tax on salaries was established, which will gradually decrease to 20 percent by 2023: 
      
             Period                                                         Income tax rate
          From 1 January 2020                                                    23 %
          From 1 January 2021                                                    22 %
          From 1 January 2022                                                    21%
          From 1 January 2023                                                    20 %
        
        (Source https://home.kpmg/xx/en/home/insights/2021/07/armenia-thinking-beyond-borders.html)
        
            
    """   
    
    pit_wages = (rate1 * min(tti_wages, tbrk1) +
                            rate2 * min(tbrk2 - tbrk1, max(0., tti_wages - tbrk1)) +
                            rate3 * min(tbrk3 - tbrk2, max(0., tti_wages - tbrk2)) +
                            rate4 * max(0., tti_wages - tbrk3))
    
        
    return (pit_wages)
    

                       
"Calculation for total tax from royalty "
@iterate_jit(nopython=True)
def cal_pit_royalty(tti_royalty, rate_royalty, pit_royalty):
    pit_royalty = tti_royalty * rate_royalty
    return (pit_royalty)

"Calculation for total tax from interest "
@iterate_jit(nopython=True)
def cal_pit_interest(tti_interest, rate_interest, pit_interest):
    pit_interest = tti_interest * rate_interest
    return (pit_interest)

"Calculation for total tax from rent"
@iterate_jit(nopython=True)
def cal_pit_rent(tti_rent, rate_rent, pit_rent):
    pit_rent = tti_rent * rate_rent
    return (pit_rent)

"Calculation for total tax from rent higher than AMD 60 mn"
@iterate_jit(nopython=True)
def cal_pit_rent_high(tti_rent_high, rate_rent_high, pit_rent_high):
    pit_rent_high = tti_rent_high * rate_rent_high
    return (pit_rent_high)

"Calculation for total tax from sale of property by developer"
@iterate_jit(nopython=True)
def cal_pit_sale_prop_dev(tti_sale_prop_dev, rate_sale_prop_dev, pit_sale_prop_dev):
    pit_sale_prop_dev = tti_sale_prop_dev * rate_sale_prop_dev
    return (pit_sale_prop_dev)

"Calculation for total tax from sale of property by other than developer"
@iterate_jit(nopython=True)
def cal_pit_sale_prop(tti_sale_prop, rate_sale_prop, pit_sale_prop):
    pit_sale_prop = tti_sale_prop * rate_sale_prop
    return (pit_sale_prop)

"Calculation for total tax from sale of cars"
@iterate_jit(nopython=True)
def cal_pit_cars(tax_cars):
    pit_cars = tax_cars
    return (pit_cars)

"Calculation for total tax from sale of securities"
@iterate_jit(nopython=True)
def cal_pit_stocks(tti_stocks, rate_stocks, pit_stocks):
    pit_stocks = tti_stocks * rate_stocks
    return (pit_stocks)

"Calculation for total tax from dividends"
@iterate_jit(nopython=True)
def cal_pit_dividends(tti_dividends, rate_dividends, pit_dividends):
    pit_dividends = tti_dividends * rate_dividends
    return (pit_dividends)

"Calculation for total tax from all sources"
@iterate_jit(nopython=True)
def cal_pit_all(pit_wages, pit_royalty, pit_interest, pit_rent, pit_rent_high, pit_sale_prop, pit_sale_prop_dev, pit_cars, pit_stocks, pit_dividends, pitax_all):
    pitax_all = pit_wages + pit_royalty+pit_interest+pit_rent+pit_rent_high+pit_sale_prop+pit_sale_prop_dev+pit_cars+pit_stocks+pit_dividends
    return (pitax_all)


"Calculation for incorporating behavior - uses tax elasticity of total tax from labour income "
"Elasticity = % Change in income / % Change in tax rate "

@iterate_jit(nopython=True)
def cal_tti_wages_behavior(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3,
                         rate1_curr_law, rate2_curr_law, rate3_curr_law, 
                         rate4_curr_law, tbrk1_curr_law, tbrk2_curr_law,
                         tbrk3_curr_law,
                         elasticity_pit_taxable_income_threshold,
                         elasticity_pit_taxable_income_value, tti_wages,
                         tti_wages_behavior):
    """
    Compute taxable total income after adjusting for behavior.
    """  
    elasticity_taxable_income_threshold0 = elasticity_pit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_pit_taxable_income_threshold[1]
    #elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_pit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_pit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_pit_taxable_income_value[2]
    if tti_wages<=0:
        elasticity=0
    elif tti_wages<elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif tti_wages<elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    else:
        elasticity=elasticity_taxable_income_value2

    if tti_wages<0:
        marg_rate=0
    elif tti_wages<=tbrk1:
        marg_rate=rate1
    elif tti_wages<=tbrk2:
        marg_rate=rate2
    elif tti_wages<=tbrk3:
        marg_rate=rate3
    else:        
        marg_rate=rate4

    if tti_wages<0:
        marg_rate_curr_law=0
    elif tti_wages<=tbrk1_curr_law:
        marg_rate_curr_law=rate1_curr_law
    elif tti_wages<=tbrk2_curr_law:
        marg_rate_curr_law=rate2_curr_law
    elif tti_wages<=tbrk3_curr_law:
        marg_rate_curr_law=rate3_curr_law
    else:        
        marg_rate_curr_law=rate4_curr_law
    
    frac_change_net_of_pit_rate = ((1-marg_rate)-(1-marg_rate_curr_law))/(1-marg_rate_curr_law)
    frac_change_tti_wages = elasticity*(frac_change_net_of_pit_rate)  
    tti_wages_behavior = tti_wages*(1+frac_change_tti_wages)
    return (tti_wages_behavior)


"Calculation behavior"
@iterate_jit(nopython=True)
def cal_tti_c_behavior(rate_capital, rate_capital_curr_law, 
                      rate_dividends, rate_dividends_curr_law,
                      elasticity_pit_capital_income_threshold,
                      elasticity_pit_capital_income_value,
                      tti_all, tti_dividends, tti_c_all_behavior, tti_c_div_behavior):
    """
    Compute capital income under behavioral response
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    intrducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    elasticity_pit_capital_income_threshold0 = elasticity_pit_capital_income_threshold[0]
    elasticity_pit_capital_income_threshold1 = elasticity_pit_capital_income_threshold[1]
    
    elasticity_pit_capital_income_value0=elasticity_pit_capital_income_value[0]
    elasticity_pit_capital_income_value1=elasticity_pit_capital_income_value[1]
    elasticity_pit_capital_income_value2=elasticity_pit_capital_income_value[2]
    
    tti_c = tti_all + tti_dividends
    
    if tti_c<=0:
        elasticity=0
    elif tti_c<=elasticity_pit_capital_income_threshold0:
        elasticity=elasticity_pit_capital_income_value0
    elif tti_c<=elasticity_pit_capital_income_threshold1:
        elasticity=elasticity_pit_capital_income_value1
    else:
        elasticity=elasticity_pit_capital_income_value2
    
    frac_change_net_of_pit_capital_income_rate_all = ((1-rate_capital)-(1-rate_capital_curr_law))/(1-rate_capital_curr_law)
    frac_change_tti_c_all = elasticity*(frac_change_net_of_pit_capital_income_rate_all) 
    frac_change_net_of_pit_capital_income_rate_div = ((1-rate_dividends)-(1-rate_dividends_curr_law))/(1-rate_dividends_curr_law)
    frac_change_tti_c_div = elasticity*(frac_change_net_of_pit_capital_income_rate_div)   
    tti_c_all_behavior = tti_all*(1+frac_change_tti_c_all)    
    tti_c_div_behavior = tti_dividends*(1+frac_change_tti_c_div)
    return tti_c_all_behavior, tti_c_div_behavior

"Calculation for PIT from capital incorporating behavioural response"
@iterate_jit(nopython=True)
def cal_pit_cap_behavior(rate_capital, rate_dividends, tti_c_all_behavior, tti_c_div_behavior, pit_c_behavior):
    pit_c_behavior = (tti_c_all_behavior*rate_capital) + (tti_c_div_behavior*rate_dividends)
    return pit_c_behavior

"Calculation for PIT from labor income incorporating behavioural response"
@iterate_jit(nopython=True)
def cal_pit_w_behavior(tti_wages_behavior, rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, pit_w_behavior):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tti_wages_behavior  
    
    pit_w_behavior = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))
        
    return (pit_w_behavior)



@iterate_jit(nopython=True)
def cal_pit_behavior(pit_c_behavior,pit_w_behavior, pitax):
    """
    Explanation about total PIT calculation
    
    Gross amount of income tax:
    ------------------------------------------------------------------
    Employment contracts, civil contracts, and other incomes = 396.64
    Other sources of income (royalties, interest incomes etc.) = 44.56
    Temporary disability benefits=15.10
    Income declared by individuals (residents and nonresidents)= 2.70
    -----------------------------------------------------------------
    Total gross amount of income tax  = 459 
    
    Cash back from income tax:	
    -----------------------------------------------------------------
    Mortgage 	-22.70
    Dividends	-9.40
    Tuition fee 	-0.20
    -----------------------------------------------------------------
    Total cash back of income tax = 32.3
    
    
    Annual PIT amount, reported on the State Revenue Committee’s official website
    -----------------------------------------------------------------
    Net PIT= 459-32.3= 426.70 (bln. AMD)
    
    """
    
    pitax = pit_c_behavior+pit_w_behavior
   
    return (pitax)


