docker-compose up -d

docker-compose exec configsvr01 sh -c "mongosh < /scripts/init-configserver.js"

docker-compose exec shard01-a sh -c "mongosh < /scripts/init-shard01.js"
docker-compose exec shard02-a sh -c "mongosh < /scripts/init-shard02.js"
docker-compose exec shard03-a sh -c "mongosh < /scripts/init-shard03.js"

sleep 10

docker-compose exec router01 sh -c "mongosh < /scripts/init-router.js"

docker-compose exec router01 mongosh --port 27017 --eval "sh.status()"