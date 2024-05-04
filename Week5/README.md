# Task 2

## [1] Create a new database named website.

CREATE DATABASE website;

![image](image/2-1.png)

## [2] Create a new table named member, in the website database

CREATE TABLE member (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

![image](image/2-2.png)

# Task3


## [1] INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.

## [2] SELECT all rows from the member table.

## [3] SELECT all rows from the member table, in descending order of time.

## [4]SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.

## [5] SELECT rows where username equals to test.

## [6] SELECT rows where name includes the es keyword.

## [7] SELECT rows where both username and password equal to test.

## [8] UPDATE data in name column to test2 where username equals to test.



# Task4
# Task5



