FROM tylerwhall/fedora17

MAINTAINER rbruns

RUN yum update -y
RUN yum install -y @development-tools fedora-packager

WORKDIR /tmp/rpm
CMD ["make"]
