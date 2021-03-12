/* * MySql Sql Generate * */
 
/*
警告: 字段名可能非法 - type
*/

create table  ad
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       beginDate         DATETIME comment '起始日期',
       `CONTENT`         LONGBLOB comment '内容',
       endDate           DATETIME comment '结束日期',
       `PATH`            VARCHAR(255) comment '路径',
       title             VARCHAR(255) not null comment '标题',
       `TYPE`            INT not null comment '类型',
       url               VARCHAR(255) comment '链接地址',
       adPosition_id     INT not null comment '广告位'
) comment '广告';

create table  socialuser
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       loginPluginId     VARCHAR(255) not null comment '登录插件ID',
       uniqueId          VARCHAR(255) not null comment '唯一ID',
       user_id           INT comment '用户'
) comment '社会化用户';

create table  admin_role
(
       admins_id         INT not null comment '管理员',
       roles_id          INT not null comment '角色'
) comment '管理员角色中间表';

create table  adposition
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       description       VARCHAR(255) comment '描述',
       height            INT not null comment '高度',
       name              VARCHAR(255) not null comment '名称',
       `TEMPLATE`        LONGBLOB not null comment '模板',
       width             INT not null comment '宽度'
) comment '广告位';

create table  area
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       fullName          LONGBLOB not null comment '全称',
       grade             INT not null comment '层级',
       name              VARCHAR(255) not null comment '名称',
       treePath          VARCHAR(255) not null comment '树路径',
       parent_id         INT comment '上级地区'
) comment '地区';

create table  areafreightconfig
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       continuePrice     DOUBLE(23,6) not null comment '续重价格',
       continueWeight    INT not null comment '续重量',
       firstPrice        DOUBLE(23,6) not null comment '首重价格',
       firstWeight       INT not null comment '首重量',
       shippingMethod_id INT not null comment '配送方式',
       store_id          INT not null comment '店铺',
       area_id           INT not null comment '地区'
) comment '地区运费配置';

create table  article
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       author            VARCHAR(255) comment '作者',
       `CONTENT`         LONGBLOB comment '内容',
       hits              INT not null comment '点击数',
       isPublication     BIT not null comment '是否发布',
       isTop             BIT not null comment '是否置顶',
       seoDescription    VARCHAR(255) comment '页面描述',
       seoKeywords       VARCHAR(255) comment '页面关键词',
       seoTitle          VARCHAR(255) comment '页面标题',
       title             VARCHAR(255) not null comment '标题',
       articleCategory_id INT not null comment '文章分类'
) comment '文章';


create table  article_articletag
(
       articles_id       INT not null comment '文章',
       articleTags_id    INT not null comment '文章标签'
) comment '文章文章标签中间表';

create table  business
(
       id                INT not null comment 'ID',
       balance           DOUBLE(29,12) not null comment '余额',
       bankAccount       VARCHAR(255) comment '银行账号',
       bankName          VARCHAR(255) comment '银行开户名',
       email             VARCHAR(255) not null comment 'E-mail',
       encodedPassword   VARCHAR(255) not null comment '加密密码',
       frozenFund        DOUBLE(29,12) not null comment '冻结金额',
       idCard            VARCHAR(255) comment '法人代表身份证',
       idCardImage       VARCHAR(255) comment '法人代表身份证图片',
       identificationNumber VARCHAR(255) comment '纳税人识别号',
       legalPerson       VARCHAR(255) comment '法人代表姓名',
       licenseImage      VARCHAR(255) comment '营业执照号图片',
       licenseNumber     VARCHAR(255) comment '营业执照号',
       mobile            VARCHAR(255) comment '手机',
       name              VARCHAR(255) comment '名称',
       organizationCode  VARCHAR(255) comment '组织机构代码',
       organizationImage VARCHAR(255) comment '组织机构代码证图片',
       phone             VARCHAR(255) comment '电话',
       safeKeyExpire     DATETIME comment '安全密匙',
       safeKeyValue      VARCHAR(255) comment '安全密匙',
       taxImage          VARCHAR(255) comment '税务登记证图片',
       username          VARCHAR(255) not null comment '用户名',
       attributeValue0   VARCHAR(255) comment '商家注册项值0',
       attributeValue1   VARCHAR(255) comment '商家注册项值1',
       attributeValue2   VARCHAR(255) comment '商家注册项值2',
       attributeValue3   VARCHAR(255) comment '商家注册项值3',
       attributeValue4   VARCHAR(255) comment '商家注册项值4',
       attributeValue5   VARCHAR(255) comment '商家注册项值5',
       attributeValue6   VARCHAR(255) comment '商家注册项值6',
       attributeValue7   VARCHAR(255) comment '商家注册项值7',
       attributeValue8   VARCHAR(255) comment '商家注册项值8',
       attributeValue9   VARCHAR(255) comment '商家注册项值9',
       attributeValue10  VARCHAR(255) comment '商家注册项值10',
       attributeValue11  VARCHAR(255) comment '商家注册项值11',
       attributeValue12  VARCHAR(255) comment '商家注册项值12',
       attributeValue13  VARCHAR(255) comment '商家注册项值13',
       attributeValue14  VARCHAR(255) comment '商家注册项值14',
       attributeValue15  VARCHAR(255) comment '商家注册项值15',
       attributeValue16  VARCHAR(255) comment '商家注册项值16',
       attributeValue17  VARCHAR(255) comment '商家注册项值17',
       attributeValue18  VARCHAR(255) comment '商家注册项值18',
       attributeValue19  VARCHAR(255) comment '商家注册项值19'
) comment '商家';

create table  articlecategory
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       grade             INT not null comment '层级',
       name              VARCHAR(255) not null comment '名称',
       seoDescription    VARCHAR(255) comment '页面描述',
       seoKeywords       VARCHAR(255) comment '页面关键词',
       seoTitle          VARCHAR(255) comment '页面标题',
       treePath          VARCHAR(255) not null comment '树路径',
       parent_id         INT comment '上级分类'
) comment '文章分类';

create table  articletag
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       icon              VARCHAR(255) comment '图标',
       memo              VARCHAR(255) comment '备注',
       name              VARCHAR(255) not null comment '名称'
) comment '文章标签';

create table  `ADMIN`
(
       id                INT not null comment 'ID',
       department        VARCHAR(255) comment '部门',
       email             VARCHAR(255) not null comment 'E-mail',
       encodedPassword   VARCHAR(255) not null comment '加密密码',
       name              VARCHAR(255) comment '姓名',
       username          VARCHAR(255) not null comment '用户名'
) comment '管理员';

create table  `ATTRIBUTE`
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       name              VARCHAR(255) not null comment '名称',
       `OPTIONS`         LONGBLOB not null comment '可选项',
       propertyIndex     INT not null comment '属性序号',
       productCategory_id INT not null comment '绑定分类'
) comment '属性';

create table  auditlog
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       `ACTION`          VARCHAR(255) not null comment '动作',
       detail            VARCHAR(255) comment '详情',
       ip                VARCHAR(255) not null comment 'IP',
       parameters        LONGBLOB comment '请求参数',
       requestUrl        VARCHAR(255) not null comment '请求URL',
       user_id           INT comment '用户'
) comment '审计日志';

create table  brand
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       introduction      LONGBLOB comment '介绍',
       logo              VARCHAR(255) comment 'logo',
       name              VARCHAR(255) not null comment '名称',
       `TYPE`            INT not null comment '类型',
       url               VARCHAR(255) comment '网址'
) comment '品牌';

create table  businessattribute
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       isEnabled         BIT not null comment '是否启用',
       isRequired        BIT not null comment '是否必填',
       name              VARCHAR(255) not null comment '名称',
       `OPTIONS`         LONGBLOB comment '可选项',
       pattern           VARCHAR(255) comment '配比',
       propertyIndex     INT comment '属性序号',
       `TYPE`            INT not null comment '类型'
) comment '商家注册项';

create table  businessdepositlog
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       balance           DOUBLE(23,6) not null comment '当前余额',
       credit            DOUBLE(23,6) not null comment '收入金额',
       debit             DOUBLE(23,6) not null comment '支出金额',
       memo              VARCHAR(255) comment '备注',
       `TYPE`            INT not null comment '类型',
       business_id       INT not null comment '商家'
) comment '商家预存款记录';

create table  cart
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       expire            DATETIME comment '过期时间',
       cartKey           VARCHAR(255) not null comment '密钥',
       member_id         INT comment '会员'
) comment '购物车';

