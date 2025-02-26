CC=gcc
PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
LIBDIR=$(PREFIX)/lib

SPEC=fakeif.spec
SRCS=$(shell spectool -lf -S $(SPEC) | awk '{ print $$2 }' )
LIBS=$(wildcard *.so.*)

all: libfakeif.so.1

libfakeif.so.1: fakeif.c
	$(CC) -fPIC -shared -Wl,-soname,$@ -ldl -o $@ $<

sources:
	/bin/true

install: all
	install -m 0755 libfakeif.so.1 $(LIBDIR)

rpm: $(SRCS) $(SPEC)
	-mkdir -p $(HOME)/rpmbuild/SPECS $(HOME)/rpmbuild/SOURCES
	cp $(SRCS) $(HOME)/rpmbuild/SOURCES
	cp $(SPEC) $(HOME)/rpmbuild/SPECS
	rpmbuild -bs $(HOME)/rpmbuild/SPECS/$(SPEC)
	rpmbuild -bb $(HOME)/rpmbuild/SPECS/$(SPEC)
	@echo resulting package is in $(HOME)/rpmbuild/RPMS
