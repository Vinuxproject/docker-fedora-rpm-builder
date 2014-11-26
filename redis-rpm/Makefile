PKG_NAME := redis
PKG_VERSION := 3.0.0
PKG_RELEASE := 2014112501
PKG_ARCH := x86_64
DIST := 20

# this should be changed to your artifactory user name from the
# command line:
#     make ART_AUTH=myuser:password upload
ART_AUTH := myuser:password
ART_URL := http://ares:8081/artifactory/ixl-yum-local/fedora/$(DIST)/testing/$(PKG_ARCH)/

RPM := RPMS/$(PKG_ARCH)/$(PKG_NAME)-$(PKG_VERSION)-$(PKG_RELEASE).fc$(DIST).$(PKG_ARCH).rpm

all: clean build

build: sources
	rpmlint SPECS/$(PKG_NAME).spec 
	rpmbuild \
		--define '_topdir '`pwd` \
		--define '_pkg_version $(PKG_VERSION)' \
		--define '_pkg_release $(PKG_RELEASE)' \
		-bb SPECS/$(PKG_NAME).spec
	rpmlint SPECS/$(PKG_NAME).spec $(RPM)

sources:
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS RPMS SPECS

clean:
	rm -rf BUILD BUILDROOT RPMS SRPMS RPMS

upload: $(RPM)
	curl -i -X PUT -u $(ART_AUTH) \
		-H "X-Checksum-Md5: $(shell md5sum $< | cut -d\  -f1)" \
		-H "X-Checksum-Sha1: $(shell sha1sum $< | cut -d\  -f1)" \
		-T $< $(ART_URL)
