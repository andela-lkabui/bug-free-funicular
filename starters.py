from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
	return 'Welcome home!'


@app.route('/outlets', methods=['GET', 'POST', 'PUT'])
def outlets():
	if request.method == 'GET':
		return 'Your outlets!'
	if request.method == 'POST':
		return 'Write some posting logic here'


@app.route('/expenses')
def expenses():
	return 'Your expenses!'


@app.route('/accounts')
def accounts():
	return 'Your accounts!'

if __name__ == '__main__':
	app.run()