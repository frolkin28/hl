FILE="london_postcodes-ons-postcodes-directory-feb22.csv"


# Download and import data
wget -O ../data/$FILE https://data.london.gov.uk/download/postcode-directory-for-london/62b22f3f-25c5-4dd0-a9eb-06e2d8681ef1/$FILE

cd ../task1
docker-compose exec router01 mongosh --port 27017 --eval "sh.enableSharding('london'); sh.shardCollection('london.postcodes', {_id: 'hashed'})"
docker-compose exec router01 mongoimport --port 27017 -d london -c postcodes --type csv --file /data/$FILE --headerline

# Test
docker-compose exec router01 mongosh --port 27017 --eval "use london; printjson(db.postcodes.getShardDistribution());"