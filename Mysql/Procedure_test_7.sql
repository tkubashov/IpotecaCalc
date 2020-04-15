delimiter $$
create procedure test_7(IN payment_month decimal(50,2), IN sum_kredit decimal(50,2), IN loan_period_month INT)
begin
declare month_year date default curdate();
declare payment_percent, payment_credit,balance_owed, c1, incr decimal(50,2);
declare i int;
set i = 1;
set payment_credit = payment_month*0.12;
set c1 = payment_month*0.12;
set payment_percent = payment_month - payment_credit;
set balance_owed = sum_kredit - payment_credit;
set incr = (sum_kredit*2/loan_period_month - 2*c1)/(loan_period_month-1);
truncate table payment_schedule;
while i <= loan_period_month
do
insert into payment_schedule
(month_year,payment_month, payment_credit,payment_percent,balance_owed)
values
(month_year,payment_month,payment_credit,payment_percent,balance_owed);
set i = i + 1;
set month_year = date_add(month_year, interval 1 month);
set payment_credit = payment_credit + incr;
set payment_percent = payment_month - payment_credit;
set balance_owed = balance_owed - payment_credit;
end while;
end$$