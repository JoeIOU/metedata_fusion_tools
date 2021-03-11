/* * MySql Sql Generate * */
-- ad
/*
警告: 字段名可能非法 - content
警告: 字段名可能非法 - path
警告: 字段名可能非法 - type
*/
create table  ad
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       beginDate         DATETIME 	/*起始日期*/,
       CONTENT         BLOB 	/*内容*/,
       endDate           DATETIME 	/*结束日期*/,
       PATH            VARCHAR(255) 	/*路径*/,
       title             VARCHAR(255) not null 	/*标题*/,
       TYPE            INTEGER not null 	/*类型*/,
       url               VARCHAR(255) 	/*链接地址*/,
       adPosition_id     INTEGER not null 	/*广告位*/
);
alter  table ad
       add constraint PK_ad_id primary key (id);
create index IDX_adPosition_id on ad(adPosition_id);

-- socialuser 
create table  socialuser
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       loginPluginId     VARCHAR(255) not null 	/*登录插件ID*/,
       uniqueId          VARCHAR(255) not null 	/*唯一ID*/,
       user_id           INTEGER 	/*用户*/ 
);
alter  table socialuser
       add constraint PK_socialuser_id primary key (id);
create index IDX_socialuser_loginPlnId1870 on socialuser(loginPluginId);
create index IDX_socialuser_user_id on socialuser(user_id);

-- admin_role
create table  admin_role
(
       admins_id         INTEGER not null 	/*管理员*/,
       roles_id          INTEGER not null 	/*角色*/
);

-- adposition
/*
警告: 字段名可能非法 - template
*/
create table  adposition
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       description       VARCHAR(255) 	/*描述*/,
       height            INTEGER not null 	/*高度*/,
       name              VARCHAR(255) not null 	/*名称*/,
       TEMPLATE        BLOB not null 	/*模板*/,
       width             INTEGER not null 	/*宽度*/
);
alter  table adposition
       add constraint PK_adposition_id primary key (id);

-- area
create table  area
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       fullName          BLOB not null 	/*全称*/,
       grade             INTEGER not null 	/*层级*/,
       name              VARCHAR(255) not null 	/*名称*/,
       treePath          VARCHAR(255) not null 	/*树路径*/,
       parent_id         INTEGER 	/*上级地区*/
);
alter  table area
       add constraint PK_area_id primary key (id);
create index IDX_area_parent_id on area(parent_id);

-- areafreightconfig
create table  areafreightconfig
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       continuePrice     NUMERIC(23,6) not null 	/*续重价格*/,
       continueWeight    INTEGER not null 	/*续重量*/,
       firstPrice        NUMERIC(23,6) not null 	/*首重价格*/,
       firstWeight       INTEGER not null 	/*首重量*/,
       shippingMethod_id INTEGER not null 	/*配送方式*/,
       store_id          INTEGER not null 	/*店铺*/,
       area_id           INTEGER not null 	/*地区*/
);
alter  table areafreightconfig
       add constraint PK_areafreightconfig_id primary key (id);
create index IDX_areafrefig_shippin_idB829 on areafreightconfig(shippingMethod_id);
create index IDX_areafrefig_store_id358E on areafreightconfig(store_id);
create index IDX_areafrefig_area_idD57E on areafreightconfig(area_id);

-- article
/*
警告: 字段名可能非法 - content
*/
create table  article
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       author            VARCHAR(255) 	/*作者*/,
       CONTENT         BLOB 	/*内容*/,
       hits              INTEGER not null 	/*点击数*/,
       isPublication     BIT not null 	/*是否发布*/,
       isTop             BIT not null 	/*是否置顶*/,
       seoDescription    VARCHAR(255) 	/*页面描述*/,
       seoKeywords       VARCHAR(255) 	/*页面关键词*/,
       seoTitle          VARCHAR(255) 	/*页面标题*/,
       title             VARCHAR(255) not null 	/*标题*/,
       articleCategory_id INTEGER not null 	/*文章分类*/
);
alter  table article
       add constraint PK_article_id primary key (id);
create index IDX_articleCategory_id on article(articleCategory_id);

-- article_articletag
create table  article_articletag
(
       articles_id       INTEGER not null 	/*文章*/,
       articleTags_id    INTEGER not null 	/*文章标签*/
);

-- business
create table  business
(
       id                INTEGER not null 	/*ID*/,
       balance           NUMERIC(29,12) not null 	/*余额*/,
       bankAccount       VARCHAR(255) 	/*银行账号*/,
       bankName          VARCHAR(255) 	/*银行开户名*/,
       email             VARCHAR(255) not null 	/*E-mail*/,
       encodedPassword   VARCHAR(255) not null 	/*加密密码*/,
       frozenFund        NUMERIC(29,12) not null 	/*冻结金额*/,
       idCard            VARCHAR(255) 	/*法人代表身份证*/,
       idCardImage       VARCHAR(255) 	/*法人代表身份证图片*/,
       identificationNumber VARCHAR(255) 	/*纳税人识别号*/,
       legalPerson       VARCHAR(255) 	/*法人代表姓名*/,
       licenseImage      VARCHAR(255) 	/*营业执照号图片*/,
       licenseNumber     VARCHAR(255) 	/*营业执照号*/,
       mobile            VARCHAR(255) 	/*手机*/,
       name              VARCHAR(255) 	/*名称*/,
       organizationCode  VARCHAR(255) 	/*组织机构代码*/,
       organizationImage VARCHAR(255) 	/*组织机构代码证图片*/,
       phone             VARCHAR(255) 	/*电话*/,
       safeKeyExpire     DATETIME 	/*安全密匙*/,
       safeKeyValue      VARCHAR(255) 	/*安全密匙*/,
       taxImage          VARCHAR(255) 	/*税务登记证图片*/,
       username          VARCHAR(255) not null 	/*用户名*/,
       attributeValue0   VARCHAR(255) 	/*商家注册项值0*/,
       attributeValue1   VARCHAR(255) 	/*商家注册项值1*/,
       attributeValue2   VARCHAR(255) 	/*商家注册项值2*/,
       attributeValue3   VARCHAR(255) 	/*商家注册项值3*/,
       attributeValue4   VARCHAR(255) 	/*商家注册项值4*/,
       attributeValue5   VARCHAR(255) 	/*商家注册项值5*/,
       attributeValue6   VARCHAR(255) 	/*商家注册项值6*/,
       attributeValue7   VARCHAR(255) 	/*商家注册项值7*/,
       attributeValue8   VARCHAR(255) 	/*商家注册项值8*/,
       attributeValue9   VARCHAR(255) 	/*商家注册项值9*/,
       attributeValue10  VARCHAR(255) 	/*商家注册项值10*/,
       attributeValue11  VARCHAR(255) 	/*商家注册项值11*/,
       attributeValue12  VARCHAR(255) 	/*商家注册项值12*/,
       attributeValue13  VARCHAR(255) 	/*商家注册项值13*/,
       attributeValue14  VARCHAR(255) 	/*商家注册项值14*/,
       attributeValue15  VARCHAR(255) 	/*商家注册项值15*/,
       attributeValue16  VARCHAR(255) 	/*商家注册项值16*/,
       attributeValue17  VARCHAR(255) 	/*商家注册项值17*/,
       attributeValue18  VARCHAR(255) 	/*商家注册项值18*/,
       attributeValue19  VARCHAR(255) 	/*商家注册项值19*/
);
alter  table business
       add constraint PK_business_id primary key (id);
create unique index IDU_business_email on business(email);
create unique index IDU_business_mobile on business(mobile);
create unique index IDU_business_username on business(username);

-- articlecategory
create table  articlecategory
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       grade             INTEGER not null 	/*层级*/,
       name              VARCHAR(255) not null 	/*名称*/,
       seoDescription    VARCHAR(255) 	/*页面描述*/,
       seoKeywords       VARCHAR(255) 	/*页面关键词*/,
       seoTitle          VARCHAR(255) 	/*页面标题*/,
       treePath          VARCHAR(255) not null 	/*树路径*/,
       parent_id         INTEGER 	/*上级分类*/
);
alter  table articlecategory
       add constraint PK_articlecategory_id primary key (id);
create index IDX_articleory_parent_id0243 on articlecategory(parent_id);

-- articletag
create table  articletag
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       icon              VARCHAR(255) 	/*图标*/,
       memo              VARCHAR(255) 	/*备注*/,
       name              VARCHAR(255) not null 	/*名称*/
);
alter  table articletag
       add constraint PK_articletag_id primary key (id);

-- admin
/*
警告: 表名可能非法 - admin
*/
create table  ADMIN
(
       id                INTEGER not null 	/*ID*/,
       department        VARCHAR(255) 	/*部门*/,
       email             VARCHAR(255) not null 	/*E-mail*/,
       encodedPassword   VARCHAR(255) not null 	/*加密密码*/,
       name              VARCHAR(255) 	/*姓名*/,
       username          VARCHAR(255) not null 	/*用户名*/
);
alter  table ADMIN
       add constraint PK_admin_id primary key (id);
create unique index IDU_admin_email on ADMIN(email);
create unique index IDU_admin_username on ADMIN(username);

