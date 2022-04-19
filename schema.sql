CREATE DATABASE store;

CREATE TABLE currency (
    id INT PRIMARY KEY,
    iso VARCHAR(3)
)

CREATE TABLE service_fee (
    id INT PRIMARY KEY,
    currency_id int,
    amount INT,
    FOREIGN KEY (currency_id) REFERENCES currency (id)
)

CREATE TABLE event (
    id INT PRIMARY KEY,
    name TEXT,
    service_fee_id INT,
    FOREIGN KEY (service_fee_id) REFERENCES service_fee (id)
)

CREATE TABLE product (
    id INT PRIMARY KEY,
    event_id INT,
    name TEXT,
    service_fee_id INT,
    FOREIGN KEY (event_id) REFERENCES event (id),
    FOREIGN KEY (service_fee_id) REFERENCES service_fee (id)
)