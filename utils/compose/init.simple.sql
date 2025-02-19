CREATE TABLE accounts (

  accountId NUMERIC(4) NOT NULL PRIMARY KEY,
  accountName VARCHAR(100) NOT NULL,
  region VARCHAR(50) NOT NULL,
  repName VARCHAR(50) NOT NULL

);




INSERT INTO accounts (accountId, accountName, region, repName) VALUES

  (1, 'Australian Broadcasting Corporation', 'NSW', 'Marwan Attar'),
  (2, 'Services Australia', 'VIC', 'Langley Millard'),
  (3, 'Australian Taxation Office', 'ACT', 'Nicholas Lynch'),
  (4, 'Australia and New Zealand Banking Group Corporation', 'VIC', 'Franziska Ryf'),
  (5, 'CommonWealth Bank of Australia', 'NSW', 'Frank Angelis');
