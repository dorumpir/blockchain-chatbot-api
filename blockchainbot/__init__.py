from flask import Flask
from flask_apscheduler import APScheduler;
from flask_elasticsearch import FlaskElasticsearch
#from blockchainbot.model import es


app = Flask(__name__)
app.config.from_pyfile('blockchainbot.cfg')
app_ctx = app.app_context() # 激活
app_ctx.push()

scheduler = APScheduler();
scheduler.init_app(app)
scheduler.start()

es = FlaskElasticsearch()
es.init_app(app)


from blockchainbot.views import bc_view
app.register_blueprint(bc_view)