-- attribute
/*
警告: 表名可能非法 - attribute
警告: 字段名可能非法 - options
*/
create table  ATTRIBUTE
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       name              VARCHAR(255) not null 	/*名称*/,
       OPTIONS         BLOB not null 	/*可选项*/,
       propertyIndex     INTEGER not null 	/*属性序号*/,
       productCategory_id INTEGER not null 	/*绑定分类*/
);
alter  table ATTRIBUTE
       add constraint PK_attribute_id primary key (id);
create index IDX_attribute_productC_id10D1 on ATTRIBUTE(productCategory_id);

-- auditlog
/*
警告: 字段名可能非法 - action
*/
create table  auditlog
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       ACTION          VARCHAR(255) not null 	/*动作*/,
       detail            VARCHAR(255) 	/*详情*/,
       ip                VARCHAR(255) not null 	/*IP*/,
       parameters        BLOB 	/*请求参数*/,
       requestUrl        VARCHAR(255) not null 	/*请求URL*/,
       user_id           INTEGER 	/*用户*/
);
alter  table auditlog
       add constraint PK_auditlog_id primary key (id);
create index IDX_auditlog_user_id on auditlog(user_id);

-- brand
/*
警告: 字段名可能非法 - type
*/
create table  brand
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       introduction      BLOB 	/*介绍*/,
       logo              VARCHAR(255) 	/*logo*/,
       name              VARCHAR(255) not null 	/*名称*/,
       TYPE            INTEGER not null 	/*类型*/,
       url               VARCHAR(255) 	/*网址*/
);
alter  table brand
       add constraint PK_brand_id primary key (id);

-- businessattribute
/*
警告: 字段名可能非法 - options
警告: 字段名可能非法 - type
*/
create table  businessattribute
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       isEnabled         BIT not null 	/*是否启用*/,
       isRequired        BIT not null 	/*是否必填*/,
       name              VARCHAR(255) not null 	/*名称*/,
       OPTIONS         BLOB 	/*可选项*/,
       pattern           VARCHAR(255) 	/*配比*/,
       propertyIndex     INTEGER 	/*属性序号*/,
       TYPE            INTEGER not null 	/*类型*/
);
alter  table businessattribute
       add constraint PK_businessattribute_id primary key (id);

-- businessdepositlog
/*
警告: 字段名可能非法 - type
*/
create table  businessdepositlog
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       balance           NUMERIC(23,6) not null 	/*当前余额*/,
       credit            NUMERIC(23,6) not null 	/*收入金额*/,
       debit             NUMERIC(23,6) not null 	/*支出金额*/,
       memo              VARCHAR(255) 	/*备注*/,
       TYPE            INTEGER not null 	/*类型*/,
       business_id       INTEGER not null 	/*商家*/
);
alter  table businessdepositlog
       add constraint PK_businessdepositlog_id primary key (id);
create index IDX_busineslog_busines_id736A on businessdepositlog(business_id);

-- cart
create table  cart
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       expire            DATETIME 	/*过期时间*/,
       cartKey           VARCHAR(255) not null 	/*密钥*/,
       member_id         INTEGER 	/*会员*/
);
alter  table cart
       add constraint PK_cart_id primary key (id);
create unique index IDU_cartKey on cart(cartKey);
create index IDX_cart_member_id on cart(member_id);

-- cartitem
create table  cartitem
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       quantity          INTEGER not null 	/*数量*/,
       cart_id           INTEGER not null 	/*购物车*/,
       sku_id            INTEGER not null 	/*SKU*/
);
alter  table cartitem
       add constraint PK_cartitem_id primary key (id);
create index IDX_cartitem_cart_id on cartitem(cart_id);
create index IDX_cartitem_sku_id on cartitem(sku_id);

-- cash
/*
警告: 字段名可能非法 - status
*/
create table  cash
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       account           VARCHAR(255) not null 	/*收款账号*/,
       amount            NUMERIC(23,6) not null 	/*金额*/,
       bank              VARCHAR(255) not null 	/*收款银行*/,
       STATUS          INTEGER not null 	/*状态*/,
       business_id       INTEGER not null 	/*商家*/
);
alter  table cash
       add constraint PK_cash_id primary key (id);
create index IDX_cash_business_id on cash(business_id);

-- categoryapplication
/*
警告: 字段名可能非法 - status
*/
create table  categoryapplication
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       rate              NUMERIC not null 	/*分佣比例*/,
       STATUS          INTEGER not null 	/*状态*/,
       productCategory_id INTEGER not null 	/*经营分类*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table categoryapplication
       add constraint PK_categorion_id6D53 primary key (id);
create index IDX_categorion_product_id37A2 on categoryapplication(productCategory_id);
create index IDX_categorion_store_id2C32 on categoryapplication(store_id);

-- consultation
/*
警告: 字段名可能非法 - content
*/
create table  consultation
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       CONTENT         VARCHAR(255) not null 	/*内容*/,
       ip                VARCHAR(255) not null 	/*IP*/,
       isShow            BIT not null 	/*是否显示*/,
       forConsultation_id INTEGER 	/*咨询*/,
       member_id         INTEGER 	/*会员*/,
       product_id        INTEGER not null 	/*商品*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table consultation
       add constraint PK_consultation_id primary key (id);
create index IDX_consultion_forCons_idB45A on consultation(forConsultation_id);
create index IDX_consultion_member_id08AC on consultation(member_id);
create index IDX_consultion_product_id2382 on consultation(product_id);
create index IDX_consultation_store_id on consultation(store_id);

-- coupon
/*
警告: 字段名可能非法 - point
*/
create table  coupon
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       beginDate         DATETIME 	/*使用起始日期*/,
       endDate           DATETIME 	/*使用结束日期*/,
       introduction      BLOB 	/*介绍*/,
       isEnabled         BIT not null 	/*是否启用*/,
       isExchange        BIT not null 	/*是否允许积分兑换*/,
       maximumPrice      NUMERIC(23,6) 	/*最大商品价格*/,
       maximumQuantity   INTEGER 	/*最大商品数量*/,
       minimumPrice      NUMERIC(23,6) 	/*最小商品价格*/,
       minimumQuantity   INTEGER 	/*最小商品数量*/,
       name              VARCHAR(255) not null 	/*名称*/,
       POINT           INTEGER 	/*积分兑换数*/,
       prefix            VARCHAR(255) not null 	/*前缀*/,
       priceExpression   VARCHAR(255) 	/*价格运算表达式*/,
       store_id          INTEGER 	/*店铺*/
);
alter  table coupon
       add constraint PK_coupon_id primary key (id);
create index IDX_coupon_store_id on coupon(store_id);

-- couponcode
/*
警告: 字段名可能非法 - code
*/
create table  couponcode
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       CODE            VARCHAR(255) not null 	/*号码*/,
       isUsed            BIT not null 	/*是否已使用*/,
       usedDate          DATETIME 	/*使用日期*/,
       coupon_id         INTEGER not null 	/*优惠券*/,
       member_id         INTEGER 	/*会员*/
);
alter  table couponcode
       add constraint PK_couponcode_id primary key (id);
create unique index IDU_couponcode_code on couponcode(CODE);
create index IDX_couponcode_coupon_id on couponcode(coupon_id);
create index IDX_couponcode_member_id on couponcode(member_id);

-- defaultfreightconfig
create table  defaultfreightconfig
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       continuePrice     NUMERIC(23,6) not null 	/*续重价格*/,
       continueWeight    INTEGER not null 	/*续重量*/,
       firstPrice        NUMERIC(23,6) not null 	/*首重价格*/,
       firstWeight       INTEGER not null 	/*首重量*/,
       shippingMethod_id INTEGER not null 	/*配送方式*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table defaultfreightconfig
       add constraint PK_defaultfig_idD0E3 primary key (id);
create index IDX_defaultfig_shippin_idD899 on defaultfreightconfig(shippingMethod_id);
create index IDX_defaultfig_store_id76C5 on defaultfreightconfig(store_id);

-- deliverycenter
create table  deliverycenter
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       address           VARCHAR(255) not null 	/*地址*/,
       areaName          VARCHAR(255) not null 	/*地区名称*/,
       contact           VARCHAR(255) not null 	/*联系人*/,
       isDefault         BIT not null 	/*是否默认*/,
       memo              VARCHAR(255) 	/*备注*/,
       mobile            VARCHAR(255) 	/*手机*/,
       name              VARCHAR(255) not null 	/*名称*/,
       phone             VARCHAR(255) 	/*电话*/,
       zipCode           VARCHAR(255) 	/*邮编*/,
       area_id           INTEGER 	/*地区*/,
       store_id          INTEGER 	/*店铺*/
);
alter  table deliverycenter
       add constraint PK_deliverycenter_id primary key (id);
create index IDX_deliverter_area_id6436 on deliverycenter(area_id);
create index IDX_deliverter_store_idBDFA on deliverycenter(store_id);

-- deliverycorp
/*
警告: 字段名可能非法 - code
*/
create table  deliverycorp
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       CODE            VARCHAR(255) 	/*代码*/,
       name              VARCHAR(255) not null 	/*名称*/,
       url               VARCHAR(255) 	/*网址*/
);
alter  table deliverycorp
       add constraint PK_deliverycorp_id primary key (id);

