var entity_info_url = url_root + "/services/findEntityByCode";
var entity_info_list = url_root + "/services/queryEntityList";
//var url_fields = url_root + "/services/queryFieldsByCodeOrID?$_ENTITY_ID={0}";
var url_entity = url_root + "/services/queryEntityByCodeOrID?$_ENTITY_CODE={0}";
//var url_entity_current = url_root + "/services/queryEntityByCodeOrID?$_ENTITY_ID={0}";
var entitySetup_url = "entity_setup1.html?entity_id={0}&isReadonly=0";
var table_url = url_root + "/services/findTableByName";
var gl_app = null;
var gl_app1 = null;
var gl_field_type = null;
var gl_field_isNull_dict = null;
var gl_field_iskey_dict = null;
var label_gl = null;
var GL_ENTITY_ID = null;
var for_new_entity_id = null;
var gl_sys_flag = null;
var gl_select_data = null;
var gl_privilege_group_id = null;
var gl_privilege_role_id = null;

//long类型转换设置
axios_long_parse();
//cookie认证传递
axios.defaults.withCredentials = true;
axios.get(url_entity.format("md_entities"))
	.then(res => {
		var data = null;
		var d = res.data.data;
		if (d) {
			data = d[0];
			var entity_id = data['md_entity_id'];
			for_new_entity_id = entity_id;
		}
	});


axios.get(url_entity.format("data_privileges_rel"))
	.then(res => {
		var data = null;
		var d = res.data.data;
		if (d) {
			data = d[0];
			var entity_id = data['md_entity_id'];
			gl_privilege_group_id = entity_id;
		}
	});
axios.get(url_entity.format("role_privileges"))
	.then(res => {
		var data = null;
		var d = res.data.data;
		if (d) {
			data = d[0];
			var entity_id = data['md_entity_id'];
			gl_privilege_role_id = entity_id;
		}
	});

function queryEntityByCode(code, app) {
	where_params = null;
	if (code == "data_privileges" || code == 'entity_privileges')
		where_params = {
			"md_entity_id": GL_ENTITY_ID
		}
	var params = {
		"$_ENTITY_CODE": code,
		"where": where_params
	}
	axios.post(entity_info_url, params)
		.then(res => {
			var data = null;
			var d = res.data.data;
			if (d) {
				var options = [];
				var len = d.length;
				for (var i = 0; i < len; i++) {
					item = d[i];
					var dict = null;
					if (code == 'roles') {
						dict = {
							key: item['role_id'].toString(),
							label: item['role_name'],
							value: item['role_id'].toString()
						}
					} else if (code == 'user_groups') {
						dict = {
							key: item['group_id'].toString(),
							label: item['user_group_name'],
							value: item['group_id'].toString()
						}
					} else if (code == 'entity_privileges') {
						var v = item['privilege_type'];
						var label_cn = "";
						if (v == 'READ')
							label_cn = "（读取）"
						else if (v == 'CREATE')
							label_cn = "（新增）"
						else if (v == 'UPDATE')
							label_cn = "（修改）"
						else if (v == 'DELETE')
							label_cn = "（删除）"
						dict = {
							key: item['privilege_code'],
							label: item['privilege_type'] + label_cn,
							value: item['entity_privilege_id'].toString()
						}
					} else if (code == 'data_privileges') {
						dict = {
							key: item['data_privilege_code'],
							label: item['data_privilege_desc'],
							value: item['data_privilege_id'].toString()
						}
					}
					if (dict)
						options.push(dict);
				}

				if (code == 'roles') {
					app.role_options = options;
				} else if (code == 'user_groups') {
					app.group_options = options;
				} else if (code == 'entity_privileges') {
					app.authorize_options = options;
				} else if (code == 'data_privileges') {
					app.data_privilege_options = options;
				}
			}
		});
}

function queryEntity(app) {
	var data = null;
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
					if (key == 'md_entity_id') {
						d['value'] = data[i][key];
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
			app.options = options;
		})
}


function insertData(data) {
	if (!data)
		return null;
	return axios.post(url_root + '/services/insertEntity', data);
};

