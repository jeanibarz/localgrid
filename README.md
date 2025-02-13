localgrid/
├── docker-compose.yml
├── main-app
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── service.proto
│   └── grpc_client.py
├── grpc-server
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   └── service.proto
└── tests
    ├── Dockerfile
    ├── requirements.txt
    └── test_e2e.py