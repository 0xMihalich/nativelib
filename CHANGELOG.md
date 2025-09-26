# Version History

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
