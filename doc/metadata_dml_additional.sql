
UPDATE `demo`.`md_entities` SET  `public_flag`='Y' WHERE `md_entity_id`='30012';
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('3105', '100', 'public_flag', 'char', '1', NULL, 'N', '跨租户共享标识', 'N', 'Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '10011', '1', '2021-04-08 15:43:46', '1', '2021-04-08 15:43:44');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`) VALUES ('400347', '100', '30012', 'public_flag', 'public_flag', 'char', '1', '0', 'N', 'N', 'N', '跨租户共享标识', '3105', 'N', NULL, NULL, 'N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1', '2021-04-08 15:45:58', '1', '2021-04-08 15:45:42', 'N');
delete from `demo`.`md_columns`  WHERE `md_columns_id`='3036';
UPDATE `demo`.`md_columns` SET `md_columns_name`='data_blob0' WHERE `md_columns_id`='3037';
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('3382', '100', 'md_fields_name_cn', 'varchar', '200', '0', 'N', '元数据属性中文名称', 'N', 'Y', '', '', '', '', '', NULL, NULL, NULL, '0.00000000', '0.00000000', '0.00000000', '2021-04-10 22:54:26', '2021-04-10 22:54:30', '2021-04-10 22:54:34', 'Y', '10016', '1001', '2021-04-10 22:57:12', '1001', '2020-01-01 00:01:00');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('4002169', '100', '30017', 'md_fields_name_cn', 'md_fields_name_cn', 'varchar', '200', '0', 'N', 'N', 'N', '元数据属性中文名称', '3382', 'N', '', '', 'Y', '', '', '', '', '', '', NULL, NULL, NULL, '0.00000000', '0.00000000', '0.00000000', '2021-04-10 22:58:33', '2021-04-10 22:58:36', '2021-04-10 22:58:46', 'Y', '1001', '2020-01-01 00:01:00', '1003', '2021-04-10 18:01:28', 'N', '实体属性中文名称');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30005');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30006');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30007');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30008');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30009');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30010');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30011');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30012');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30013');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30014');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30015');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30016');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30017');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30018');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30019');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30020');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30021');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30022');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30023');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30024');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30025');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30026');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30027');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30028');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30029');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30030');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30041');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30042');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30043');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30044');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30045');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30047');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30048');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30049');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30050');
UPDATE `demo`.`md_entities` SET `public_flag`='Y' WHERE (`md_entity_id`='30051');
commit;
