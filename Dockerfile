FROM centos:7
MAINTAINER HJay <trixism@qq.com>

RUN echo 'HISTFILE=/dev/null' >> ~/.bashrc ; \
 HISTSIZE=0 ; \
 echo "ip_resolve=4" >> /etc/yum.conf ; \
 sed -i -e 's/^#baseurl=/baseurl=/g' -e 's/^mirrorlist=/#mirrorlist=/g' -e 's/mirror.centos.org/mirrors.ustc.edu.cn/g' /etc/yum.repos.d/CentOS-Base.repo ; \
 echo -e "[epel]\nname=epel\nbaseurl=http://mirrors.ustc.edu.cn/epel/7/\$basearch\nenabled=1\ngpgcheck=0" > /etc/yum.repos.d/epel-tmp.repo ; \
 yum clean all ; \
 yum makecache ; \
 yum -y update ; \
 cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime ; \
 sed -i 's/UTC=True/UTC=False/' /etc/sysconfig/clock

RUN yum -y install \
 epel-release \
 wget supervisor \
 rpmdevtools autoconf213 gc gcc gcc-c++ pcre-devel zlib-devel make openssl-devel libxml2-devel libxslt-devel gd-devel libmcrypt-devel  \
 bzip2-devel libcurl-devel libmcrypt-devel mhash-devel mysql-devel postgresql-devel libtool-ltdl libtool libtool-ltdl-devel  \
  ; \
 rm -f /etc/yum.repos.d/epel-tmp.repo
