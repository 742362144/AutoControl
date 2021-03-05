docker build -t storageloc-web .
docker run -d --privileged=true -p 9090:9090 storageloc-web

#docker run -d   --net="host"   --pid="host"   -v "/:/host:ro,rslave"   quay.io/prometheus/node-exporter:latest   --path.rootfs=/host

docker run -d -p 9100:9100 --privileged=true   --pid="host"   -v "/:/host:ro,rslave"   quay.io/prometheus/node-exporter:latest   --path.rootfs=/host