create table  cartitem
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       quantity          INT not null comment '数量',
       cart_id           INT not null comment '购物车',
       sku_id            INT not null comment 'SKU'
) comment '购物车项';
create table  cash
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       account           VARCHAR(255) not null comment '收款账号',
       amount            DOUBLE(23,6) not null comment '金额',
       bank              VARCHAR(255) not null comment '收款银行',
       `STATUS`          INT not null comment '状态',
       business_id       INT not null comment '商家'
) comment '提现';
create table  categoryapplication
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       rate              DOUBLE not null comment '分佣比例',
       `STATUS`          INT not null comment '状态',
       productCategory_id INT not null comment '经营分类',
       store_id          INT not null comment '店铺'
) comment '经营分类申请';
create table  consultation
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       `CONTENT`         VARCHAR(255) not null comment '内容',
       ip                VARCHAR(255) not null comment 'IP',
       isShow            BIT not null comment '是否显示',
       forConsultation_id INT comment '咨询',
       member_id         INT comment '会员',
       product_id        INT not null comment '商品',
       store_id          INT not null comment '店铺'
) comment '咨询';
create table  coupon
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       beginDate         DATETIME comment '使用起始日期',
       endDate           DATETIME comment '使用结束日期',
       introduction      LONGBLOB comment '介绍',
       isEnabled         BIT not null comment '是否启用',
       isExchange        BIT not null comment '是否允许积分兑换',
       maximumPrice      DOUBLE(23,6) comment '最大商品价格',
       maximumQuantity   INT comment '最大商品数量',
       minimumPrice      DOUBLE(23,6) comment '最小商品价格',
       minimumQuantity   INT comment '最小商品数量',
       name              VARCHAR(255) not null comment '名称',
       `POINT`           INT comment '积分兑换数',
       prefix            VARCHAR(255) not null comment '前缀',
       priceExpression   VARCHAR(255) comment '价格运算表达式',
       store_id          INT comment '店铺'
) comment '优惠券';
create table  couponcode
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       `CODE`            VARCHAR(255) not null comment '号码',
       isUsed            BIT not null comment '是否已使用',
       usedDate          DATETIME comment '使用日期',
       coupon_id         INT not null comment '优惠券',
       member_id         INT comment '会员'
) comment '优惠码';
create table  defaultfreightconfig
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       continuePrice     DOUBLE(23,6) not null comment '续重价格',
       continueWeight    INT not null comment '续重量',
       firstPrice        DOUBLE(23,6) not null comment '首重价格',
       firstWeight       INT not null comment '首重量',
       shippingMethod_id INT not null comment '配送方式',
       store_id          INT not null comment '店铺'
) comment '默认运费配置';
create table  deliverycenter
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       address           VARCHAR(255) not null comment '地址',
       areaName          VARCHAR(255) not null comment '地区名称',
       contact           VARCHAR(255) not null comment '联系人',
       isDefault         BIT not null comment '是否默认',
       memo              VARCHAR(255) comment '备注',
       mobile            VARCHAR(255) comment '手机',
       name              VARCHAR(255) not null comment '名称',
       phone             VARCHAR(255) comment '电话',
       zipCode           VARCHAR(255) comment '邮编',
       area_id           INT comment '地区',
       store_id          INT comment '店铺'
) comment '发货点';
create table  deliverycorp
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       `CODE`            VARCHAR(255) comment '代码',
       name              VARCHAR(255) not null comment '名称',
       url               VARCHAR(255) comment '网址'
) comment '物流公司';
create table  deliverytemplate
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       background        VARCHAR(255) comment '背景图',
       `CONTENT`         LONGBLOB not null comment '内容',
       height            INT not null comment '高度',
       isDefault         BIT not null comment '是否默认',
       memo              VARCHAR(255) comment '备注',
       name              VARCHAR(255) not null comment '名称',
       offsetX           INT not null comment '偏移量X',
       offsetY           INT not null comment '偏移量Y',
       width             INT not null comment '宽度',
       store_id          INT not null comment '店铺'
) comment '快递单模板';
create table  friendlink
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       logo              VARCHAR(255) comment 'logo',
       name              VARCHAR(255) not null comment '名称',
       `TYPE`            INT not null comment '类型',
       url               VARCHAR(255) not null comment '链接地址'
) comment '友情链接';
create table  idgenerator
(
       sequence_name     VARCHAR(255) not null comment '序列名',
       next_val          INT comment '序列值'
) comment 'ID管理表';
create table  instantmessage
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       account           VARCHAR(255) not null comment '账号',
       name              VARCHAR(255) not null comment '名称',
       `TYPE`            INT not null comment '类型',
       store_id          INT comment '店铺'
) comment '即时通讯';
create table  `MEMBER`
(
       id                INT not null comment 'ID',
       area_id           INT comment '地区',
       memberRank_id     INT not null comment '会员等级',
       address           VARCHAR(255) comment '地址',
       amount            DOUBLE(29,12) not null comment '消费金额',
       balance           DOUBLE(29,12) not null comment '余额',
       birth             DATETIME comment '出生日期',
       email             VARCHAR(255) not null comment 'E-mail',
       encodedPassword   VARCHAR(255) not null comment '加密密码',
       gender            INT comment '性别',
       mobile            VARCHAR(255) comment '手机',
       name              VARCHAR(255) comment '姓名',
       phone             VARCHAR(255) comment '电话',
       `POINT`           INT not null comment '积分',
       safeKeyExpire     DATETIME comment '安全密匙',
       safeKeyValue      VARCHAR(255) comment '安全密匙',
       username          VARCHAR(255) not null comment '用户名',
       zipCode           VARCHAR(255) comment '邮编',
       attributeValue0   VARCHAR(255) comment '会员注册项值0',
       attributeValue1   VARCHAR(255) comment '会员注册项值1',
       attributeValue2   VARCHAR(255) comment '会员注册项值2',
       attributeValue3   VARCHAR(255) comment '会员注册项值3',
       attributeValue4   VARCHAR(255) comment '会员注册项值4',
       attributeValue5   VARCHAR(255) comment '会员注册项值5',
       attributeValue6   VARCHAR(255) comment '会员注册项值6',
       attributeValue7   VARCHAR(255) comment '会员注册项值7',
       attributeValue8   VARCHAR(255) comment '会员注册项值8',
       attributeValue9   VARCHAR(255) comment '会员注册项值9'
) comment '会员';
create table  memberattribute
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       isEnabled         BIT not null comment '是否启用',
       isRequired        BIT not null comment '是否必填',
       name              VARCHAR(255) not null comment '名称',
       `OPTIONS`         LONGBLOB comment '可选项',
       pattern           VARCHAR(255) comment '配比',
       propertyIndex     INT comment '属性序号',
       `TYPE`            INT not null comment '类型'
) comment '会员注册项';
create table  memberdepositlog
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       balance           DOUBLE(23,6) not null comment '当前余额',
       credit            DOUBLE(23,6) not null comment '收入金额',
       debit             DOUBLE(23,6) not null comment '支出金额',
       memo              VARCHAR(255) comment '备注',
       `TYPE`            INT not null comment '类型',
       member_id         INT not null comment '会员'
) comment '会员预存款记录';
create table  memberrank
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       amount            DOUBLE(23,6) comment '消费金额',
       isDefault         BIT not null comment '是否默认',
       isSpecial         BIT not null comment '是否特殊',
       name              VARCHAR(255) not null comment '名称',
       `SCALE`           DOUBLE not null comment '优惠比例'
) comment '会员等级';
create table  message
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       `CONTENT`         LONGBLOB not null comment '内容',
       ip                VARCHAR(255) not null comment 'ip',
       isDraft           BIT not null comment '是否为草稿',
       receiverDelete    BIT not null comment '收件人删除',
       receiverRead      BIT not null comment '收件人已读',
       senderDelete      BIT not null comment '发件人删除',
       senderRead        BIT not null comment '发件人已读',
       title             VARCHAR(255) not null comment '标题',
       forMessage_id     INT comment '原消息',
       receiver_id       INT comment '收件人',
       sender_id         INT comment '发件人'
) comment '消息';
create table  messageconfig
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       isMailEnabled     BIT not null comment '是否启用邮件',
       isSmsEnabled      BIT not null comment '是否启用短信',
       `TYPE`            INT not null comment '类型'
) comment '消息配置';
create table  navigation
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       isBlankTarget     BIT not null comment '是否新窗口打开',
       name              VARCHAR(255) not null comment '名称',
       `POSITION`        INT not null comment '位置',
       url               VARCHAR(255) not null comment '链接地址'
) comment '导航';
create table  orderitem
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       commissionTotals  DOUBLE(23,6) not null comment '佣金小计',
       isDelivery        BIT not null comment '是否需要物流',
       name              VARCHAR(255) not null comment '名称',
       price             DOUBLE(23,6) not null comment '价格',
       quantity          INT not null comment '数量',
       returnedQuantity  INT not null comment '已退货数量',
       shippedQuantity   INT not null comment '已发货数量',
       sn                VARCHAR(255) not null comment '编号',
       specifications    LONGBLOB comment '规格',
       thumbnail         VARCHAR(255) comment '缩略图',
       `TYPE`            INT not null comment '类型',
       weight            INT comment '重量',
       orders            INT not null comment '订单',
       sku_id            INT comment 'SKU'
) comment '订单项';
create table  orderlog
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       detail            VARCHAR(255) comment '详情',
       `TYPE`            INT not null comment '类型',
       orders            INT not null comment '订单'
) comment '订单记录';
create table  orderpayment
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       account           VARCHAR(255) comment '收款账号',
       amount            DOUBLE(23,6) not null comment '付款金额',
       bank              VARCHAR(255) comment '收款银行',
       fee               DOUBLE(23,6) not null comment '支付手续费',
       memo              VARCHAR(255) comment '备注',
       `METHOD`          INT not null comment '方式',
       payer             VARCHAR(255) comment '付款人',
       paymentMethod     VARCHAR(255) comment '支付方式',
       sn                VARCHAR(255) not null comment '编号',
       orders            INT not null comment '订单'
) comment '订单支付';
create table  orderrefunds
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       account           VARCHAR(255) comment '退款账号',
       amount            DOUBLE(23,6) not null comment '退款金额',
       bank              VARCHAR(255) comment '退款银行',
       memo              VARCHAR(255) comment '备注',
       `METHOD`          INT not null comment '方式',
       payee             VARCHAR(255) comment '收款人',
       paymentMethod     VARCHAR(255) comment '支付方式',
       sn                VARCHAR(255) not null comment '编号',
       orders            INT not null comment '订单'
) comment '订单退款';
create table  orderreturnsitem
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       name              VARCHAR(255) not null comment '名称',
       quantity          INT not null comment '数量',
       sn                VARCHAR(255) not null comment '编号',
       specifications    LONGBLOB comment '规格',
       orderReturns_id   INT not null comment '订单退货'
) comment '退货项';
create table  orders
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       address           VARCHAR(255) comment '地址',
       amount            DOUBLE(23,6) not null comment '订单金额',
       amountPaid        DOUBLE(23,6) not null comment '已付金额',
       areaName          VARCHAR(255) comment '地区名称',
       completeDate      DATETIME comment '完成日期',
       consignee         VARCHAR(255) comment '收货人',
       couponDiscount    DOUBLE(23,6) not null comment '优惠券折扣',
       exchangePoint     INT not null comment '兑换积分',
       expire            DATETIME comment '过期时间',
       fee               DOUBLE(23,6) not null comment '支付手续费',
       freight           DOUBLE(23,6) not null comment '运费',
       invoiceContent    VARCHAR(255) comment '发票',
       invoiceTitle      VARCHAR(255) comment '发票',
       isAllocatedStock  BIT not null comment '是否已分配库存',
       isExchangePoint   BIT not null comment '是否已兑换积分',
       isUseCouponCode   BIT not null comment '是否已使用优惠码',
       memo              VARCHAR(255) comment '附言',
       offsetAmount      DOUBLE(23,6) not null comment '调整金额',
       paymentMethodName VARCHAR(255) comment '支付方式名称',
       paymentMethodType INT comment '支付方式类型',
       phone             VARCHAR(255) comment '电话',
       price             DOUBLE(23,6) not null comment '价格',
       promotionDiscount DOUBLE(23,6) not null comment '促销折扣',
       promotionNames    LONGBLOB comment '促销名称',
       quantity          INT not null comment '数量',
       refundAmount      DOUBLE(23,6) not null comment '退款金额',
       returnedQuantity  INT not null comment '已退货数量',
       rewardPoint       INT not null comment '赠送积分',
       shippedQuantity   INT not null comment '已发货数量',
       shippingMethodName VARCHAR(255) comment '配送方式名称',
       sn                VARCHAR(255) not null comment '编号',
       `STATUS`          INT not null comment '状态',
       tax               DOUBLE(23,6) not null comment '税金',
       `TYPE`            INT not null comment '类型',
       weight            INT not null comment '重量',
       zipCode           VARCHAR(255) comment '邮编',
       area_id           INT comment '地区',
       couponCode_id     INT comment '优惠码',
       member_id         INT not null comment '会员',
       paymentMethod_id  INT comment '支付方式',
       shippingMethod_id INT comment '配送方式',
       store_id          INT not null comment '店铺'
) comment '订单';
create table  orders_coupon
(
       orders_id         INT not null comment '订单',
       coupons_id        INT not null comment '赠送优惠券'
) comment '订单优惠券中间表';
create table  ordershipping
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       address           VARCHAR(255) comment '地址',
       area              VARCHAR(255) comment '地区',
       consignee         VARCHAR(255) comment '收货人',
       deliveryCorp      VARCHAR(255) comment '物流公司',
       deliveryCorpCode  VARCHAR(255) comment '物流公司代码',
       deliveryCorpUrl   VARCHAR(255) comment '物流公司网址',
       freight           DOUBLE(23,6) comment '物流费用',
       memo              VARCHAR(255) comment '备注',
       phone             VARCHAR(255) comment '电话',
       shippingMethod    VARCHAR(255) comment '配送方式',
       sn                VARCHAR(255) not null comment '编号',
       trackingNo        VARCHAR(255) comment '运单号',
       zipCode           VARCHAR(255) comment '邮编',
       orders            INT not null comment '订单'
) comment '订单发货';
create table  ordershippingitem
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       isDelivery        BIT not null comment '是否需要物流',
       name              VARCHAR(255) not null comment 'SKU名称',
       quantity          INT not null comment '数量',
       sn                VARCHAR(255) not null comment 'SKU编号',
       specifications    LONGBLOB comment '规格',
       orderShipping_id  INT not null comment '订单发货',
       sku_id            INT comment 'SKU'
) comment '发货项';
create table  `PARAMETER`
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       parameterGroup    VARCHAR(255) not null comment '参数组',
       `NAMES`           LONGBLOB not null comment '参数名称',
       productCategory_id INT not null comment '绑定分类'
) comment '参数';
create table  paymentmethod
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       `CONTENT`         LONGBLOB comment '内容',
       description       VARCHAR(255) comment '介绍',
       icon              VARCHAR(255) comment '图标',
       `METHOD`          INT not null comment '方式',
       name              VARCHAR(255) not null comment '名称',
       timeout           INT comment '超时时间',
       `TYPE`            INT not null comment '类型'
) comment '支付方式';
create table  paymenttransaction
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       amount            DOUBLE(23,6) not null comment '金额',
       expire            DATETIME comment '过期时间',
       fee               DOUBLE(23,6) not null comment '支付手续费',
       isSuccess         BIT comment '是否成功',
       paymentPluginId   VARCHAR(255) comment '支付插件ID',
       paymentPluginName VARCHAR(255) comment '支付插件名称',
       sn                VARCHAR(255) not null comment '编号',
       `TYPE`            INT comment '类型',
       orders            INT comment '订单',
       parent_id         INT comment '父事务',
       store_id          INT comment '店铺',
       svc_id            INT comment '服务',
       user_id           INT comment '用户'
) comment '支付事务';
create table  platformsvc
(
       id                INT not null comment 'ID'
) comment '平台服务';
create table  pluginconfig
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       `ATTRIBUTES`      LONGBLOB comment '属性',
       isEnabled         BIT not null comment '是否启用',
       pluginId          VARCHAR(255) not null comment '插件ID'
) comment '插件配置';
create table  pointlog
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       balance           INT not null comment '当前积分',
       credit            INT not null comment '获取积分',
       debit             INT not null comment '扣除积分',
       memo              VARCHAR(255) comment '备注',
       `TYPE`            INT not null comment '类型',
       member_id         INT not null comment '会员'
) comment '积分记录';
create table  product
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       caption           VARCHAR(255) comment '副标题',
       `COST`            DOUBLE(23,6) comment '成本价',
       hits              INT not null comment '点击数',
       image             VARCHAR(255) comment '展示图片',
       introduction      LONGBLOB comment '介绍',
       isActive          BIT not null comment '是否有效',
       isDelivery        BIT not null comment '是否需要物流',
       isList            BIT not null comment '是否列出',
       isMarketable      BIT not null comment '是否上架',
       isTop             BIT not null comment '是否置顶',
       keyword           VARCHAR(255) comment '搜索关键词',
       marketPrice       DOUBLE(23,6) not null comment '市场价',
       memo              VARCHAR(255) comment '备注',
       monthHits         INT not null comment '月点击数',
       monthHitsDate     DATETIME not null comment '月点击数更新日期',
       monthSales        INT not null comment '月销量',
       monthSalesDate    DATETIME not null comment '月销量更新日期',
       name              VARCHAR(255) not null comment '名称',
       parameterValues   LONGBLOB comment '参数值',
       price             DOUBLE(23,6) not null comment '销售价',
       productImages     LONGBLOB comment '商品图片',
       sales             INT not null comment '销量',
       score             DOUBLE(12,6) not null comment '评分',
       scoreCount        INT not null comment '评分数',
       sn                VARCHAR(255) not null comment '编号',
       specificationItems LONGBLOB comment '规格项',
       totalScore        INT not null comment '总评分',
       `TYPE`            INT not null comment '类型',
       unit              VARCHAR(255) comment '单位',
       weekHits          INT not null comment '周点击数',
       weekHitsDate      DATETIME not null comment '周点击数更新日期',
       weekSales         INT not null comment '周销量',
       weekSalesDate     DATETIME not null comment '周销量更新日期',
       weight            INT comment '重量',
       brand_id          INT comment '品牌',
       productCategory_id INT not null comment '商品分类',
       store_id          INT not null comment '店铺',
       storeProductCategory_id INT comment '店铺商品分类',
       attributeValue0   VARCHAR(255) comment '属性值0',
       attributeValue1   VARCHAR(255) comment '属性值1',
       attributeValue2   VARCHAR(255) comment '属性值2',
       attributeValue3   VARCHAR(255) comment '属性值3',
       attributeValue4   VARCHAR(255) comment '属性值4',
       attributeValue5   VARCHAR(255) comment '属性值5',
       attributeValue6   VARCHAR(255) comment '属性值6',
       attributeValue7   VARCHAR(255) comment '属性值7',
       attributeValue8   VARCHAR(255) comment '属性值8',
       attributeValue9   VARCHAR(255) comment '属性值9'
) comment '商品';
create table  product_promotion
(
       products_id       INT not null comment '商品',
       promotions_id     INT not null comment '促销'
) comment '商品促销中间表';
create table  product_storeproducttag
(
       products_id       INT not null comment '商品',
       storeProductTags_id INT not null comment '店铺商品标签'
) comment '商品店铺商品标签中间表';
create table  productcategory
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       generalRate       DOUBLE not null comment '普通店铺分佣比例',
       grade             INT not null comment '层级',
       name              VARCHAR(255) not null comment '名称',
       selfRate          DOUBLE not null comment '自营店铺分佣比例',
       seoDescription    VARCHAR(255) comment '页面描述',
       seoKeywords       VARCHAR(255) comment '页面关键词',
       seoTitle          VARCHAR(255) comment '页面标题',
       treePath          VARCHAR(255) not null comment '树路径',
       parent_id         INT comment '上级分类'
) comment '商品分类';
create table  productcategory_brand
(
       productCategories_id INT not null comment '商品分类',
       brands_id         INT not null comment '关联品牌'
) comment '商品分类品牌中间表';
create table  productcategory_promotion
(
       productCategories_id INT not null comment '商品分类',
       promotions_id     INT not null comment '关联促销'
) comment '商品分类促销中间表';
create table  productfavorite
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       member_id         INT not null comment '会员',
       product_id        INT not null comment '商品'
) comment '商品收藏';
create table  productnotify
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       email             VARCHAR(255) not null comment 'E-mail',
       hasSent           BIT not null comment '是否已发送',
       member_id         INT comment '会员',
       sku_id            INT not null comment 'SKU'
) comment '到货通知';
create table  producttag
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       icon              VARCHAR(255) comment '图标',
       memo              VARCHAR(255) comment '备注',
       name              VARCHAR(255) not null comment '名称'
) comment '商品标签';
create table  promotion
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       beginDate         DATETIME comment '起始日期',
       conditionsAmount  DOUBLE(23,6) comment '条件金额',
       conditionsNumber  INT comment '条件数量',
       creditAmount      DOUBLE(23,6) comment '减免金额',
       creditNumber      INT comment '满减数量',
       discount          DOUBLE comment '折扣',
       endDate           DATETIME comment '结束日期',
       image             VARCHAR(255) comment '图片',
       introduction      LONGBLOB comment '介绍',
       isCouponAllowed   BIT not null comment '是否允许使用优惠券',
       isEnabled         BIT not null comment '是否启用',
       isFreeShipping    BIT not null comment '是否免运费',
       maximumPrice      DOUBLE(23,6) comment '最大SKU价格',
       maximumQuantity   INT comment '最大SKU数量',
       minimumPrice      DOUBLE(23,6) comment '最小SKU价格',
       minimumQuantity   INT comment '最小SKU数量',
       name              VARCHAR(255) not null comment '名称',
       priceExpression   VARCHAR(255) comment '价格运算表达式',
       title             VARCHAR(255) not null comment '标题',
       `TYPE`            INT not null comment '类型',
       store_id          INT not null comment '店铺'
) comment '促销';
create table  promotion_coupon
(
       promotions_id     INT not null comment '促销',
       coupons_id        INT not null comment '赠送优惠券'
) comment '促销优惠券中间表';
create table  promotion_memberrank
(
       promotions_id     INT not null comment '促销',
       memberRanks_id    INT not null comment '允许参加会员等级'
) comment '促销会员等级中间表';
create table  promotion_sku
(
       giftPromotions_id INT not null comment '赠品促销',
       gifts_id          INT not null comment '赠品'
) comment '促销SKU中间表';
create table  promotionpluginsvc
(
       promotionPluginId VARCHAR(255) comment '促销插件Id',
       id                INT not null comment 'ID'
) comment '促销插件服务';
create table  receiver
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       address           VARCHAR(255) not null comment '地址',
       areaName          VARCHAR(255) not null comment '地区名称',
       consignee         VARCHAR(255) not null comment '收货人',
       isDefault         BIT not null comment '是否默认',
       phone             VARCHAR(255) not null comment '电话',
       zipCode           VARCHAR(255) not null comment '邮编',
       area_id           INT not null comment '地区',
       member_id         INT not null comment '会员'
) comment '收货地址';
create table  review
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       `CONTENT`         VARCHAR(255) not null comment '内容',
       ip                VARCHAR(255) not null comment 'IP',
       isShow            BIT not null comment '是否显示',
       score             INT not null comment '评分',
       forReview_id      INT comment '评论',
       member_id         INT not null comment '会员',
       product_id        INT not null comment '商品',
       store_id          INT not null comment '店铺'
) comment '评论';
create table  `ROLE`
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       description       VARCHAR(255) comment '描述',
       isSystem          BIT not null comment '是否内置',
       name              VARCHAR(255) not null comment '名称',
       permissions       LONGBLOB not null comment '权限'
) comment '角色';
create table  seo
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       description       VARCHAR(255) comment '页面描述',
       keywords          VARCHAR(255) comment '页面关键词',
       title             VARCHAR(255) comment '页面标题',
       `TYPE`            INT not null comment '类型'
) comment 'SEO设置';
create table  shippingmethod
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       description       VARCHAR(255) comment '介绍',
       icon              VARCHAR(255) comment '图标',
       name              VARCHAR(255) not null comment '名称',
       defaultDeliveryCorp_id INT comment '默认物流公司'
) comment '配送方式';
create table  shippingmethod_paymentmethod
(
       shippingMethods_id INT not null comment '配送方式',
       paymentMethods_id INT not null comment '支持支付方式'
) comment '配送方式支付方式中间表';
create table  sku
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       allocatedStock    INT not null comment '已分配库存',
       `COST`            DOUBLE(23,6) comment '成本价',
       exchangePoint     INT not null comment '兑换积分',
       isDefault         BIT not null comment '是否默认',
       marketPrice       DOUBLE(23,6) not null comment '市场价',
       price             DOUBLE(23,6) not null comment '销售价',
       rewardPoint       INT not null comment '赠送积分',
       sn                VARCHAR(255) not null comment '编号',
       specificationValues LONGBLOB comment '规格值',
       stock             INT not null comment '库存',
       product_id        INT not null comment '商品'
) comment 'SKU';
create table  sn
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       lastValue         INT not null comment '末值',
       `TYPE`            INT not null comment '类型'
) comment '序列号';
create table  specification
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       name              VARCHAR(255) not null comment '名称',
       `OPTIONS`         LONGBLOB not null comment '可选项',
       productCategory_id INT not null comment '绑定分类'
) comment '规格';
create table  statistic
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       `DAY`             INT not null comment '日',
       `MONTH`           INT not null comment '月',
       `TYPE`            INT not null comment '类型',
       `VALUE`           DOUBLE(23,6) not null comment '值',
       `YEAR`            INT not null comment '年',
       store_id          INT comment '店铺'
) comment '统计';
create table  stocklog
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       inQuantity        INT not null comment '入库数量',
       memo              VARCHAR(255) comment '备注',
       outQuantity       INT not null comment '出库数量',
       stock             INT not null comment '当前库存',
       `TYPE`            INT not null comment '类型',
       sku_id            INT not null comment 'SKU'
) comment '库存记录';
create table  store
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       address           VARCHAR(255) comment '地址',
       bailPaid          DOUBLE(29,12) not null comment '已付保证金',
       discountPromotionEndDate DATETIME comment '折扣促销到期日期',
       email             VARCHAR(255) not null comment 'E-mail',
       endDate           DATETIME not null comment '到期日期',
       fullReductionPromotionEndDate DATETIME comment '满减促销到期日期',
       introduction      LONGBLOB comment '简介',
       isEnabled         BIT not null comment '是否启用',
       keyword           VARCHAR(255) comment '搜索关键词',
       logo              VARCHAR(255) comment 'logo',
       mobile            VARCHAR(255) not null comment '手机',
       name              VARCHAR(255) not null comment '名称',
       phone             VARCHAR(255) comment '电话',
       `STATUS`          INT not null comment '状态',
       `TYPE`            INT not null comment '类型',
       zipCode           VARCHAR(255) comment '邮编',
       business_id       INT not null comment '商家',
       storeCategory_id  INT not null comment '店铺分类',
       storeRank_id      INT not null comment '店铺等级'
) comment '店铺';
create table  store_productcategory
(
       stores_id         INT not null comment '店铺',
       productCategories_id INT not null comment '经营分类'
) comment '店铺商品分类中间表';
create table  storeadimage
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       image             VARCHAR(255) not null comment '图片',
       title             VARCHAR(255) comment '标题',
       url               VARCHAR(255) comment '链接地址',
       store_id          INT not null comment '店铺'
) comment '店铺广告图片';
create table  storecategory
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       bail              DOUBLE(23,6) not null comment '保证金',
       name              VARCHAR(255) not null comment '名称'
) comment '店铺分类';
create table  storefavorite
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       member_id         INT not null comment '会员',
       store_id          INT not null comment '店铺'
) comment '店铺收藏';
create table  storeproductcategory
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       grade             INT not null comment '层级',
       name              VARCHAR(255) not null comment '分类名称',
       treePath          VARCHAR(255) not null comment '树路径',
       parent_id         INT comment '上级分类',
       store_id          INT not null comment '店铺'
) comment '店铺商品分类';
create table  storeproducttag
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       icon              VARCHAR(255) comment '图标',
       isEnabled         BIT not null comment '是否启用',
       memo              VARCHAR(255) comment '备注',
       name              VARCHAR(255) not null comment '名称',
       store_id          INT not null comment '店铺'
) comment '店铺商品标签';
 create table  storerank
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       orders            INT comment '排序',
       isAllowRegister   BIT not null comment '是否允许注册',
       memo              VARCHAR(255) comment '备注',
       name              VARCHAR(255) not null comment '名称',
       quantity          INT comment '可发布商品数',
       serviceFee        DOUBLE(23,6) not null comment '服务费'
) comment '店铺等级';
create table  svc
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       amount            DOUBLE(23,6) not null comment '金额',
       durationDays      INT comment '有效天数',
       sn                VARCHAR(255) not null comment '编号',
       store_id          INT comment '店铺'
) comment '服务';
create table  users
(
       id                INT not null comment 'ID',
       createDate        DATETIME not null comment '创建日期',
       modifyDate        DATETIME not null comment '最后修改日期',
       isEnabled         BIT not null comment '是否启用',
       isLocked          BIT not null comment '是否锁定',
       lastLoginDate     DATETIME comment '最后登录日期',
       lastLoginIp       VARCHAR(255) comment '最后登录IP',
       lockDate          DATETIME comment '锁定日期'
) comment '用户';
create table  product_producttag
(
       products_id       INT not null comment '商品',
       productTags_id    INT not null comment '商品标签'
) comment '商品商品标签中间表';

