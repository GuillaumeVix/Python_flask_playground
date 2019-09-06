##building stage
FROM python:3
ADD app/app.py /
RUN pip install -r requirements.txt

##running stage
EXPOSE 8000
CMD ["python", ".app/app.py"]