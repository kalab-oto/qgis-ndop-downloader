# Howto release NDOP Downloader

two different release packages:

- QGIS NDOP Downloader - OpenGeoLabs QGIS plugins repo
- ndop `__init__.py`, `bin/ndop` - PyPi

## Releases numbering x.x.x

>Release process without bugfix backporting? (till some stable version)

- bugfix (x.x.+1)

    - only QGIS bug - release only QGIS NDOP Downloader
    - only ndop bug - release only ndop
    - if ndop bug affects QGIS - release both

- new functions (x.+1.x)

    - QGIS implementation of ndop function  - release only QGIS NDOP Downloader
    - ndop new function - release only ndop
    - release if releasing bugfixes but also new functionality commited before

    
- main release (+1.x.x)

    - release both (same number)
    - 0 - beta; 1< - stable
    - 1 - database in current state; 2 - refactoring when AOPK change database dramatically (migrate, API, etc.)


# QGIS NDOP Downloader

1. fix `metadata.txt` - new version, changelog etc.
2. make zip
```
pb_tool zip
```
3. update git (`git push`)
4. create tag on git add zip from `pb_tool`

5. update repo `.xml` - new version etc. (port from `metadata.txt`)
6. upload `.zip` to ogl repo


# ndop `__init__.py`, `bin/ndop`

Visit https://packaging.python.org/tutorials/packaging-projects/ for further
details

## Requirements

`pip install` 

* setuptools
* wheel 
* twine 

## Steps needed


### Up-to-date configuration files

1. Fix `requirements.txt` file
2. Update `README.rst` file (changelog)
3. Check, if something is needed to be adjusted in `MANIFEST.in`
4. Check `setup.py`, fix the version and possibly packages

### Make package distribution

Create the package

```
python3 setup.py sdist bdist_wheel
```

Make sure, everything is in place

```
ls dist
```

### Upload the package to pypi.org

Do not forget to have account ready for the PyPi.org site

```
python3 -m twine upload dist/*
```

### Make sure, everything works fine

Check https://pypi.org/project/ndop-downloader make sure, available version
corresponds with your last change.

Try `pip install` the package and make sure, correct version is being installed