ALTER TABLE ad ADD CONSTRAINT PK_ad_id PRIMARY KEY (id);

CREATE INDEX IDX_adPosition_id ON ad (adPosition_id);

ALTER TABLE socialuser ADD CONSTRAINT PK_socialuser_id PRIMARY KEY (id);

CREATE INDEX IDX_socialuser_loginPlnId1870 ON socialuser (loginPluginId);

CREATE INDEX IDX_socialuser_user_id ON socialuser (user_id);

ALTER TABLE adposition ADD CONSTRAINT PK_adposition_id PRIMARY KEY (id);

ALTER TABLE area ADD CONSTRAINT PK_area_id PRIMARY KEY (id);

CREATE INDEX IDX_area_parent_id ON area (parent_id);

ALTER TABLE areafreightconfig ADD CONSTRAINT PK_areafreightconfig_id PRIMARY KEY (id);

CREATE INDEX IDX_areafrefig_shippin_idB829 ON areafreightconfig (shippingMethod_id);

CREATE INDEX IDX_areafrefig_store_id358E ON areafreightconfig (store_id);

CREATE INDEX IDX_areafrefig_area_idD57E ON areafreightconfig (area_id);

ALTER TABLE article ADD CONSTRAINT PK_article_id PRIMARY KEY (id);

