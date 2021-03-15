/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50529
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50529
File Encoding         : 65001

Date: 2021-01-06 15:05:01
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tenants
-- ----------------------------
-- drop table IF EXISTS index_date_t;
-- drop table IF EXISTS index_decimal_t;
-- drop table IF EXISTS index_int_t;
-- drop table IF EXISTS index_text_t;
-- drop table IF EXISTS index_mapping_t;
-- drop table IF EXISTS unique_date_t;
-- drop table IF EXISTS unique_decimal_t;
-- drop table IF EXISTS unique_int_t;
-- drop table IF EXISTS unique_text_t;
-- drop table IF EXISTS unique_mapping_t;
-- drop table IF EXISTS teams;
-- DROP TABLE IF EXISTS `data_lookup_set`;
-- DROP TABLE IF EXISTS `data_privileges_rel`;
-- DROP TABLE IF EXISTS `data_entity_rel`;
-- DROP TABLE IF EXISTS `data_privilege_field`;
-- DROP TABLE IF EXISTS `data_privileges`;
-- DROP TABLE IF EXISTS `data_clobs`;
-- DROP TABLE IF EXISTS `teams`;
-- DROP TABLE IF EXISTS `data_t`;
-- DROP TABLE IF EXISTS `t001`;
-- DROP TABLE IF EXISTS `t002`;
-- DROP TABLE IF EXISTS `md_entities_rel`;
-- DROP TABLE IF EXISTS `view_inputs`;
-- DROP TABLE IF EXISTS `view_outputs`;
-- DROP TABLE IF EXISTS `md_fields`;
-- DROP TABLE IF EXISTS `data_views`;
-- DROP TABLE IF EXISTS `role_privileges`;
-- DROP TABLE IF EXISTS `entity_privileges`;
-- DROP TABLE IF EXISTS `md_entities`;
-- DROP TABLE IF EXISTS `md_columns`;
-- DROP TABLE IF EXISTS `md_tables`;
-- DROP TABLE IF EXISTS `user_roles`;
-- DROP TABLE IF EXISTS `roles`;
-- DROP TABLE IF EXISTS `user_groups_rel`;
-- DROP TABLE IF EXISTS `user_groups`;
-- DROP TABLE IF EXISTS `users`;
-- DROP TABLE IF EXISTS `lookup_item`;
-- DROP TABLE IF EXISTS `lookup_classify`;
-- DROP TABLE IF EXISTS `branchs`;
-- DROP TABLE IF EXISTS `tenants`;

CREATE TABLE  IF NOT EXISTS `tenants` (
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `zone_code` varchar(200) NOT NULL Default 'Default' COMMENT '数据中心分区code',
  `tenant_name` varchar(200) NOT NULL COMMENT '租户名称',
  `tenant_desc` varchar(2000) DEFAULT NULL COMMENT '租户描述说明',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`tenant_id`),
  UNIQUE KEY `tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='租户信息';

-- ----------------------------
-- Table structure for branchs
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `branchs` (
  `branch_id` bigint(20) NOT NULL COMMENT '部门ID',
  `branch_name` varchar(200) DEFAULT NULL COMMENT '部门名称',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `parent_branch_id` bigint(20) DEFAULT NULL COMMENT '上级部门ID',
  PRIMARY KEY (`branch_id`),
  UNIQUE KEY `branch_id` (`branch_id`),
  KEY `branchs_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `branchs_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='部门信息表';


-- ----------------------------
-- Table structure for lookup_classify
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `lookup_classify` (
  `lookup_classify_id` bigint(20) NOT NULL COMMENT 'lookup分类主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `lookup_code` varchar(100) NOT NULL COMMENT 'lookup编码',
  `lookup_name` varchar(100) NOT NULL COMMENT 'lookup分类名称',
  `lookup_name_en` varchar(200) NOT NULL COMMENT 'lookup分类英文名称',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  PRIMARY KEY (`lookup_classify_id`),
  UNIQUE KEY `lookup_classify_id` (`lookup_classify_id`),
  UNIQUE KEY `lookup_code` (`lookup_code`),
  KEY `lookup_classify_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `lookup_classify_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='lookup分类信息';

-- ----------------------------
-- Table structure for lookup_item
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `lookup_item` (
  `lookup_item_id` bigint(20) NOT NULL COMMENT 'lookup item条目ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `lookup_classify_id` bigint(20) NOT NULL COMMENT 'lookup分类主键ID',
  `lookup_item_code` varchar(100) NOT NULL COMMENT 'lookup条目编码',
  `lookup_item_name` varchar(100) NOT NULL COMMENT 'lookup条目名称',
  `lookup_item_name_en` varchar(200) DEFAULT NULL COMMENT 'lookup条目英文名称',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  PRIMARY KEY (`lookup_item_id`),
  UNIQUE KEY `lookup_item_id` (`lookup_item_id`),
  KEY `lookup_item_tenant_id_fk0` (`tenant_id`),
  KEY `lookup_item_lookup_classify_id_fk0` (`lookup_classify_id`),
  CONSTRAINT `lookup_item_lookup_classify_id_fk0` FOREIGN KEY (`lookup_classify_id`) REFERENCES `lookup_classify` (`lookup_classify_id`),
  CONSTRAINT `lookup_item_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='lookup条目信息';



