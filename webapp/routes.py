from webapp import lmcz_app
from settings import DEBUG

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    lmcz_app.run(debug=DEBUG)