FROM python:3.8
ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -q -r /tmp/requirements.txt
ADD . /var/www/app
WORKDIR /var/www/app
CMD gunicorn -b 0.0.0.0:$PORT src.wsgi
