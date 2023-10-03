FROM python:3.10-alpine

WORKDIR app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR hackathon_projects

CMD sh -c "python manage.py migrate && \
           python manage.py collectstatic --no-input && \
           gunicorn hackathon_projects.wsgi:application --bind 0:8000"