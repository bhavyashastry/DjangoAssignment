# DjangoAssignment

# How the Code Works:
# Question 1: Signals are Synchronous:

custom_signal_handler includes a 2-second delay to simulate blocking.
The output proves that the signal handler blocks further execution, meaning signals are synchronous by default.
# Question 2: Same Thread:

The signal handler and the signal sender both print their thread IDs using threading.get_ident().
This confirms that both run on the same thread.
# Question 3: Same Database Transaction:

A model (MyModel) and a database transaction (transaction.atomic()) are created.
The signal handler uses transaction.on_commit() to verify if it’s part of the same transaction.
# Rectangle Class:

The Rectangle class implements __iter__() so that instances can be iterated over, returning the length and width in the required format.