CREATE INDEX IDX_articleCategory_id ON article (articleCategory_id);

ALTER TABLE business ADD CONSTRAINT PK_business_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_business_email ON business (email);

CREATE UNIQUE INDEX IDU_business_mobile ON business (mobile);

CREATE UNIQUE INDEX IDU_business_username ON business (username);

ALTER TABLE articlecategory ADD CONSTRAINT PK_articlecategory_id PRIMARY KEY (id);

CREATE INDEX IDX_articleory_parent_id0243 ON articlecategory (parent_id);

ALTER TABLE articletag ADD CONSTRAINT PK_articletag_id PRIMARY KEY (id);

ALTER TABLE ADMIN ADD CONSTRAINT PK_admin_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_admin_email ON ADMIN (email);

CREATE UNIQUE INDEX IDU_admin_username ON ADMIN (username);

ALTER TABLE ATTRIBUTE ADD CONSTRAINT PK_attribute_id PRIMARY KEY (id);

CREATE INDEX IDX_attribute_productC_id10D1 ON ATTRIBUTE (productCategory_id);

ALTER TABLE auditlog ADD CONSTRAINT PK_auditlog_id PRIMARY KEY (id);

CREATE INDEX IDX_auditlog_user_id ON auditlog (user_id);

ALTER TABLE brand ADD CONSTRAINT PK_brand_id PRIMARY KEY (id);

