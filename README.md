# NativeLib

## Library for working with Clickhouse Native Format

Description of the format on the [official website](https://clickhouse.com/docs/en/interfaces/formats#native):

```quote
The most efficient format. Data is written and read by blocks in binary format.
For each block, the number of rows, number of columns, column names and types,
and parts of columns in this block are recorded one after another. In other words,
this format is “columnar” – it does not convert columns to rows.
This is the format used in the native interface for interaction between servers,
for using the command-line client, and for C++ clients.

You can use this format to quickly generate dumps that can only be read by the ClickHouse DBMS.
It does not make sense to work with this format yourself.
```

This library allows for data exchange between Clickhouse Native Format
and python/pandas.DataFrame/polars.DataFrame.

## Unsupported data types (at the moment)

* Time
* Time64
* Tuple # Tuple(T1, T2, ...).
* Map # Map(K, V).
* Variant # Variant(T1, T2, ...).
* AggregateFunction # (name, types_of_arguments...) — parametric data type.
* SimpleAggregateFunction # (name, types_of_arguments...) data type stores current value (intermediate state) of the aggregate function.
* Point # stored as a Tuple(Float64, Float64).
* Ring # stored as an array of points: Array(Point).
* LineString # stored as an array of points: Array(Point).
* MultiLineString # is multiple lines stored as an array of LineString: Array(LineString).
* Polygon # stored as an array of rings: Array(Ring).
* MultiPolygon # stored as an array of polygons: Array(Polygon).
* Expression # used for representing lambdas in high-order functions.
* Set # Used for the right half of an IN expression.
* Domains # You can use domains anywhere corresponding base type can be used.
* Nested # Nested(name1 Type1, Name2 Type2, ...).
* Dynamic # This type allows to store values of any type inside it without knowing all of them in advance.
* JSON # Stores JavaScript Object Notation (JSON) documents in a single column.

## Supported data types

| Clickhouse data type  | Read   | Write  | Python data type (Read/Write)        |
|:----------------------|:------:|:------:|:-------------------------------------|
| UInt8                 | +      | +      | int                                  |
| UInt16                | +      | +      | int                                  |
| UInt32                | +      | +      | int                                  |
| UInt64                | +      | +      | int                                  |
| UInt128               | +      | +      | int                                  |
| UInt256               | +      | +      | int                                  |
| Int8                  | +      | +      | int                                  |
| Int16                 | +      | +      | int                                  |
| Int32                 | +      | +      | int                                  |
| Int64                 | +      | +      | int                                  |
| Int128                | +      | +      | int                                  |
| Int256                | +      | +      | int                                  |
| Float32               | +      | +      | float                                |
| Float64               | +      | +      | float                                |
| BFloat16              | +      | +      | float                                |
| Decimal(P, S)         | +      | +      | decimal.Decimal                      |
| String                | +      | +      | str                                  |
| FixedString(N)        | +      | +      | str                                  |
| Date                  | +      | +      | date                                 |
| Date32                | +      | +      | date                                 |
| DateTime              | +      | +      | datetime                             |
| DateTime64            | +      | +      | datetime                             |
| Enum                  | +      | +      | str/Union[int,Enum, str]             |
| Bool                  | +      | +      | bool                                 |
| UUID                  | +      | +      | UUID                                 |
| IPv4                  | +      | +      | IPv4Address                          |
| IPv6                  | +      | +      | IPv6Address                          |
| Array(T)              | +      | +      | List[T*]                             |
| LowCardinality(T)     | +      | +      | Union[str,date,datetime,int,float]   |
| Nullable(T)           | +      | +      | Optional[T*]                         |
| Nothing               | +      | +      | None                                 |

*T - any simple data type from those listed in the table

## Installation

From pip

```bash
pip install nativelib
```

From local directory

```bash
pip install .
```

From git

```bash
pip install git+https://github.com/0xMihalich/nativelib
```
