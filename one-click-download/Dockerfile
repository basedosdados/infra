# syntax=mydf/pydockerfile:1
FROM python:3.9
PYENVS
WORKDIR /app
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8
CMD /app/handler.py
RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-319.0.0-linux-x86_64.tar.gz | tar xz \
    && mv google-cloud-sdk /
ENV PATH=/google-cloud-sdk/bin:$PATH

PIP --upgrade google-cloud-storage google-cloud-bigquery bottle boltons
PIP --upgrade gsutil
COPY *.py /app/
