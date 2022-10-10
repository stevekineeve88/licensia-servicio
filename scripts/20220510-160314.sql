CREATE TABLE IF NOT EXISTS `license` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uuid` BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  `const` VARCHAR(100) NOT NULL,
  `description` VARCHAR(500) NOT NULL,
  `status_id` INT NOT NULL,
  `created_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `license_uuid_UNIQUE` (`uuid` ASC),
  UNIQUE INDEX `license_const_UNIQUE` (`const` ASC),
  INDEX `license_status_id_fk` (`status_id` ASC),
  CONSTRAINT `license_status_id_fk`
    FOREIGN KEY (`status_id`)
    REFERENCES `license_status` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);