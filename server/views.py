import logging
import config

@config.g_app.route("/")
def index():
    return "Artspeaker job offer and portfolio services."

if __name__ == '__main__':
    config.g_app.run(host="0.0.0.0",port=config.serverPort,debug=True)