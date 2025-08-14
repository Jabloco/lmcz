from flask import render_template
from webapp import lmcz_app

from settings import DEBUG


@lmcz_app.route('/')
@lmcz_app.route('/index')
def index():
    return render_template('index.html', title='Данные о состоянии ЛМЧЗ')


if __name__ == '__main__':
    lmcz_app.run(debug=DEBUG)
