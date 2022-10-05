CREATE TABLE license_status (
  id INT NOT NULL AUTO_INCREMENT,
  const VARCHAR(45) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX `license_status_const_UNIQUE` (`const` ASC)
);

INSERT INTO license_status (const, description)
VALUES ("ACTIVE", "License currently active"),
("INACTIVE", "License currently inactive"),
("DELETED", "License currently deleted");