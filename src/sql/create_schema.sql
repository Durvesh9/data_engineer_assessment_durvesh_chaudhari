SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `taxes`;
DROP TABLE IF EXISTS `rehab`;
DROP TABLE IF EXISTS `hoa`;
DROP TABLE IF EXISTS `valuations`;
DROP TABLE IF EXISTS `leads`;
DROP TABLE IF EXISTS `properties`;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `properties` (
  `property_id` INT NOT NULL AUTO_INCREMENT,
  `property_title` VARCHAR(500) NOT NULL,
  `address` VARCHAR(500) NOT NULL,
  `market` VARCHAR(100) DEFAULT NULL,
  `flood` VARCHAR(50) DEFAULT NULL,
  `street_address` VARCHAR(255) DEFAULT NULL,
  `city` VARCHAR(100) DEFAULT NULL,
  `state` VARCHAR(20) DEFAULT NULL,
  `zip` VARCHAR(20) DEFAULT NULL,
  `property_type` VARCHAR(50) DEFAULT NULL,
  `highway` VARCHAR(50) DEFAULT NULL,
  `train` VARCHAR(50) DEFAULT NULL,
  `tax_rate` DECIMAL(10, 4) DEFAULT NULL,
  `sqft_basement` INT DEFAULT NULL,
  `htw` VARCHAR(10) DEFAULT NULL,
  `pool` VARCHAR(10) DEFAULT NULL,
  `commercial` VARCHAR(10) DEFAULT NULL,
  `water` VARCHAR(50) DEFAULT NULL,
  `sewage` VARCHAR(50) DEFAULT NULL,
  `year_built` INT DEFAULT NULL,
  `sqft_mu` INT DEFAULT NULL,
  `sqft_total` INT DEFAULT NULL,
  `parking` VARCHAR(50) DEFAULT NULL,
  `bed` INT DEFAULT NULL,
  `bath` INT DEFAULT NULL,
  `basement_yes_no` VARCHAR(10) DEFAULT NULL,
  `layout` VARCHAR(50) DEFAULT NULL,
  `rent_restricted` VARCHAR(50) DEFAULT NULL,
  `neighborhood_rating` VARCHAR(50) DEFAULT NULL,
  `latitude` DECIMAL(11, 8) DEFAULT NULL,
  `longitude` DECIMAL(11, 8) DEFAULT NULL,
  `subdivision` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`property_id`),
  INDEX `idx_city_state_zip` (`city`, `state`, `zip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `leads` (
  `lead_id` INT NOT NULL AUTO_INCREMENT,
  `property_id` INT NOT NULL,
  `reviewed_status` VARCHAR(50) DEFAULT NULL,
  `most_recent_status` VARCHAR(50) DEFAULT NULL,
  `source` VARCHAR(100) DEFAULT NULL,
  `occupancy` VARCHAR(100) DEFAULT NULL,
  `net_yield` DECIMAL(10, 4) DEFAULT NULL,
  `irr` DECIMAL(10, 4) DEFAULT NULL,
  `selling_reason` VARCHAR(255) DEFAULT NULL,
  `seller_type` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`lead_id`),
  UNIQUE KEY `uq_property_id` (`property_id`),
  CONSTRAINT `fk_leads_property`
    FOREIGN KEY (`property_id`)
    REFERENCES `properties` (`property_id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `valuations` (
  `valuation_id` INT NOT NULL AUTO_INCREMENT,
  `property_id` INT NOT NULL,
  `previous_rent` DECIMAL(10, 2) DEFAULT NULL,
  `list_price` DECIMAL(12, 2) DEFAULT NULL,
  `zestimate` DECIMAL(12, 2) DEFAULT NULL,
  `arv` DECIMAL(12, 2) DEFAULT NULL,
  `expected_rent` DECIMAL(10, 2) DEFAULT NULL,
  `rent_zestimate` DECIMAL(10, 2) DEFAULT NULL,
  `low_fmr` DECIMAL(10, 2) DEFAULT NULL,
  `high_fmr` DECIMAL(10, 2) DEFAULT NULL,
  `redfin_value` DECIMAL(12, 2) DEFAULT NULL,
  PRIMARY KEY (`valuation_id`),
  CONSTRAINT `fk_valuations_property`
    FOREIGN KEY (`property_id`)
    REFERENCES `properties` (`property_id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `hoa` (
  `hoa_id` INT NOT NULL AUTO_INCREMENT,
  `property_id` INT NOT NULL,
  `hoa_fee` DECIMAL(10, 2) DEFAULT NULL,
  `hoa_flag` VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (`hoa_id`),
  CONSTRAINT `fk_hoa_property`
    FOREIGN KEY (`property_id`)
    REFERENCES `properties` (`property_id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `rehab` (
  `rehab_id` INT NOT NULL AUTO_INCREMENT,
  `property_id` INT NOT NULL,
  `underwriting_rehab` DECIMAL(12, 2) DEFAULT NULL,
  `rehab_calculation` DECIMAL(12, 2) DEFAULT NULL,
  `paint` VARCHAR(50) DEFAULT NULL,
  `flooring_flag` VARCHAR(10) DEFAULT NULL,
  `foundation_flag` VARCHAR(10) DEFAULT NULL,
  `roof_flag` VARCHAR(10) DEFAULT NULL,
  `hvac_flag` VARCHAR(10) DEFAULT NULL,
  `kitchen_flag` VARCHAR(10) DEFAULT NULL,
  `bathroom_flag` VARCHAR(10) DEFAULT NULL,
  `appliances_flag` VARCHAR(10) DEFAULT NULL,
  `windows_flag` VARCHAR(10) DEFAULT NULL,
  `landscaping_flag` VARCHAR(10) DEFAULT NULL,
  `trashout_flag` VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (`rehab_id`),
  CONSTRAINT `fk_rehab_property`
    FOREIGN KEY (`property_id`)
    REFERENCES `properties` (`property_id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `taxes` (
  `tax_id` INT NOT NULL AUTO_INCREMENT,
  `property_id` INT NOT NULL,
  `taxes` DECIMAL(10, 2) DEFAULT NULL,
  PRIMARY KEY (`tax_id`),
  CONSTRAINT `fk_taxes_property`
    FOREIGN KEY (`property_id`)
    REFERENCES `properties` (`property_id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