-- deliverytemplate
/*
警告: 字段名可能非法 - content
*/
create table  deliverytemplate
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       background        VARCHAR(255) 	/*背景图*/,
       CONTENT         BLOB not null 	/*内容*/,
       height            INTEGER not null 	/*高度*/,
       isDefault         BIT not null 	/*是否默认*/,
       memo              VARCHAR(255) 	/*备注*/,
       name              VARCHAR(255) not null 	/*名称*/,
       offsetX           INTEGER not null 	/*偏移量X*/,
       offsetY           INTEGER not null 	/*偏移量Y*/,
       width             INTEGER not null 	/*宽度*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table deliverytemplate
       add constraint PK_deliverytemplate_id primary key (id);
create index IDX_deliverate_store_idC35C on deliverytemplate(store_id);

-- friendlink
/*
警告: 字段名可能非法 - type
*/
create table  friendlink
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       logo              VARCHAR(255) 	/*logo*/,
       name              VARCHAR(255) not null 	/*名称*/,
       TYPE            INTEGER not null 	/*类型*/,
       url               VARCHAR(255) not null 	/*链接地址*/
);
alter  table friendlink
       add constraint PK_friendlink_id primary key (id);

-- idgenerator
create table  idgenerator
(
       sequence_name     VARCHAR(255) not null 	/*序列名*/,
       next_val          INTEGER 	/*序列值*/
);
alter  table idgenerator
       add constraint PK_idgenertor_sequencame6A0F primary key (sequence_name);

-- instantmessage
/*
警告: 字段名可能非法 - type
*/
create table  instantmessage
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       account           VARCHAR(255) not null 	/*账号*/,
       name              VARCHAR(255) not null 	/*名称*/,
       TYPE            INTEGER not null 	/*类型*/,
       store_id          INTEGER 	/*店铺*/
);
alter  table instantmessage
       add constraint PK_instantmessage_id primary key (id);
create index IDX_instantage_store_idF853 on instantmessage(store_id);

-- member
/*
警告: 表名可能非法 - member
警告: 字段名可能非法 - point
*/
create table  MEMBER
(
       id                INTEGER not null 	/*ID*/,
       area_id           INTEGER 	/*地区*/,
       memberRank_id     INTEGER not null 	/*会员等级*/,
       address           VARCHAR(255) 	/*地址*/,
       amount            NUMERIC(29,12) not null 	/*消费金额*/,
       balance           NUMERIC(29,12) not null 	/*余额*/,
       birth             DATETIME 	/*出生日期*/,
       email             VARCHAR(255) not null 	/*E-mail*/,
       encodedPassword   VARCHAR(255) not null 	/*加密密码*/,
       gender            INTEGER 	/*性别*/,
       mobile            VARCHAR(255) 	/*手机*/,
       name              VARCHAR(255) 	/*姓名*/,
       phone             VARCHAR(255) 	/*电话*/,
       POINT           INTEGER not null 	/*积分*/,
       safeKeyExpire     DATETIME 	/*安全密匙*/,
       safeKeyValue      VARCHAR(255) 	/*安全密匙*/,
       username          VARCHAR(255) not null 	/*用户名*/,
       zipCode           VARCHAR(255) 	/*邮编*/,
       attributeValue0   VARCHAR(255) 	/*会员注册项值0*/,
       attributeValue1   VARCHAR(255) 	/*会员注册项值1*/,
       attributeValue2   VARCHAR(255) 	/*会员注册项值2*/,
       attributeValue3   VARCHAR(255) 	/*会员注册项值3*/,
       attributeValue4   VARCHAR(255) 	/*会员注册项值4*/,
       attributeValue5   VARCHAR(255) 	/*会员注册项值5*/,
       attributeValue6   VARCHAR(255) 	/*会员注册项值6*/,
       attributeValue7   VARCHAR(255) 	/*会员注册项值7*/,
       attributeValue8   VARCHAR(255) 	/*会员注册项值8*/,
       attributeValue9   VARCHAR(255) 	/*会员注册项值9*/
);
alter  table MEMBER
       add constraint PK_member_id primary key (id);
create index IDX_member_area_id on MEMBER(area_id);
create index IDX_memberRank_id on MEMBER(memberRank_id);
create unique index IDU_member_email on MEMBER(email);
create unique index IDU_member_mobile on MEMBER(mobile);
create unique index IDU_member_username on MEMBER(username);

-- memberattribute
/*
警告: 字段名可能非法 - options
警告: 字段名可能非法 - type
*/
create table  memberattribute
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       isEnabled         BIT not null 	/*是否启用*/,
       isRequired        BIT not null 	/*是否必填*/,
       name              VARCHAR(255) not null 	/*名称*/,
       OPTIONS         BLOB 	/*可选项*/,
       pattern           VARCHAR(255) 	/*配比*/,
       propertyIndex     INTEGER 	/*属性序号*/,
       TYPE            INTEGER not null 	/*类型*/
);
alter  table memberattribute
       add constraint PK_memberattribute_id primary key (id);

-- memberdepositlog
/*
警告: 字段名可能非法 - type
*/
create table  memberdepositlog
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       balance           NUMERIC(23,6) not null 	/*当前余额*/,
       credit            NUMERIC(23,6) not null 	/*收入金额*/,
       debit             NUMERIC(23,6) not null 	/*支出金额*/,
       memo              VARCHAR(255) 	/*备注*/,
       TYPE            INTEGER not null 	/*类型*/,
       member_id         INTEGER not null 	/*会员*/
);
alter  table memberdepositlog
       add constraint PK_memberdepositlog_id primary key (id);
create index IDX_memberdlog_member_id448F on memberdepositlog(member_id);

-- memberrank
/*
警告: 字段名可能非法 - scale
*/
create table  memberrank
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       amount            NUMERIC(23,6) 	/*消费金额*/,
       isDefault         BIT not null 	/*是否默认*/,
       isSpecial         BIT not null 	/*是否特殊*/,
       name              VARCHAR(255) not null 	/*名称*/,
       SCALE           NUMERIC not null 	/*优惠比例*/
);
alter  table memberrank
       add constraint PK_memberrank_id primary key (id);

-- message
/*
警告: 字段名可能非法 - content
*/
create table  message
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       CONTENT         BLOB not null 	/*内容*/,
       ip                VARCHAR(255) not null 	/*ip*/,
       isDraft           BIT not null 	/*是否为草稿*/,
       receiverDelete    BIT not null 	/*收件人删除*/,
       receiverRead      BIT not null 	/*收件人已读*/,
       senderDelete      BIT not null 	/*发件人删除*/,
       senderRead        BIT not null 	/*发件人已读*/,
       title             VARCHAR(255) not null 	/*标题*/,
       forMessage_id     INTEGER 	/*原消息*/,
       receiver_id       INTEGER 	/*收件人*/,
       sender_id         INTEGER 	/*发件人*/
);
alter  table message
       add constraint PK_message_id primary key (id);
create index IDX_message_forMessage_id on message(forMessage_id);
create index IDX_message_receiver_id on message(receiver_id);
create index IDX_message_sender_id on message(sender_id);

-- messageconfig
/*
警告: 字段名可能非法 - type
*/
create table  messageconfig
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       isMailEnabled     BIT not null 	/*是否启用邮件*/,
       isSmsEnabled      BIT not null 	/*是否启用短信*/,
       TYPE            INTEGER not null 	/*类型*/
);
alter  table messageconfig
       add constraint PK_messageconfig_id primary key (id);
create unique index IDU_messageconfig_type on messageconfig(TYPE);

-- navigation
/*
警告: 字段名可能非法 - position
*/
create table  navigation
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       isBlankTarget     BIT not null 	/*是否新窗口打开*/,
       name              VARCHAR(255) not null 	/*名称*/,
       POSITION        INTEGER not null 	/*位置*/,
       url               VARCHAR(255) not null 	/*链接地址*/
);
alter  table navigation
       add constraint PK_navigation_id primary key (id);

-- orderitem
/*
警告: 字段名可能非法 - type
*/
create table  orderitem
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       commissionTotals  NUMERIC(23,6) not null 	/*佣金小计*/,
       isDelivery        BIT not null 	/*是否需要物流*/,
       name              VARCHAR(255) not null 	/*名称*/,
       price             NUMERIC(23,6) not null 	/*价格*/,
       quantity          INTEGER not null 	/*数量*/,
       returnedQuantity  INTEGER not null 	/*已退货数量*/,
       shippedQuantity   INTEGER not null 	/*已发货数量*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       specifications    BLOB 	/*规格*/,
       thumbnail         VARCHAR(255) 	/*缩略图*/,
       TYPE            INTEGER not null 	/*类型*/,
       weight            INTEGER 	/*重量*/,
       orders            INTEGER not null 	/*订单*/,
       sku_id            INTEGER 	/*SKU*/
);
alter  table orderitem
       add constraint PK_orderitem_id primary key (id);
create index IDX_orderitem_orders on orderitem(orders);
create index IDX_orderitem_sku_id on orderitem(sku_id);

