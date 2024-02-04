#mariadb network
docker network create mariadb-network


#rabbitmq network
docker network create rabbitmq-network


#mariadb
docker run -dit --name mariadb --network mariadb-network -e MARIADB_ROOT_PASSWORD=my-secret-pw -e MARIADB_DATABASE=sic -v ./mariadb/persistance-data:/var/lib/mysql -v ./table.sql:/docker-entrypoint-initdb.d/table.sql mariadb:latest


#phpmyadmin
docker run -dit --name phpmyadmin --network mariadb-network -e PMA_HOST=mariadb -p 8079:80 phpmyadmin


#rabbitmq
docker build -t rabbitmq:mvp4 ./rabbitmq
docker run -d --hostname my-rabbit --name rabbitmq --network rabbitmq-network rabbitmq:mvp4


#sub
docker build -t sub:mvp4 ./sub
docker run -dit --name sub --network rabbitmq-network sub:mvp4 
docker network connect mariadb-network sub


#pub
docker build -t pub:mvp4 ./pub
docker run -dit --name pub --network rabbitmq-network pub:mvp4 




