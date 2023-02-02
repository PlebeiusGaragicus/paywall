import time
import queue
import threading

class tobj:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "tobj: " + self.name

# Create a queue to store messages
q = queue.Queue()

# Define a function that will run in a separate thread
def worker(obj: tobj):
    while True:
        message = q.get()
        if message is None:
            break
        # print("Received message:", message)
        time.sleep(1)
        print("Received message:", message, " using: ", obj)

asdf = tobj("test")

# Start the worker thread
t = threading.Thread(target=lambda: worker( asdf ))
t.start()

# Send messages to the worker thread
q.put("Hello")
q.put("World")

# Send a "None" message to stop the worker thread
q.put(None)

# Wait for the worker thread to finish
t.join()







#### EXAMPLE FROM CHATGPT
# import queue
# import threading

# # Create a queue to store messages
# q = queue.Queue()

# # Define a function that will run in a separate thread
# def worker():
#     while True:
#         message = q.get()
#         if message is None:
#             break
#         print("Received message:", message)

# # Start the worker thread
# t = threading.Thread(target=worker)
# t.start()

# # Send messages to the worker thread
# q.put("Hello")
# q.put("World")

# # Send a "None" message to stop the worker thread
# q.put(None)

# # Wait for the worker thread to finish
# t.join()