-- orderlog
/*
警告: 字段名可能非法 - type
*/
create table  orderlog
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       detail            VARCHAR(255) 	/*详情*/,
       TYPE            INTEGER not null 	/*类型*/,
       orders            INTEGER not null 	/*订单*/
);
alter  table orderlog
       add constraint PK_orderlog_id primary key (id);
create index IDX_orderlog_orders on orderlog(orders);

-- orderpayment
/*
警告: 字段名可能非法 - method
*/
create table  orderpayment
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       account           VARCHAR(255) 	/*收款账号*/,
       amount            NUMERIC(23,6) not null 	/*付款金额*/,
       bank              VARCHAR(255) 	/*收款银行*/,
       fee               NUMERIC(23,6) not null 	/*支付手续费*/,
       memo              VARCHAR(255) 	/*备注*/,
       METHOD          INTEGER not null 	/*方式*/,
       payer             VARCHAR(255) 	/*付款人*/,
       paymentMethod     VARCHAR(255) 	/*支付方式*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       orders            INTEGER not null 	/*订单*/
);
alter  table orderpayment
       add constraint PK_orderpayment_id primary key (id);
create unique index IDU_orderpayment_sn on orderpayment(sn);
create index IDX_orderpayment_orders on orderpayment(orders);

-- orderrefunds
/*
警告: 字段名可能非法 - method
*/
create table  orderrefunds
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       account           VARCHAR(255) 	/*退款账号*/,
       amount            NUMERIC(23,6) not null 	/*退款金额*/,
       bank              VARCHAR(255) 	/*退款银行*/,
       memo              VARCHAR(255) 	/*备注*/,
       METHOD          INTEGER not null 	/*方式*/,
       payee             VARCHAR(255) 	/*收款人*/,
       paymentMethod     VARCHAR(255) 	/*支付方式*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       orders            INTEGER not null 	/*订单*/
);
alter  table orderrefunds
       add constraint PK_orderrefunds_id primary key (id);
create unique index IDU_orderrefunds_sn on orderrefunds(sn);
create index IDX_orderrefunds_orders on orderrefunds(orders);

-- orderreturns
create table  orderreturns
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       address           VARCHAR(255) 	/*地址*/,
       area              VARCHAR(255) 	/*地区*/,
       deliveryCorp      VARCHAR(255) 	/*物流公司*/,
       freight           NUMERIC(23,6) 	/*物流费用*/,
       memo              VARCHAR(255) 	/*备注*/,
       phone             VARCHAR(255) 	/*电话*/,
       shipper           VARCHAR(255) 	/*发货人*/,
       shippingMethod    VARCHAR(255) 	/*配送方式*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       trackingNo        VARCHAR(255) 	/*运单号*/,
       zipCode           VARCHAR(255) 	/*邮编*/,
       orders            INTEGER not null 	/*订单*/
);
alter  table orderreturns
       add constraint PK_orderreturns_id primary key (id);
create unique index IDU_orderreturns_sn on orderreturns(sn);
create index IDX_orderreturns_orders on orderreturns(orders);

-- orderreturnsitem
create table  orderreturnsitem
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       name              VARCHAR(255) not null 	/*名称*/,
       quantity          INTEGER not null 	/*数量*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       specifications    BLOB 	/*规格*/,
       orderReturns_id   INTEGER not null 	/*订单退货*/
);
alter  table orderreturnsitem
       add constraint PK_orderreturnsitem_id primary key (id);
create index IDX_orderretem_orderRe_id0239 on orderreturnsitem(orderReturns_id);

-- orders
/*
警告: 字段名可能非法 - status
警告: 字段名可能非法 - type
*/
create table  orders
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       address           VARCHAR(255) 	/*地址*/,
       amount            NUMERIC(23,6) not null 	/*订单金额*/,
       amountPaid        NUMERIC(23,6) not null 	/*已付金额*/,
       areaName          VARCHAR(255) 	/*地区名称*/,
       completeDate      DATETIME 	/*完成日期*/,
       consignee         VARCHAR(255) 	/*收货人*/,
       couponDiscount    NUMERIC(23,6) not null 	/*优惠券折扣*/,
       exchangePoint     INTEGER not null 	/*兑换积分*/,
       expire            DATETIME 	/*过期时间*/,
       fee               NUMERIC(23,6) not null 	/*支付手续费*/,
       freight           NUMERIC(23,6) not null 	/*运费*/,
       invoiceContent    VARCHAR(255) 	/*发票*/,
       invoiceTitle      VARCHAR(255) 	/*发票*/,
       isAllocatedStock  BIT not null 	/*是否已分配库存*/,
       isExchangePoint   BIT not null 	/*是否已兑换积分*/,
       isUseCouponCode   BIT not null 	/*是否已使用优惠码*/,
       memo              VARCHAR(255) 	/*附言*/,
       offsetAmount      NUMERIC(23,6) not null 	/*调整金额*/,
       paymentMethodName VARCHAR(255) 	/*支付方式名称*/,
       paymentMethodType INTEGER 	/*支付方式类型*/,
       phone             VARCHAR(255) 	/*电话*/,
       price             NUMERIC(23,6) not null 	/*价格*/,
       promotionDiscount NUMERIC(23,6) not null 	/*促销折扣*/,
       promotionNames    BLOB 	/*促销名称*/,
       quantity          INTEGER not null 	/*数量*/,
       refundAmount      NUMERIC(23,6) not null 	/*退款金额*/,
       returnedQuantity  INTEGER not null 	/*已退货数量*/,
       rewardPoint       INTEGER not null 	/*赠送积分*/,
       shippedQuantity   INTEGER not null 	/*已发货数量*/,
       shippingMethodName VARCHAR(255) 	/*配送方式名称*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       STATUS          INTEGER not null 	/*状态*/,
       tax               NUMERIC(23,6) not null 	/*税金*/,
       TYPE            INTEGER not null 	/*类型*/,
       weight            INTEGER not null 	/*重量*/,
       zipCode           VARCHAR(255) 	/*邮编*/,
       area_id           INTEGER 	/*地区*/,
       couponCode_id     INTEGER 	/*优惠码*/,
       member_id         INTEGER not null 	/*会员*/,
       paymentMethod_id  INTEGER 	/*支付方式*/,
       shippingMethod_id INTEGER 	/*配送方式*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table orders
       add constraint PK_orders_id primary key (id);
create unique index IDU_orders_sn on orders(sn);
create index IDX_orders_area_id on orders(area_id);
create index IDX_orders_couponCode_id on orders(couponCode_id);
create index IDX_orders_member_id on orders(member_id);
create index IDX_orders_paymentMeth_idB472 on orders(paymentMethod_id);
create index IDX_orders_shippingMet_id75EB on orders(shippingMethod_id);
create index IDX_orders_store_id on orders(store_id);

-- orders_coupon
create table  orders_coupon
(
       orders_id         INTEGER not null 	/*订单*/,
       coupons_id        INTEGER not null 	/*赠送优惠券*/
);
create index IDX_orders_pon_orders_id072C on orders_coupon(orders_id);
create index IDX_orders_pon_coupons_idBEC6 on orders_coupon(coupons_id);

-- ordershipping
create table  ordershipping
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       address           VARCHAR(255) 	/*地址*/,
       area              VARCHAR(255) 	/*地区*/,
       consignee         VARCHAR(255) 	/*收货人*/,
       deliveryCorp      VARCHAR(255) 	/*物流公司*/,
       deliveryCorpCode  VARCHAR(255) 	/*物流公司代码*/,
       deliveryCorpUrl   VARCHAR(255) 	/*物流公司网址*/,
       freight           NUMERIC(23,6) 	/*物流费用*/,
       memo              VARCHAR(255) 	/*备注*/,
       phone             VARCHAR(255) 	/*电话*/,
       shippingMethod    VARCHAR(255) 	/*配送方式*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       trackingNo        VARCHAR(255) 	/*运单号*/,
       zipCode           VARCHAR(255) 	/*邮编*/,
       orders            INTEGER not null 	/*订单*/
);
alter  table ordershipping
       add constraint PK_ordershipping_id primary key (id);
create unique index IDU_ordershipping_sn on ordershipping(sn);
create index IDX_ordershipping_orders on ordershipping(orders);

-- ordershippingitem
create table  ordershippingitem
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       isDelivery        BIT not null 	/*是否需要物流*/,
       name              VARCHAR(255) not null 	/*SKU名称*/,
       quantity          INTEGER not null 	/*数量*/,
       sn                VARCHAR(255) not null 	/*SKU编号*/,
       specifications    BLOB 	/*规格*/,
       orderShipping_id  INTEGER not null 	/*订单发货*/,
       sku_id            INTEGER 	/*SKU*/
);
alter  table ordershippingitem
       add constraint PK_ordershippingitem_id primary key (id);
create index IDX_ordershtem_orderSh_id6260 on ordershippingitem(orderShipping_id);
create index IDX_ordershtem_sku_id92BA on ordershippingitem(sku_id);

-- parameter
/*
警告: 表名可能非法 - parameter
警告: 字段名可能非法 - names
*/
create table  PARAMETER
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       parameterGroup    VARCHAR(255) not null 	/*参数组*/,
       NAMES           BLOB not null 	/*参数名称*/,
       productCategory_id INTEGER not null 	/*绑定分类*/
);
alter  table PARAMETER
       add constraint PK_parameter_id primary key (id);
