import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))

threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5000')
# bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5000')


forwarded_allow_ips = '*'

# secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl',
#                          'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}


# def post_worker_init(worker):
#     from Main import start_thread1, start_thread2
#     start_thread1()
#     start_thread2()
