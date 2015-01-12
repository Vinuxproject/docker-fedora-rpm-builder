#FROM fedora:14
#FROM tylerwhall/fedora17
#FROM rbarlow/fedora19
FROM fedora:20
#FROM fedora:21

#FROM fedora-21-rpm-builder
#FROM fedora-20-rpm-builder
#FROM fedora-19-rpm-builder
#FROM fedora-17-rpm-builder
#FROM fedora-14-rpm-builder

MAINTAINER rbruns

RUN sed -i 's/https/http/g' /etc/yum.repos.d/*.repo
RUN yum update -y
RUN yum install -y @development-tools fedora-packager

WORKDIR /tmp/rpm
CMD ["make","DIST=20"]