create index IDX_parameter_productC_idCF42 on PARAMETER(productCategory_id);

-- paymentmethod
/*
警告: 字段名可能非法 - content
警告: 字段名可能非法 - method
警告: 字段名可能非法 - type
*/
create table  paymentmethod
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       CONTENT         BLOB 	/*内容*/,
       description       VARCHAR(255) 	/*介绍*/,
       icon              VARCHAR(255) 	/*图标*/,
       METHOD          INTEGER not null 	/*方式*/,
       name              VARCHAR(255) not null 	/*名称*/,
       timeout           INTEGER 	/*超时时间*/,
       TYPE            INTEGER not null 	/*类型*/
);
alter  table paymentmethod
       add constraint PK_paymentmethod_id primary key (id);

-- paymenttransaction
/*
警告: 字段名可能非法 - type
*/
create table  paymenttransaction
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       amount            NUMERIC(23,6) not null 	/*金额*/,
       expire            DATETIME 	/*过期时间*/,
       fee               NUMERIC(23,6) not null 	/*支付手续费*/,
       isSuccess         BIT 	/*是否成功*/,
       paymentPluginId   VARCHAR(255) 	/*支付插件ID*/,
       paymentPluginName VARCHAR(255) 	/*支付插件名称*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       TYPE            INTEGER 	/*类型*/,
       orders            INTEGER 	/*订单*/,
       parent_id         INTEGER 	/*父事务*/,
       store_id          INTEGER 	/*店铺*/,
       svc_id            INTEGER 	/*服务*/,
       user_id           INTEGER 	/*用户*/
);
alter  table paymenttransaction
       add constraint PK_paymenttransaction_id primary key (id);
create unique index IDU_paymenttransaction_sn on paymenttransaction(sn);
create index IDX_paymention_ordersB61A on paymenttransaction(orders);
create index IDX_paymention_parent_id9F71 on paymenttransaction(parent_id);
create index IDX_paymention_store_id0E4C on paymenttransaction(store_id);
create index IDX_paymention_svc_id2E01 on paymenttransaction(svc_id);
create index IDX_paymention_user_id8350 on paymenttransaction(user_id);

-- platformsvc
create table  platformsvc
(
       id                INTEGER not null 	/*ID*/
);
alter  table platformsvc
       add constraint PK_platformsvc_id primary key (id);

-- pluginconfig
/*
警告: 字段名可能非法 - attributes
*/
create table  pluginconfig
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       ATTRIBUTES      BLOB 	/*属性*/,
       isEnabled         BIT not null 	/*是否启用*/,
       pluginId          VARCHAR(255) not null 	/*插件ID*/
);
alter  table pluginconfig
       add constraint PK_pluginconfig_id primary key (id);
create unique index IDU_pluginconfig_pluginId on pluginconfig(pluginId);

-- pointlog
/*
警告: 字段名可能非法 - type
*/
create table  pointlog
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       balance           INTEGER not null 	/*当前积分*/,
       credit            INTEGER not null 	/*获取积分*/,
       debit             INTEGER not null 	/*扣除积分*/,
       memo              VARCHAR(255) 	/*备注*/,
       TYPE            INTEGER not null 	/*类型*/,
       member_id         INTEGER not null 	/*会员*/
);
alter  table pointlog
       add constraint PK_pointlog_id primary key (id);
create index IDX_pointlog_member_id on pointlog(member_id);

-- product
/*
警告: 字段名可能非法 - cost
警告: 字段名可能非法 - type
*/
create table  product
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       caption           VARCHAR(255) 	/*副标题*/,
       COST            NUMERIC(23,6) 	/*成本价*/,
       hits              INTEGER not null 	/*点击数*/,
       image             VARCHAR(255) 	/*展示图片*/,
       introduction      BLOB 	/*介绍*/,
       isActive          BIT not null 	/*是否有效*/,
       isDelivery        BIT not null 	/*是否需要物流*/,
       isList            BIT not null 	/*是否列出*/,
       isMarketable      BIT not null 	/*是否上架*/,
       isTop             BIT not null 	/*是否置顶*/,
       keyword           VARCHAR(255) 	/*搜索关键词*/,
       marketPrice       NUMERIC(23,6) not null 	/*市场价*/,
       memo              VARCHAR(255) 	/*备注*/,
       monthHits         INTEGER not null 	/*月点击数*/,
       monthHitsDate     DATETIME not null 	/*月点击数更新日期*/,
       monthSales        INTEGER not null 	/*月销量*/,
       monthSalesDate    DATETIME not null 	/*月销量更新日期*/,
       name              VARCHAR(255) not null 	/*名称*/,
       parameterValues   BLOB 	/*参数值*/,
       price             NUMERIC(23,6) not null 	/*销售价*/,
       productImages     BLOB 	/*商品图片*/,
       sales             INTEGER not null 	/*销量*/,
       score             NUMERIC(12,5) not null 	/*评分*/,
       scoreCount        INTEGER not null 	/*评分数*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       specificationItems BLOB 	/*规格项*/,
       totalScore        INTEGER not null 	/*总评分*/,
       TYPE            INTEGER not null 	/*类型*/,
       unit              VARCHAR(255) 	/*单位*/,
       weekHits          INTEGER not null 	/*周点击数*/,
       weekHitsDate      DATETIME not null 	/*周点击数更新日期*/,
       weekSales         INTEGER not null 	/*周销量*/,
       weekSalesDate     DATETIME not null 	/*周销量更新日期*/,
       weight            INTEGER 	/*重量*/,
       brand_id          INTEGER 	/*品牌*/,
       productCategory_id INTEGER not null 	/*商品分类*/,
       store_id          INTEGER not null 	/*店铺*/,
       storeProductCategory_id INTEGER 	/*店铺商品分类*/
);
alter  table product
       add constraint PK_product_id primary key (id);
create unique index IDU_product_sn on product(sn);
create index IDX_product_brand_id on product(brand_id);
create index IDX_productCategory_id on product(productCategory_id);
create index IDX_product_store_id on product(store_id);
create index IDX_product_storeProdu_id5DF6 on product(storeProductCategory_id);

-- product_producttag
create table  product_producttag
(
       products_id       INTEGER not null 	/*商品*/,
       productTags_id    INTEGER not null 	/*商品标签*/
);

-- product_promotion
create table  product_promotion
(
       products_id       INTEGER not null 	/*商品*/,
       promotions_id     INTEGER not null 	/*促销*/
);

-- product_storeproducttag
create table  product_storeproducttag
(
       products_id       INTEGER not null 	/*商品*/,
       storeProductTags_id INTEGER not null 	/*店铺商品标签*/
);

-- productcategory
create table  productcategory
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       generalRate       NUMERIC not null 	/*普通店铺分佣比例*/,
       grade             INTEGER not null 	/*层级*/,
       name              VARCHAR(255) not null 	/*名称*/,
       selfRate          NUMERIC not null 	/*自营店铺分佣比例*/,
       seoDescription    VARCHAR(255) 	/*页面描述*/,
       seoKeywords       VARCHAR(255) 	/*页面关键词*/,
       seoTitle          VARCHAR(255) 	/*页面标题*/,
       treePath          VARCHAR(255) not null 	/*树路径*/,
       parent_id         INTEGER 	/*上级分类*/
);
alter  table productcategory
       add constraint PK_productcategory_id primary key (id);
create index IDX_productory_parent_id39CF on productcategory(parent_id);

-- productcategory_brand
create table  productcategory_brand
(
       productCategories_id INTEGER not null 	/*商品分类*/,
       brands_id         INTEGER not null 	/*关联品牌*/
);

-- productcategory_promotion
create table  productcategory_promotion
(
       productCategories_id INTEGER not null 	/*商品分类*/,
       promotions_id     INTEGER not null 	/*关联促销*/
);

-- productfavorite
create table  productfavorite
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       member_id         INTEGER not null 	/*会员*/,
       product_id        INTEGER not null 	/*商品*/
);
alter  table productfavorite
       add constraint PK_productfavorite_id primary key (id);
create index IDX_productite_member_id8273 on productfavorite(member_id);
create index IDX_productite_product_id7D25 on productfavorite(product_id);

-- productnotify
create table  productnotify
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       email             VARCHAR(255) not null 	/*E-mail*/,
       hasSent           BIT not null 	/*是否已发送*/,
       member_id         INTEGER 	/*会员*/,
       sku_id            INTEGER not null 	/*SKU*/
);
alter  table productnotify
       add constraint PK_productnotify_id primary key (id);
create index IDX_productify_member_id9214 on productnotify(member_id);
create index IDX_productnotify_sku_id on productnotify(sku_id);

-- producttag
create table  producttag
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       icon              VARCHAR(255) 	/*图标*/,
       memo              VARCHAR(255) 	/*备注*/,
       name              VARCHAR(255) not null 	/*名称*/
);
alter  table producttag
       add constraint PK_producttag_id primary key (id);

