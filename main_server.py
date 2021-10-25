from blockchainbot import app

if __name__ == "__main__":
	app.run(host='0.0.0.0')#processes=app.config.get('FLASK_PROCESSES', 4))