ALTER TABLE businessattribute ADD CONSTRAINT PK_businessattribute_id PRIMARY KEY (id);

ALTER TABLE businessdepositlog ADD CONSTRAINT PK_businessdepositlog_id PRIMARY KEY (id);

CREATE INDEX IDX_busineslog_busines_id736A ON businessdepositlog (business_id);

ALTER TABLE cart ADD CONSTRAINT PK_cart_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_cartKey ON cart (cartKey);

CREATE INDEX IDX_cart_member_id ON cart (member_id);

ALTER TABLE cartitem ADD CONSTRAINT PK_cartitem_id PRIMARY KEY (id);

CREATE INDEX IDX_cartitem_cart_id ON cartitem (cart_id);

CREATE INDEX IDX_cartitem_sku_id ON cartitem (sku_id);

ALTER TABLE cash ADD CONSTRAINT PK_cash_id PRIMARY KEY (id);

CREATE INDEX IDX_cash_business_id ON cash (business_id);

ALTER TABLE categoryapplication ADD CONSTRAINT PK_categorion_id6D53 PRIMARY KEY (id);

CREATE INDEX IDX_categorion_product_id37A2 ON categoryapplication (productCategory_id);

CREATE INDEX IDX_categorion_store_id2C32 ON categoryapplication (store_id);

ALTER TABLE consultation ADD CONSTRAINT PK_consultation_id PRIMARY KEY (id);

CREATE INDEX IDX_consultion_forCons_idB45A ON consultation (forConsultation_id);

CREATE INDEX IDX_consultion_member_id08AC ON consultation (member_id);

CREATE INDEX IDX_consultion_product_id2382 ON consultation (product_id);

CREATE INDEX IDX_consultation_store_id ON consultation (store_id);

ALTER TABLE coupon ADD CONSTRAINT PK_coupon_id PRIMARY KEY (id);

CREATE INDEX IDX_coupon_store_id ON coupon (store_id);

ALTER TABLE couponcode ADD CONSTRAINT PK_couponcode_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_couponcode_code ON couponcode (CODE);

CREATE INDEX IDX_couponcode_coupon_id ON couponcode (coupon_id);

CREATE INDEX IDX_couponcode_member_id ON couponcode (member_id);

ALTER TABLE defaultfreightconfig ADD CONSTRAINT PK_defaultfig_idD0E3 PRIMARY KEY (id);

CREATE INDEX IDX_defaultfig_shippin_idD899 ON defaultfreightconfig (shippingMethod_id);

CREATE INDEX IDX_defaultfig_store_id76C5 ON defaultfreightconfig (store_id);

ALTER TABLE deliverycenter ADD CONSTRAINT PK_deliverycenter_id PRIMARY KEY (id);

CREATE INDEX IDX_deliverter_area_id6436 ON deliverycenter (area_id);

CREATE INDEX IDX_deliverter_store_idBDFA ON deliverycenter (store_id);

ALTER TABLE deliverycorp ADD CONSTRAINT PK_deliverycorp_id PRIMARY KEY (id);

ALTER TABLE deliverytemplate ADD CONSTRAINT PK_deliverytemplate_id PRIMARY KEY (id);

CREATE INDEX IDX_deliverate_store_idC35C ON deliverytemplate (store_id);

ALTER TABLE friendlink ADD CONSTRAINT PK_friendlink_id PRIMARY KEY (id);

ALTER TABLE idgenerator ADD CONSTRAINT PK_idgenertor_sequencame6A0F PRIMARY KEY (sequence_name);

ALTER TABLE instantmessage ADD CONSTRAINT PK_instantmessage_id PRIMARY KEY (id);

CREATE INDEX IDX_instantage_store_idF853 ON instantmessage (store_id);

ALTER TABLE MEMBER ADD CONSTRAINT PK_member_id PRIMARY KEY (id);

CREATE INDEX IDX_member_area_id ON MEMBER (area_id);

CREATE INDEX IDX_memberRank_id ON MEMBER (memberRank_id);

CREATE UNIQUE INDEX IDU_member_email ON MEMBER (email);

CREATE UNIQUE INDEX IDU_member_mobile ON MEMBER (mobile);

CREATE UNIQUE INDEX IDU_member_username ON MEMBER (username);

ALTER TABLE memberattribute ADD CONSTRAINT PK_memberattribute_id PRIMARY KEY (id);

ALTER TABLE memberdepositlog ADD CONSTRAINT PK_memberdepositlog_id PRIMARY KEY (id);

