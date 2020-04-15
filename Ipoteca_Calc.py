#   x = K * S; K = (p * (1 + p)n) / (1 + p)n – 1),
#   где: x – ежемесячный размер аннуитета.
#   S – сумма ипотеки.
#   p – месячная процентная ставка, если ставка годовая,
#   то берем 1/12 часть и делим на 100.
#   n – длительность кредитования в месяцах.
#   K – коэффициент аннуитета.
from flask import Flask, render_template,request,escape
from math import ceil

from DBcm import UseDatabase

app = Flask(__name__)
app.config['dbconfig'] = {'host':'127.0.0.1',
                          'database':'ipotecacalc',
                          'user' : 'admin',
                          'password' : 'admin',}


def ipoteca_calc(property_value:int, initial_payment:int,
                 loan_period:int, interest_rate:float):
    S = (property_value - initial_payment)
    p = interest_rate/1200
    n = loan_period * 12
    K = (p * (1 + p)**n)/ ((1 + p)**n -1)
    x_all = ceil(K * S * n)
    x_month = ceil(K * S)
    return x_month

def log_request( property_value:int, initial_payment:int,
                 loan_period:int, interest_rate:float, credit_month:int):
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """
        insert into i_log (property_value, initial_payment, loan_period,interest_rate,credit_month)
        values (%s, %s, %s, %s, %s)
         """
        cursor.execute(_SQL, (property_value,
                              initial_payment,
                              loan_period,
                              interest_rate,
                              credit_month,))

def load_payment_schedule( property_value:int, initial_payment:int,
                 loan_period:int, interest_rate:float, credit_month:int):
    S = (property_value - initial_payment)
    p = interest_rate / 1200
    n = loan_period * 12
    K = (p * (1 + p) ** n) / ((1 + p) ** n - 1)
    x_all = ceil(K * S * n)
    x_month = ceil(K * S)
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.callproc('test_7',(x_month, S, n))



@app.route('/calculation', methods = ['POST'])
def ipoteca_calc_finish()-> 'html':
    property_value = int(request.form['property_value'])  #Возможно нужно поменять местами def entry_page и def ipoteca_calc_finish 
    initial_payment = int(request.form['initial_payment'])
    loan_period = int(request.form['loan_period'])
    interest_rate = float(request.form['interest_rate'])
    credit_month = ipoteca_calc(property_value, initial_payment,
                 loan_period, interest_rate)
    credit_all = credit_month * 12 * loan_period
    credit_over = credit_all - (property_value  - initial_payment)
    overpayment = ceil(credit_all / property_value *100)
    log_request(property_value, initial_payment,
                 loan_period, interest_rate,credit_month)
    load_payment_schedule(property_value, initial_payment,
                 loan_period, interest_rate,credit_month)
    return render_template ('results.html',
                            the_title = 'Результаты расчета',
                            the_credit_month = credit_month,
                            the_credit_all = credit_all,
                            the_credit_over = credit_over,
                            the_overpayment = overpayment,)

@app.route('/')
def entry_page() ->'html':
    return render_template('entry.html', the_title = 'Калькулятор ипотеки онлайн')

@app.route('/vcalc')
def view_the_loq() ->'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """ select * from i_log """
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ("ID", "Время", "Сумма ипотеки", "Первоначальный взнос", "Срок ипотеки",
              "Процентная ставка", "Платеж в месяц")
    return render_template('viewlog.html',
                           the_title = 'Журнал расчетов ипотеки',
                           the_row_titles = titles,
                           the_data = contents,)


@app.route('/var')
def view_payment_schedule():
    with UseDatabase(app.config['dbconfig']) as cursor:
         _SQL = """select * from payment_schedule """
         cursor.execute(_SQL)
         contents = cursor.fetchall()
         titles = ("ID", "Дата платежа", "Сумма платежа, руб.", "Платеж по основному долгу, руб.",
              "Платеж по процентам, руб.",
              "Остаток долга, руб.")
    return render_template('view_payment_schedule.html',
                           the_title = 'График платежей',
                           the_row_titles = titles,
                           the_data = contents,)


app.run(debug=True) 
  
