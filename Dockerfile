FROM python:3
ADD api.py /
RUN pip install flask
CMD ["python", "./app.py"]