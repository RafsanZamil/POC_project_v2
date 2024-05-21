from locust import HttpUser, task, between
from random import randint


class LoadTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_square(self):
        self.client.get("blog/view/")

