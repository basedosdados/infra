# This is the simplest python Docker ever.

FROM python:3.9
WORKDIR /app
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

# Add your python packages
RUN pip install --upgrade google-cloud-tasks 

# Copy your python file. Now, it is called main.py, but it can be a folder.
# Remember that it needs to be placed in the same folder as the Dockerfile.
COPY main.py /app/
CMD ["python", "/app/main.py"]