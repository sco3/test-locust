from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_printer
from locust import HttpUser, TaskSet, task
import gevent

class UserBehavior(TaskSet):
    @task
    def my_task(self):
        self.client.get("/")

class MyUser(HttpUser):
    tasks = [UserBehavior]

    def wait_time(self):
        return 1

def main():
    setup_logging("INFO", None)

    # Set up Locust Environment and Runner
    env = Environment(user_classes=[MyUser])
    env.create_local_runner()

    # Start a greenlet that periodically outputs stats
    gevent.spawn(stats_printer(env.stats))

    # Start running the tasks
    env.runner.start(1, spawn_rate=1)  # Start with 1 user and 1 spawn rate

    # Run for a certain duration (e.g., 10 seconds)
    gevent.spawn_later(10, lambda: env.runner.quit())
    env.runner.greenlet.join()

    # Stop Locust environment
    print("Test finished!")

if __name__ == "__main__":
    main()
