# build mirror
docker build -t code_sandbox_cwz:latest .

# run docker
docker run -p 8111:8111 code_sandbox_cwz