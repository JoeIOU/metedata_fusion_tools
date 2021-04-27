var url_entity_by_id = url_root + "/services/findEntitySetup?$_ENTITY_ID={0}";
var login_url = url_root + "/services/user";
var url_entity = url_root + "/services/queryEntityByCodeOrID?$_ENTITY_CODE=md_entities";
var url_field = url_root + "/services/queryFieldsByCodeOrID?$_ENTITY_CODE=md_fields";
var entity_info_list = url_root + "/services/queryEntityList";
var app_gl = null;
var label_gl = null;
var edit_gl = false;
var gl_entity_list = null;
var GL_ENTITY_ID = null;
var GL_FIELD_ID = null;
var GL_TENANT_ID = null;
//让ajax携带cookie
axios.get(login_url)
	.then(res => {
		if (res && res.data.data)
			GL_TENANT_ID = res.data.data.tenant_id;
		var rs = JSONbig.stringify(res);
		//console.log(rs);
	});
axios.get(url_entity)
	.then(res => {
		var rs = JSONbig.stringify(res);
		var data = res.data.data[0];
		var entity_id = data['md_entity_id'];
		GL_ENTITY_ID = entity_id;
		//console.log(rs);
	});
axios.get(url_field)
	.then(res => {
		var rs = JSONbig.stringify(res);
		var data = res.data.data[0];
		var entity_id = data['md_entity_id'];
		GL_FIELD_ID = entity_id;
		//console.log(rs);
	});

function get_entity_list() {
	axios.get(entity_info_list)
		.then(res => {
			data = res.data.data;
			var len = 0;
			if (data)
				len = data.length;
			var options = [];
			for (var i = 0; i < len; i++) {
				var d = {};
				var b1 = false;
				var b2 = false;
				for (var key in data[i]) {
					if (key == 'md_entity_code') {
						d['value'] = data[i][key].toString();
						b1 = true;
					}
					if (key == 'md_entity_name') {
						d['label'] = data[i][key];
						b2 = true;
					}
					if (b1 && b2) break;
				}
				options[i] = d;
			}
			gl_entity_list = options;
			if (app_gl)
				app_gl.entity_options = options;
		});
}

function queryMetadata(url, id) {
	if (app_gl)
		app_gl.loading = true
	axios.get(url)
		.then(res => {
			var data = res.data.data;
			var cols = [];
			var dict = {
				columns: [],
				datas: [],
				size: 0
			};
			if (data) {
				var len = 0;
				if (data)
					len = data.length;
				var i = 0;
				var row = data[0];
				for (var key in row) {
					var type1 = null;
					var vis = true;
					var read_only = true;
					var width1 = null;
					var title_str = key;
					switch (key) {
						case 'md_entity_id':
							title_str = '实体ID';
							break;
						case 'md_entity_code':
							title_str = '实体编码';
							break;
						case 'md_entity_name':
							title_str = '实体名称';
							break;
						case 'md_entity_name_en':
							title_str = '实体英文名称';
							break;
						case 'md_entity_desc':
							title_str = '实体描述';
							break;
						case 'md_fields_id':
							title_str = '属性ID';
							break;
						case 'md_fields_name':
							title_str = '属性名称';
							break;
						case 'md_fields_name_cn':
							title_str = '属性中文名称';
							break;
						case 'md_fields_name_en':
							title_str = '属性英文名称';
							break;
						case 'md_fields_type':
							title_str = '属性类型';
							break;
						case 'md_fields_desc':
							title_str = '属性描述';
							break;
						case 'md_fields_length':
							title_str = '属性长度';
							break;
						case 'md_decimals_length':
							title_str = '属性小数位';
							break;
						case 'lookup_flag':
							title_str = '是否多值字段';
							break;
						case 'lookup_entity':
							title_str = '对应Lookup实体';
							break;
						case 'lookup_type':
							title_str = '对应Lookup分类';
							break;
						case 'default_value':
							title_str = '属性默认值';
							break;
						case 'is_null':
							title_str = '可否为空';
							break;
						case 'is_indexed':
							title_str = '是否索引字段';
							break;
						case 'is_unique':
							title_str = '是否唯一键';
							break;
						case 'public_flag':
							title_str = '跨租户共享标识';
							break;
						case 'active_flag':
							title_str = '是否有效';
							break;
						case 'md_tables_name':
							title_str = '数据表名称';
							break;
						case 'md_tables_desc':
							title_str = '数据表描述';
							break;
						case 'md_columns_name':
							title_str = '字段名称';
							break;
						case 'md_columns_desc':
							title_str = '字段描述';
							break;
						case 'md_columns_type':
							title_str = '字段类型';
							break;
						case 'md_columns_length':
							title_str = '字段长度';
							break;
						case 'md_dec_length':
							title_str = '小数位数';
							break;
						default:
							title_str = key;
					}

					if (key === 'md_entity_id' || key === 'md_entity_code' || key === 'md_entity_name' || key === 'md_tables_id' ||key == "is_unique" || key == "public_flag" ||
						key === 'md_columns_id' || key === 'md_entity_name_en' || key === 'md_entity_desc' || key == 'blank_flag' || key=='entity_public_flag'
						|| key=='md_tables_name'|| key=='md_tables_desc'|| key=='md_columns_name'|| key=='md_columns_desc'|| key=='md_columns_type'|| key=='md_columns_length'|| key=='md_dec_length')
						vis = false
					if (key === 'md_fields_id' || key === 'md_fields_length' || key === 'md_decimals_length' || key === 'md_columns_length' || key === 'md_dec_length')
						type1 = 'int'
					else if (key === '' || key === '')
						type1 = 'varchar'
					else
						type1 = 'varchar'
					if (key === 'md_fields_type' || key === 'md_fields_name_cn' || key === 'md_fields_name_en' || key === 'md_fields_length' || key === 'md_decimals_length' ||
						key === 'md_entity_name_en' || key === 'md_entity_desc' || key === 'md_fields_desc' || key === 'lookup_flag' || key === 'default_value' ||
						key == "is_null" || key == "is_indexed" ||  key === 'lookup_entity' || key === 'lookup_type') {
						read_only = false;
					}
					if (key === 'md_fields_name' || key === 'md_fields_name_cn' || key === 'md_fields_name_en' || key === 'md_fields_type' || key === 'md_entity_name_en' || key === 'md_entity_desc' || key === 'md_fields_desc' ||
						key === 'md_tables_name' || key === 'md_tables_desc' || key === 'md_columns_name' || key === 'md_columns_desc' || key === 'lookup_entity')
						width1 = 130
					else
						width1 = 100;
					var dict0 = {
						field: key,
						title: title_str,
						type: type1,
						width: width1,
						visible: vis,
						readonly: read_only
					}
					cols[i] = dict0;
					i++;
				}
				for (var i = 0; i < len; i++) {
					var d = data[i];
					//赋值id为第一个序号的值，以便后续编辑，一般是key id的值，标识行的唯一性。
					d["$$_id_"] = i + 1;
				}
				dict = {
					columns: cols,
					datas: data,
					size: len
				};
			}
			renderTable(dict, id);
		})
}

