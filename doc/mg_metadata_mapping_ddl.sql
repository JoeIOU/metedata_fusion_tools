

-- ----------------------------
-- Table structure for mg_tables_mapping
-- ----------------------------
CREATE TABLE `mg_tables_mapping` (
  `tables_mapping_id` bigint(20) NOT NULL COMMENT '数据表mappingID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `from_tables_id` bigint(20) NOT NULL COMMENT 'from旧数据表ID',
  `to_tables_id` bigint(20) COMMENT 'to新数据表ID',
  `migration_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '迁移标识，Y迁移，N不迁移',
  `tables_mapping_name` varchar(100) NOT NULL COMMENT '数据表映射名称',
  `tables_mapping_desc` varchar(2000)  COMMENT '数据表映射描述',
  `public_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '全局公共标识，Y是，N否',
  `text_column1` varchar(2000) DEFAULT NULL COMMENT '预留文本字段1',
  `text_column2` varchar(2000) DEFAULT NULL COMMENT '预留文本字段2',
  `text_column3` varchar(2000) DEFAULT NULL COMMENT '预留文本字段3',
  `text_column4` varchar(2000) DEFAULT NULL COMMENT '预留文本字段4',
  `text_column5` varchar(2000) DEFAULT NULL COMMENT '预留文本字段5',
  `int_column1` bigint(20) DEFAULT NULL COMMENT '预留整数字段1',
  `int_column2` bigint(20) DEFAULT NULL COMMENT '预留整数字段2',
  `int_column3` bigint(20) DEFAULT NULL COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段3',
  `date_column1` datetime DEFAULT NULL COMMENT '预留日期字段1',
  `date_column2` datetime DEFAULT NULL COMMENT '预留日期字段2',
  `date_column3` datetime DEFAULT NULL COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`tables_mapping_id`),
  UNIQUE KEY `tables_mapping_id` (`tables_mapping_id`),
  UNIQUE KEY `tables_mapping_unique01` (`tenant_id`,`from_tables_id`,`to_tables_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据表迁移映射关系信息';

-- ----------------------------
-- Table structure for mg_columns_mapping
-- ----------------------------
DROP TABLE IF EXISTS `mg_columns_mapping`;
CREATE TABLE `md_columns_mapping` (
  `columns_mapping_id` bigint(20) NOT NULL COMMENT '数据字段mappingID',
  `tables_mapping_id` bigint(20) NOT NULL COMMENT '数据表mappingID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `columns_mapping_name` varchar(200) NOT NULL COMMENT '数据字段mapping名称',
  `columns_transform_logic` varchar(4000)  COMMENT '字段转换逻辑描述',
  `columns_mapping_desc` varchar(4000)  COMMENT '字段mapping描述',
  `from_tables_id` bigint(20) NOT NULL COMMENT 'from旧数据表ID',
  `from_columns_id` bigint(20)  COMMENT 'from旧数据表字段ID',
  `to_tables_id` bigint(20) COMMENT 'to新数据表ID',
  `to_columns_id` bigint(20)  COMMENT 'to新数据表字段ID',
  `migration_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '迁移标识，Y迁移，N不迁移',
  `public_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '全局公共标识，Y是，N否',
  `text_column1` varchar(2000) DEFAULT NULL COMMENT '预留文本字段1',
  `text_column2` varchar(2000) DEFAULT NULL COMMENT '预留文本字段2',
  `text_column3` varchar(2000) DEFAULT NULL COMMENT '预留文本字段3',
  `text_column4` varchar(2000) DEFAULT NULL COMMENT '预留文本字段4',
  `text_column5` varchar(2000) DEFAULT NULL COMMENT '预留文本字段5',
  `int_column1` bigint(20) DEFAULT NULL COMMENT '预留整数字段1',
  `int_column2` bigint(20) DEFAULT NULL COMMENT '预留整数字段2',
  `int_column3` bigint(20) DEFAULT NULL COMMENT '预留整数字段3',
  `num_column1` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段1',
  `num_column2` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段2',
  `num_column3` decimal(30,8) DEFAULT NULL COMMENT '预留数值字段3',
  `date_column1` datetime DEFAULT NULL COMMENT '预留日期字段1',
  `date_column2` datetime DEFAULT NULL COMMENT '预留日期字段2',
  `date_column3` datetime DEFAULT NULL COMMENT '预留日期字段3',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `md_tables_id` bigint(20) NOT NULL COMMENT '元数据数据表ID',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`columns_mapping_id`),
  UNIQUE KEY `columns_mapping_id` (`columns_mapping_id`),
  KEY `md_columns_mapping_fk1` (`tables_mapping_id`), 
  CONSTRAINT `md_columns_mapping_fk1` FOREIGN KEY (`tables_mapping_id`) REFERENCES `mg_tables_mapping` (`tables_mapping_id`),
  KEY `md_columns_mapping_fk0` (`md_tables_id`),
  CONSTRAINT `md_columns_mapping_fk0` FOREIGN KEY (`md_tables_id`) REFERENCES `md_tables` (`md_tables_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='数据迁移字段mapping信息';