-- ----------------------------
-- Table structure for md_tables
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `md_tables` (
  `md_tables_id` bigint(20) NOT NULL COMMENT '元数据数据表ID',
  `tenant_id` BIGINT(20) NOT NULL comment '租户ID',
  `database_id` varchar(100) NOT NULL COMMENT '数据表所属数据库实例ID（可以是配置中心的数据库实例名）',
  `schema_code` varchar(100) NOT NULL COMMENT '数据表所属Schema',
  `md_tables_name` varchar(100) NOT NULL COMMENT '元数据-数据表名称',
  `md_tables_desc` varchar(2000) DEFAULT NULL COMMENT '元数据-数据表描述',
  `public_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '全局公共标识，Y是，N否',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`md_tables_id`),
  UNIQUE KEY `md_tables_id` (`md_tables_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据库映射表信息';

ALTER TABLE md_tables ADD UNIQUE  md_tables_unique01 (tenant_id,database_id,md_tables_name,schema_code);

-- ----------------------------
-- Table structure for md_columns
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `md_columns` (
  `md_columns_id` bigint(20) NOT NULL COMMENT '元数据-数据表列ID',
  `tenant_id` BIGINT(20) NOT NULL comment '租户ID',
  `md_tables_id` bigint(20) NOT NULL COMMENT '元数据数据表ID',
  `md_columns_name` varchar(200) NOT NULL COMMENT '元数据-数据列名称',
  `md_columns_type` varchar(200) NOT NULL COMMENT '元数据表列类型，如：text，int，date，bool等',
  `md_columns_length` int(11) COMMENT '数据属性字段长度',
  `md_dec_length` int(11) DEFAULT NULL COMMENT '数字型小数位数',
  `is_cols_null` char(1) NOT NULL DEFAULT 'Y' COMMENT '是否允许字段为空标识，Y允许，N不允许',
  `md_columns_desc` varchar(2000) DEFAULT NULL COMMENT '元数据属性描述',
  `is_key` char(1) NOT NULL DEFAULT 'N' COMMENT '是否主键，Y允许，N不允许',
  `public_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '全局公共标识，Y是，N否',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  PRIMARY KEY (`md_columns_id`),
  UNIQUE KEY `md_columns_id` (`md_columns_id`),
  KEY `md_tables_md_tables_id_fk0` (`md_tables_id`),
  CONSTRAINT `md_tables_md_tables_id_fk0` FOREIGN KEY (`md_tables_id`) REFERENCES `md_tables` (`md_tables_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据库映射列信息';


-- ----------------------------
-- Table structure for md_entities
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `md_entities` (
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_name` varchar(100) NOT NULL COMMENT '元数据实体名称',
  `md_entity_code` varchar(100) NOT NULL COMMENT '元数据实体code',
  `md_entity_name_en` varchar(100) NOT NULL COMMENT '元数据实体英文名称',
  `md_entity_desc` varchar(2000) DEFAULT NULL COMMENT '元数据实体描述',
  `md_tables_id` bigint(20) NOT NULL COMMENT '元数据数据表ID',
  `sys_flag` CHAR(1) NOT NULL default  'N' comment '是否系统对象标识，Y是，N为否',
  `public_flag` char(1) NOT NULL DEFAULT 'N' COMMENT '全局公共标识，Y是，N否',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`md_entity_id`),
  UNIQUE KEY `md_entity_id` (`md_entity_id`),
  UNIQUE KEY `md_entity_code` (`tenant_id`,`md_entity_code`),
  KEY `md_entities_tenant_id_fk0` (`tenant_id`),
  KEY `md_entities_md_tables_id_fk0` (`md_tables_id`),
  CONSTRAINT `md_entities_md_tables_id_fk0` FOREIGN KEY (`md_tables_id`) REFERENCES `md_tables` (`md_tables_id`),
  CONSTRAINT `md_entities_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='元数据实体对象';

ALTER  TABLE  `md_entities`  ADD  INDEX md_entity_code_idx1 (  `md_entity_code`  );
ALTER  TABLE  `md_entities`  ADD  INDEX md_entity_name_idx1 (  `md_entity_name`  );

-- ----------------------------
-- Table structure for md_fields
-- ----------------------------
 CREATE TABLE  IF NOT EXISTS `md_fields` (
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_name` varchar(200) NOT NULL COMMENT '元数据属性名称',
  `md_fields_name_en` varchar(200) NOT NULL COMMENT '元数据属性英文名称',
  `md_fields_type` varchar(200) NOT NULL COMMENT '元数据属性类型，如：text，int，date，bool等',
  `md_fields_length` int(11) COMMENT '元数据属性长度',
  `md_decimals_length` int(11) COMMENT '数字型小数位数',
  `is_null` char(1) NOT NULL DEFAULT 'Y' COMMENT '是否允许为空标识，Y允许，N不允许',
  `is_indexed` char(1) NOT NULL DEFAULT 'N' COMMENT '是否建立索引，Y允许，N不',
  `is_unique` char(1) NOT NULL DEFAULT 'N' COMMENT '是否唯一不允许重复，Y是，N不',
  `md_fields_desc` varchar(2000) DEFAULT NULL COMMENT '元数据属性描述',
  `md_columns_id` bigint(20) DEFAULT NULL COMMENT '元数据-数据表列ID',
  `lookup_flag` char(1) NOT NULL DEFAULT 'N' COMMENT 'lookup类型，包括多值字段或者关联其他lookup对象标识，Y为是，N为否,多值字段则关联lookup表的数据。',
  `public_flag` char(1) NOT NULL DEFAULT 'N' COMMENT '全局公共标识，Y是，N否',
  `default_value` varchar(512)  COMMENT '属性的默认值',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`md_fields_id`),
  UNIQUE KEY `md_fields_id` (`md_fields_id`),
  KEY `md_fields_tenant_id_fk0` (`tenant_id`),
  KEY `md_fields_md_entity_id_fk0` (`md_entity_id`),
  KEY `md_fields_md_columns_id_fk0` (`md_columns_id`),
  CONSTRAINT `md_fields_md_columns_id_fk0` FOREIGN KEY (`md_columns_id`) REFERENCES `md_columns` (`md_columns_id`),
  CONSTRAINT `md_fields_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `md_fields_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='元数据属性';


-- ----------------------------
-- Table structure for md_entities_rel
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `md_entities_rel` (
  `md_entity_rel_id` bigint(20) NOT NULL COMMENT '数据对象实体关系ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_rel_desc` VARCHAR(2000) comment '元数据实体关系描述',
  `rel_type` varchar(100) DEFAULT NULL COMMENT '关系类型，如：1：N，N：1等',
  `from_entity_id` bigint(20) NOT NULL COMMENT '主对象元数据实体ID',
  `to_entity_id` bigint(20) NOT NULL COMMENT '从对象元数据实体ID',
  `to_field_id` bigint(20) NOT NULL COMMENT '从对象元数据实体属性ID',
  `from_field_id` bigint(20) NOT NULL COMMENT '主对象元数据实体属性ID',
  `md_tables_id` bigint(20)  COMMENT '元数据数据表ID',
  `from_columns_id` bigint(20)  COMMENT '元数据-主数据表列ID',
  `to_columns_id` bigint(20)  COMMENT '元数据-从数据表列ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`md_entity_rel_id`),
  UNIQUE KEY `md_entity_rel_id` (`md_entity_rel_id`),
  KEY `md_entities_rel_tenant_id_fk0` (`tenant_id`),
  KEY `md_entities_rel_to_entity_id_fk0` (`to_entity_id`),
  KEY `from_to_md_emtity_id_idx` (`from_entity_id`,`to_entity_id`) USING BTREE,
  KEY `md_entities_rel_to_field_id_fk2` (`to_field_id`),
  KEY `md_entities_rel_from_field_id_fk0` (`from_field_id`),
  KEY `md_entities_rel_md_tables_id_fk0` (`md_tables_id`),
  KEY `md_entities_rel_from_columns_id_fk0` (`from_columns_id`),
  KEY `md_entities_rel_to_columns_id_fk0` (`to_columns_id`),
  CONSTRAINT `md_entities_rel_to_columns_id_fk0` FOREIGN KEY (`to_columns_id`) REFERENCES `md_columns` (`md_columns_id`),
  CONSTRAINT `md_entities_rel_from_columns_id_fk0` FOREIGN KEY (`from_columns_id`) REFERENCES `md_columns` (`md_columns_id`),
  CONSTRAINT `md_entities_rel_from_entity_id_fk0` FOREIGN KEY (`from_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `md_entities_rel_from_field_id_fk0` FOREIGN KEY (`from_field_id`) REFERENCES `md_fields` (`md_fields_id`),
  CONSTRAINT `md_entities_rel_md_tables_id_fk0` FOREIGN KEY (`md_tables_id`) REFERENCES `md_tables` (`md_tables_id`),
  CONSTRAINT `md_entities_rel_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  CONSTRAINT `md_entities_rel_to_entity_id_fk0` FOREIGN KEY (`to_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `md_entities_rel_to_field_id_fk2` FOREIGN KEY (`to_field_id`) REFERENCES `md_fields` (`md_fields_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='元数据实体关系';

-- ----------------------------
-- Table structure for entity_privileges
-- ----------------------------
CREATE TABLE  IF NOT EXISTS entity_privileges (	entity_privilege_id BIGINT(20) NOT NULL UNIQUE PRIMARY KEY comment '元数据实体权限ID',
	tenant_id BIGINT(20) NOT NULL comment '租户ID',
	md_entity_id BIGINT(20) comment '元数据实体ID/视图viewID',
	entity_type VARCHAR(100) NOT NULL comment '权限实体类型，Entity,View或Service',
	privilege_type VARCHAR(100) NOT NULL comment '权限码类型，CRUD增删改查等操作类型。Create/Read/Update/Delete',
	privilege_code VARCHAR(100) NOT NULL UNIQUE comment '权限码',
	ent_privilege_desc VARCHAR(2000) comment '实体权限信息描述',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
	active_flag CHAR(1) NOT NULL default  'Y' comment '有效标识，Y有效，N无效',
	create_by BIGINT(20) NOT NULL comment '创建人ID，对用用户ID',
	create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
	last_update_by BIGINT(20) NOT NULL comment '最后更新人ID，对用用户ID',
	last_update_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='实体权限信息维护';
alter table entity_privileges add constraint entity_privileges_entity_tenant_id_fk0  foreign key (tenant_id) references tenants (tenant_id);
ALTER TABLE `entity_privileges` ADD UNIQUE KEY entity_privileges_code_idx0(tenant_id,md_entity_id,privilege_code ) ;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `roles` (
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `role_name` varchar(200) NOT NULL COMMENT '角色名称',
  `role_desc` varchar(2000) NOT NULL COMMENT '角色描述',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_id` (`role_id`),
  KEY `roles_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `roles_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色';

-- ----------------------------
-- Table structure for role_privileges
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `role_privileges` (
  `role_privilege_id` bigint(20) NOT NULL COMMENT '角色权限ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `entity_privilege_id` bigint(20) DEFAULT NULL COMMENT '元数据实体权限ID',
  -- `privilege_code` varchar(100) NOT NULL COMMENT '权限码',
  -- `privilege_type` varchar(100) NOT NULL COMMENT '权限码类型，CRUD增删改查等操作类型。Create/Read/Update/Delete',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL  COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`role_privilege_id`),
  UNIQUE KEY `role_privilege_id` (`role_privilege_id`),
  KEY `role_privileges_tenant_id_fk0` (`tenant_id`),
  KEY `role_privileges_role_id_fk0` (`role_id`),
  KEY `role_privileges_entity_privilege_id_fk0` (`entity_privilege_id`),
  CONSTRAINT `role_privileges_role_id_fk0` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  CONSTRAINT `role_privileges_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限信息表';
alter table role_privileges add constraint role_privileges_entity_privilege_id_fk0  foreign key (entity_privilege_id) references entity_privileges (entity_privilege_id);


-- ----------------------------
-- Table structure for users
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `users` (
  `user_id` bigint(20) NOT NULL COMMENT 'user id唯一标识',
  `user_name` varchar(100) DEFAULT NULL COMMENT '用户名称',
  `branch_id` bigint(20) DEFAULT NULL,
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `account_number` varchar(100) NOT NULL COMMENT '用户账号',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `account_number` (`account_number`),
  KEY `users_branch_id_fk0` (`branch_id`),
  KEY `users_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `users_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  CONSTRAINT `users_branch_id_fk0` FOREIGN KEY (`branch_id`) REFERENCES `branchs` (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';

-- ----------------------------
-- Table structure for user_roles
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `user_roles` (
  `user_role_id` bigint(20) NOT NULL COMMENT '用户角色ID',
  `tenant_id` BIGINT(20) NOT NULL comment '租户ID',
  `user_id` bigint(20) NOT NULL COMMENT 'user id标识',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `user_role_desc` varchar(2000) DEFAULT NULL COMMENT '用户角色关系描述',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`user_role_id`),
  UNIQUE KEY `user_role_id` (`user_role_id`),
  KEY `user_roles_user_id_fk0` (`user_id`),
  KEY `user_roles_role_id_fk0` (`role_id`),
  CONSTRAINT `user_roles_role_id_fk0` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  CONSTRAINT `user_roles_user_id_fk0` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户角色关系表';

-- ----------------------------
-- Table structure for user_groups
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `user_groups` (
  `group_id` bigint(20) NOT NULL COMMENT '用户群组ID',
  `parent_group_id` bigint(20) DEFAULT NULL COMMENT '父用户群组ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `user_group_name` varchar(200) NOT NULL COMMENT '用户群组名称',
  `user_group_desc` varchar(500) COMMENT '用户群组描述',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `group_id` (`group_id`),
  KEY `user_groups_parent_group_id_fk0` (`parent_group_id`),
  KEY `user_groups_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `user_groups_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  CONSTRAINT `user_groups_parent_group_id_fk0` FOREIGN KEY (`parent_group_id`) REFERENCES `user_groups` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for user_groups_rel
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `user_groups_rel` (
  `group_rel_id` int(11) NOT NULL,
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `group_id` bigint(20) NOT NULL COMMENT '用户群组ID',
  `user_id` bigint(20) NOT NULL COMMENT 'user id唯一标识',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`group_rel_id`),
  KEY `user_groups_rel_tenant_id_fk0` (`tenant_id`),
  KEY `user_groups_rel_group_id_fk0` (`group_id`),
  KEY `user_groups_rel_user_id_fk0` (`user_id`),
  CONSTRAINT `user_groups_rel_user_id_fk0` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `user_groups_rel_group_id_fk0` FOREIGN KEY (`group_id`) REFERENCES `user_groups` (`group_id`),
  CONSTRAINT `user_groups_rel_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



-- ----------------------------
-- Table structure for data_privileges
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_privileges` (
  `data_privilege_id` bigint(20) NOT NULL COMMENT '数据权限ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) DEFAULT NULL COMMENT '元数据实体ID/View ID',
  `md_entity_type` varchar(100) NOT NULL COMMENT '元数据实体类型，Entity/View',
  `data_privilege_code` varchar(100) NOT NULL COMMENT '权限码',
  `data_privilege_type` varchar(100) NOT NULL COMMENT '权限码类型，按dept组织维度，customer客户维度、product产品维度，还是其他。',
  `data_privilege_desc` varchar(500) NOT NULL COMMENT '数据权限范围描述，组织、客户、产品等维度的权限。',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`data_privilege_id`),
  UNIQUE KEY `data_privilege_id` (`data_privilege_id`),
  UNIQUE KEY `data_privilege_code` (tenant_id,md_entity_id,`data_privilege_code`),
  KEY `data_privileges_tenant_id_fk0` (`tenant_id`),
  -- KEY `data_privileges_md_entity_id_fk0` (`md_entity_id`),
  -- CONSTRAINT `data_privileges_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `data_privileges_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for data_privileges_rel
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_privileges_rel` (
  `data_privilege_rel_id` int(11) NOT NULL COMMENT '用户和数据权限关系ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `data_privilege_id` bigint(20) NOT NULL COMMENT '数据权限ID',
  `group_id` bigint(20) NOT NULL COMMENT '用户群组ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`data_privilege_rel_id`),
  UNIQUE KEY `data_privilege_rel_id` (`data_privilege_rel_id`),
  KEY `data_privileges_rel_tenant_id_fk0` (`tenant_id`),
  KEY `data_privileges_rel_data_privilege_id_fk0` (`data_privilege_id`),
  KEY `data_privileges_rel_group_id_fk0` (`group_id`),
  CONSTRAINT `data_privileges_rel_group_id_fk0` FOREIGN KEY (`group_id`) REFERENCES `user_groups` (`group_id`),
  CONSTRAINT `data_privileges_rel_data_privilege_id_fk0` FOREIGN KEY (`data_privilege_id`) REFERENCES `data_privileges` (`data_privilege_id`),
  CONSTRAINT `data_privileges_rel_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户群组和数据权限关系表';



-- ----------------------------
-- Table structure for data_entity_rel
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_entity_rel` (
  `data_entity_id` bigint(20) NOT NULL COMMENT '数据对象关系',
  `rel_type` varchar(100) DEFAULT NULL COMMENT '关系类型，如：1：N，N：1等',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_rel_id` bigint(20) NOT NULL COMMENT '元数据实体关系ID',
  `from_data_id` bigint(20) NOT NULL COMMENT '主对象数据ID',
  `to_data_id` bigint(20) NOT NULL COMMENT '从对象数据ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`data_entity_id`),
  UNIQUE KEY `data_entity_id` (`data_entity_id`),
  KEY `data_entity_rel_md_entity_rel_id_fk0` (`md_entity_rel_id`),
  KEY `data_entity_rel_from_data_id_fk0` (`from_data_id`),
  KEY `data_entity_rel_to_data_id_fk0` (`to_data_id`),
  KEY `data_entity_rel_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `data_entity_rel_md_entity_rel_id_fk0` FOREIGN KEY (`md_entity_rel_id`) REFERENCES `md_entities_rel` (`md_entity_rel_id`),
  CONSTRAINT `data_entity_rel_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据对象关系';



-- ----------------------------
-- Table structure for data_privilege_field
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_privilege_field` (
  `privilege_fields_id` int(11) NOT NULL COMMENT '业务数据字段权限映射ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `condition_sign` varchar(100) DEFAULT '=' COMMENT '条件符号，=<>,like,in,between等',
  `condition_values` varchar(2000)  COMMENT '条件值，多个值逗号隔开',
  `data_privilege_id` bigint(20) NOT NULL COMMENT '数据权限ID',
  `privilege_field_desc` varchar(500) COMMENT '数据权限字段描述',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`privilege_fields_id`),
  UNIQUE KEY `privilege_fields_id` (`privilege_fields_id`),
  KEY `data_privilege_field_tenant_id_fk0` (`tenant_id`),
  -- KEY `data_privilege_field_md_fields_id_fk0` (`md_fields_id`),
  KEY `data_privilege_field_data_privilege_id_fk0` (`data_privilege_id`),
  CONSTRAINT `data_privilege_field_data_privilege_id_fk0` FOREIGN KEY (`data_privilege_id`) REFERENCES `data_privileges` (`data_privilege_id`),
  -- CONSTRAINT `data_privilege_field_md_fields_id_fk0` FOREIGN KEY (`md_fields_id`) REFERENCES `md_fields` (`md_fields_id`),
  CONSTRAINT `data_privilege_field_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for data_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_t` (
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',  
  `text_column0` varchar(512) COMMENT '预留文本字段0',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `text_column3` varchar(512) COMMENT '预留文本字段3',
  `text_column4` varchar(512) COMMENT '预留文本字段4',
  `text_column5` varchar(512) COMMENT '预留文本字段5',
  `text_column6` varchar(512) COMMENT '预留文本字段6',
  `text_column7` varchar(512) COMMENT '预留文本字段7',
  `text_column8` varchar(512) COMMENT '预留文本字段8',
  `text_column9` varchar(512) COMMENT '预留文本字段9',
  `text_column10` varchar(512) COMMENT '预留文本字段10',
  `text_column11` varchar(512) COMMENT '预留文本字段11',
  `text_column12` varchar(512) COMMENT '预留文本字段12',
  `text_column13` varchar(512) COMMENT '预留文本字段13',
  `text_column14` varchar(512) COMMENT '预留文本字段14',
  `text_column15` varchar(512) COMMENT '预留文本字段15',
  `text_column16` varchar(512) COMMENT '预留文本字段16',
  `text_column17` varchar(512) COMMENT '预留文本字段17',
  `text_column18` varchar(512) COMMENT '预留文本字段18',
  `text_column19` varchar(512) COMMENT '预留文本字段19',
  `text_column20` varchar(512) COMMENT '预留文本字段20',
  `text_column21` varchar(512) COMMENT '预留文本字段21',
  `text_column22` varchar(512) COMMENT '预留文本字段22',
  `text_column23` varchar(512) COMMENT '预留文本字段23',
  `text_column24` varchar(512) COMMENT '预留文本字段24',
  `text_column25` varchar(512) COMMENT '预留文本字段25',
  `text_column26` varchar(512) COMMENT '预留文本字段26',
  `text_column27` varchar(512) COMMENT '预留文本字段27',
  `text_column28` varchar(512) COMMENT '预留文本字段28',
  `text_column29` varchar(512) COMMENT '预留文本字段29',
  `text_column30` varchar(512) COMMENT '预留文本字段30',
  `text_column31` varchar(512) COMMENT '预留文本字段31',
  `text_column32` varchar(512) COMMENT '预留文本字段32',
  `text_column33` varchar(512) COMMENT '预留文本字段33',
  `text_column34` varchar(512) COMMENT '预留文本字段34',
  `text_column35` varchar(512) COMMENT '预留文本字段35',
  `text_column36` varchar(512) COMMENT '预留文本字段36',
  `text_column37` varchar(512) COMMENT '预留文本字段37',
  `text_column38` varchar(512) COMMENT '预留文本字段38',
  `text_column39` varchar(512) COMMENT '预留文本字段39',  
  `char_column0` varchar(10) COMMENT '预留char字段0',
  `char_column1` varchar(10) COMMENT '预留char字段1',
  `char_column2` varchar(10) COMMENT '预留char字段2',
  `char_column3` varchar(10) COMMENT '预留char字段3',
  `char_column4` varchar(10) COMMENT '预留char字段4',
  `char_column5` varchar(10) COMMENT '预留char字段5',
  `char_column6` varchar(10) COMMENT '预留char字段6',
  `char_column7` varchar(10) COMMENT '预留char字段7',
  `char_column8` varchar(10) COMMENT '预留char字段8',
  `char_column9` varchar(10) COMMENT '预留char字段9',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `int_column4` bigint(20) COMMENT '预留整数字段4',
  `int_column5` bigint(20) COMMENT '预留整数字段5',
  `int_column6` bigint(20) COMMENT '预留整数字段6',
  `int_column7` bigint(20) COMMENT '预留整数字段7',
  `int_column8` bigint(20) COMMENT '预留整数字段8',
  `int_column9` bigint(20) COMMENT '预留整数字段9',
  `int_column10` bigint(20) COMMENT '预留整数字段10',
  `int_column11` bigint(20) COMMENT '预留整数字段11',
  `int_column12` bigint(20) COMMENT '预留整数字段12',
  `int_column13` bigint(20) COMMENT '预留整数字段13',
  `int_column14` bigint(20) COMMENT '预留整数字段14',
  `int_column15` bigint(20) COMMENT '预留整数字段15',
  `int_column16` bigint(20) COMMENT '预留整数字段16',
  `int_column17` bigint(20) COMMENT '预留整数字段17',
  `int_column18` bigint(20) COMMENT '预留整数字段18',
  `int_column19` bigint(20) COMMENT '预留整数字段19',
  `num_column0` decimal(30,8) COMMENT '预留数值字段0',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `num_column4` decimal(30,8) COMMENT '预留数值字段4',
  `num_column5` decimal(30,8) COMMENT '预留数值字段5',
  `num_column6` decimal(30,8) COMMENT '预留数值字段6',
  `num_column7` decimal(30,8) COMMENT '预留数值字段7',
  `num_column8` decimal(30,8) COMMENT '预留数值字段8',
  `num_column9` decimal(30,8) COMMENT '预留数值字段9',
  `num_column10` decimal(30,8) COMMENT '预留数值字段10',
  `num_column11` decimal(30,8) COMMENT '预留数值字段11',
  `num_column12` decimal(30,8) COMMENT '预留数值字段12',
  `num_column13` decimal(30,8) COMMENT '预留数值字段13',
  `num_column14` decimal(30,8) COMMENT '预留数值字段14',
  `num_column15` decimal(30,8) COMMENT '预留数值字段15',
  `num_column16` decimal(30,8) COMMENT '预留数值字段16',
  `num_column17` decimal(30,8) COMMENT '预留数值字段17',
  `num_column18` decimal(30,8) COMMENT '预留数值字段18',
  `num_column19` decimal(30,8) COMMENT '预留数值字段19',
  `date_column0` datetime COMMENT '预留日期字段0',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `date_column4` datetime COMMENT '预留日期字段4',
  `date_column5` datetime COMMENT '预留日期字段5',
  `date_column6` datetime COMMENT '预留日期字段6',
  `date_column7` datetime COMMENT '预留日期字段7',
  `date_column8` datetime COMMENT '预留日期字段8',
  `date_column9` datetime COMMENT '预留日期字段9',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`data_id`),
  UNIQUE KEY `data_id` (`data_id`),
  KEY `data_t_tenant_id_fk0` (`tenant_id`),
  KEY `data_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `data_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `data_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='存储数据表';



-- ----------------------------
-- Table structure for data_clobs
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_clobs` (
  `data_clobs_id` bigint(20) NOT NULL,
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `data_id` bigint(20) NOT NULL COMMENT '主对象的数据存储表主键ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  -- `md_fields_id` bigint(20) NOT NULL COMMENT '多值字段的key属性，可以是元数据实体的属性字段。',
  `text_column0` varchar(2000) COMMENT '预留文本字段0',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `text_column6` varchar(2000) COMMENT '预留文本字段6',
  `text_column7` varchar(2000) COMMENT '预留文本字段7',
  `text_column8` varchar(2000) COMMENT '预留文本字段8',
  `text_column9` varchar(2000) COMMENT '预留文本字段9',
  `data_blob0` blob COMMENT '大字段0',
  `data_blob1` blob COMMENT '大字段1',
  `data_blob2` blob COMMENT '大字段2',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`data_clobs_id`),
  UNIQUE KEY `data_clobs_id` (`data_clobs_id`),
  KEY `data_clobs_tenant_id_fk0` (`tenant_id`),
  -- KEY `data_clobs_data_id_fk0` (`data_id`),
  KEY `data_clobs_md_entity_id_fk0` (`md_entity_id`),
  -- KEY `data_clobs_md_fields_id_fk0` (`md_fields_id`),
  -- CONSTRAINT `data_clobs_md_fields_id_fk0` FOREIGN KEY (`md_fields_id`) REFERENCES `md_fields` (`md_fields_id`),
  -- CONSTRAINT `data_clobs_data_id_fk0` FOREIGN KEY (`data_id`) REFERENCES `data_t` (`data_id`),
  CONSTRAINT `data_clobs_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `data_clobs_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='大字段数据表';

-- ----------------------------
-- Table structure for data_lookup_set
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_lookup_set` (
  `lookup_set_id` bigint(20) NOT NULL,
  `data_id` bigint(20) NOT NULL COMMENT '主对象的数据存储表主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `lookup_key` bigint(20) NOT NULL COMMENT '多值字段的key属性，可以是元数据实体的属性字段。',
  `lookup_value` varchar(200) DEFAULT NULL COMMENT '多值字段的key属性对应lookup值',
  `lookup_classify_id` bigint(20) NOT NULL COMMENT 'lookup分类主键ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`lookup_set_id`),
  UNIQUE KEY `lookup_set_id` (`lookup_set_id`),
  -- KEY `data_lookup_set_data_id_fk0` (`data_id`),
  KEY `data_lookup_set_md_entity_id_fk0` (`md_entity_id`),
  KEY `data_lookup_set_lookup_key_fk0` (`lookup_key`),
  KEY `data_lookup_set_tenant_id_fk0` (`tenant_id`),
  KEY `data_lookup_set_lookup_classify_id_fk0` (`lookup_classify_id`),
  CONSTRAINT `data_lookup_set_lookup_classify_id_fk0` FOREIGN KEY (`lookup_classify_id`) REFERENCES `lookup_classify` (`lookup_classify_id`),
  -- CONSTRAINT `data_lookup_set_data_id_fk0` FOREIGN KEY (`data_id`) REFERENCES `data_t` (`data_id`),
  CONSTRAINT `data_lookup_set_lookup_key_fk0` FOREIGN KEY (`lookup_key`) REFERENCES `md_fields` (`md_fields_id`),
  CONSTRAINT `data_lookup_set_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `data_lookup_set_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='多值数据集合';

-- ----------------------------
-- Table structure for data_views
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `data_views` (
  `data_view_id` bigint(20) NOT NULL COMMENT '查询视图ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_main_entity_id` bigint(20) NOT NULL COMMENT '主元数据实体ID',
  `data_view_name` varchar(100) DEFAULT NULL COMMENT '查询视图名称',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  PRIMARY KEY (`data_view_id`),
  UNIQUE KEY `data_view_id` (`data_view_id`),
  KEY `data_views_tenant_id_fk0` (`tenant_id`),
  KEY `data_views_md_main_entity_id_fk0` (`md_main_entity_id`),
  CONSTRAINT `data_views_md_main_entity_id_fk0` FOREIGN KEY (`md_main_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `data_views_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='查询视图，跨多表查询';


-- ----------------------------
-- Table structure for view_inputs
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `view_inputs` (
  `view_input_id` bigint(20) NOT NULL COMMENT '视图输入参数ID',
  `tenant_id` BIGINT(20) NOT NULL comment '租户ID',
  `data_view_id` bigint(20) NOT NULL COMMENT '查询视图ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID',
  `view_input_name` varchar(100) DEFAULT NULL COMMENT '查询输入参数名称',
  `compute_sign` varchar(100) DEFAULT NULL COMMENT '查询条件符号，=<>,like,in,between等',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`view_input_id`),
  UNIQUE KEY `view_input_id` (`view_input_id`),
  KEY `view_inputs_data_view_id_fk0` (`data_view_id`),
  KEY `view_inputs_md_entity_id_fk0` (`md_entity_id`),
  KEY `view_inputs_md_fields_id_fk0` (`md_fields_id`),
  CONSTRAINT `view_inputs_data_view_id_fk0` FOREIGN KEY (`data_view_id`) REFERENCES `data_views` (`data_view_id`),
  CONSTRAINT `view_inputs_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `view_inputs_md_fields_id_fk0` FOREIGN KEY (`md_fields_id`) REFERENCES `md_fields` (`md_fields_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='查询视图输入参数';


-- ----------------------------
-- Table structure for view_outputs
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `view_outputs` (
  `view_output_id` bigint(20) NOT NULL COMMENT '视图输出参数ID',
  `tenant_id` BIGINT(20) NOT NULL comment '租户ID',
  `data_view_id` bigint(20) NOT NULL COMMENT '查询视图ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID',
  `view_output_name` varchar(100) DEFAULT NULL COMMENT '查询输出参数名称',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`view_output_id`),
  UNIQUE KEY `view_output_id` (`view_output_id`),
  KEY `view_outputs_data_view_id_fk0` (`data_view_id`),
  KEY `view_outputs_md_entity_id_fk0` (`md_entity_id`),
  KEY `view_outputs_md_fields_id_fk0` (`md_fields_id`),
  CONSTRAINT `view_outputs_md_fields_id_fk0` FOREIGN KEY (`md_fields_id`) REFERENCES `md_fields` (`md_fields_id`),
  CONSTRAINT `view_outputs_data_view_id_fk0` FOREIGN KEY (`data_view_id`) REFERENCES `data_views` (`data_view_id`),
  CONSTRAINT `view_outputs_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='查询视图输出参数';

-- ----------------------------
-- Table structure for t001
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `t001` (
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `text_column0` varchar(2000) DEFAULT NULL COMMENT '预留字段0',
  `text_column1` varchar(2000) DEFAULT NULL COMMENT '预留字段1',
  `text_column2` varchar(2000) DEFAULT NULL COMMENT '预留字段2',
  `text_column3` varchar(2000) DEFAULT NULL COMMENT '预留字段3',
  `text_column4` varchar(2000) DEFAULT NULL COMMENT '预留字段4',
  `text_column5` varchar(2000) DEFAULT NULL COMMENT '预留字段5',
  `text_column6` varchar(2000) DEFAULT NULL COMMENT '预留字段6',
  `text_column7` varchar(2000) DEFAULT NULL COMMENT '预留字段7',
  `text_column8` varchar(2000) DEFAULT NULL COMMENT '预留字段8',
  `text_column9` varchar(2000) DEFAULT NULL COMMENT '预留字段9',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column0` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段0',
  `num_column1` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段3',
  `num_column4` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段4',
  `num_column5` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段5',
  `date_column0` datetime DEFAULT NULL COMMENT '预留日期字段0',
  `date_column1` datetime DEFAULT NULL COMMENT '预留日期字段1',
  `date_column2` datetime DEFAULT NULL COMMENT '预留日期字段2',
  `date_column3` datetime DEFAULT NULL COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`data_id`),
  UNIQUE KEY `data_id` (`data_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='存储数据表1';


-- ----------------------------
-- Table structure for teams
-- ----------------------------
CREATE TABLE  IF NOT EXISTS teams (	team_id BIGINT(20) NOT NULL UNIQUE PRIMARY KEY comment '团队ID',
	md_entity_id BIGINT(20) NOT NULL comment '元数据实体ID',
	tenant_id BIGINT(20) NOT NULL comment '租户ID',
	team_name VARCHAR(200) comment '团队名称',
	data_id BIGINT(20) NOT NULL comment '主对象的数据存储表主键ID',
	user_id BIGINT(20) NOT NULL comment 'user id标识',
	role_id BIGINT(20) NOT NULL comment '角色ID',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
	active_flag CHAR(1) NOT NULL default  'Y' comment '有效标识，Y有效，N无效',
	create_by BIGINT(20) NOT NULL comment '创建人ID，对用用户ID',
	create_date TIMESTAMP NOT NULL default  NOW() comment '创建时间',
	last_update_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '最后更新时间',
	last_update_by BIGINT(20) NOT NULL comment '最后更新人ID，对用用户ID'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目团队';

alter table teams add constraint teams_md_entity_id_fk0  foreign key (md_entity_id) references md_entities (md_entity_id);
alter table teams add constraint teams_tenant_id_fk0  foreign key (tenant_id) references tenants (tenant_id);
-- alter table teams add constraint teams_data_id_fk0  foreign key (data_id) references data_t (data_id);
alter table teams add constraint teams_user_id_fk0  foreign key (user_id) references users (user_id);


-- ----------------------------
-- Table structure for index_mapping_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `index_mapping_t` (
  `index_mapping_id` bigint(20) NOT NULL COMMENT '索引跟元数据mapping主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `mapping_type` varchar(2000) NOT NULL COMMENT '索引映射类型，Text/Int/Decimal/Date等类型，分别映射四类索引表',
  `unique_flag` char(1) NOT NULL DEFAULT 'N' COMMENT '是否唯一索引标识，Y是，N否',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`index_mapping_id`),
  UNIQUE KEY `index_mapping_id` (`index_mapping_id`),
  KEY `index_mapping_t_tenant_id_fk0` (`tenant_id`),
  KEY `index_mapping_t_md_entity_id_fk0` (`md_entity_id`),
  KEY `index_mapping_t_md_fields_id_fk0` (`md_fields_id`),
  CONSTRAINT `index_mapping_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `index_mapping_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  CONSTRAINT `index_mapping_t_md_fields_id_fk0` FOREIGN KEY (`md_fields_id`) REFERENCES `md_fields` (`md_fields_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='索引跟元数据mapping表';

-- ----------------------------
-- Table structure for index_text_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `index_text_t` (
  `index_text_id` bigint(20) NOT NULL COMMENT '文本型索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `text_value` varchar(512) COMMENT '文本索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`index_text_id`),
  UNIQUE KEY `index_text_id` (`index_text_id`),
  KEY `index_text_t_tenant_id_fk0` (`tenant_id`),
  KEY `index_text_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `index_text_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `index_text_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用文本型索引表';

ALTER TABLE index_text_t ADD UNIQUE  index_text_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE index_text_t ADD INDEX index_text_t_idx0 (md_entity_id,md_fields_id,text_value);

-- ----------------------------
-- Table structure for index_int_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `index_int_t` (
  `index_int_id` bigint(20) NOT NULL COMMENT '整型索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `int_value` bigint(20) COMMENT '整型索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`index_int_id`),
  UNIQUE KEY `index_int_id` (`index_int_id`),
  KEY `index_int_t_tenant_id_fk0` (`tenant_id`),
  KEY `index_int_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `index_int_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `index_int_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用整型索引表';

ALTER TABLE index_int_t ADD UNIQUE  index_int_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE index_int_t ADD INDEX index_int_t_idx0 (md_entity_id,md_fields_id,int_value);



-- ----------------------------
-- Table structure for index_decimal_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `index_decimal_t` (
  `index_decimal_id` bigint(20) NOT NULL COMMENT '数值型索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `num_value` decimal(30,8) COMMENT '数字型索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`index_decimal_id`),
  UNIQUE KEY `index_decimal_id` (`index_decimal_id`),
  KEY `index_decimal_t_tenant_id_fk0` (`tenant_id`),
  KEY `index_decimal_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `index_decimal_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `index_decimal_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用数值型索引表';

ALTER TABLE index_decimal_t ADD UNIQUE  index_decimal_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE index_decimal_t ADD INDEX index_decimal_t_idx0 (md_entity_id,md_fields_id,num_value);


-- ----------------------------
-- Table structure for index_date_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `index_date_t` (
  `index_date_id` bigint(20) NOT NULL COMMENT '日期型索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `date_value` datetime COMMENT '日期索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`index_date_id`),
  UNIQUE KEY `index_date_id` (`index_date_id`),
  KEY `index_date_t_tenant_id_fk0` (`tenant_id`),
  KEY `index_date_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `index_date_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `index_date_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用日期型索引表';

ALTER TABLE index_date_t ADD UNIQUE  index_date_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE index_date_t ADD INDEX index_date_t_idx0 (md_entity_id,md_fields_id,date_value);



-- ----------------------------
-- Table structure for unique_mapping_t
-- ----------------------------
/*
CREATE TABLE  IF NOT EXISTS `unique_mapping_t` (
  `unique_mapping_id` bigint(20) NOT NULL COMMENT '唯一索引跟元数据映射主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `mapping_type` varchar(2000) NOT NULL COMMENT '索引映射类型，Text/Int/Decimal/Date等类型，分别映射四类索引表',
  `text_column1` varchar(2000) COMMENT '预留文本字段1',
  `text_column2` varchar(2000) COMMENT '预留文本字段2',
  `text_column3` varchar(2000) COMMENT '预留文本字段3',
  `text_column4` varchar(2000) COMMENT '预留文本字段4',
  `text_column5` varchar(2000) COMMENT '预留文本字段5',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `int_column2` bigint(20) COMMENT '预留整数字段2',
  `int_column3` bigint(20) COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) COMMENT '预留数值字段3',
  `date_column1` datetime COMMENT '预留日期字段1',
  `date_column2` datetime COMMENT '预留日期字段2',
  `date_column3` datetime COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`unique_mapping_id`),
  UNIQUE KEY `unique_mapping_id` (`unique_mapping_id`),
  KEY `unique_mapping_t_tenant_id_fk0` (`tenant_id`),
  KEY `unique_mapping_t_md_entity_id_fk0` (`md_entity_id`),
  KEY `unique_mapping_t_md_fields_id_fk0` (`md_fields_id`),
  CONSTRAINT `unique_mapping_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `unique_mapping_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  CONSTRAINT `unique_mapping_t_md_fields_id_fk0` FOREIGN KEY (`md_fields_id`) REFERENCES `md_fields` (`md_fields_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='唯一键索引映射表';
*/


-- ----------------------------
-- Table structure for unique_text_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `unique_text_t` (
  `unique_text_id` bigint(20) NOT NULL COMMENT '文本型唯一索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `text_value` varchar(512) COMMENT '文本唯一索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`unique_text_id`),
  UNIQUE KEY `unique_text_id` (`unique_text_id`),
  KEY `unique_text_t_tenant_id_fk0` (`tenant_id`),
  KEY `unique_text_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `unique_text_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `unique_text_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用文本型唯一索引表';

ALTER TABLE unique_text_t ADD UNIQUE  unique_text_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE unique_text_t ADD UNIQUE  unique_text_t_unique1 (md_entity_id,md_fields_id,text_value(255));


-- ----------------------------
-- Table structure for unique_int_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `unique_int_t` (
  `unique_int_id` bigint(20) NOT NULL COMMENT '整型唯一索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `int_value` bigint(20) COMMENT '整型唯一索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`unique_int_id`),
  UNIQUE KEY `unique_int_id` (`unique_int_id`),
  KEY `unique_int_t_tenant_id_fk0` (`tenant_id`),
  KEY `unique_int_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `unique_int_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `unique_int_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用整型唯一索引表';

ALTER TABLE unique_int_t ADD UNIQUE  unique_int_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE unique_int_t ADD UNIQUE  unique_int_t_unique1 (md_entity_id,md_fields_id,int_value);



-- ----------------------------
-- Table structure for unique_decimal_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `unique_decimal_t` (
  `unique_decimal_id` bigint(20) NOT NULL COMMENT '数值型唯一索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `num_value` decimal(30,8) COMMENT '数值型唯一索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`unique_decimal_id`),
  UNIQUE KEY `unique_decimal_id` (`unique_decimal_id`),
  KEY `unique_decimal_t_tenant_id_fk0` (`tenant_id`),
  KEY `unique_decimal_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `unique_decimal_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `unique_decimal_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用数值型唯一索引表';

ALTER TABLE unique_decimal_t ADD UNIQUE  unique_decimal_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE unique_decimal_t ADD UNIQUE  unique_decimal_t_unique1 (md_entity_id,md_fields_id,num_value);


-- ----------------------------
-- Table structure for unique_date_t
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `unique_date_t` (
  `unique_date_id` bigint(20) NOT NULL COMMENT '日期型唯一索引主键ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID',
  `md_fields_id` bigint(20) NOT NULL COMMENT '元数据属性ID/视图viewID',
  `data_id` bigint(20) NOT NULL COMMENT '数据存储表主键ID',
  `date_value` datetime COMMENT '日期唯一索引值',
  `text_column1` varchar(512) COMMENT '预留文本字段1',
  `text_column2` varchar(512) COMMENT '预留文本字段2',
  `int_column1` bigint(20) COMMENT '预留整数字段1',
  `num_column1` decimal(30,8) COMMENT '预留数值字段1',
  `date_column1` datetime COMMENT '预留日期字段1',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`unique_date_id`),
  UNIQUE KEY `unique_date_id` (`unique_date_id`),
  KEY `unique_date_t_tenant_id_fk0` (`tenant_id`),
  KEY `unique_date_t_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `unique_date_t_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `unique_date_t_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='通用日期型唯一索引表';

ALTER TABLE unique_date_t ADD UNIQUE  unique_date_t_unique0 (tenant_id,md_entity_id,md_fields_id,data_id);
ALTER TABLE unique_date_t ADD UNIQUE  unique_date_t_unique1 (md_entity_id,md_fields_id,date_value);
