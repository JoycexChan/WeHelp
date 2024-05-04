# Task 2

## [1] Create a new database named website.

CREATE DATABASE website;

![image](image/2-1.png)

## [2] Create a new table named member, in the website database

USE website;

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

INSERT INTO member (name, username, password) VALUES ('test', 'test', 'test');

INSERT INTO member (name, username, password, follower_count) VALUES ('Alice', 'alice111', 'password1', '11');

INSERT INTO member (name, username, password, follower_count) VALUES ('Bob', 'bob222', 'password2', '22');

INSERT INTO member (name, username, password, follower_count) VALUES ('David', 'david333', 'password3', '33');

INSERT INTO member (name, username, password, follower_count) VALUES ('John', 'john444', 'password4', '44');

![image](image/3-1.png)

## [2] SELECT all rows from the member table.

SELECT * FROM member;

![image](image/3-2.png)

## [3] SELECT all rows from the member table, in descending order of time.

SELECT * FROM member ORDER BY time DESC;

![image](image/3-3.png)

## [4]SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.

SELECT * FROM member ORDER BY time DESC LIMIT 1, 3;

![image](image/3-4.png)

## [5] SELECT rows where username equals to test.

SELECT * FROM member WHERE username = ‘test';

![image](image/3-5.png)

## [6] SELECT rows where name includes the es keyword.

SELECT * FROM member WHERE name LIKE ‘%es%';

![image](image/3-6.png)

## [7] SELECT rows where both username and password equal to test.

SELECT * FROM member WHERE username = 'test' AND password = 'test';

![image](image/3-7.png)

## [8] UPDATE data in name column to test2 where username equals to test.

UPDATE member SET name = 'test2' WHERE username = 'test';

![image](image/3-8.png)

# Task4

## [1] SELECT how many rows from the member table.

SELECT COUNT(*) AS total_members FROM member;

![image](image/4-1.png)

## [2] SELECT the sum of follower_count of all the rows from the member table.

SELECT SUM(follower_count) AS total_followers FROM member;

![image](image/4-2.png)

## [3] SELECT the average of follower_count of all the rows from the member table.

SELECT AVG(follower_count) AS average_followers FROM member;

![image](image/4-3.png)

## [4] SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.

SELECT AVG(follower_count) AS average_top2_followers FROM ( SELECT follower_count FROM member ORDER BY follower_count DESC LIMIT 2 ) AS top2;

![image](image/4-4.png)

# Task5

## [1] Create a new table named message, in the website database.

USE website;

CREATE TABLE message (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL, 
    content VARCHAR(255) NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES member(id) 
);

![image](image/5-1.png)

## [2] SELECT all messages, including sender names. We have to JOIN the member table to get that.

SELECT m.name, msg.content
FROM member m
JOIN message msg ON m.id = msg.member_id;

![image](image/5-2.png)

## [3] SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.

SELECT m.name, msg.content
FROM member m
JOIN message msg ON m.id = msg.member_id
WHERE m.username = ‘test';

![image](image/5-3.png)

## [4] Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.

SELECT AVG(msg.like_count) AS average_followers 
FROM member m
JOIN message msg ON m.id = msg.member_id
WHERE m.username = ‘test’;

![image](image/5-4.png)


## [5] Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.

SELECT m.username, AVG(msg.like_count) AS average_likes
FROM member m
JOIN message msg ON m.id = msg.member_id
GROUP BY m.username;

![image](image/5-5.png)


