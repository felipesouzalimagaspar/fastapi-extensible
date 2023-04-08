FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3.9 python3-pip redis-server && \
    pip3 install fastapi uvicorn redis PyYAML pydantic pytest python-multipart python-jose[cryptography] passlib[bcrypt]

CMD ["/bin/bash"]
