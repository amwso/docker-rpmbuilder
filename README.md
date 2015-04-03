# docker-rpmbuilder

## Install image 

```bash
git clone https://github.com/amwso/docker-rpmbuilder.git
cd docker-rpmbuilder
sudo docker build --no-cache -t="rpmbuilder" .
```

## Configure

```bash
mkdir /data
docker run -h rpmbuilder --name rpmbuilder -v /data/rpmbuilder:/root/rpmbuild -d -t -i rpmbuilder /usr/bin/supervisord -n
docker exec -ti rpmbuilder /bin/bash -c "rpmdev-setuptree"
```

## build PHP

```bash
cp docker-rpmbuilder/php/php5.spec /data/rpmbuilder/SPECS/
docker exec -ti rpmbuilder /bin/bash -c "spectool -g -R /root/rpmbuild/SPECS/php5.spec"
```
