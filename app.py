from flask import Flask
from bot.jobs.scheduler import scheduler
import time

app = Flask(__name__)

if __name__ == "__main__":
    # app.run(debug=True)
    scheduler.start()
    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
