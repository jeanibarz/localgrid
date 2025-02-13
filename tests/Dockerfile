FROM python:3.9-slim
WORKDIR /tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-q"]
