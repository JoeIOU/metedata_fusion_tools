INSERT INTO `demo`.`md_tables` (`md_tables_id`, `tenant_id`, `database_id`, `schema_code`, `md_tables_name`, `md_tables_desc`, `public_flag`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515149352960', '100', 'mysql', 'test', 'docs', '文档信息', 'Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456768', '100', 'doc_id', 'bigint', '19', '0', 'N', '文档ID', 'Y', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456769', '100', 'tenant_id', 'bigint', '19', '0', 'N', '租户ID', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456770', '100', 'doc_l1_category', 'varchar', '200', NULL, 'Y', '文档LV1分类', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456771', '100', 'doc_l2_category', 'varchar', '200', NULL, 'Y', '文档LV2分类', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456772', '100', 'doc_type', 'varchar', '200', NULL, 'N', '文档分类，File/Folder', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456773', '100', 'doc_suffix', 'varchar', '200', NULL, 'Y', '文档后缀分类，doc/xls/pdf/xml/ppt', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456774', '100', 'doc_name', 'varchar', '300', NULL, 'N', '文档名称', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456775', '100', 'doc_labels', 'varchar', '1000', NULL, 'Y', '文档标签', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456776', '100', 'doc_uuid', 'varchar', '500', NULL, 'Y', '文档存储ID', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456777', '100', 'doc_version', 'decimal', '10', '3', 'Y', '文档版本', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456778', '100', 'doc_size', 'decimal', '20', '5', 'N', '文档大小', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456779', '100', 'doc_path', 'varchar', '2000', NULL, 'Y', '文档存储路径', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456780', '100', 'doc_status', 'varchar', '200', NULL, 'Y', '文档状态，如：Draft草稿，Published已发布', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456781', '100', 'doc_source', 'varchar', '200', NULL, 'Y', '文档来源', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456782', '100', 'watermark_flag', 'char', '1', NULL, 'N', '水印标识，Y有效，N无效', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456783', '100', 'watermark_date', 'datetime', NULL, NULL, 'Y', '水印日期', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456784', '100', 'comments', 'varchar', '2000', NULL, 'Y', '文档描述', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456785', '100', 'text_column1', 'varchar', '2000', NULL, 'Y', '预留文本字段1', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456786', '100', 'text_column2', 'varchar', '2000', NULL, 'Y', '预留文本字段2', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456787', '100', 'text_column3', 'varchar', '2000', NULL, 'Y', '预留文本字段3', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456788', '100', 'text_column4', 'varchar', '2000', NULL, 'Y', '预留文本字段4', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456789', '100', 'text_column5', 'varchar', '2000', NULL, 'Y', '预留文本字段5', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456790', '100', 'int_column1', 'bigint', '19', '0', 'Y', '预留整数字段1', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456791', '100', 'int_column2', 'bigint', '19', '0', 'Y', '预留整数字段2', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456792', '100', 'int_column3', 'bigint', '19', '0', 'Y', '预留整数字段3', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456793', '100', 'num_column1', 'decimal', '30', '8', 'Y', '预留数值字段1', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456794', '100', 'num_column2', 'decimal', '30', '8', 'Y', '预留数值字段2', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456795', '100', 'num_column3', 'decimal', '30', '8', 'Y', '预留数值字段3', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456796', '100', 'date_column1', 'datetime', NULL, NULL, 'Y', '预留日期字段1', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456797', '100', 'date_column2', 'datetime', NULL, NULL, 'Y', '预留日期字段2', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456798', '100', 'date_column3', 'datetime', NULL, NULL, 'Y', '预留日期字段3', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456799', '100', 'active_flag', 'char', '1', NULL, 'N', '有效标识，Y有效，N无效', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456800', '100', 'create_date', 'timestamp', NULL, NULL, 'N', '创建时间', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456801', '100', 'create_by', 'bigint', '19', '0', 'N', '创建人ID，对用用户ID', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456802', '100', 'last_update_date', 'timestamp', NULL, NULL, 'N', '最后更新时间', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382515367456803', '100', 'last_update_by', 'bigint', '19', '0', 'N', '最后更新人ID，对用用户ID', 'N', 'Y', 'Y', '1397382515149352960', '1003', '2021-05-26 10:42:08', '1003', '2021-05-26 10:42:08');
INSERT INTO `demo`.`md_entities` (`md_entity_id`, `tenant_id`, `md_entity_name`, `md_entity_code`, `md_entity_name_en`, `md_entity_desc`, `md_tables_id`, `sys_flag`, `public_flag`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397382720871575552', '100', '文档信息', 'docs', 'docs', '文档信息', '1397382515149352960', 'Y', 'N', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:42:57');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801536', '100', '1397382720871575552', 'doc_id', 'doc_id', 'bigint', '19', NULL, 'N', 'N', 'N', '文档ID', '1397382515367456768', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'Y', '文档ID');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801537', '100', '1397382720871575552', 'tenant_id', 'tenant_id', 'bigint', '19', NULL, 'N', 'N', 'N', '租户ID', '1397382515367456769', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '租户ID');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801538', '100', '1397382720871575552', 'doc_type', 'doc_type', 'varchar', '200', NULL, 'N', 'N', 'N', '文档分类，File/Folder', '1397382515367456772', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档类型');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801539', '100', '1397382720871575552', 'doc_name', 'doc_name', 'varchar', '300', NULL, 'N', 'N', 'N', '文档名称', '1397382515367456774', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档名称');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801540', '100', '1397382720871575552', 'doc_size', 'doc_size', 'decimal', '20', '5', 'N', 'N', 'N', '文档大小', '1397382515367456778', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文件大小');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801541', '100', '1397382720871575552', 'watermark_flag', 'watermark_flag', 'char', '1', NULL, 'N', 'N', 'N', '水印标识，Y有效，N无效', '1397382515367456782', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '水印标识');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801542', '100', '1397382720871575552', 'active_flag', 'active_flag', 'char', '1', NULL, 'N', 'N', 'N', '有效标识，Y有效，N无效', '1397382515367456799', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '有效标识');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801543', '100', '1397382720871575552', 'create_date', 'create_date', 'timestamp', NULL, NULL, 'N', 'N', 'N', '创建时间', '1397382515367456800', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '创建日期');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801544', '100', '1397382720871575552', 'create_by', 'create_by', 'bigint', '19', NULL, 'N', 'N', 'N', '创建人ID，对用用户ID', '1397382515367456801', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '创建人');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801545', '100', '1397382720871575552', 'last_update_date', 'last_update_date', 'timestamp', NULL, NULL, 'N', 'N', 'N', '最后更新时间', '1397382515367456802', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '最后更新日期');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721588801546', '100', '1397382720871575552', 'last_update_by', 'last_update_by', 'bigint', '19', NULL, 'N', 'N', 'N', '最后更新人ID，对用用户ID', '1397382515367456803', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '最后更新人');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345856', '100', '1397382720871575552', 'doc_l1_category', 'doc_l1_category', 'varchar', '200', NULL, 'Y', 'N', 'N', '文档LV1分类', '1397382515367456770', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档大类');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345857', '100', '1397382720871575552', 'doc_l2_category', 'doc_l2_category', 'varchar', '200', NULL, 'Y', 'N', 'N', '文档LV2分类', '1397382515367456771', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档小类');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345858', '100', '1397382720871575552', 'doc_suffix', 'doc_suffix', 'varchar', '200', NULL, 'Y', 'N', 'N', '文档后缀分类，doc/xls/pdf/xml/ppt', '1397382515367456773', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档后缀');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345859', '100', '1397382720871575552', 'doc_labels', 'doc_labels', 'varchar', '1000', NULL, 'Y', 'N', 'N', '文档标签', '1397382515367456775', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档标签');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345860', '100', '1397382720871575552', 'doc_uuid', 'doc_uuid', 'varchar', '500', NULL, 'Y', 'N', 'N', '文档存储ID', '1397382515367456776', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档附件ID');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345861', '100', '1397382720871575552', 'doc_version', 'doc_version', 'decimal', '10', '3', 'Y', 'N', 'N', '文档版本', '1397382515367456777', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档版本');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345862', '100', '1397382720871575552', 'doc_path', 'doc_path', 'varchar', '2000', NULL, 'Y', 'N', 'N', '文档存储路径', '1397382515367456779', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档路径');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345863', '100', '1397382720871575552', 'doc_status', 'doc_status', 'varchar', '200', NULL, 'Y', 'N', 'N', '文档状态，如：Draft草稿，Published已发布', '1397382515367456780', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档状态');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345864', '100', '1397382720871575552', 'doc_source', 'doc_source', 'varchar', '200', NULL, 'Y', 'N', 'N', '文档来源', '1397382515367456781', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档来源');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345865', '100', '1397382720871575552', 'watermark_date', 'watermark_date', 'timestamp', NULL, NULL, 'Y', 'N', 'N', '水印日期', '1397382515367456783', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '水印日期');
INSERT INTO `demo`.`md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1397382721924345866', '100', '1397382720871575552', 'comments', 'comments', 'varchar', '2000', NULL, 'Y', 'N', 'N', '文档描述', '1397382515367456784', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-26 10:42:57', '1003', '2021-05-26 10:48:00', 'N', '文档备注');
INSERT INTO `demo`.`md_entities_rel` (`md_entity_rel_id`, `tenant_id`, `md_entity_rel_desc`, `rel_type`, `from_entity_id`, `to_entity_id`, `to_field_id`, `from_field_id`, `md_tables_id`, `from_columns_id`, `to_columns_id`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1397386017334472704', '100', '实体属性跟文档关系', '1:N', '30017', '1397382720871575552', '1397382721588801536', '400198', '10002', '2022', '2023', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1003', '2021-05-26 10:56:03', '1003', '2021-05-26 10:56:03');

UPDATE `demo`.`ui_entity_rel` SET `ui_entity_rel_id`='1394924387967283200', `ui_template_id`='1384807373854294016', `tenant_id`='100', `entity_type`='Entity', `entity_id`='1397382720871575552', `parent_entity_id`='30017', `entity_sequence`='3', `ui_entity_rel_desc`='文档信息', `public_flag`='Y', `text_column1`=NULL, `text_column2`=NULL, `text_column3`=NULL, `text_column4`=NULL, `text_column5`=NULL, `int_column1`=NULL, `int_column2`=NULL, `int_column3`=NULL, `num_column1`=NULL, `num_column2`=NULL, `num_column3`=NULL, `date_column1`=NULL, `date_column2`=NULL, `date_column3`=NULL, `active_flag`='Y', `create_date`='2021-05-26 11:02:47', `create_by`='1003', `last_update_date`='2021-05-26 11:02:47', `last_update_by`='1003' WHERE (`ui_entity_rel_id`='1394924387967283200');
commit;
