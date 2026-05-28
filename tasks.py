import time
import random

from celery_app import celery

@celery.task
def random_number():
    print("\ngenerating a random number....\n")
    time.sleep(10)
    return random.randint(0, 100)


def estimate_pi(num_samples: int) -> float:

    print("\n----->calculating PI estimation...\n")

    random_float = random.random
    inside_circle = 0
    
    for _ in range(num_samples):
        x = random_float()
        y = random_float()

        if x * x + y * y <= 1.0:
            inside_circle += 1
            
    return 4.0 * inside_circle / num_samples

