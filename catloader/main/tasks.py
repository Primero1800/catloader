from celery import shared_task


@shared_task
def addff(x, y):
    return x + y