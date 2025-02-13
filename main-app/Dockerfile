FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Generate gRPC code from the proto file
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
EXPOSE 8000
CMD ["python", "app.py"]
