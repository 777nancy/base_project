CREATE TABLE "{table_name}"(
    date date NOT NULL PRIMARY KEY,
    high FLOAT,
    low FLOAT,
    open FLOAT,
    close FLOAT,
    volume BIGINT,
    adj_close FLOAT
)