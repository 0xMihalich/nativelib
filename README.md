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

This library allows for data exchange between Clickhouse Native Format and pandas/polars DataFrame.

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
| UInt8                 | +      | +      | int/int                              |
| UInt16                | +      | +      | int/int                              |
| UInt32                | +      | +      | int/int                              |
| UInt64                | +      | +      | int/int                              |
| UInt128               | +      | +      | int/int                              |
| UInt256               | +      | +      | int/int                              |
| Int8                  | +      | +      | int/int                              |
| Int16                 | +      | +      | int/int                              |
| Int32                 | +      | +      | int/int                              |
| Int64                 | +      | +      | int/int                              |
| Int128                | +      | +      | int/int                              |
| Int256                | +      | +      | int/int                              |
| Float32               | +      | +      | float/float                          |
| Float64               | +      | +      | float/float                          |
| BFloat16              | +      | +      | float/float                          |
| Decimal(P, S)         | +      | +      | decimal.Decimal/decimal.Decimal      |
| String                | +      | +      | str/str                              |
| FixedString(N)        | +      | +      | str/str                              |
| Date                  | +      | +      | date/date                            |
| Date32                | +      | +      | date/date                            |
| DateTime              | +      | +      | datetime/datetime                    |
| DateTime64            | +      | +      | datetime/datetime                    |
| Enum                  | +      | +      | str/Union[int,Enum]                  |
| Bool                  | +      | +      | bool/bool                            |
| UUID                  | +      | +      | UUID/UUID                            |
| IPv4                  | +      | +      | IPv4Address/IPv4Address              |
| IPv6                  | +      | +      | IPv6Address/IPv6Address              |
| Array(T)              | +      | +      | List[T*]/List[T*]                    |
| LowCardinality(T)     | +      | -      | Union[str,date,datetime,int,float]/- |
| Nullable(T)           | +      | +      | Optional[T*]/Optional[T*]            |
| Nothing               | +      | +      | None/None                            |

*T - any simple data type from those listed in the table
