
-- ----------------------------
-- Table structure for rules
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `rules` (
  `rule_id` bigint(20) NOT NULL COMMENT '规则ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `rule_code` varchar(200) NOT NULL COMMENT '规则编码',
  `rule_name` varchar(200) NOT NULL COMMENT '规则名称',
  `rule_category` varchar(200) NOT NULL COMMENT '规则分类，Validation校验类，Computing计算等分类',
  `rule_type` varchar(200) NOT NULL COMMENT '规则类型，regex为正则表达式，script为脚本，service为服务',
  `rule_script` varchar(4000) NOT NULL COMMENT '规则脚本或表达式',
  `rule_demo` varchar(200) COMMENT '规则示例',
  `rule_desc` varchar(2000) DEFAULT NULL COMMENT '规则描述',
  `rule_desc_en` varchar(2000) DEFAULT NULL COMMENT '规则英文描述',
  `public_flag` char(1) NOT NULL DEFAULT 'N' COMMENT '跨租户共享标识，Y是，N否',
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
  PRIMARY KEY (`rule_id`),
  UNIQUE KEY `rule_id` (`rule_id`),
  UNIQUE KEY `rule_code` (`rule_code`),
  KEY `rules_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `rules_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='校验规则';

-- ----------------------------
-- Table structure for rules_entity_rel
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `rules_entity_rel` (
  `rule_entity_rel_id` bigint(20) NOT NULL COMMENT '规则与实体关系ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `entity_type` varchar(200) NOT NULL COMMENT '元数据类型，Entity实体，View视图',
  `md_entity_id` bigint(20) NOT NULL COMMENT '元数据实体ID或数据视图ID',
  `input_params`  varchar(2000) COMMENT '输入参数，跟实体属性名称匹配（可以多个，list形式）',
  `output_params` varchar(2000) COMMENT '输出参数，跟实体属性名称匹配（可以多个，list形式）',
  `rule_id` bigint(20) NOT NULL COMMENT '规则ID',
  `rule_rel_desc` varchar(2000) DEFAULT NULL COMMENT '规则关系描述',
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
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`rule_entity_rel_id`),
  UNIQUE KEY `rule_entity_rel_id` (`rule_entity_rel_id`),
  KEY `rule_entity_rel_id_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `rule_entity_rel_id_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  KEY `rule_entity_rel_id_rule_id_fk0` (`rule_id`),
  CONSTRAINT `rule_entity_rel_id_rule_id_fk0` FOREIGN KEY (`rule_id`) REFERENCES `rules` (`rule_id`),
  KEY `rule_entity_rel_id_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `rule_entity_rel_id_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='规则与实体关系';


-- ----------------------------
-- Table structure for rules_ui_rel
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `rules_ui_rel` (
  `rule_ui_rel_id` bigint(20) NOT NULL COMMENT '规则与UI关系ID',
  `tenant_id` bigint(20) NOT NULL COMMENT '租户ID',
  `ui_template_id` bigint(20) NOT NULL COMMENT 'UI模板ID',
  `ui_fields_id` bigint(20) COMMENT 'UI属性ID',
  `rule_id` bigint(20) NOT NULL COMMENT '规则ID',
  `rule_ui_desc` varchar(2000) DEFAULT NULL COMMENT '规则UI关系描述',
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
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对应用户ID',
  `last_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对应用户ID',
  PRIMARY KEY (`rule_ui_rel_id`),
  UNIQUE KEY `rule_ui_rel_id` (`rule_ui_rel_id`),
  KEY `rule_ui_rel_id_tenant_id_fk0` (`tenant_id`),
  CONSTRAINT `rule_ui_rel_id_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  KEY `rule_ui_rel_id_rule_id_fk0` (`rule_id`),
  CONSTRAINT `rule_ui_rel_id_rule_id_fk0` FOREIGN KEY (`rule_id`) REFERENCES `rules` (`rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='规则与UI关系';

-- ----------------------------
-- Table structure for system_entities
-- ----------------------------
CREATE TABLE  IF NOT EXISTS `system_entities` (
  `data_id` bigint(20) NOT NULL COMMENT '主键ID',
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
  `public_flag` char(1) NOT NULL DEFAULT 'N' COMMENT '跨租户共享标识，Y则共享，N不共享',
  `active_flag` char(1) NOT NULL DEFAULT 'Y' COMMENT '有效标识，Y有效，N无效',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_by` bigint(20) NOT NULL COMMENT '创建人ID，对用用户ID',
  `last_update_date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `last_update_by` bigint(20) NOT NULL COMMENT '最后更新人ID，对用用户ID',
  PRIMARY KEY (`data_id`),
  UNIQUE KEY `data_id` (`data_id`),
  KEY `system_entities_tenant_id_fk0` (`tenant_id`),
  KEY `system_entities_md_entity_id_fk0` (`md_entity_id`),
  CONSTRAINT `system_entities_md_entity_id_fk0` FOREIGN KEY (`md_entity_id`) REFERENCES `md_entities` (`md_entity_id`),
  CONSTRAINT `system_entities_tenant_id_fk0` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统对象表';

