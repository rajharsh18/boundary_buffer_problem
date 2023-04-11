import threading
import time

# Defining Constants
# FULL_CAP = int(input("Enter the capacity of buffer: "))
# MAX_ITEMS = int(input("Enter the max count print commands: "))
# TIME_PROD = float(input("Enter the time for giving a print command(in seconds): "))
# TIME_CONS = float(input("Enter the time for printing the file(in seconds): "))
BUFFER_CAP = 10
MAX_ITEMS = 20
TIME_PROD = 1
TIME_CONS = 3
# Defining variables
buffer = [-1 for i in range(BUFFER_CAP)]
in_index = 0
out_index = 0
# Defining Semaphore
mutex = threading.Semaphore()
empty = threading.Semaphore(BUFFER_CAP)
full = threading.Semaphore(0)

# Producer Function
def Producer():
    global buffer, in_index, out_index
    global mutex, empty, full
    items_produced = 0
    counter = 0
    while items_produced < MAX_ITEMS:
      empty.acquire()
      mutex.acquire()
      counter += 1
      buffer[in_index] = counter
      in_index = (in_index + 1)%BUFFER_CAP
      print(f"{counter} print command sent.")
      if (counter == MAX_ITEMS):
         print("\n************************")
         print("| Production Completed |")
         print("************************\n")
      mutex.release()
      full.release()
      time.sleep(TIME_PROD)
      items_produced += 1
 
# Consumer Function
def Consumer():
    global buffer, in_index, out_index, counter
    global mutex, empty, full
    items_consumed = 0
    while items_consumed < MAX_ITEMS:
      full.acquire()
      mutex.acquire()
      item = buffer[out_index]
      out_index = (out_index + 1)%BUFFER_CAP
      print("\n------------------------------------")
      print(f"| {item} document printed successfully. |")
      print("------------------------------------\n")
      mutex.release()
      empty.release()
      time.sleep(TIME_CONS)
      items_consumed += 1

# Creating Threads of functions
producer = threading.Thread(target=Producer)
consumer = threading.Thread(target=Consumer)

# Starting Function Threads
consumer.start()
producer.start()

# Waiting for the threads to complete
producer.join()
consumer.join()