function renderToolbar() {
	//主要内容
	var app = new Vue({
		el: "#app1",
		data() {
			return {
				options: [],
				data_privilege_options: [],
				authorize_options: [],
				role_options: [],
				group_options: [],
				select1: '',
				entity_name: "",
				entity_name1: "",
				select_value: "",
				addFormVisible: false,
				authorFormVisible: false,
				iframe_url: null,
				table_options: [],
				form_data: {
					md_entity_code: null,
					md_entity_name: null,
					md_entity_name_en: null,
					md_tables_id: null,
					md_entity_desc: null,
					public_flag: "N"
				},
				author_data: {
					md_entity_id: null,
					md_entity_name: null,
					md_entity_name_en: null,
					md_entity_desc: null,
					role_id: null,
					data_group_id: null,
					data_privilege_id: null,
					authorization_id: null
				}
			}
		},
		methods: {
			handleClick(data) {
				const {
					value,
					label
				} = data;
				gl_select_data = data;
				GL_ENTITY_ID = value.toString();
				app.select_value = GL_ENTITY_ID;
				if (gl_app) {
					gl_app.dialog_title = label;
					label_gl = label;
				} else {
					label_gl = label;
				}
				app.author_data.md_entity_id = value;
				app.author_data.md_entity_name = label;
				//        app.author_data.md_entity_name_en= null;
				//        app.author_data.md_entity_desc=null;
				app.author_data.role_id = null;
				app.author_data.data_group_id = null;
				app.author_data.data_privilege_id = null;
				app.author_data.authorization_id = null;

				var url = entitySetup_url.format(GL_ENTITY_ID);
				app.iframe_url = url;
			},
			handleAuthChange(data) {
				console.log(data)
			},
			table_load() {
				axios.get(table_url)
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
							var item = data[i];
							options.push({
								"value": item["md_tables_id"],
								"label": item["md_tables_name"] + "(" + item["md_tables_desc"] + ")"
							});
						}
						app.table_options = options;
					})

			},
			entity_author() {
				let entity_id = GL_ENTITY_ID;
				if (!entity_id || entity_id.trim() == '') {
					app.$message.warning("请先选择需要授权的实体对象！");
					return;
				}

				//app.table_load();
				var res = null;
				queryEntityByCode("roles", app);
				queryEntityByCode("user_groups", app);
				queryEntityByCode("data_privileges", app);
				queryEntityByCode("entity_privileges", app);
				app.authorFormVisible = true;
			},
			entity_del() {

				if (!GL_ENTITY_ID || GL_ENTITY_ID.trim() == '') {
					app.$message.warning("请先选择需要删除的实体对象！");
					return;
				}
				if (GL_ENTITY_ID)
					this.$confirm('你确定要删除当前选择的实体吗?', '警告', {
						confirmButtonText: '确定',
						cancelButtonText: '取消',
						type: 'warning'
					})
					.then(() => {
						//点击确定的操作(调用接口)
						if (gl_select_data) {
							const {
								value,
								label
							} = gl_select_data;
							where_dict = {
								md_entity_id: value
							};
							var data_upd_entity = {
								"$_ENTITY_ID": for_new_entity_id,
								"where": [where_dict]
							};
							axios.all([app.deleteData(data_upd_entity)])
								.then(axios.spread(function(acct, perms) {
									// 两个请求现在都执行完成
									//row.isSet = false;
									edit_gl = false;
									var res_data = null;
									if (perms)
										res_data = perms.data
                                    else if (acct)
                                        res_data = acct.data;
									if (res_data && res_data.status >= 300) {
										app.$message.warning({
											type: 'Failed',
											message: res_data.message
										});
										return;
									} else
										app.$message({
											type: 'success',
											message: "Save success."
										});
									//console.log(acct,perms);
									window.location.reload();
								}));
						}
						url = entitySetup_url.format("");
						app.iframe_url = url;
						queryEntity(app);
						app.select1 = "";
					})
					.catch(() => {
						//点击取消的提示
						return;
					});
				return;

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
			entity_add() {
				app.table_load();
				app.addFormVisible = true;
			},
			submit_auth() {
				if (app.author_data.md_entity_id == null || app.author_data.md_entity_id.length <= 0) {
					app.$message.warning("entity should be null,please input first.");
					return;
				}
				if (app.author_data.md_entity_name == null || app.author_data.md_entity_name.trim()
					.length <= 0) {
					app.$message.warning("entity name should be null,please input first.");
					return;
				}
				if (app.author_data.data_group_id == null || app.author_data.data_group_id.length <= 0) {
					app.$message.warning("user group should be null,please select first.");
					return;
				}
				if (app.author_data.data_privilege_id == null || app.author_data.data_privilege_id.length <= 0) {
					app.$message.warning("data scope should be null,please select first.");
					return;
				}
				if (app.author_data.role_id == null || app.author_data.role_id.length <= 0) {
					app.$message.warning("user role should be null,please select first.");
					return;
				}
				if (app.author_data.authorization_id == null || app.author_data.authorization_id.length <= 0) {
					app.$message.warning("Operation Authorization should be null,please select first.");
					return;
				}
				let sel_data = app.author_data;
				//app.author_data['md_entity_id']=for_new_entity_id;
				var data_role_privilege = [];
				if (app.author_data.role_id && app.author_data.authorization_id)
					var len1 = app.author_data.role_id.length;
				var len2 = app.author_data.authorization_id.length;
				for (var i = 0; i < len1; i++) {
					var item1 = app.author_data.role_id[i];
					for (var j = 0; j < len2; j++) {
						var item2 = app.author_data.authorization_id[j];
						new_dict = {
							'role_id': item1,
							'entity_privilege_id': item2
						}
						//                      new_dict['role_id']=item1['value'];
						//                      new_dict['entity_privilege_id']=item2['value'];
						data_role_privilege.push(new_dict);
					}
				}
				var data_group_privilege = [];
				if (app.author_data.data_group_id && app.author_data.data_privilege_id)
					var len1 = app.author_data.data_group_id.length;
				var len2 = app.author_data.data_privilege_id.length;
				for (var i = 0; i < len1; i++) {
					var item1 = app.author_data.data_group_id[i];
					for (var j = 0; j < len2; j++) {
						var item2 = app.author_data.data_privilege_id[j];
						new_dict = {
							'group_id': item1,
							'data_privilege_id': item2
						}
						//                      new_dict[]=item1['value'];
						//                      new_dict['data_privilege_id']=item2['value'];
						data_group_privilege.push(new_dict);
					}
				}

				var data_add_role = {
					"$_ENTITY_ID": gl_privilege_role_id,
					"data": data_role_privilege
				};
				var data_add_group = {
					"$_ENTITY_ID": gl_privilege_group_id,
					"data": data_group_privilege
				};
				axios.all([insertData(data_add_role), insertData(data_add_group)])
					.then(axios.spread(function(acct, perms) {
						// 两个请求现在都执行完成
						app.$message({
							type: 'success',
							message: "Save success."
						});
					}));
				app.authorFormVisible = false;

			},
			submit_entity() {
				var data_add = {
					"$_ENTITY_ID": for_new_entity_id,
					"data": app.form_data
				};
				//let sel_data = app.form_data;
				if (app.form_data.md_entity_code == null || app.form_data.md_entity_code.trim()
					.length <= 0) {
					app.$message.warning("entity code should be null,please input first.");
					return;
				}
				if (app.form_data.md_entity_name == null || app.form_data.md_entity_name.trim()
					.length <= 0) {
					app.$message.warning("entity name should be null,please input first.");
					return;
				}
				if (app.form_data.md_tables_id == null || app.form_data.md_tables_id.length <= 0) {
					app.$message.warning("tables_id should be null,please select first.");
					return;
				}
				axios.all([insertData(data_add)])
					.then(axios.spread(function(acct, perms) {
						// 两个请求现在都执行完成
						app.$message({
							type: 'success',
							message: "Save success."
						});
						queryEntity(app);
						app.form_data = {
							md_entity_code: null,
							md_entity_name: null,
							md_entity_name_en: null,
							md_tables_id: null,
							md_entity_desc: null
						}
						//console.log(acct,perms);
						url = entitySetup_url.format(acct.data.data.ids[0].toString());
						app.iframe_url = url;
						//window.open(url,'_blank') ;// 新窗口打开外链接
					}));
				app.addFormVisible = false;
			},
			setup(data) {
				url = entitySetup_url.format(data);
				app.iframe_url = url;
				window.open(url, '_blank'); // 新窗口打开外链接
			},
			async queryFields(url) {
				let res = await axios.get(url)
					.then(res => {
						var dict1 = {};
						var dict2 = {};
						var dict3 = {};
						var data = res.data.data;
						if (data) {
							var len = 0;
							if (data)
								len = data.length;
							for (var i = 0; i < len; i++) {
								var d = data[i];
								dict1[d["md_fields_name"]] = d["md_fields_type"];
								dict2[d["md_fields_name"]] = d["is_null"];
								dict3[d["md_fields_name"]] = d["is_key"];
							}
						}
						gl_field_type = JSONbig.parse(JSONbig.stringify(dict1));
						gl_field_isNull_dict = JSONbig.parse(JSONbig.stringify(dict2));
						gl_field_iskey_dict = JSONbig.parse(JSONbig.stringify(dict3));
						if (gl_app)
							load_column_info(gl_app);
					});
			}

		}
	});
	gl_app1 = app;
	queryEntity(app);
}

renderToolbar();