-- promotion
/*
警告: 字段名可能非法 - type
*/
create table  promotion
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       beginDate         DATETIME 	/*起始日期*/,
       conditionsAmount  NUMERIC(23,6) 	/*条件金额*/,
       conditionsNumber  INTEGER 	/*条件数量*/,
       creditAmount      NUMERIC(23,6) 	/*减免金额*/,
       creditNumber      INTEGER 	/*满减数量*/,
       discount          NUMERIC 	/*折扣*/,
       endDate           DATETIME 	/*结束日期*/,
       image             VARCHAR(255) 	/*图片*/,
       introduction      BLOB 	/*介绍*/,
       isCouponAllowed   BIT not null 	/*是否允许使用优惠券*/,
       isEnabled         BIT not null 	/*是否启用*/,
       isFreeShipping    BIT not null 	/*是否免运费*/,
       maximumPrice      NUMERIC(23,6) 	/*最大SKU价格*/,
       maximumQuantity   INTEGER 	/*最大SKU数量*/,
       minimumPrice      NUMERIC(23,6) 	/*最小SKU价格*/,
       minimumQuantity   INTEGER 	/*最小SKU数量*/,
       name              VARCHAR(255) not null 	/*名称*/,
       priceExpression   VARCHAR(255) 	/*价格运算表达式*/,
       title             VARCHAR(255) not null 	/*标题*/,
       TYPE            INTEGER not null 	/*类型*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table promotion
       add constraint PK_promotion_id primary key (id);
create index IDX_promotion_store_id on promotion(store_id);

-- promotion_coupon
create table  promotion_coupon
(
       promotions_id     INTEGER not null 	/*促销*/,
       coupons_id        INTEGER not null 	/*赠送优惠券*/
);

-- promotion_memberrank
create table  promotion_memberrank
(
       promotions_id     INTEGER not null 	/*促销*/,
       memberRanks_id    INTEGER not null 	/*允许参加会员等级*/
);

-- promotion_sku
create table  promotion_sku
(
       giftPromotions_id INTEGER not null 	/*赠品促销*/,
       gifts_id          INTEGER not null 	/*赠品*/
);

-- promotionpluginsvc
create table  promotionpluginsvc
(
       promotionPluginId VARCHAR(255) 	/*促销插件Id*/,
       id                INTEGER not null 	/*ID*/
);
alter  table promotionpluginsvc
       add constraint PK_promotionpluginsvc_id primary key (id);

-- receiver
create table  receiver
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       address           VARCHAR(255) not null 	/*地址*/,
       areaName          VARCHAR(255) not null 	/*地区名称*/,
       consignee         VARCHAR(255) not null 	/*收货人*/,
       isDefault         BIT not null 	/*是否默认*/,
       phone             VARCHAR(255) not null 	/*电话*/,
       zipCode           VARCHAR(255) not null 	/*邮编*/,
       area_id           INTEGER not null 	/*地区*/,
       member_id         INTEGER not null 	/*会员*/
);
alter  table receiver
       add constraint PK_receiver_id primary key (id);
create index IDX_receiver_area_id on receiver(area_id);
create index IDX_receiver_member_id on receiver(member_id);

-- review
/*
警告: 字段名可能非法 - content
*/
create table  review
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       CONTENT         VARCHAR(255) not null 	/*内容*/,
       ip                VARCHAR(255) not null 	/*IP*/,
       isShow            BIT not null 	/*是否显示*/,
       score             INTEGER not null 	/*评分*/,
       forReview_id      INTEGER 	/*评论*/,
       member_id         INTEGER not null 	/*会员*/,
       product_id        INTEGER not null 	/*商品*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table review
       add constraint PK_review_id primary key (id);
create index IDX_review_forReview_id on review(forReview_id);
create index IDX_review_member_id on review(member_id);
create index IDX_review_product_id on review(product_id);
create index IDX_review_store_id on review(store_id);

-- role
/*
警告: 表名可能非法 - role
*/
create table  ROLE
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       description       VARCHAR(255) 	/*描述*/,
       isSystem          BIT not null 	/*是否内置*/,
       name              VARCHAR(255) not null 	/*名称*/,
       permissions       BLOB not null 	/*权限*/
);
alter  table ROLE
       add constraint PK_role_id primary key (id);

-- seo
/*
警告: 字段名可能非法 - type
*/
create table  seo
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       description       VARCHAR(255) 	/*页面描述*/,
       keywords          VARCHAR(255) 	/*页面关键词*/,
       title             VARCHAR(255) 	/*页面标题*/,
       TYPE            INTEGER not null 	/*类型*/
);
alter  table seo
       add constraint PK_seo_id primary key (id);
create unique index IDU_seo_type on seo(TYPE);

-- shippingmethod
create table  shippingmethod
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       description       VARCHAR(255) 	/*介绍*/,
       icon              VARCHAR(255) 	/*图标*/,
       name              VARCHAR(255) not null 	/*名称*/,
       defaultDeliveryCorp_id INTEGER 	/*默认物流公司*/
);
alter  table shippingmethod
       add constraint PK_shippingmethod_id primary key (id);
create index IDX_shippinhod_default_id0C2A on shippingmethod(defaultDeliveryCorp_id);

-- shippingmethod_paymentmethod
create table  shippingmethod_paymentmethod
(
       shippingMethods_id INTEGER not null 	/*配送方式*/,
       paymentMethods_id INTEGER not null 	/*支持支付方式*/
);

-- sku
/*
警告: 字段名可能非法 - cost
*/
create table  sku
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       allocatedStock    INTEGER not null 	/*已分配库存*/,
       COST            NUMERIC(23,6) 	/*成本价*/,
       exchangePoint     INTEGER not null 	/*兑换积分*/,
       isDefault         BIT not null 	/*是否默认*/,
       marketPrice       NUMERIC(23,6) not null 	/*市场价*/,
       price             NUMERIC(23,6) not null 	/*销售价*/,
       rewardPoint       INTEGER not null 	/*赠送积分*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       specificationValues BLOB 	/*规格值*/,
       stock             INTEGER not null 	/*库存*/,
       product_id        INTEGER not null 	/*商品*/
);
alter  table sku
       add constraint PK_sku_id primary key (id);
create unique index IDU_sku_sn on sku(sn);
create index IDX_sku_product_id on sku(product_id);

-- sn
/*
警告: 字段名可能非法 - type
*/
create table  sn
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       lastValue         INTEGER not null 	/*末值*/,
       TYPE            INTEGER not null 	/*类型*/
);
alter  table sn
       add constraint PK_sn_id primary key (id);
create unique index IDU_sn_type on sn(TYPE);

-- specification
/*
警告: 字段名可能非法 - options
*/
create table  specification
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       name              VARCHAR(255) not null 	/*名称*/,
       OPTIONS         BLOB not null 	/*可选项*/,
       productCategory_id INTEGER not null 	/*绑定分类*/
);
alter  table specification
       add constraint PK_specification_id primary key (id);
create index IDX_specifiion_product_id8C1C on specification(productCategory_id);

-- statistic
/*
警告: 字段名可能非法 - day
警告: 字段名可能非法 - month
警告: 字段名可能非法 - type
警告: 字段名可能非法 - value
警告: 字段名可能非法 - year
*/
create table  statistic
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       DAY             INTEGER not null 	/*日*/,
       MONTH           INTEGER not null 	/*月*/,
       TYPE            INTEGER not null 	/*类型*/,
       VALUE           NUMERIC(23,6) not null 	/*值*/,
       YEAR            INTEGER not null 	/*年*/,
       store_id          INTEGER 	/*店铺*/
);
alter  table statistic
       add constraint PK_statistic_id primary key (id);
create index IDX_statistic_store_id on statistic(store_id);

-- stocklog
/*
警告: 字段名可能非法 - type
*/
create table  stocklog
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       inQuantity        INTEGER not null 	/*入库数量*/,
       memo              VARCHAR(255) 	/*备注*/,
       outQuantity       INTEGER not null 	/*出库数量*/,
       stock             INTEGER not null 	/*当前库存*/,
       TYPE            INTEGER not null 	/*类型*/,
       sku_id            INTEGER not null 	/*SKU*/
);
alter  table stocklog
       add constraint PK_stocklog_id primary key (id);
create index IDX_stocklog_sku_id on stocklog(sku_id);

-- store
/*
警告: 字段名可能非法 - status
警告: 字段名可能非法 - type
*/
create table  store
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       address           VARCHAR(255) 	/*地址*/,
       bailPaid          NUMERIC(29,12) not null 	/*已付保证金*/,
       discountPromotionEndDate DATETIME 	/*折扣促销到期日期*/,
       email             VARCHAR(255) not null 	/*E-mail*/,
       endDate           DATETIME not null 	/*到期日期*/,
       fullReductionPromotionEndDate DATETIME 	/*满减促销到期日期*/,
       introduction      BLOB 	/*简介*/,
       isEnabled         BIT not null 	/*是否启用*/,
       keyword           VARCHAR(255) 	/*搜索关键词*/,
       logo              VARCHAR(255) 	/*logo*/,
       mobile            VARCHAR(255) not null 	/*手机*/,
       name              VARCHAR(255) not null 	/*名称*/,
       phone             VARCHAR(255) 	/*电话*/,
       STATUS          INTEGER not null 	/*状态*/,
       TYPE            INTEGER not null 	/*类型*/,
       zipCode           VARCHAR(255) 	/*邮编*/,
       business_id       INTEGER not null 	/*商家*/,
       storeCategory_id  INTEGER not null 	/*店铺分类*/,
       storeRank_id      INTEGER not null 	/*店铺等级*/
);
alter  table store
       add constraint PK_store_id primary key (id);
