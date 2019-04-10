annual_sal = float(input('Enter your annual salary: '))
monthly_sal = annual_sal / 12

portion_saved = float(input('Enter portion saved: '))
monthly_savings = monthly_sal * portion_saved

total_cost = float(input('Enter total cost: '))

portion_down_payment = 0.25
current_savings = 0.0
r = 0.04
months = 0

while current_savings <= total_cost * portion_down_payment:    
    monthly_returns = current_savings * (r/12)
    current_savings += monthly_returns + monthly_savings
    months += 1    
    
print('Number of months:', months)

