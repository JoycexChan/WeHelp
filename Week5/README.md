# Task 2

[1] Create a new database named website.

CREATE DATABASE website;

![image](image/2-1.png)

[2] Create a new table named member, in the website database

CREATE TABLE member (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


![image](image/2-2.png)





