FROM python:3.10.7

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

RUN python -m venv /venv
RUN . venv/bin/activate

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8005

RUN python manage.py makemigrations
RUN python manage.py migrate


CMD ["python", "manage.py", "runserver"]