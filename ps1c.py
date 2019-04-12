annual_salary = int(input('Enter your annual salary: '))
for_annual_raise = annual_salary

#GIVEN VARIABLES: 
semi_annual_raise = 0.07
annual_return = 0.04
total_cost = 1000000
down_payment = total_cost * 0.25

#OTHER REQUIRED VARIABLES:
high_val = 10000
low_val = 0
bisected_rate = (high_val + low_val) // 2
rate = bisected_rate / 10000
bisection_count = 0

current_savings = 0

while abs(current_savings - down_payment) > 100:
    bisection_count += 1 
    current_savings = 0
    rate = bisected_rate / 10000
    monthly_salary = annual_salary / 12    
    for each_month in range(36):
        if each_month % 6 == 0 and each_month != 0:
            monthly_salary += monthly_salary * semi_annual_raise
        monthly_savings = monthly_salary * rate
        monthly_investment = current_savings * (annual_return / 12)
        current_savings += monthly_savings + monthly_investment        
    if current_savings < down_payment - 100:
        low_val = bisected_rate
    else:
        high_val = bisected_rate
    bisected_rate = (high_val + low_val) / 2
    if bisection_count > 13:
        break

#OUTPUTS:
if bisection_count <= 13:
    print('Best rate:', rate * 100, '%')
    print('Number of bisections:', bisection_count)
elif bisection_count > 13 and abs(current_savings - down_payment) < 100:
    print('Best rate:', rate * 100, '%')
    print('Number of bisections:', bisection_count)
else:
    print('Get a higher paying job ;)')

        

    

    

