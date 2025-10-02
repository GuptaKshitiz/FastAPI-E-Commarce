from fastapi import BackgroundTasks, APIRouter
import time

router = APIRouter()

def write_log(message: str):
    print(f"BACKGROUND TASK: {message}")
    time.sleep(5)  # Simulate a long-running task
    with open("log.txt", mode="a") as log:
        log.write(f"{message}\n")
    print("BACKGROUND TASK: Completed writing to log.")

@router.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Sending notification to {email} with message: It's too long!")
    return {"message": "Notification will be sent in the background."}