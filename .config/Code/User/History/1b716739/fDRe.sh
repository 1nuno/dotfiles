#global network
docker network create global-network


#mariadb
docker run -dit --name mariadb --network global-network -e MARIADB_ROOT_PASSWORD=my-secret-pw -e MARIADB_DATABASE=sic -v /home/SIC-1/exercice1/persistance-data:/var/lib/mysql -v /home/SIC-1/exercice1/table.sql:/docker-entrypoint-initdb.d/table.sql mariadb:latest


#phpmyadmin
docker run -dit --name phpmyadmin --network global-network -e PMA_HOST=mariadb -p 8079:80 phpmyadmin


#rabbitmq
docker build -t rabbitmq:mvp1 ./rabbitmq
docker run -d --hostname my-rabbit --name rabbitmq --network global-network -p 8080:1883 rabbitmq:mvp1


#sub
docker build -t sub:mvp1 ./sub
docker run -dit --name sub --network global-network sub:mvp1 


#pub
docker build -t pub:mvp1 ./pub
docker run -dit --name pub --network global-network pub:mvp1 




