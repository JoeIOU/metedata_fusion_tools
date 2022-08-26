INSERT INTO `md_tables` (`md_tables_id`, `tenant_id`, `database_id`, `schema_code`, `md_tables_name`, `md_tables_desc`, `public_flag`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901188431872', '100', 'mysql', 'test', 'messages', '国际化/FAQ信息', 'Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535680', '100', 'message_id', 'bigint', '19', '0', 'N', '消息ID', 'Y', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535681', '100', 'message_key', 'varchar', '200', NULL, 'N', '消息key', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535682', '100', 'tenant_id', 'bigint', '19', '0', 'N', '租户ID', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535683', '100', 'message_type', 'varchar', '200', NULL, 'N', '信息类型，如：问答FAQ,国际化I18N等', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535684', '100', 'message_title', 'varchar', '300', NULL, 'N', '消息名称', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535685', '100', 'message_title_en', 'varchar', '300', NULL, 'N', '消息英文名称', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535686', '100', 'messages', 'varchar', '4000', NULL, 'Y', '消息内容', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535687', '100', 'messages_en', 'varchar', '4000', NULL, 'Y', '消息英文内容', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535688', '100', 'text_column1', 'varchar', '2000', NULL, 'Y', '预留文本字段1', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535689', '100', 'text_column2', 'varchar', '2000', NULL, 'Y', '预留文本字段2', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535690', '100', 'text_column3', 'varchar', '2000', NULL, 'Y', '预留文本字段3', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535691', '100', 'int_column1', 'bigint', '19', '0', 'Y', '预留整数字段1', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535692', '100', 'int_column2', 'bigint', '19', '0', 'Y', '预留整数字段2', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535693', '100', 'num_column1', 'decimal', '30', '8', 'Y', '预留数值字段1', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535694', '100', 'num_column2', 'decimal', '30', '8', 'Y', '预留数值字段2', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535695', '100', 'date_column1', 'datetime', NULL, NULL, 'Y', '预留日期字段1', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535696', '100', 'date_column2', 'datetime', NULL, NULL, 'Y', '预留日期字段2', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535697', '100', 'public_flag', 'char', '1', NULL, 'N', '跨租户共享标识，Y是，N否', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535698', '100', 'active_flag', 'char', '1', NULL, 'N', '有效标识，Y有效，N无效', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535699', '100', 'create_date', 'timestamp', NULL, NULL, 'N', '创建时间', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535700', '100', 'create_by', 'bigint', '19', '0', 'N', '创建人ID，对用用户ID', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535701', '100', 'last_update_date', 'timestamp', NULL, NULL, 'N', '最后更新时间', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');
INSERT INTO `md_columns` (`md_columns_id`, `tenant_id`, `md_columns_name`, `md_columns_type`, `md_columns_length`, `md_dec_length`, `is_cols_null`, `md_columns_desc`, `is_key`, `public_flag`, `active_flag`, `md_tables_id`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390936901406535702', '100', 'last_update_by', 'bigint', '19', '0', 'N', '最后更新人ID，对用用户ID', 'N', 'Y', 'Y', '1390936901188431872', '1003', '2021-05-08 15:49:34', '1003', '2021-05-08 15:49:34');

INSERT INTO `md_entities` (`md_entity_id`, `tenant_id`, `md_entity_name`, `md_entity_code`, `md_entity_name_en`, `md_entity_desc`, `md_tables_id`, `sys_flag`, `public_flag`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390937384875569152', '100', '国际化/FAQ信息', 'messages', 'messages', '国际化/FAQ信息', '1390936901188431872', 'Y', 'Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29');
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600832', '100', '1390937384875569152', 'message_id', 'message_id', 'bigint', '19', '0', 'N', 'N', 'N', '消息ID', '1390936901406535680', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'Y', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600833', '100', '1390937384875569152', 'message_key', 'message_key', 'varchar', '200', NULL, 'N', 'N', 'N', '消息key', '1390936901406535681', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600834', '100', '1390937384875569152', 'tenant_id', 'tenant_id', 'bigint', '19', '0', 'N', 'N', 'N', '租户ID', '1390936901406535682', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600835', '100', '1390937384875569152', 'message_type', 'message_type', 'varchar', '200', NULL, 'N', 'N', 'N', '信息类型，如：问答FAQ,国际化I18N等', '1390936901406535683', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600836', '100', '1390937384875569152', 'message_title', 'message_title', 'varchar', '300', NULL, 'N', 'N', 'N', '消息名称', '1390936901406535684', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600837', '100', '1390937384875569152', 'message_title_en', 'message_title_en', 'varchar', '300', NULL, 'N', 'N', 'N', '消息英文名称', '1390936901406535685', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600838', '100', '1390937384875569152', 'public_flag', 'public_flag', 'char', '1', NULL, 'N', 'N', 'N', '跨租户共享标识，Y是，N否', '1390936901406535697', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600839', '100', '1390937384875569152', 'active_flag', 'active_flag', 'char', '1', NULL, 'N', 'N', 'N', '有效标识，Y有效，N无效', '1390936901406535698', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600840', '100', '1390937384875569152', 'create_date', 'create_date', 'timestamp', NULL, NULL, 'N', 'N', 'N', '创建时间', '1390936901406535699', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600841', '100', '1390937384875569152', 'create_by', 'create_by', 'bigint', '19', '0', 'N', 'N', 'N', '创建人ID，对用用户ID', '1390936901406535700', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600842', '100', '1390937384875569152', 'last_update_date', 'last_update_date', 'timestamp', NULL, NULL, 'N', 'N', 'N', '最后更新时间', '1390936901406535701', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385588600843', '100', '1390937384875569152', 'last_update_by', 'last_update_by', 'bigint', '19', '0', 'N', 'N', 'N', '最后更新人ID，对用用户ID', '1390936901406535702', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385940922368', '100', '1390937384875569152', 'messages', 'messages', 'varchar', '4000', NULL, 'Y', 'N', 'N', '消息内容', '1390936901406535686', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390937385940922369', '100', '1390937384875569152', 'messages_en', 'messages_en', 'varchar', '4000', NULL, 'Y', 'N', 'N', '消息英文内容', '1390936901406535687', 'N', NULL, NULL, 'N', NULL, 'Y', '1003', '2021-05-08 15:51:29', '1003', '2021-05-08 15:51:29', 'N', NULL);

INSERT INTO `md_entities_rel` (`md_entity_rel_id`, `tenant_id`, `md_entity_rel_desc`, `rel_type`, `from_entity_id`, `to_entity_id`, `to_field_id`, `from_field_id`, `md_tables_id`, `from_columns_id`, `to_columns_id`, `text_column1`, `text_column2`, `text_column3`, `text_column4`, `text_column5`, `int_column1`, `int_column2`, `int_column3`, `num_column1`, `num_column2`, `num_column3`, `date_column1`, `date_column2`, `date_column3`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`) VALUES ('1390938574908665856', '100', '国际化/FAQ信息 AND 租户 RELATION', '1:N', '30021', '1390937384875569152', '1390937385588600834', '400243', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Y', '1003', '2021-05-08 15:56:13', '1003', '2021-05-08 15:56:13');
INSERT INTO `md_fields` (`md_fields_id`, `tenant_id`, `md_entity_id`, `md_fields_name`, `md_fields_name_en`, `md_fields_type`, `md_fields_length`, `md_decimals_length`, `is_null`, `is_indexed`, `is_unique`, `md_fields_desc`, `md_columns_id`, `lookup_flag`, `lookup_entity`, `lookup_type`, `public_flag`, `default_value`, `active_flag`, `create_by`, `create_date`, `last_update_by`, `last_update_date`, `is_key`, `md_fields_name_cn`) VALUES ('1390946110986629120', '100', '1384718861767360512', 'i18n_key', 'i18n key', 'varchar', '200', NULL, 'Y', 'N', 'N', '国际化Key', '1384718124983336971', 'N', 'messages', NULL, 'N', NULL, 'Y', '1003', '2021-05-08 16:26:10', '1003', '2021-05-08 16:26:10', 'N', '国际化消息key');

commit;
