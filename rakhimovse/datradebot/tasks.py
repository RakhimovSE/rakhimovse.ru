from celery.task import task


@task
def test():
    print('This is print text')
    return 'This is return text'
