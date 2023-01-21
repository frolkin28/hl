docker build -t data-generator .
docker run --rm --network task1_default --name data-gen data-generator
