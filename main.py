import time
import threading
from django.dispatch import Signal, receiver
from django.db import models, transaction
import django
from django.conf import settings

# Configuring minimal Django settings for standalone usage
settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',  # for model use
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
django.setup()

# === Question 1 & 2: Django Signals ===

# Defining a custom signal
custom_signal = Signal()


# Signal Handler
@receiver(custom_signal)
def custom_signal_handler(sender, **kwargs):
    print("Signal handler started")
    print(f"Signal handler is running on thread: {threading.get_ident()}")
    time.sleep(2)  # Simulate a delay of 2 seconds
    print("Signal handler finished")


# Trigger the signal and test if it is synchronous and runs in the same thread
def trigger_signal():
    print("Triggering signal")
    print(f"Signal trigger is running on thread: {threading.get_ident()}")

    start_time = time.time()

    # Send the signal
    custom_signal.send(sender=None)

    # time after signal is triggered
    signal_triggered_time = time.time()
    print(f"Time taken for signal handler: {signal_triggered_time - start_time:.2f} seconds")

    print("Code after signal triggered")
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")


# === Question 3: Same Database Transaction ===

class MyModel(models.Model):
    name = models.CharField(max_length=100)


# Signal Handler for database transaction
@receiver(custom_signal)
def db_signal_handler(sender, **kwargs):
    print("Inside DB signal handler")

    def after_transaction_commit():
        print("Signal handler committed to the database transaction.")

    # Check if signal works in the same transaction
    transaction.on_commit(after_transaction_commit)


# Trigger signal in a transaction
def trigger_db_signal():
    print("Triggering signal inside a database transaction")

    with transaction.atomic():
        custom_signal.send(sender=None)
        print("Inside transaction, signal sent")

        # Normally, the changes to the database would be committed at the end of this transaction


# === Rectangle Class ===
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}


# === Testing the Assignment ===
if __name__ == "__main__":
    # Question 1: Signals are synchronous
    trigger_signal()

    # Question 2: Signals run in the same thread
    # Already demonstrated in trigger_signal()

    # Question 3: Signals in the same database transaction
    trigger_db_signal()

    # Custom Class Test
    rect = Rectangle(length=10, width=5)
    for dimension in rect:
        print(dimension)