create unique index IDU_store_name on store(name);
create index IDX_store_business_id on store(business_id);
create index IDX_storeCategory_id on store(storeCategory_id);
create index IDX_storeRank_id on store(storeRank_id);

-- store_productcategory
create table  store_productcategory
(
       stores_id         INTEGER not null 	/*店铺*/,
       productCategories_id INTEGER not null 	/*经营分类*/
);

-- storeadimage
create table  storeadimage
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       image             VARCHAR(255) not null 	/*图片*/,
       title             VARCHAR(255) 	/*标题*/,
       url               VARCHAR(255) 	/*链接地址*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table storeadimage
       add constraint PK_storeadimage_id primary key (id);
create index IDX_storeadimage_store_id on storeadimage(store_id);

-- storecategory
create table  storecategory
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       bail              NUMERIC(23,6) not null 	/*保证金*/,
       name              VARCHAR(255) not null 	/*名称*/
);
alter  table storecategory
       add constraint PK_storecategory_id primary key (id);

-- storefavorite
create table  storefavorite
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       member_id         INTEGER not null 	/*会员*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table storefavorite
       add constraint PK_storefavorite_id primary key (id);
create index IDX_storefaite_member_idFF10 on storefavorite(member_id);
create index IDX_storefaite_store_id5C73 on storefavorite(store_id);

-- storeproductcategory
create table  storeproductcategory
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       grade             INTEGER not null 	/*层级*/,
       name              VARCHAR(255) not null 	/*分类名称*/,
       treePath          VARCHAR(255) not null 	/*树路径*/,
       parent_id         INTEGER 	/*上级分类*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table storeproductcategory
       add constraint PK_storeprory_id7D11 primary key (id);
create index IDX_storeprory_parent_id7F8B on storeproductcategory(parent_id);
create index IDX_storeprory_store_id56AD on storeproductcategory(store_id);

-- storeproducttag
create table  storeproducttag
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       icon              VARCHAR(255) 	/*图标*/,
       isEnabled         BIT not null 	/*是否启用*/,
       memo              VARCHAR(255) 	/*备注*/,
       name              VARCHAR(255) not null 	/*名称*/,
       store_id          INTEGER not null 	/*店铺*/
);
alter  table storeproducttag
       add constraint PK_storeproducttag_id primary key (id);
create index IDX_storeprtag_store_idDA31 on storeproducttag(store_id);

-- storerank
create table  storerank
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       orders            INTEGER 	/*排序*/,
       isAllowRegister   BIT not null 	/*是否允许注册*/,
       memo              VARCHAR(255) 	/*备注*/,
       name              VARCHAR(255) not null 	/*名称*/,
       quantity          INTEGER 	/*可发布商品数*/,
       serviceFee        NUMERIC(23,6) not null 	/*服务费*/
);
alter  table storerank
       add constraint PK_storerank_id primary key (id);
create unique index IDU_storerank_name on storerank(name);

-- svc
create table  svc
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       amount            NUMERIC(23,6) not null 	/*金额*/,
       durationDays      INTEGER 	/*有效天数*/,
       sn                VARCHAR(255) not null 	/*编号*/,
       store_id          INTEGER 	/*店铺*/
);
alter  table svc
       add constraint PK_svc_id primary key (id);
create unique index IDU_svc_sn on svc(sn);
create index IDX_svc_store_id on svc(store_id);

-- users
create table  users
(
       id                INTEGER not null 	/*ID*/,
       createDate        DATETIME not null 	/*创建日期*/,
       modifyDate        DATETIME not null 	/*最后修改日期*/,
       isEnabled         BIT not null 	/*是否启用*/,
       isLocked          BIT not null 	/*是否锁定*/,
       lastLoginDate     DATETIME 	/*最后登录日期*/,
       lastLoginIp       VARCHAR(255) 	/*最后登录IP*/,
       lockDate          DATETIME 	/*锁定日期*/
);
alter  table users
       add constraint PK_users_id primary key (id);

alter  table ad
       add constraint FK_adPosition_id foreign key (adPosition_id)
       references adposition(id);

alter  table socialuser
       add constraint FK_socialuser_user_id foreign key (user_id)
       references users(id);

alter  table admin_role
       add constraint FK_admin_role_admins_id foreign key (admins_id)
       references ADMIN(id);
alter  table admin_role
       add constraint FK_admin_role_roles_id foreign key (roles_id)
       references ROLE(id);

alter  table area
       add constraint FK_area_parent_id foreign key (parent_id)
       references area(id);

alter  table areafreightconfig
       add constraint FK_areafrefig_shippin_idB829 foreign key (shippingMethod_id)
       references shippingmethod(id);
alter  table areafreightconfig
       add constraint FK_areafrefig_store_id358E foreign key (store_id)
       references store(id);
alter  table areafreightconfig
       add constraint FK_areafrefig_area_idD57E foreign key (area_id)
       references area(id);

alter  table article
       add constraint FK_articleCategory_id foreign key (articleCategory_id)
       references articlecategory(id);

alter  table article_articletag
       add constraint FK_articletag_article_id9598 foreign key (articles_id)
       references article(id);
alter  table article_articletag
       add constraint FK_articletag_article_id5BEC foreign key (articleTags_id)
       references articletag(id);

alter  table business
       add constraint FK_business_id foreign key (id)
       references users(id);

alter  table articlecategory
       add constraint FK_articleory_parent_id0243 foreign key (parent_id)
       references articlecategory(id);

alter  table ADMIN
       add constraint FK_admin_id foreign key (id)
       references users(id);

alter  table ATTRIBUTE
       add constraint FK_attribute_productC_id10D1 foreign key (productCategory_id)
       references productcategory(id);

alter  table auditlog
       add constraint FK_auditlog_user_id foreign key (user_id)
       references users(id);

alter  table businessdepositlog
       add constraint FK_busineslog_busines_id736A foreign key (business_id)
       references business(id);

alter  table cart
       add constraint FK_cart_member_id foreign key (member_id)
       references MEMBER(id);

alter  table cartitem
       add constraint FK_cartitem_cart_id foreign key (cart_id)
       references cart(id);
alter  table cartitem
       add constraint FK_cartitem_sku_id foreign key (sku_id)
       references sku(id);

alter  table cash
       add constraint FK_cash_business_id foreign key (business_id)
       references business(id);

alter  table categoryapplication
       add constraint FK_categorion_product_id37A2 foreign key (productCategory_id)
       references productcategory(id);
alter  table categoryapplication
       add constraint FK_categorion_store_id2C32 foreign key (store_id)
       references store(id);

alter  table consultation
       add constraint FK_consultion_forCons_idB45A foreign key (forConsultation_id)
       references consultation(id);
alter  table consultation
       add constraint FK_consultion_member_id08AC foreign key (member_id)
       references MEMBER(id);
alter  table consultation
       add constraint FK_consultion_product_id2382 foreign key (product_id)
       references product(id);
alter  table consultation
       add constraint FK_consultation_store_id foreign key (store_id)
       references store(id);

alter  table coupon
       add constraint FK_coupon_store_id foreign key (store_id)
       references store(id);

alter  table couponcode
       add constraint FK_couponcode_coupon_id foreign key (coupon_id)
       references coupon(id);
alter  table couponcode
       add constraint FK_couponcode_member_id foreign key (member_id)
       references MEMBER(id);

alter  table defaultfreightconfig
       add constraint FK_defaultfig_shippin_idD899 foreign key (shippingMethod_id)
       references shippingmethod(id);
alter  table defaultfreightconfig
       add constraint FK_defaultfig_store_id76C5 foreign key (store_id)
       references store(id);

alter  table deliverycenter
       add constraint FK_deliverter_area_id6436 foreign key (area_id)
       references area(id);
alter  table deliverycenter
       add constraint FK_deliverter_store_idBDFA foreign key (store_id)
       references store(id);

alter  table deliverytemplate
       add constraint FK_deliverate_store_idC35C foreign key (store_id)
       references store(id);

alter  table instantmessage
       add constraint FK_instantage_store_idF853 foreign key (store_id)
       references store(id);

alter  table MEMBER
       add constraint FK_member_id foreign key (id)
       references users(id);
alter  table MEMBER
       add constraint FK_member_area_id foreign key (area_id)
       references area(id);
alter  table MEMBER
       add constraint FK_memberRank_id foreign key (memberRank_id)
       references memberrank(id);

alter  table memberdepositlog
       add constraint FK_memberdlog_member_id448F foreign key (member_id)
       references MEMBER(id);

alter  table message
       add constraint FK_message_forMessage_id foreign key (forMessage_id)
       references message(id);
alter  table message
       add constraint FK_message_receiver_id foreign key (receiver_id)
       references MEMBER(id);
alter  table message
       add constraint FK_message_sender_id foreign key (sender_id)
       references MEMBER(id);

alter  table orderitem
       add constraint FK_orderitem_orders foreign key (orders)
       references orders(id);
