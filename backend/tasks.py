from backend.workers import celery
import datetime as dt

@celery.task()
def say_hello(username):
    print("Inside task")
    return "Hello"