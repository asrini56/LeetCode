start = start_date.year

mp = {}

salary_p_month  = base_salary//12
rsu_p_month = rsu//12

if start == current_date.year:
    n_month = current_date.month - start_date.month
    first_income = salary_p_month*n_month + rsu_p_month*n_month + sign_on 
    mp[start] = first_income
    return mp
else:
    n_month = 12 - start_date.month + 1
first_income = salary_p_month*n_month + rsu_p_month*n_month + sign_on 
mp[start] = first_income

start += 1

while current_date.year != start:
    income = 12*(salary_p_month + rsu_p_month)
    mp[start] = income
    start += 1
income = (current_date.month - 1)*(salary_p_month + rsu_p_month)
mp[start] = income
print(mp)
