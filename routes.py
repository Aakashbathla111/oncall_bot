from flask import Flask, jsonify, request
from app import hit_curl
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


flaskapp = Flask(__name__)
scheduler = BackgroundScheduler()

# Schedule the task to run every day at 10 AM
scheduler.add_job(
    hit_curl,
    trigger=CronTrigger(hour=16, minute=35),
    id='daily_task',
    name='Run daily task',
    replace_existing=True,
)

# Start the scheduler when the Flask app starts
scheduler.start()


# Define the endpoint for handling POST requests
@flaskapp.route('/run-script', methods=['POST'])
def endpoint_run_script():
    if request.method == 'POST':
        # token = request.json.get('token')
        # print(token)
        hit_curl()
        return jsonify({'result': 'success'})


if __name__ == '__main__':
    flaskapp.run(debug=True)