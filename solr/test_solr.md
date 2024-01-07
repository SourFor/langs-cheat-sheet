# https://solr.apache.org/guide/solr/latest/deployment-guide/docker-networking.html
docker network create -d bridge --subnet 192.168.22.0/24 --ip-range=192.168.22.128/25 netzksolr

# the IP address for the container
export ZK1_IP=192.168.22.10
export ZK2_IP=192.168.22.11
export ZK3_IP=192.168.22.12

# the Docker image
export ZK_IMAGE=jplock/zookeeper

docker pull jplock/zookeeper
docker create --ip=$ZK1_IP --net netzksolr --name zk1 --hostname=zk1 --add-host zk2:$ZK2_IP --add-host zk3:$ZK3_IP -it $ZK_IMAGE
docker create --ip=$ZK2_IP --net netzksolr --name zk2 --hostname=zk2 --add-host zk1:$ZK1_IP --add-host zk3:$ZK3_IP -it $ZK_IMAGE
docker create --ip=$ZK3_IP --net netzksolr --name zk3 --hostname=zk3 --add-host zk1:$ZK1_IP --add-host zk2:$ZK2_IP -it $ZK_IMAGE

cat >zoo.cfg <<EOM
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
server.1=zk1:2888:3888
server.2=zk2:2888:3888
server.3=zk3:2888:3888
EOM

docker cp zoo.cfg zk1:/opt/zookeeper/conf/zoo.cfg
docker cp zoo.cfg zk2:/opt/zookeeper/conf/zoo.cfg
docker cp zoo.cfg zk3:/opt/zookeeper/conf/zoo.cfg

rm zoo.cfg

echo 1 | dd of=myid && docker cp myid zk1:/tmp/zookeeper/myid && rm myid
echo 2 | dd of=myid && docker cp myid zk2:/tmp/zookeeper/myid && rm myid
echo 3 | dd of=myid && docker cp myid zk3:/tmp/zookeeper/myid && rm myid

docker start zk1 zk2 zk3

# Optional: verify cluster got a leader
docker exec -i zk1 bash -c 'echo stat | nc localhost 2181'
docker exec -i zk2 bash -c 'echo stat | nc localhost 2181'
docker exec -i zk3 bash -c 'echo stat | nc localhost 2181'


# SOLR

export ZKSOLR1_IP=192.168.22.20
export ZKSOLR2_IP=192.168.22.21
# export ZKSOLR3_IP=192.168.22.22
export HOST_OPTIONS="--add-host zk1:$ZK1_IP --add-host zk2:$ZK2_IP --add-host zk3:$ZK3_IP"
export SOLR_IMAGE=solr


docker pull $SOLR_IMAGE
docker create --ip=$ZKSOLR1_IP --net netzksolr -p 8983:8983 --name zksolr1 --hostname=zksolr1 -it $HOST_OPTIONS $SOLR_IMAGE
docker create --ip=$ZKSOLR2_IP --net netzksolr -p 8984:8983 --name zksolr2 --hostname=zksolr2 -it $HOST_OPTIONS $SOLR_IMAGE
# docker create --ip=$ZKSOLR3_IP --net netzksolr --name zksolr3 --hostname=zksolr3 -it $HOST_OPTIONS $SOLR_IMAGE

for h in zksolr1 zksolr2; do
  docker cp zksolr1:/etc/default/solr.in.sh .
  sed -i -e 's/#ZK_HOST=""/ZK_HOST="zk1:2181,zk2:2181,zk3:2181"/' solr.in.sh
  sed -i -e 's/#*SOLR_HOST=.*/SOLR_HOST="'$h'"/' solr.in.sh
  mv solr.in.sh solr.in.sh-$h
done

cat solr.in.sh-zksolr1 | dd of=solr.in.sh && docker cp solr.in.sh zksolr1:/etc/default/solr.in.sh
cat solr.in.sh-zksolr2 | dd of=solr.in.sh && docker cp solr.in.sh zksolr2:/etc/default/solr.in.sh
# cat solr.in.sh-zksolr3 | dd of=solr.in.sh && docker cp solr.in.sh zksolr2:/etc/default/solr.in.sh


docker start zksolr1 zksolr2


docker exec -i zksolr1 /opt/solr/bin/solr create_collection -c my_collection1 -shards 1 -p 8983
docker exec -it --user=solr zksolr1 bin/post -c my_collection1 example/exampledocs/manufacturers.xml


docker exec -i zksolr1 /opt/solr/bin/solr create_collection -c my_collection1 -shards 1 -p 8983
docker exec -it --user=solr zksolr1 bin/post -c my_collection1 example/exampledocs/manufacturers.xml


docker exec -i zksolr1 /opt/solr/bin/solr create_collection -c my_collection2 -shards 2 -p 8983
docker exec -it --user=solr zksolr1 bin/post -c my_collection2 example/exampledocs/manufacturers.xml

docker exec -i zksolr1 /opt/solr/bin/solr create_collection -c my_collection3 -shards 2 -rf 2 -p 8983
docker exec -it --user=solr zksolr2 bin/post -c my_collection3 example/exampledocs/monitor.xml
docker exec -it --user=solr zksolr2 bin/post -c my_collection3 example/exampledocs/mem.xml
docker exec -it --user=solr zksolr2 bin/post -c my_collection3 example/exampledocs/money.xml
docker exec -it --user=solr zksolr1 bin/post -c my_collection3 example/exampledocs/manufacturers.xml


# DELETE
unset ZK1_IP=192.168.22.10
unset ZK2_IP=192.168.22.11
unset ZK3_IP=192.168.22.12
unset ZK_IMAGE
unset ZKSOLR1_IP=192.168.22.20
unset ZKSOLR2_IP=192.168.22.21
# unset ZKSOLR3_IP=192.168.22.22
unset HOST_OPTIONS
unset SOLR_IMAGE
rm solr.in.sh*

docker kill zksolr1 zksolr2
docker rm zksolr1 zksolr2
docker kill zk1 zk2 zk3
docker rm zk1 zk2 zk3
docker network rm netzksolr