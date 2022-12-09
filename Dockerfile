FROM python:3.9.4
WORKDIR /heartstroke
COPY requirements.txt /heartstroke/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /heartstroke
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]