import json
import time

import httpx
import uuid

import redis
from celery import shared_task
from django.conf import settings

from catloader.celery import app

#CAT_URL = "https://cataas.com/cat"

CAT_URL = "https://thecatapi.com/api/images/get?format=src&type=gif"
DOG_URL = "https://thedogapi.com/api/images/get?format=src&type=gif"


def get_periodictask_name(task):
    result = ''
    headers = task.request.headers
    if headers:
        print(f"**********!!!!!!!!!!!!!!****************** {headers}, items: {headers.items()}")
        result = headers.get('name', '')
    else:
        print("No headers available.")
    return result


def get_filename(response, periodictask_name):
    try:
        if response and response.status_code == 200:
            file_ext = response.headers.get("Content-Type").split('/')[1]
        else:
            file_ext = '.err'
    except (IndexError, AttributeError):
        return False
    return settings.BASE_DIR / 'cats' / (periodictask_name + str(uuid.uuid4()) + '.' + file_ext)


def write_result(response, periodictask_name):
    print(f"Inner result Response={response}")

    file_name = get_filename(
        response=response,
        periodictask_name=periodictask_name
    )
    if not file_name:
        return False

    try:
        with open(file_name, 'wb') as file:
            if response and response.status_code == 200:
                for chunk in response.iter_bytes(chunk_size=256):
                    file.write(chunk)
            elif response:
                file.write(f"{response.status_code} -- {response.headers} -- {response.content}".encode())
            else:
                file.write('No response error'.encode())
    except Exception as exc:
        print(response.status_code, periodictask_name, f'Error while writing file: {exc}')
        return False
    return file_name


@shared_task
def add_ff(x, y):
    return x + y


@shared_task(bind=True)
def import_image_of_cat(self, *args, **kwargs):
    periodictask_name = get_periodictask_name(self)

    with httpx.Client() as client:
        response = client.get(CAT_URL, follow_redirects=True)

    result_image = write_result(response=response, periodictask_name=periodictask_name)
    if not result_image:
        return None
    return str(result_image)


@shared_task(bind=True)
def import_image_of_dog(self, *args, **kwargs):
    periodictask_name = get_periodictask_name(self)

    with httpx.Client() as client:
        response = client.get(DOG_URL, follow_redirects=True)

    result_image = write_result(response=response, periodictask_name=periodictask_name)
    if not result_image:
        return None
    return str(result_image)


@shared_task(bind=True)
def import_image_of_pet(self, *args, pet=None, **kwargs):
    periodictask_name = get_periodictask_name(self)

    if pet:
        if pet == 'cat':
            pet_url = CAT_URL
        elif pet == 'dog':
            pet_url = DOG_URL
        else:
            pet_url = None
    if not pet or not pet_url:
        print(periodictask_name, pet, pet_url)
        return None

    with httpx.Client() as client:
        response = client.get(pet_url, follow_redirects=True)

    result_image = write_result(response=response, periodictask_name=periodictask_name)
    if not result_image:
        return None
    return str(result_image)


@shared_task(bind=True)
def problemator(self, *args, times=1, **kwargs):
    task_name = get_periodictask_name(self)
    if not args:
        args = (1, 2, 3, 4,)
    res = 0
    redis_parameters = settings.REDIS_PARAMETERS
    with redis.Redis(**redis_parameters) as client:
        for _ in range(times):
            for arg in args:
                client.lpush('problemator', json.dumps((arg, task_name)))
            time.sleep(4)


@shared_task(bind=True)
def problemator_solver(self, *args, **kwargs):
    task_name = get_periodictask_name(self)
    redis_parameters = settings.REDIS_PARAMETERS
    with redis.Redis(**redis_parameters) as client:
        result =''
        while True:
            answer = client.rpop('problemator')
            if answer:
                answer = str(json.loads(answer)[0])
                result += answer
            else:
                break
    return result