CREATE INDEX IDX_memberdlog_member_id448F ON memberdepositlog (member_id);

ALTER TABLE memberrank ADD CONSTRAINT PK_memberrank_id PRIMARY KEY (id);

ALTER TABLE message ADD CONSTRAINT PK_message_id PRIMARY KEY (id);

CREATE INDEX IDX_message_forMessage_id ON message (forMessage_id);

CREATE INDEX IDX_message_receiver_id ON message (receiver_id);

CREATE INDEX IDX_message_sender_id ON message (sender_id);

ALTER TABLE messageconfig ADD CONSTRAINT PK_messageconfig_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_messageconfig_type ON messageconfig (TYPE);

ALTER TABLE navigation ADD CONSTRAINT PK_navigation_id PRIMARY KEY (id);

ALTER TABLE orderitem ADD CONSTRAINT PK_orderitem_id PRIMARY KEY (id);

CREATE INDEX IDX_orderitem_orders ON orderitem (orders);

CREATE INDEX IDX_orderitem_sku_id ON orderitem (sku_id);

ALTER TABLE orderlog ADD CONSTRAINT PK_orderlog_id PRIMARY KEY (id);

CREATE INDEX IDX_orderlog_orders ON orderlog (orders);

ALTER TABLE orderpayment ADD CONSTRAINT PK_orderpayment_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_orderpayment_sn ON orderpayment (sn);

CREATE INDEX IDX_orderpayment_orders ON orderpayment (orders);

ALTER TABLE orderrefunds ADD CONSTRAINT PK_orderrefunds_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_orderrefunds_sn ON orderrefunds (sn);

CREATE INDEX IDX_orderrefunds_orders ON orderrefunds (orders);

ALTER TABLE orderreturnsitem ADD CONSTRAINT PK_orderreturns_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_orderreturns_sn ON orderreturnsitem (sn);

CREATE INDEX IDX_orderreturns_orders ON orderreturnsitem (orderReturns_id);

-- ALTER TABLE orderreturnsitem ADD CONSTRAINT PK_orderreturnsitem_id PRIMARY KEY (id);

CREATE INDEX IDX_orderretem_orderRe_id0239 ON orderreturnsitem (orderReturns_id);

ALTER TABLE orders ADD CONSTRAINT PK_orders_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_orders_sn ON orders (sn);

CREATE INDEX IDX_orders_area_id ON orders (area_id);

CREATE INDEX IDX_orders_couponCode_id ON orders (couponCode_id);

CREATE INDEX IDX_orders_member_id ON orders (member_id);

CREATE INDEX IDX_orders_paymentMeth_idB472 ON orders (paymentMethod_id);

CREATE INDEX IDX_orders_shippingMet_id75EB ON orders (shippingMethod_id);

CREATE INDEX IDX_orders_store_id ON orders (store_id);

CREATE INDEX IDX_orders_pon_orders_id072C ON orders_coupon (orders_id);

CREATE INDEX IDX_orders_pon_coupons_idBEC6 ON orders_coupon (coupons_id);

ALTER TABLE ordershipping ADD CONSTRAINT PK_ordershipping_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_ordershipping_sn ON ordershipping (sn);

CREATE INDEX IDX_ordershipping_orders ON ordershipping (orders);

ALTER TABLE ordershippingitem ADD CONSTRAINT PK_ordershippingitem_id PRIMARY KEY (id);

CREATE INDEX IDX_ordershtem_orderSh_id6260 ON ordershippingitem (orderShipping_id);

CREATE INDEX IDX_ordershtem_sku_id92BA ON ordershippingitem (sku_id);

ALTER TABLE PARAMETER ADD CONSTRAINT PK_parameter_id PRIMARY KEY (id);

CREATE INDEX IDX_parameter_productC_idCF42 ON PARAMETER (productCategory_id);

ALTER TABLE paymentmethod ADD CONSTRAINT PK_paymentmethod_id PRIMARY KEY (id);

ALTER TABLE paymenttransaction ADD CONSTRAINT PK_paymenttransaction_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_paymenttransaction_sn ON paymenttransaction (sn);

CREATE INDEX IDX_paymention_ordersB61A ON paymenttransaction (orders);

CREATE INDEX IDX_paymention_parent_id9F71 ON paymenttransaction (parent_id);

CREATE INDEX IDX_paymention_store_id0E4C ON paymenttransaction (store_id);

CREATE INDEX IDX_paymention_svc_id2E01 ON paymenttransaction (svc_id);

CREATE INDEX IDX_paymention_user_id8350 ON paymenttransaction (user_id);

ALTER TABLE platformsvc ADD CONSTRAINT PK_platformsvc_id PRIMARY KEY (id);

ALTER TABLE pluginconfig ADD CONSTRAINT PK_pluginconfig_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_pluginconfig_pluginId ON pluginconfig (pluginId);

ALTER TABLE pointlog ADD CONSTRAINT PK_pointlog_id PRIMARY KEY (id);

CREATE INDEX IDX_pointlog_member_id ON pointlog (member_id);

ALTER TABLE product ADD CONSTRAINT PK_product_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_product_sn ON product (sn);

CREATE INDEX IDX_product_brand_id ON product (brand_id);

CREATE INDEX IDX_productCategory_id ON product (productCategory_id);

CREATE INDEX IDX_product_store_id ON product (store_id);

CREATE INDEX IDX_product_storeProdu_id5DF6 ON product (storeProductCategory_id);

ALTER TABLE productcategory ADD CONSTRAINT PK_productcategory_id PRIMARY KEY (id);

CREATE INDEX IDX_productory_parent_id39CF ON productcategory (parent_id);

ALTER TABLE productfavorite ADD CONSTRAINT PK_productfavorite_id PRIMARY KEY (id);

CREATE INDEX IDX_productite_member_id8273 ON productfavorite (member_id);

CREATE INDEX IDX_productite_product_id7D25 ON productfavorite (product_id);

ALTER TABLE productnotify ADD CONSTRAINT PK_productnotify_id PRIMARY KEY (id);

CREATE INDEX IDX_productify_member_id9214 ON productnotify (member_id);

CREATE INDEX IDX_productnotify_sku_id ON productnotify (sku_id);

ALTER TABLE producttag ADD CONSTRAINT PK_producttag_id PRIMARY KEY (id);

ALTER TABLE promotion ADD CONSTRAINT PK_promotion_id PRIMARY KEY (id);

CREATE INDEX IDX_promotion_store_id ON promotion (store_id);

ALTER TABLE promotionpluginsvc ADD CONSTRAINT PK_promotionpluginsvc_id PRIMARY KEY (id);

ALTER TABLE receiver ADD CONSTRAINT PK_receiver_id PRIMARY KEY (id);

CREATE INDEX IDX_receiver_area_id ON receiver (area_id);

CREATE INDEX IDX_receiver_member_id ON receiver (member_id);

ALTER TABLE review ADD CONSTRAINT PK_review_id PRIMARY KEY (id);

CREATE INDEX IDX_review_forReview_id ON review (forReview_id);

CREATE INDEX IDX_review_member_id ON review (member_id);

CREATE INDEX IDX_review_product_id ON review (product_id);

CREATE INDEX IDX_review_store_id ON review (store_id);

ALTER TABLE ROLE ADD CONSTRAINT PK_role_id PRIMARY KEY (id);

ALTER TABLE seo ADD CONSTRAINT PK_seo_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_seo_type ON seo (TYPE);

ALTER TABLE shippingmethod ADD CONSTRAINT PK_shippingmethod_id PRIMARY KEY (id);

CREATE INDEX IDX_shippinhod_default_id0C2A ON shippingmethod (defaultDeliveryCorp_id);

ALTER TABLE sku ADD CONSTRAINT PK_sku_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_sku_sn ON sku (sn);

CREATE INDEX IDX_sku_product_id ON sku (product_id);

ALTER TABLE sn ADD CONSTRAINT PK_sn_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_sn_type ON sn (TYPE);

ALTER TABLE specification ADD CONSTRAINT PK_specification_id PRIMARY KEY (id);

CREATE INDEX IDX_specifiion_product_id8C1C ON specification (productCategory_id);

ALTER TABLE statistic ADD CONSTRAINT PK_statistic_id PRIMARY KEY (id);

CREATE INDEX IDX_statistic_store_id ON statistic (store_id);

ALTER TABLE stocklog ADD CONSTRAINT PK_stocklog_id PRIMARY KEY (id);

CREATE INDEX IDX_stocklog_sku_id ON stocklog (sku_id);

ALTER TABLE store ADD CONSTRAINT PK_store_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_store_name ON store (NAME);

CREATE INDEX IDX_store_business_id ON store (business_id);

CREATE INDEX IDX_storeCategory_id ON store (storeCategory_id);

CREATE INDEX IDX_storeRank_id ON store (storeRank_id);

ALTER TABLE storeadimage ADD CONSTRAINT PK_storeadimage_id PRIMARY KEY (id);

CREATE INDEX IDX_storeadimage_store_id ON storeadimage (store_id);

ALTER TABLE storecategory ADD CONSTRAINT PK_storecategory_id PRIMARY KEY (id);

