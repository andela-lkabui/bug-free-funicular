from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	return 'Welcome home!'

@app.route('/outlets')
def outlets():
	return 'Your outlets!'

@app.route('/expenses')
def expenses():
	return 'Your expenses!'

@app.route('/accounts')
def accounts():
	return 'Your accounts!'

if __name__ == '__main__':
	app.run()