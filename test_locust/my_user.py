import threading

import gevent
from locust import HttpUser, TaskSet, task
from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_printer
from locust.web import WebUI


class UserBehavior(TaskSet):
    @task
    def my_task(self):
        self.client.get("/")


class MyUser(HttpUser):
    host = "http://localhost:8000"
    tasks = [UserBehavior]

    def wait_time(self):
        return 1


# def start_web_ui(env):
#    print(env)
#    web_ui = WebUI("0.0.0.0", 8089, env)
#    web_ui.start()


def main():
    setup_logging("INFO", None)

    # Set up Locust Environment and Runner
    env = Environment(user_classes=[MyUser])
    env.create_local_runner()

    # Start the web UI in a separate thread
    #    threading.Thread(target=start_web_ui, args=(env,), daemon=True).start()

    # Start a greenlet that periodically outputs stats
    gevent.spawn(stats_printer(env.stats))

    # Start running the tasks
    env.runner.start(1, spawn_rate=1)  # Start with 1 user and 1 spawn rate

    # Run for a certain duration (e.g., 10 seconds)
    gevent.spawn_later(1000, lambda: env.runner.quit())
    env.runner.greenlet.join()

    # Stop Locust environment
    print("Test finished!")


if __name__ == "__main__":
    main()
