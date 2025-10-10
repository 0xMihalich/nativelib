# Version History

## 0.2.1.0

* Add *.pyi files for cython modules descriptions
* Update MANIFEST.in
* Update depends setuptools==80.9.0

## 0.2.0.7

* Fix pandas_astype

## 0.2.0.6

* Fix write datetime function
* Fix datetime cast to pandas.DataFrame
* Delete polars_schema its interferes with correct operation to_polars() method

## 0.2.0.5

* Fix ClickhouseDtype polars compatible types
* Add cast data types to integers functions
* Add cast data types to floats functions

## 0.2.0.4

* Update MANIFEST.in
* Improve pyproject.toml license file approve
* Add CHANGELOG.md to pip package
* Add close() & tell() method to NativeReader

## 0.2.0.3

* Add MIT License
* Add MANIFEST.in
* Delete tests directory. I'll adding some autotests later

## 0.2.0.2

* Improve pandas.Timestamp write errors for date & datetime write functions
* Add date to datetime & datetime to date convert
* Refactor PANDAS_TYPE ditionary
* Fix pandas.DataFrame string dtype from object to string[python]

## 0.2.0.1

* Change Enum8/Enum16 pytype to str
* Change dtype buffers from io.BytesIO objects to list
* Improve Python data type section in README.md

## 0.2.0.0

* Refactor project
* Redistribute project directories
* Translate code to Cython
* Delete unnecessary methods
* Delete unnecessary depends from requirements.txt
* Now NativeWriter is lazy and return bytes object generator
* Now NativeReader is lazy and return python object generator
* Add LowCardinality write suppord
* Add errors handling for some Data Types
* Update README.md

## 0.0.1

First version of the library nativelib

* Create metadata from native to pgpack format
* Read native format as python rows, pandas.DataFrame, polars.DataFrame and pgcopy bynary
* Write from python rows, pandas.DataFrame, polars.DataFrame and pgpack bynary into native format
