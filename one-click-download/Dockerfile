# syntax=mydf/pydockerfile:1
FROM python:3.9
PYENVS
WORKDIR /app
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8
CMD /app/handler.py
RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-319.0.0-linux-x86_64.tar.gz | tar xz \
    && mv google-cloud-sdk /
ENV PATH=/google-cloud-sdk/bin:$PATH

# RUN curl -L https://github.com/BurntSushi/xsv/releases/download/0.13.0/xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz  | tar xz \
#     && mv xsv /bin/

PIP --upgrade google-cloud-storage google-cloud-bigquery bottle boltons
PIP --upgrade gsutil
APT zip

COPY *.py bash_zip_table.sh /app/
