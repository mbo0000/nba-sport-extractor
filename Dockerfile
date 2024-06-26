
FROM python:3.9

WORKDIR /usr/src/app

COPY . .

# download requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]

CMD ["sh", "-c", "python ./main.py & tail -f /dev/null"]