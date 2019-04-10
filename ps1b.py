annual_sal = float(input('Enter your annual salary: '))
monthly_sal = annual_sal / 12

portion_saved = float(input('Enter portion saved: '))
monthly_savings = monthly_sal * portion_saved

total_cost = float(input('Enter total cost: '))

semi_annual_raise = float(input('Enter your semi-annual raise: '))

portion_down_payment = 0.25
current_savings = 0.0
r = 0.04
months = 0
salary_raise = 0.0

sixth_month_counter = 0

while current_savings <= total_cost * portion_down_payment:

    months += 1
    sixth_month_counter += 1
    
    if sixth_month_counter == 6:
        monthly_sal += (monthly_sal * semi_annual_raise)
        monthly_savings = monthly_sal * portion_saved
        sixth_month_counter = 0
        
    monthly_returns = current_savings * (r/12)
    current_savings += monthly_returns + monthly_savings

    
print('Number of months:', months)

