FROM python:3.9
ADD . /bitrix24_dayOff
WORKDIR /bitrix24_dayOff
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python","AddTasks.py"]