ALTER TABLE storefavorite ADD CONSTRAINT PK_storefavorite_id PRIMARY KEY (id);

CREATE INDEX IDX_storefaite_member_idFF10 ON storefavorite (member_id);

CREATE INDEX IDX_storefaite_store_id5C73 ON storefavorite (store_id);

ALTER TABLE storeproductcategory ADD CONSTRAINT PK_storeprory_id7D11 PRIMARY KEY (id);

CREATE INDEX IDX_storeprory_parent_id7F8B ON storeproductcategory (parent_id);

CREATE INDEX IDX_storeprory_store_id56AD ON storeproductcategory (store_id);

ALTER TABLE storeproducttag ADD CONSTRAINT PK_storeproducttag_id PRIMARY KEY (id);

CREATE INDEX IDX_storeprtag_store_idDA31 ON storeproducttag (store_id);

ALTER TABLE storerank ADD CONSTRAINT PK_storerank_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_storerank_name ON storerank (NAME);

ALTER TABLE svc ADD CONSTRAINT PK_svc_id PRIMARY KEY (id);

CREATE UNIQUE INDEX IDU_svc_sn ON svc (sn);

CREATE INDEX IDX_svc_store_id ON svc (store_id);

ALTER TABLE users ADD CONSTRAINT PK_users_id PRIMARY KEY (id);

ALTER TABLE ad ADD CONSTRAINT FK_adPosition_id FOREIGN KEY (adPosition_id) REFERENCES adposition (id);

ALTER TABLE socialuser ADD CONSTRAINT FK_socialuser_user_id FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE admin_role ADD CONSTRAINT FK_admin_role_admins_id FOREIGN KEY (admins_id) REFERENCES ADMIN (id);

ALTER TABLE admin_role ADD CONSTRAINT FK_admin_role_roles_id FOREIGN KEY (roles_id) REFERENCES ROLE (id);

ALTER TABLE area ADD CONSTRAINT FK_area_parent_id FOREIGN KEY (parent_id) REFERENCES area (id);

ALTER TABLE areafreightconfig ADD CONSTRAINT FK_areafrefig_shippin_idB829 FOREIGN KEY (shippingMethod_id) REFERENCES shippingmethod (id);

ALTER TABLE areafreightconfig ADD CONSTRAINT FK_areafrefig_store_id358E FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE areafreightconfig ADD CONSTRAINT FK_areafrefig_area_idD57E FOREIGN KEY (area_id) REFERENCES area (id);

ALTER TABLE article ADD CONSTRAINT FK_articleCategory_id FOREIGN KEY (articleCategory_id) REFERENCES articlecategory (id);

ALTER TABLE article_articletag ADD CONSTRAINT FK_articletag_article_id9598 FOREIGN KEY (articles_id) REFERENCES article (id);

ALTER TABLE article_articletag ADD CONSTRAINT FK_articletag_article_id5BEC FOREIGN KEY (articleTags_id) REFERENCES articletag (id);

ALTER TABLE business ADD CONSTRAINT FK_business_id FOREIGN KEY (id) REFERENCES users (id);

ALTER TABLE articlecategory ADD CONSTRAINT FK_articleory_parent_id0243 FOREIGN KEY (parent_id) REFERENCES articlecategory (id);

ALTER TABLE ADMIN ADD CONSTRAINT FK_admin_id FOREIGN KEY (id) REFERENCES users (id);

ALTER TABLE ATTRIBUTE ADD CONSTRAINT FK_attribute_productC_id10D1 FOREIGN KEY (productCategory_id) REFERENCES productcategory (id);

ALTER TABLE auditlog ADD CONSTRAINT FK_auditlog_user_id FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE businessdepositlog ADD CONSTRAINT FK_busineslog_busines_id736A FOREIGN KEY (business_id) REFERENCES business (id);

ALTER TABLE cart ADD CONSTRAINT FK_cart_member_id FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE cartitem ADD CONSTRAINT FK_cartitem_cart_id FOREIGN KEY (cart_id) REFERENCES cart (id);

ALTER TABLE cartitem ADD CONSTRAINT FK_cartitem_sku_id FOREIGN KEY (sku_id) REFERENCES sku (id);

ALTER TABLE cash ADD CONSTRAINT FK_cash_business_id FOREIGN KEY (business_id) REFERENCES business (id);

ALTER TABLE categoryapplication ADD CONSTRAINT FK_categorion_product_id37A2 FOREIGN KEY (productCategory_id) REFERENCES productcategory (id);

ALTER TABLE categoryapplication ADD CONSTRAINT FK_categorion_store_id2C32 FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE consultation ADD CONSTRAINT FK_consultion_forCons_idB45A FOREIGN KEY (forConsultation_id) REFERENCES consultation (id);

ALTER TABLE consultation ADD CONSTRAINT FK_consultion_member_id08AC FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE consultation ADD CONSTRAINT FK_consultion_product_id2382 FOREIGN KEY (product_id) REFERENCES product (id);

ALTER TABLE consultation ADD CONSTRAINT FK_consultation_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE coupon ADD CONSTRAINT FK_coupon_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE couponcode ADD CONSTRAINT FK_couponcode_coupon_id FOREIGN KEY (coupon_id) REFERENCES coupon (id);

ALTER TABLE couponcode ADD CONSTRAINT FK_couponcode_member_id FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE defaultfreightconfig ADD CONSTRAINT FK_defaultfig_shippin_idD899 FOREIGN KEY (shippingMethod_id) REFERENCES shippingmethod (id);

ALTER TABLE defaultfreightconfig ADD CONSTRAINT FK_defaultfig_store_id76C5 FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE deliverycenter ADD CONSTRAINT FK_deliverter_area_id6436 FOREIGN KEY (area_id) REFERENCES area (id);

ALTER TABLE deliverycenter ADD CONSTRAINT FK_deliverter_store_idBDFA FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE deliverytemplate ADD CONSTRAINT FK_deliverate_store_idC35C FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE instantmessage ADD CONSTRAINT FK_instantage_store_idF853 FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE MEMBER ADD CONSTRAINT FK_member_id FOREIGN KEY (id) REFERENCES users (id);

ALTER TABLE MEMBER ADD CONSTRAINT FK_member_area_id FOREIGN KEY (area_id) REFERENCES area (id);

ALTER TABLE MEMBER ADD CONSTRAINT FK_memberRank_id FOREIGN KEY (memberRank_id) REFERENCES memberrank (id);

ALTER TABLE memberdepositlog ADD CONSTRAINT FK_memberdlog_member_id448F FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE message ADD CONSTRAINT FK_message_forMessage_id FOREIGN KEY (forMessage_id) REFERENCES message (id);

ALTER TABLE message ADD CONSTRAINT FK_message_receiver_id FOREIGN KEY (receiver_id) REFERENCES MEMBER (id);

ALTER TABLE message ADD CONSTRAINT FK_message_sender_id FOREIGN KEY (sender_id) REFERENCES MEMBER (id);

ALTER TABLE orderitem ADD CONSTRAINT FK_orderitem_orders FOREIGN KEY (orders) REFERENCES orders (id);

ALTER TABLE orderitem ADD CONSTRAINT FK_orderitem_sku_id FOREIGN KEY (sku_id) REFERENCES sku (id);

ALTER TABLE orderlog ADD CONSTRAINT FK_orderlog_orders FOREIGN KEY (orders) REFERENCES orders (id);

ALTER TABLE orderpayment ADD CONSTRAINT FK_orderpayment_orders FOREIGN KEY (orders) REFERENCES orders (id);

ALTER TABLE orderrefunds ADD CONSTRAINT FK_orderrefunds_orders FOREIGN KEY (orders) REFERENCES orders (id);

ALTER TABLE orderreturnsitem ADD CONSTRAINT FK_orderreturns_orders FOREIGN KEY (orderReturns_id) REFERENCES orders (id);

ALTER TABLE orderreturnsitem ADD CONSTRAINT FK_orderretem_orderRe_id0239 FOREIGN KEY (orderReturns_id) REFERENCES orderreturnsitem (id);

ALTER TABLE orders ADD CONSTRAINT FK_orders_area_id FOREIGN KEY (area_id) REFERENCES area (id);

ALTER TABLE orders ADD CONSTRAINT FK_orders_couponCode_id FOREIGN KEY (couponCode_id) REFERENCES couponcode (id);

ALTER TABLE orders ADD CONSTRAINT FK_orders_member_id FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE orders ADD CONSTRAINT FK_orders_paymentMeth_idB472 FOREIGN KEY (paymentMethod_id) REFERENCES paymentmethod (id);

ALTER TABLE orders ADD CONSTRAINT FK_orders_shippingMet_id75EB FOREIGN KEY (shippingMethod_id) REFERENCES shippingmethod (id);

ALTER TABLE orders ADD CONSTRAINT FK_orders_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE orders_coupon ADD CONSTRAINT FK_orders_pon_orders_id072C FOREIGN KEY (orders_id) REFERENCES orders (id);

ALTER TABLE orders_coupon ADD CONSTRAINT FK_orders_pon_coupons_idBEC6 FOREIGN KEY (coupons_id) REFERENCES coupon (id);