alter  table orderitem
       add constraint FK_orderitem_sku_id foreign key (sku_id)
       references sku(id);

alter  table orderlog
       add constraint FK_orderlog_orders foreign key (orders)
       references orders(id);

alter  table orderpayment
       add constraint FK_orderpayment_orders foreign key (orders)
       references orders(id);

alter  table orderrefunds
       add constraint FK_orderrefunds_orders foreign key (orders)
       references orders(id);

alter  table orderreturns
       add constraint FK_orderreturns_orders foreign key (orders)
       references orders(id);

alter  table orderreturnsitem
       add constraint FK_orderretem_orderRe_id0239 foreign key (orderReturns_id)
       references orderreturns(id);

alter  table orders
       add constraint FK_orders_area_id foreign key (area_id)
       references area(id);
alter  table orders
       add constraint FK_orders_couponCode_id foreign key (couponCode_id)
       references couponcode(id);
alter  table orders
       add constraint FK_orders_member_id foreign key (member_id)
       references MEMBER(id);
alter  table orders
       add constraint FK_orders_paymentMeth_idB472 foreign key (paymentMethod_id)
       references paymentmethod(id);
alter  table orders
       add constraint FK_orders_shippingMet_id75EB foreign key (shippingMethod_id)
       references shippingmethod(id);
alter  table orders
       add constraint FK_orders_store_id foreign key (store_id)
       references store(id);

alter  table orders_coupon
       add constraint FK_orders_pon_orders_id072C foreign key (orders_id)
       references orders(id);
alter  table orders_coupon
       add constraint FK_orders_pon_coupons_idBEC6 foreign key (coupons_id)
       references coupon(id);

alter  table ordershipping
       add constraint FK_ordershipping_orders foreign key (orders)
       references orders(id);

alter  table ordershippingitem
       add constraint FK_ordershtem_orderSh_id6260 foreign key (orderShipping_id)
       references ordershipping(id);
alter  table ordershippingitem
       add constraint FK_ordershtem_sku_id92BA foreign key (sku_id)
       references sku(id);

alter  table PARAMETER
       add constraint FK_parameter_productC_idCF42 foreign key (productCategory_id)
       references productcategory(id);

alter  table paymenttransaction
       add constraint FK_paymention_ordersB61A foreign key (orders)
       references orders(id);
alter  table paymenttransaction
       add constraint FK_paymention_parent_id9F71 foreign key (parent_id)
       references paymenttransaction(id);
alter  table paymenttransaction
       add constraint FK_paymention_store_id0E4C foreign key (store_id)
       references store(id);
alter  table paymenttransaction
       add constraint FK_paymention_svc_id2E01 foreign key (svc_id)
       references svc(id);
alter  table paymenttransaction
       add constraint FK_paymention_user_id8350 foreign key (user_id)
       references users(id);

alter  table platformsvc
       add constraint FK_platformsvc_id foreign key (id)
       references svc(id);

alter  table pointlog
       add constraint FK_pointlog_member_id foreign key (member_id)
       references MEMBER(id);

alter  table product
       add constraint FK_product_brand_id foreign key (brand_id)
       references brand(id);
alter  table product
       add constraint FK_productCategory_id foreign key (productCategory_id)
       references productcategory(id);
alter  table product
       add constraint FK_product_store_id foreign key (store_id)
       references store(id);
alter  table product
       add constraint FK_product_storeProdu_id5DF6 foreign key (storeProductCategory_id)
       references storeproductcategory(id);

alter  table product_producttag
       add constraint FK_producttag_product_id6BC3 foreign key (products_id)
       references product(id);
alter  table product_producttag
       add constraint FK_producttag_product_id012C foreign key (productTags_id)
       references producttag(id);

alter  table product_promotion
       add constraint FK_production_product_id2B3E foreign key (products_id)
       references product(id);
alter  table product_promotion
       add constraint FK_production_promoti_id5772 foreign key (promotions_id)
       references promotion(id);

alter  table product_storeproducttag
       add constraint FK_producttag_product_id0101 foreign key (products_id)
       references product(id);
alter  table product_storeproducttag
       add constraint FK_producttag_storePr_id1681 foreign key (storeProductTags_id)
       references storeproducttag(id);

alter  table productcategory
       add constraint FK_productory_parent_id39CF foreign key (parent_id)
       references productcategory(id);

alter  table productcategory_brand
       add constraint FK_productand_product_id5E1A foreign key (productCategories_id)
       references productcategory(id);
alter  table productcategory_brand
       add constraint FK_productand_brands_id3B3D foreign key (brands_id)
       references brand(id);

alter  table productcategory_promotion
       add constraint FK_production_product_id4DC7 foreign key (productCategories_id)
       references productcategory(id);
alter  table productcategory_promotion
       add constraint FK_production_promoti_id5503 foreign key (promotions_id)
       references promotion(id);

alter  table productfavorite
       add constraint FK_productite_member_id8273 foreign key (member_id)
       references MEMBER(id);
alter  table productfavorite
       add constraint FK_productite_product_id7D25 foreign key (product_id)
       references product(id);

alter  table productnotify
       add constraint FK_productify_member_id9214 foreign key (member_id)
       references MEMBER(id);
alter  table productnotify
       add constraint FK_productnotify_sku_id foreign key (sku_id)
       references sku(id);

alter  table promotion
       add constraint FK_promotion_store_id foreign key (store_id)
       references store(id);

alter  table promotion_coupon
       add constraint FK_promotipon_promoti_idC3DC foreign key (promotions_id)
       references promotion(id);
alter  table promotion_coupon
       add constraint FK_promotipon_coupons_id8C82 foreign key (coupons_id)
       references coupon(id);

alter  table promotion_memberrank
       add constraint FK_promotiank_promoti_id2937 foreign key (promotions_id)
       references promotion(id);
alter  table promotion_memberrank
       add constraint FK_promotiank_memberR_id7CC7 foreign key (memberRanks_id)
       references memberrank(id);

alter  table promotion_sku
       add constraint FK_promotisku_giftPro_id9890 foreign key (giftPromotions_id)
       references promotion(id);
alter  table promotion_sku
       add constraint FK_promotisku_gifts_id1A00 foreign key (gifts_id)
       references sku(id);

alter  table promotionpluginsvc
       add constraint FK_promotionpluginsvc_id foreign key (id)
       references svc(id);

alter  table receiver
       add constraint FK_receiver_area_id foreign key (area_id)
       references area(id);
alter  table receiver
       add constraint FK_receiver_member_id foreign key (member_id)
       references MEMBER(id);

alter  table review
       add constraint FK_review_forReview_id foreign key (forReview_id)
       references review(id);
alter  table review
       add constraint FK_review_member_id foreign key (member_id)
       references MEMBER(id);
alter  table review
       add constraint FK_review_product_id foreign key (product_id)
       references product(id);
alter  table review
       add constraint FK_review_store_id foreign key (store_id)
       references store(id);

alter  table shippingmethod
       add constraint FK_shippinhod_default_id0C2A foreign key (defaultDeliveryCorp_id)
       references deliverycorp(id);

alter  table shippingmethod_paymentmethod
       add constraint FK_shippinhod_shippin_idFFB3 foreign key (shippingMethods_id)
       references shippingmethod(id);
alter  table shippingmethod_paymentmethod
       add constraint FK_shippinhod_payment_id23AB foreign key (paymentMethods_id)
       references paymentmethod(id);

alter  table sku
       add constraint FK_sku_product_id foreign key (product_id)
       references product(id);

alter  table specification
       add constraint FK_specifiion_product_id8C1C foreign key (productCategory_id)
       references productcategory(id);

alter  table statistic
       add constraint FK_statistic_store_id foreign key (store_id)
       references store(id);

alter  table stocklog
       add constraint FK_stocklog_sku_id foreign key (sku_id)
       references sku(id);

alter  table store
       add constraint FK_store_business_id foreign key (business_id)
       references business(id);
alter  table store
       add constraint FK_storeCategory_id foreign key (storeCategory_id)
       references storecategory(id);
alter  table store
       add constraint FK_storeRank_id foreign key (storeRank_id)
       references storerank(id);

alter  table store_productcategory
       add constraint FK_store_pory_stores_idB2A9 foreign key (stores_id)
       references store(id);
alter  table store_productcategory
       add constraint FK_store_pory_product_id829B foreign key (productCategories_id)
       references productcategory(id);

alter  table storeadimage
       add constraint FK_storeadimage_store_id foreign key (store_id)
       references store(id);

alter  table storefavorite
       add constraint FK_storefaite_member_idFF10 foreign key (member_id)
       references MEMBER(id);
alter  table storefavorite
       add constraint FK_storefaite_store_id5C73 foreign key (store_id)
       references store(id);

alter  table storeproductcategory
       add constraint FK_storeprory_parent_id7F8B foreign key (parent_id)
       references storeproductcategory(id);
alter  table storeproductcategory
       add constraint FK_storeprory_store_id56AD foreign key (store_id)
       references store(id);

alter  table storeproducttag
       add constraint FK_storeprtag_store_idDA31 foreign key (store_id)
       references store(id);

alter  table svc
       add constraint FK_svc_store_id foreign key (store_id)
       references store(id);
