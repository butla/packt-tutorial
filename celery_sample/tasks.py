import math
import os
from celery import Celery

# TODO configure
# let's say that it always will be the guest user, which, of course, isn't safe and shouldn't be used in production

queue_host = os.environ['QUEUE_HOST']
app = Celery('tasks', broker=f'amqp://guest@{queue_host}//')


@app.task
def print_factorial_digits(number):
    factorial = math.factorial(number)
    factorial_digits = len(str(factorial))
    print(f'Factorial of {number} has {factorial_digits} digits.')
