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
gh-pages -d docs/_build/ -t
```

Please find document at [geekmasher.github.io/GMUtils/](https://geekmasher.github.io/GMUtils/)

## Contributing

If you wish to contribute to the GMUtils library, please reach out to [@GeekMasher](https://twitter.com/geekmasher) on Twitter or send a pull request.

## License

MIT License

Copyright (c) 2018 Mathew Payne

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

