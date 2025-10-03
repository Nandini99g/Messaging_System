from flask import Flask, request
from tasks import send_email_task, log_time_task

app = Flask(__name__)

@app.route("/action")
def action():
    if "sendmail" in request.args:
        recipient = request.args.get("sendmail")
        send_email_task.delay(recipient)  # Async task
        return f"Email task queued for {recipient}"

    elif "talktome" in request.args:
        log_time_task.apply_async()  # Run logging task
        return "Time logging task executed"

    else:
        return "Invalid action. Use ?sendmail=<email> or ?talktome"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
