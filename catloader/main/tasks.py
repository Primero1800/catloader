import httpx
import uuid

from celery import shared_task
from django.conf import settings

from catloader.celery import app

#CAT_URL = "https://cataas.com/cat"
CAT_URL = "https://thecatapi.com/api/images/get?format=src&type=gif"

@shared_task
def add_ff(x, y):
    return x + y


@shared_task(bind=True)
def import_image_of_cat(self, *args, **kwargs):

    headers = self.request.headers
    if headers:
        print("Headers:")
        for key, value in headers.items():
            print(f"{key}: {value}")
    else:
        print("No headers available.")

    with httpx.Client() as client:
        response = client.get(CAT_URL, follow_redirects=True)

    print(f"Inner result Response={response}")

    if response and response.status_code == 200:
        file_ext = response.headers.get("Content-Type").split('/')[1]
    else:
        file_ext = '.err'
    file_name = settings.BASE_DIR / 'cats' / (str(uuid.uuid4()) + '.' + file_ext)

    with open(file_name, 'wb') as file:
        if response and response.status_code == 200:
            for chunk in response.iter_bytes(chunk_size=256):
                file.write(chunk)
        elif response:
            file.write(f"{response.status_code} -- {response.headers} -- {response.content}".encode())
        else:
            file.write('No response error'.encode())

        return True
