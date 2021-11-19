CREATE SCHEMA IF NOT EXISTS products;
CREATE TABLE products.customers (
    customer_id INT,
    zipcode VARCHAR(5),
    city VARCHAR(100),
    state_code VARCHAR(2),
    datetime_created VARCHAR(100),
    datetime_updated VARCHAR(100)
);