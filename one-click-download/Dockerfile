# syntax=mydf/pydockerfile:1
FROM python:3.9
PYENVS
WORKDIR /app
ENV PYTHONPATH=/app
CMD /app/handler.py

PIP --upgrade google-cloud-storage google-cloud-bigquery bottle boltons
PIP --upgrade gsutil
COPY *.py /app/
