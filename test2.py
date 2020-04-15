
from flask import Flask, render_template,request,escape
from math import ceil

from DBcm import UseDatabase

app = Flask(__name__)
app.config['dbconfig'] = {'host':'127.0.0.1',
                          'database':'ipotecacalc',
                          'user' : 'admin',
                          'password' : 'admin',}

a = '2020-05-24'
b = 10000
c = 100.21
i = 3
n = 6
@app.route('/testt')
def payment_schedule() ->'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        cursor.callproc('test_7_1',(a, b, c, i, n))
        # _SQL = """select * from payment_schedule """
        # cursor.execute(_SQL)
        # contents = cursor.fetchall()
        for result in cursor.stored_results():
            contents = result.fetchall()
    titles = ("a", "b", "c", "i","n")
    return render_template('viewlog.html',
                           the_title = 'График платежей',
                           the_row_titles = titles,
                           the_data = contents,)


app.run(debug=True) 
  