function queryData() {
	if (!gl_entity_list)
		get_entity_list();
	let id = getUrlKey('entity_id');
	if (!id)
		id = -1
	renderTable([], id);
	var s = url_entity_by_id.format(id);
	queryMetadata(s, id);
}

function renderTable(result, id) {
	if (!result) return;
	let readonly = getUrlKey('isReadonly');
	var cols = result.columns;
	var data1 = result.datas;
	var field_types = result.field_types;
	var gl_entity_id = id;
	var app = null;
	//主要内容
	if (app_gl) {
		app_gl.loading = true;
		app = app_gl;
		if (gl_entity_list)
			app.entity_options = gl_entity_list;
		app.currentPage = 1;
		if (readonly && readonly == '1')
			app.isReadonly = true
		else
			app.isReadonly = false
	} else {
		app = new Vue({
			el: "#app",
			data: {
				master_user: {
					sel: null, //选中行
					columns: [],
					data: []
				},
				currentPage: 1, //默认显示页面为1
				pagesize: 10, //    每页的数据条数
				options: [{
					value: 'int',
					label: '整数型(32位)'
				}, {
					value: 'bigint',
					label: '长整型(64位)'
				}, {
					value: 'decimal',
					label: '数值型(带小数)'
				}, {
					value: 'varchar',
					label: '文本型'
				}, {
					value: 'char',
					label: '字符型'
				}, {
					value: 'timestamp',
					label: '日期型'
				}, {
					value: 'clob',
					label: '大对象型'
				}],
				entity_options: null,
				test11: true,
				$_ENTITY_ID: gl_entity_id,
				loading: true,
				isReadonly: true
			},
			methods: {
				//每页下拉显示数据
				handleSizeChange: function(size) {
					this.pagesize = size;
					/*console.log(this.pagesize) */
				},
				//点击第几页
				handleCurrentChange: function(currentPage) {
					this.currentPage = currentPage;
					/*console.log(this.currentPage) */
				},
				//添加账号
				addUser() {},
				//读取表格数据
				readMasterUser() {
					//根据实际情况，自己改下啊
					app.master_user.data.map(i => {
						//模拟后台插入成功后有了id
						i.isSet = false;
						//给后台返回数据添加`isSet`标识
						return i;
					});
				},
				onchange(field_name, row, index) {
					row.isEdit = true;
					edit_gl = true;
					row.isSet = true;
					var id = field_name + index;
					var dom = document.getElementById(id);
					//dom.style.backgroundColor="#FFEE00";
					if (dom)
						dom.style.border = '1px solid #33FF00';
				},
				setStyle(row, index, del_flag) {
					for (item in row) {
						var id = item + index;
						var dom = document.getElementById(id);
						if (!dom)
							continue
						if (dom && del_flag) {
							if (row.isDel)
								dom.style.textDecoration = 'none'
							else
								dom.style.textDecoration = 'line-through'
						} else if (dom && !dom.hasAttribute("disabled")) {
							dom.value = '';
							dom.style.border = null;
							row[item] = '';
							row.isEdit = false;
						}
					}
					if (del_flag)
						if (row.isDel == null)
							row.isDel = true
					else
						row.isDel = !row.isDel;
				},
				//修改
				pwdChange(row, index, cg) {
					//是否是取消操作
					if (!cg) {
						if (row.md_fields_id) {
							//delete
							app.setStyle(row, index, true);
							return;
						} else {
							//cancel
							if (row.isSet == "undefined")
								row.isSet = false
							app.setStyle(row, index);
							return row.isSet = !row.isSet;
						}
					} else {
						row.isSet = true;
						this.$set(app.master_user.data, index, row);
					}
				},
				close() {
					if (edit_gl) {
						this.$confirm('你有编辑内容未保存，关闭将会丢失, 是否确认关闭?', '警告', {
								confirmButtonText: '确定',
								cancelButtonText: '取消',
								type: 'warning'
							})
							.then(() => {
								//点击确定的操作(调用接口)
								window.close();
							})
							.catch(() => {
								//点击取消的提示
								return;
							});
						return;
					} else
						window.close();
				},
				insertData(data) {
					if (!data)
						return null;
					return axios.post(url_root + '/services/insertEntity', data);
				},
				updateData(data) {
					if (!data)
						return null;
					return axios.post(url_root + '/services/updateEntity', data);
				},
				deleteData(data) {
					if (!data)
						return null;
					return axios.post(url_root + '/services/deleteEntity', data);
				},
				set_unfill_fields(index, item) {
					var is_not_ok = false;
					if (item.md_fields_name == null || item.md_fields_name == '') {
						var id = "md_fields_name" + index;
						var dom = document.getElementById(id);
						if (dom)
							dom.style.border = '1px solid #FF8800';
						is_not_ok = true;
					}
					if (item.md_fields_name_en == null || item.md_fields_name_en == '') {
						var id = "md_fields_name_en" + index;
						var dom = document.getElementById(id);
						if (dom)
							dom.style.border = '1px solid #FF8800';
						is_not_ok = true;
					}
					if (item.md_fields_type == null || item.md_fields_type == '') {
						var id = "md_fields_type" + index;
						var dom = document.getElementById(id);
						if (dom)
							dom.style.border = '1px solid #FF8800';
						is_not_ok = true;
					}
					if (item.is_null == null || item.is_null == '') {
						var id = "is_null" + index;
						var dom = document.getElementById(id);
						if (dom)
							dom.style.border = '1px solid #FF8800';
						is_not_ok = true;
					}
					if (item.lookup_flag == null || item.lookup_flag == '') {
						var id = "lookup_flag" + index;
						var dom = document.getElementById(id);
						if (dom)
							dom.style.border = '1px solid #FF8800';
						is_not_ok = true;
					}
//					if (item.public_flag == null || item.public_flag == '') {
//						var id = "public_flag" + index;
//						var dom = document.getElementById(id);
//						if (dom)
//							dom.style.border = '1px solid #FF8800';
//						is_not_ok = true;
//					}
					if ((item.md_fields_length == null || item.md_fields_length == '' || item.md_fields_length < 1) &&
						!(item.md_fields_type == 'timestamp' || item.md_fields_type == 'datetime' || item.md_fields_type == 'date')) {
						var id = "md_fields_length" + index;
						var dom = document.getElementById(id);
						if (dom)
							dom.style.border = '1px solid #FF8800';
						is_not_ok = true;
					}
					return is_not_ok;
				},
				submitData() {
					let data = app.master_user.data;
					let data_add_field = null;
					let data_upd_field = null;
					let data_del_field = null;
					let data_upd_entity = null;
					if (data) {
						var update_data_list = [];
						var update_where_list = [];
						var del_where_list = [];
						var insert_data_list = [];
						var warning_data_list = [];
						let len = data.length;
						var is_not_ok = null;
						var public_flag=null;
						for (var i = 0; i < len; i++) {
							var item = data[i];
                            if(item.public_flag==null ||item.public_flag=='')
                                public_flag='N';
                              else
                                public_flag=item.public_flag;

							var new_item = {
								"md_fields_name": item.md_fields_name,
								"md_fields_name_en": item.md_fields_name_en,
								"md_fields_name_cn": item.md_fields_name_cn,
								"md_fields_type": item.md_fields_type,
								"md_fields_desc": item.md_fields_desc,
								"md_fields_length": item.md_fields_length,
								"md_decimals_length": item.md_decimals_length,
								"lookup_flag": item.lookup_flag,
								"lookup_entity": item.lookup_entity,
								"lookup_type": item.lookup_type,
								"default_value": item.default_value,
								"is_null": item.is_null,
								"is_indexed": item.is_indexed,
								"is_unique": item.is_unique,
								"public_flag": public_flag,
								'active_flag': 'Y'
							};
							if (item && item.isEdit && item.md_fields_id) { //修改
								//delete new_item.md_fields_id;
								update_data_list.push(new_item);
								update_where_list.push({
									"md_fields_id": item.md_fields_id
								});
								is_not_ok = app.set_unfill_fields(item.$$_id_, new_item);
							} else if (item && item.isEdit) { //新增
								if (!GL_TENANT_ID)
									continue;
								new_item.tenant_id = GL_TENANT_ID;
								new_item.md_entity_id = item.md_entity_id;
								new_item.md_columns_id = item.md_columns_id;
								insert_data_list.push(new_item);
								is_not_ok = app.set_unfill_fields(item.$$_id_, new_item);
							} else if (item && item.isDel && item.md_fields_id) { //删除
								//new_item.active_flag = 'N';
								//data_del_field.push(new_item);
								del_where_list.push({
									"md_fields_id": item.md_fields_id
								});
								//is_not_ok = app.set_unfill_fields(item.$$_id_, new_item);
							}
						}
						if (is_not_ok) {
							app.$message({
								type: 'warning',
								message: "部分必填字段未填写，请填写（标注红色框的字段）"
							});
							return;
						}
						data_upd_field = {
							"$_ENTITY_ID": GL_FIELD_ID,
							"data": update_data_list,
							"where": update_where_list
						};
						data_del_field = {
							"$_ENTITY_ID": GL_FIELD_ID,
							"where": del_where_list
						};
						data_add_field = {
							"$_ENTITY_ID": GL_FIELD_ID,
							"data": insert_data_list
						};
						let sel_data = app.master_user.sel;
						if (sel_data && sel_data.isEdit) {
							var new_entity = {
								"md_entity_code": sel_data.md_entity_code,
								"md_entity_name": sel_data.md_entity_name,
								"md_entity_desc": sel_data.md_entity_desc,
								"entity_public_flag": sel_data.entity_public_flag,
								"md_entity_name_en": sel_data.md_entity_name_en
							}
							var where_dict = {
								"md_entity_id": sel_data.md_entity_id
							};
							data_upd_entity = {
								"$_ENTITY_ID": GL_ENTITY_ID,
								"data": [new_entity],
								"where": [where_dict]
							};
						} else
							data_upd_entity = null;
						axios.all([app.insertData(data_add_field), app.updateData(data_upd_field), app.deleteData(data_del_field), app.updateData(data_upd_entity)])
							.then(axios.spread(function(acct, perms) {
								// 两个请求现在都执行完成
								edit_gl = false;
								var res_data = null;
								if (perms)
									res_data = perms.data
                                else if (acct)
                                    res_data = acct.data;
								if (res_data && res_data.status >= 300) {
									app.$message.warning({
										type: 'warning',
										message: res_data.message
									});
									return;
								} else
									app.$message({
										type: 'success',
										message: "保存成功！"
									});
								//row.isSet = false;
								window.location.reload();
							}));
					}
				}

			}
		});

		app_gl = app;
		if (gl_entity_list)
			app.entity_options = gl_entity_list;

		if (readonly && readonly == '1')
			app.isReadonly = true
		else
			app.isReadonly = false
	}
	app.master_user.columns = cols;
	let d = null;
	// 数据属性数据
	if (data1) {
		app.master_user.data = data1;
		let len = data1.length;
		if (data1) {
			d = data1[0];
			for (var i = 0; i < len; i++) {
				var item = data1[i];
				if (item['md_entity_id'] != null) {
					d = item;
					break;
				}
			}
		}
	}
	// 查询业务数据
	if (data1 && d)
		app.master_user.sel = JSONbig.parse(JSONbig.stringify(d));

	if (app_gl)
		app_gl.loading = false;
	//	app.$message('loading data ok');
}
queryData();
