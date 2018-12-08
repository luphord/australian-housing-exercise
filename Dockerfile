FROM python:3

WORKDIR /opt/data-science-exercise

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "make", "reports" ]
