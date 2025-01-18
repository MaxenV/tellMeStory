FROM library/python:3.12.8-slim

COPY ./src/tellMeStoryBackend /app/tellMeStoryBackend
WORKDIR /app/tellMeStoryBackend

RUN pip install django==5.1.5 ollama==0.4.6
RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]