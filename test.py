
from flask import Flask, render_template,request,escape
from math import ceil

from DBcm import UseDatabase

app = Flask(__name__)
app.config['dbconfig'] = {'host':'127.0.0.1',
                          'database':'ipotecacalc',
                          'user' : 'admin',
                          'password' : 'admin',}


@app.route('/test')
def view_the_loq() ->'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.callproc('test_7')
        _SQL = """select * from payment_schedule """
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        # for result in cursor.stored_results():
        #     contents = result.fetchall()
    titles = ("ID", "Дата платежа", "Сумма платежа, руб.", "Платеж по основному долгу, руб.",
              "Платеж по процентам, руб.",
              "Остаток долга, руб.")
    return render_template('viewlog.html',
                           the_title = 'График платежей',
                           the_row_titles = titles,
                           the_data = contents,)


app.run(debug=True) 
  
