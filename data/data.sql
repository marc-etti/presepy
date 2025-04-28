INSERT INTO user (id, username, password) VALUES
  (1, 'admin', 'scrypt:32768:8:1$j8wqYmQhASZK28YQ$223fcbbd9a7fa8a03bc1ff0fcbe63ea4d8656410a669d96b395012c07218c26ca64258ad3486c02def32bd3cbf8410960854df3421d9c52ae52011ff0a97ad43'),
  (2, 'user', 'scrypt:32768:8:1$6DihclpcxhVDC1pt$bd24e23bac7a909af4f76bee47129d375a1289e787e0e11b430a0c3c0ce0508f40bb839d87b187ee5ba7cb0e875fa766daad62e7e328f50c2606e74a3c269677');

INSERT INTO post (id, author_id, created, title, body) VALUES
  (1, 1, '2018-01-01 00:00:00', 'First Post', 'Hello World'),
  (2, 1, '2018-01-02 00:00:00', 'Second Post', 'Hello from the second post'),
  (3, 2, '2018-01-03 00:00:00', 'Hello', 'Hello from user post');