ALTER TABLE ordershipping ADD CONSTRAINT FK_ordershipping_orders FOREIGN KEY (orders) REFERENCES orders (id);

ALTER TABLE ordershippingitem ADD CONSTRAINT FK_ordershtem_orderSh_id6260 FOREIGN KEY (orderShipping_id) REFERENCES ordershipping (id);

ALTER TABLE ordershippingitem ADD CONSTRAINT FK_ordershtem_sku_id92BA FOREIGN KEY (sku_id) REFERENCES sku (id);

ALTER TABLE PARAMETER ADD CONSTRAINT FK_parameter_productC_idCF42 FOREIGN KEY (productCategory_id) REFERENCES productcategory (id);

ALTER TABLE paymenttransaction ADD CONSTRAINT FK_paymention_ordersB61A FOREIGN KEY (orders) REFERENCES orders (id);

ALTER TABLE paymenttransaction ADD CONSTRAINT FK_paymention_parent_id9F71 FOREIGN KEY (parent_id) REFERENCES paymenttransaction (id);

ALTER TABLE paymenttransaction ADD CONSTRAINT FK_paymention_store_id0E4C FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE paymenttransaction ADD CONSTRAINT FK_paymention_svc_id2E01 FOREIGN KEY (svc_id) REFERENCES svc (id);

ALTER TABLE paymenttransaction ADD CONSTRAINT FK_paymention_user_id8350 FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE platformsvc ADD CONSTRAINT FK_platformsvc_id FOREIGN KEY (id) REFERENCES svc (id);

ALTER TABLE pointlog ADD CONSTRAINT FK_pointlog_member_id FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE product ADD CONSTRAINT FK_product_brand_id FOREIGN KEY (brand_id) REFERENCES brand (id);

ALTER TABLE product ADD CONSTRAINT FK_productCategory_id FOREIGN KEY (productCategory_id) REFERENCES productcategory (id);

ALTER TABLE product ADD CONSTRAINT FK_product_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE product ADD CONSTRAINT FK_product_storeProdu_id5DF6 FOREIGN KEY (storeProductCategory_id) REFERENCES storeproductcategory (id);

ALTER TABLE product_producttag ADD CONSTRAINT FK_producttag_product_id6BC3 FOREIGN KEY (products_id) REFERENCES product (id);

ALTER TABLE product_producttag ADD CONSTRAINT FK_producttag_product_id012C FOREIGN KEY (productTags_id) REFERENCES producttag (id);

ALTER TABLE product_promotion ADD CONSTRAINT FK_production_product_id2B3E FOREIGN KEY (products_id) REFERENCES product (id);

ALTER TABLE product_promotion ADD CONSTRAINT FK_production_promoti_id5772 FOREIGN KEY (promotions_id) REFERENCES promotion (id);

ALTER TABLE product_storeproducttag ADD CONSTRAINT FK_producttag_product_id0101 FOREIGN KEY (products_id) REFERENCES product (id);

ALTER TABLE product_storeproducttag ADD CONSTRAINT FK_producttag_storePr_id1681 FOREIGN KEY (storeProductTags_id) REFERENCES storeproducttag (id);

ALTER TABLE productcategory ADD CONSTRAINT FK_productory_parent_id39CF FOREIGN KEY (parent_id) REFERENCES productcategory (id);

ALTER TABLE productcategory_brand ADD CONSTRAINT FK_productand_product_id5E1A FOREIGN KEY (productCategories_id) REFERENCES productcategory (id);

ALTER TABLE productcategory_brand ADD CONSTRAINT FK_productand_brands_id3B3D FOREIGN KEY (brands_id) REFERENCES brand (id);

ALTER TABLE productcategory_promotion ADD CONSTRAINT FK_production_product_id4DC7 FOREIGN KEY (productCategories_id) REFERENCES productcategory (id);

ALTER TABLE productcategory_promotion ADD CONSTRAINT FK_production_promoti_id5503 FOREIGN KEY (promotions_id) REFERENCES promotion (id);

ALTER TABLE productfavorite ADD CONSTRAINT FK_productite_member_id8273 FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE productfavorite ADD CONSTRAINT FK_productite_product_id7D25 FOREIGN KEY (product_id) REFERENCES product (id);

ALTER TABLE productnotify ADD CONSTRAINT FK_productify_member_id9214 FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE productnotify ADD CONSTRAINT FK_productnotify_sku_id FOREIGN KEY (sku_id) REFERENCES sku (id);

ALTER TABLE promotion ADD CONSTRAINT FK_promotion_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE promotion_coupon ADD CONSTRAINT FK_promotipon_promoti_idC3DC FOREIGN KEY (promotions_id) REFERENCES promotion (id);

ALTER TABLE promotion_coupon ADD CONSTRAINT FK_promotipon_coupons_id8C82 FOREIGN KEY (coupons_id) REFERENCES coupon (id);

ALTER TABLE promotion_memberrank ADD CONSTRAINT FK_promotiank_promoti_id2937 FOREIGN KEY (promotions_id) REFERENCES promotion (id);

ALTER TABLE promotion_memberrank ADD CONSTRAINT FK_promotiank_memberR_id7CC7 FOREIGN KEY (memberRanks_id) REFERENCES memberrank (id);

ALTER TABLE promotion_sku ADD CONSTRAINT FK_promotisku_giftPro_id9890 FOREIGN KEY (giftPromotions_id) REFERENCES promotion (id);

ALTER TABLE promotion_sku ADD CONSTRAINT FK_promotisku_gifts_id1A00 FOREIGN KEY (gifts_id) REFERENCES sku (id);

ALTER TABLE promotionpluginsvc ADD CONSTRAINT FK_promotionpluginsvc_id FOREIGN KEY (id) REFERENCES svc (id);

ALTER TABLE receiver ADD CONSTRAINT FK_receiver_area_id FOREIGN KEY (area_id) REFERENCES area (id);

ALTER TABLE receiver ADD CONSTRAINT FK_receiver_member_id FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE review ADD CONSTRAINT FK_review_forReview_id FOREIGN KEY (forReview_id) REFERENCES review (id);

ALTER TABLE review ADD CONSTRAINT FK_review_member_id FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE review ADD CONSTRAINT FK_review_product_id FOREIGN KEY (product_id) REFERENCES product (id);

ALTER TABLE review ADD CONSTRAINT FK_review_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE shippingmethod ADD CONSTRAINT FK_shippinhod_default_id0C2A FOREIGN KEY (defaultDeliveryCorp_id) REFERENCES deliverycorp (id);

ALTER TABLE shippingmethod_paymentmethod ADD CONSTRAINT FK_shippinhod_shippin_idFFB3 FOREIGN KEY (shippingMethods_id) REFERENCES shippingmethod (id);

ALTER TABLE shippingmethod_paymentmethod ADD CONSTRAINT FK_shippinhod_payment_id23AB FOREIGN KEY (paymentMethods_id) REFERENCES paymentmethod (id);

ALTER TABLE sku ADD CONSTRAINT FK_sku_product_id FOREIGN KEY (product_id) REFERENCES product (id);

ALTER TABLE specification ADD CONSTRAINT FK_specifiion_product_id8C1C FOREIGN KEY (productCategory_id) REFERENCES productcategory (id);

ALTER TABLE statistic ADD CONSTRAINT FK_statistic_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE stocklog ADD CONSTRAINT FK_stocklog_sku_id FOREIGN KEY (sku_id) REFERENCES sku (id);

ALTER TABLE store ADD CONSTRAINT FK_store_business_id FOREIGN KEY (business_id) REFERENCES business (id);

ALTER TABLE store ADD CONSTRAINT FK_storeCategory_id FOREIGN KEY (storeCategory_id) REFERENCES storecategory (id);

ALTER TABLE store ADD CONSTRAINT FK_storeRank_id FOREIGN KEY (storeRank_id) REFERENCES storerank (id);

ALTER TABLE store_productcategory ADD CONSTRAINT FK_store_pory_stores_idB2A9 FOREIGN KEY (stores_id) REFERENCES store (id);

ALTER TABLE store_productcategory ADD CONSTRAINT FK_store_pory_product_id829B FOREIGN KEY (productCategories_id) REFERENCES productcategory (id);

ALTER TABLE storeadimage ADD CONSTRAINT FK_storeadimage_store_id FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE storefavorite ADD CONSTRAINT FK_storefaite_member_idFF10 FOREIGN KEY (member_id) REFERENCES MEMBER (id);

ALTER TABLE storefavorite ADD CONSTRAINT FK_storefaite_store_id5C73 FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE storeproductcategory ADD CONSTRAINT FK_storeprory_parent_id7F8B FOREIGN KEY (parent_id) REFERENCES storeproductcategory (id);

ALTER TABLE storeproductcategory ADD CONSTRAINT FK_storeprory_store_id56AD FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE storeproducttag ADD CONSTRAINT FK_storeprtag_store_idDA31 FOREIGN KEY (store_id) REFERENCES store (id);

ALTER TABLE svc ADD CONSTRAINT FK_svc_store_id FOREIGN KEY (store_id) REFERENCES store (id);
