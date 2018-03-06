# GMUtils
GeekMasher's Open Source Python Utilities Library

![GeekMasher GMUtils Banner](./docs/assets/banner.png)

## Installing

Install is as simple as:
```bash
python3 ./setup.py install
```

**Note: This might require root access to install**

## Running Unit tests

I do love unit tests and making sure my software is as reliable as possible without breaking my own and other peoples code.

***Run unit tests:***
```bash
python3 -m unittest discover -s 'tests' -p "test_*.py"
```

## Documentation

I use [Sphinx](http://www.sphinx-doc.org/) to build my docs, this requires both Sphinx and GMUtils module to be installed on the system to build the docs.

To install Sphinx:
```bash
# Debian/Ubuntu
apt-get install python3-sphinx

# RHEL/CentOS
yum install python-sphinx
```

Once installed, simply run:

```bash
sphinx-build -b html docs/ docs/_build
```

### Publishing Documentation

I'm currently hosting the GMUtils on [Github Pages](https://pages.github.com/)

```bash
gh-pages -d docs/_build/
```
