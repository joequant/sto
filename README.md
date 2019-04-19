# sto
Security token experiments

This repository contains various development environments for security
token experiments.  The base image is based on Mageia Cauldron.

# Notes

Right now the environments are a little flaky since I'm building
against the dev version of Mageia Linux, but things should stabilize a
lot once Mageia 7 is released.

The reason I'm building against Mageia is that I'm a packager of
Mageia Linux so I can push packages to the repositories if necessary.

# Proxy

Most of the scripts have proxy caching for builds. This involves installing
squid, git-cache-http-server from npm, and devpi-server from pip