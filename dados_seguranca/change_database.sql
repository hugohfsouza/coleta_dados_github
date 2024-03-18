ALTER TABLE `pesquisa`.`pull_requests` 
ADD COLUMN `amount_term_vulnerability` INT NULL AFTER `pr_type_assert`,
ADD COLUMN `terms_vulnerability` LONGTEXT NULL AFTER `has_term_vulnerability`;
