from flask import Flask
from flask import jsonify

from FlaskApp.routes import routes  # Ensure that `routes` here is your Blueprint instance

app = Flask(__name__)
app.register_blueprint(routes)  # Use register_blueprint, not register

if __name__ == '__main__':
    app.run(debug=True)
