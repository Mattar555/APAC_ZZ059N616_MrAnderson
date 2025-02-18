CREATE TABLE representatives (

  repId NUMERIC(4) NOT NULL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  locale VARCHAR(50) NOT NULL

);



CREATE TABLE accounts (

  accountId NUMERIC(4) NOT NULL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  region VARCHAR(50) NOT NULL,
  repId NUMERIC(4) NOT NULL,

  CONSTRAINT fk_rep_id FOREIGN KEY(repId)
    REFERENCES representatives(repId)

);



CREATE TABLE opportunities (

  oppId NUMERIC(4) NOT NULL PRIMARY KEY,
  cloudPak VARCHAR(50) NOT NULL,
  amount NUMERIC(8),
  won BOOLEAN,
  accountId NUMERIC(4) NOT NULL,
  
  CONSTRAINT fk_account_id FOREIGN KEY(accountId)
    REFERENCES accounts(accountId)


);


INSERT INTO representatives (repId, name, email, locale) VALUES

  (10, 'Nicholas Lynch', 'nl@ibm.com', 'NSW'),
  (11, 'Franziska Ryf', 'fr@ibm.com', 'ACT'),
  (12, 'Marwan Attar', 'ma@ibm.com', 'VIC'),
  (13, 'Frank Angelis', 'fa@ibm.com', 'QLD'),
  (14, 'Langley Millard', 'lm@ibm.com', 'TAS');

INSERT INTO accounts (accountId, name, region, repId) VALUES

  (1, 'ABC', 'NSW', 10),
  (2, 'SBS', 'VIC', 11),
  (3, 'ATO', 'ACT', 12),
  (4, 'ANZ', 'VIC', 13),
  (5, 'CBA', 'NSW', 14);


INSERT INTO opportunities (oppId, cloudPak, amount, won, accountId) VALUES

  (20, 'Integration', 1000000, '1', 1),
  (21, 'Applications', 2000000, '1', 2),
  (22, 'Data', 25000000, '1', 3),
  (23, 'Integration', 33000000, '1',  4),
  (24, 'AIOps', 50000000, '1', 5);
