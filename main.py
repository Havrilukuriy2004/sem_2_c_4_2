import threading
import random
import time
import queue

class Hotel:
    def __init__(self, num_rooms):
        self.num_rooms = num_rooms
        self.available_rooms = num_rooms
        self.lock = threading.Lock()
        self.room_queue = queue.Queue()

    def check_in(self):
        with self.lock:
            if self.available_rooms > 0:
                self.available_rooms -= 1
                return True
            else:
                return False

    def check_out(self):
        with self.lock:
            self.available_rooms += 1
            if not self.room_queue.empty():
                waiting_customer = self.room_queue.get()
                waiting_customer.set()

def customer(hotel, arrival_time, stay_time, wait_times):
    """Процес клієнта, який намагається заселитися у готель."""
    time.sleep(arrival_time)

    arrival = time.time()
    checked_in = hotel.check_in()
    if not checked_in:
        wait_event = threading.Event()
        hotel.room_queue.put(wait_event)
        wait_event.wait()
        wait_times.append(time.time() - arrival)
        hotel.check_in()

    time.sleep(stay_time)
    hotel.check_out()

def main():
    num_rooms = 10         # Кількість номерів в готелі
    t1 = 1                 # Мінімальний час до прибуття нового клієнта (секунди)
    t2 = 5                 # Максимальний час до прибуття нового клієнта (секунди)
    t3 = 1                 # Мінімальний час перебування в готелі (секунди)
    t4 = 10                # Максимальний час перебування в готелі (секунди)
    num_customers = 100    # Кількість клієнтів

    hotel = Hotel(num_rooms)
    wait_times = []

    threads = []

    for _ in range(num_customers):
        arrival_time = random.uniform(t1, t2)
        stay_time = random.uniform(t3, t4)
        thread = threading.Thread(target=customer, args=(hotel, arrival_time, stay_time, wait_times))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    average_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"Середній час очікування: {average_wait_time:.2f} секунд")

if __name__ == "__main__":
    main()
