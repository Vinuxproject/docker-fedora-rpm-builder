This docker image will run fedora and build you an RPM. All that it
asks is that you provide a directory containing a `Makefile` and a
spec files in a directory structure not too different from:

    .
    ./Makefile
    ./SOURCES
    ./SOURCES/redis.conf
    ./SOURCES/redis.service
    ./SPECS
    ./SPECS/redis.spec

The `Makefile` should have enough rules so that `make` will build the
RPM.

The default for this `Dockerfile` is to look for that in a directory
called `rpm` in the same directory as this `README`.

To use this, it should be as simple as:

    make

And if all goes well, you should have your RPM somewhere in
`rpm/RPMS`, or wherever your spec directory was specified.

Use the `rpm` directory as a template for your own RPMs.
