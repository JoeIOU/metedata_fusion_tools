var entity_info_url = url_root + "/services/findUIEntity?$_ENTITY_ID={0}&ui_template_code={1}";
var ui_template_info_url = url_root + "/services/queryUIElements?ui_template_code={0}&entity_id={1}";
var entity_url_by_code = url_root + "/services/findEntityByCode?$_ENTITY_CODE={0}";
var entity_info_url_by_parent = url_root + "/services/findEntity?$_ENTITY_ID={0}&$PARENT_ENTITY_ID={1}&$parent_data_id={2}";
var entity_rel_url = url_root + "/services/findEntityRelation";
var rule_compute_url = url_root + "/services/computeRules";
var rule_entity_url = url_root + "/services/findEntityRules";
var lookup_info_url_by_code = url_root + "/services/findLookupItemByCode?lookup_code={0}";
var entity_info_url_by_code = url_root + "/services/findLookupByEntityCode?entity_code={0}&lookup_code={1}";
var entity_info_url_by_code_and_parentId = url_root + "/services/findLookupByEntityCode?entity_code={0}&lookup_code={1}&$PARENT_ENTITY_CODE={2}&$parent_data_id={3}";
var entity_info_list = url_root + "/services/queryEntityList";
var url_fields = url_root + "/services/queryFieldsByCodeOrID?$_ENTITY_ID={0}";
var url_ui_single_entity = url_root + "/services/queryUISingleEntity?$_ENTITY_ID={0}";
var url_entity = url_root + "/services/queryEntityByCodeOrID?$_ENTITY_CODE={0}";
var url_entity_current = url_root + "/services/queryEntityByCodeOrID?$_ENTITY_ID={0}";
var entitySetup_url = "entity_setup1.html?entity_id={0}";
var table_url = url_root + "/services/findTableByName";
var gl_app = null;
var gl_app1 = null;
var gl_field_type = null;
var gl_field_lookup_entity_dict = null;
var gl_field_lookup_type_dict = null;
var gl_field_lookup_flag_dict = null;
var gl_field_name_cn_dict = null;
var gl_field_length_dict = null;
var gl_field_decimal_dict = null;
var gl_grid_columns = null;
var label_gl = null;
var GL_ENTITY_ID = null;
var for_new_entity_id = null;
var gl_sys_flag = null;
var gl_select_data = null;
var gl_dialog_title = null;
var gl_fields_list = null;
var gl_rules_list=null;
var gl_ui_single_entity=null;
var gl_linked_entity_list=null;
var gl_lookup_dict = {};
var gl_entity_relations=null;
var gl_delect_row=null;
var gl_data_view=null;
var lang=null;

//long类型转换设置
axios_long_parse();
//cookie认证传递
axios.defaults.withCredentials = true;

function getUIElements(){
	var entity_id = getUrlKey('entity_id');
	var template_code = getUrlKey('template_code');
	var header_title_show = getUrlKey('header');
    if(!template_code||!entity_id)
      return null;
	var parent_entity_id = getUrlKey('parent_entity_id');
	var parent_id = getUrlKey('parent_id');
	var is_child = getUrlKey('is_child');
	var _row_id_ = getUrlKey('_row_id_');
	if(is_child&&is_child=='1'&&parent_id)
	  _row_id_=parent_id
    var url=ui_template_info_url.format(template_code,entity_id)
	axios.get(url)
		.then(res => {
			var data = res.data.data;
			if(gl_app&&data)
			  gl_app.master_user.ui_fields=data;
			else
			  gl_app.master_user.ui_fields=[];
            entity_ids=[]
            if(entity_id)
             entity_ids.push(entity_id)
            primary_entity_id=null
            gl_data_view=data;
            if(gl_app)
              mapping_data_view_title(gl_app.master_user.columns,data)
	        //if(entity_ids)
	        // getEntityFields(entity_ids,data);
            var res_data = res.data;
            if (gl_app&&res_data && res_data.status >= 300) {
                gl_app.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})
}

function mapping_data_view_title(columns,view_data){
  if(columns&&view_data)
  for (i in columns){
    itm=columns[i]
    f=itm['field']
    for(j in view_data){
      item=view_data[j];
      //e_id=item['entity_id']
      //f_id=item['md_fields_id']
      f_name=item['md_fields_name']
      if(f&&f==f_name){
            ui_fields_name_cn=item['ui_fields_name_cn']
            ui_fields_name_en=item['ui_fields_name_en']
            if(ui_fields_name_en&&language()!='zh')
                itm["title"] = ui_fields_name_en;
            else if (ui_fields_name_cn && ui_fields_name_cn.trim() != ""&&language()=='zh')
                itm["title"] = ui_fields_name_cn;
      }
    }
  }

}

function getEntityByCode(code) {
	var url_fomat_entity = url_entity.format(code);
	axios.get(url_fomat_entity)
		.then(res => {
			var data = null;
			var d = res.data.data;
			if (d) {
				data = d[0];
				var entity_id = data['md_entity_id'];
				for_new_entity_id = entity_id;
			}
			if (gl_app1&&res.data && res.data.status >=300)
				gl_app1.$message.warning(messageI18n(res.data.message));
		});
}
getEntityByCode("md_entities");

function is_linked(field_name){
  result=false;
  if(!gl_ui_single_entity)
     return result;
  size=0;
  len=gl_ui_single_entity.length;
  for (var i=0;i<len;i++){
    item=gl_ui_single_entity[i];
    field_name1=item.md_fields_name;
    linked_field_id=item.linked_field_id;
    if(field_name1&&field_name1==field_name&&linked_field_id){
       result=true
       break;
     }
  }
  return result;
}

function getLookupEntityByParentId(col,code,parent_code,parent_data_id){
    url = entity_info_url_by_code_and_parentId.format(code,code, parent_code,parent_data_id);
	axios.get(url)
		.then(res => {
			var data = null;
			var d = res.data.data.data;
			lookup_type=null;
			var ddd = data_select_options_mapping(code, lookup_type, d);
            if(col&&ddd){
			  col.lookup_entity_list = ddd;
			  gl_app.itemkey1 = Math.random();
			 }
			var res_data=res.data;
            if (res_data && res_data.status >= 300) {
                gl_app.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		});
}

function get_entity_info_by_code(code, result, lookup_type) {
	if (!lookup_type)
		lookup_type = "";
	var sKey = code + ":" + lookup_type;
	if (gl_lookup_dict[sKey]) {
		result.lookup_entity_list = gl_lookup_dict[sKey];
		if (gl_app && result)
			set_Label_Value(result, gl_app.master_user.data);
		return result;
	}
	if(result){
	   f=result.field
	   re=is_linked(f)
	   if(re)
	    return;
	}
	var url = null;
	var url1 = null;
	if (!lookup_type)
		lookup_type = ""
	var is_entity=false
	if (code.toLowerCase() == "lookup_classify" && lookup_type && lookup_type.trim() != ""){
		url = lookup_info_url_by_code.format(lookup_type);
	    is_entity=false;
	}else{
		  url = entity_info_url_by_code.format(code, lookup_type);
		  is_entity=true;
		  //return;
		}

	axios.get(url)
		.then(res => {
			var data = null;
			var d = res.data.data;
			if(is_entity)
			 d=d.data
			var ddd = data_select_options_mapping(code, lookup_type, d);
			gl_lookup_dict[sKey] = ddd;
			result.lookup_entity_list = ddd;
			if (gl_app && result) {
				set_Label_Value(result, gl_app.master_user.data);
	            gl_app.itemkey = Math.random();
				if (gl_app){
                    if(gl_sys_flag&&gl_sys_flag=='N'){
                      gl_app.show_summary=true;
					  //gl_app.getSummaries(gl_grid_columns, true);
                    }else
                      gl_app.show_summary=false
                 }
			}

            var res_data = res.data;
            if (res_data && res_data.status >= 300) {
                gl_app.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		});
}

function set_Label_Value(col, data) {
	if (col && data) {
		len1 = data.length;
		var c = col;
		var lst = c.lookup_entity_list;
		if (lst) {
			var len2 = lst.length;
			for (var k = 0; k < len2; k++) {
				var v = lst[k];
				for (var j = 0; j < len1; j++) {
					var d = data[j];
					left = d[c.field];
					right = v.value;
					if (left && right && left.toString() == right.toString()) {
						d[c.field + "_title"] = v.label;
					}
				}
			}
		}

	}
}

function data_select_options_mapping(code, lookup_type, d) {
	var re = [];
	if (d) {
		var len = d.length;
		for (var i = 0; i < len; i++) {
			var item = d[i];
			key1 = null;
			label1 = null;
			value1 = null;
			label_en1=null;
			disabled1 = false;
			if (code && code.toLowerCase() == 'lookup_classify' && lookup_type && lookup_type.trim() != "") {
				key1 = "lookup_item_code";
				label1 = "lookup_item_name";
				label_en1 = 'lookup_item_name_en';
				value1 = "lookup_item_code";
			} else {
				key1 = 'key';
				label1 = 'label';
				label_en1 = 'label_en';
				value1 = 'value';
				disabled1 = item['disabled'];
			}
			if (item && item['active_flag'] == 'N')
				disabled1 = true;
			new_label=item[label1];
			if (!new_label || new_label ==null || new_label=="")
			  new_label=item[key1]
			if(label_en1&&item[label_en1]&&lang&&lang.toLowerCase()=='en')
			  new_label=item[label_en1]
			var dict = {
				key: item[key1],
				value: item[value1],
				label: new_label,
				label_en: item[label_en1],
				disabled: disabled1
			};
			dict = number2string(dict);
			re.push(dict);
		}
	}
	return re;
}

function getCurrentEntityByCode(code) {
	GL_ENTITY_ID = null;
	var url_fomat_entity = url_entity.format(code);
	axios.get(url_fomat_entity)
		.then(res => {
			var data = null;
			var d = res.data.data;
			if (d) {
				data = d[0];
				GL_ENTITY_ID = data['md_entity_id'];
				var entity_name = data['md_entity_name'];
				data = {
					'value': GL_ENTITY_ID,
					'label': entity_name
				};
			}
			gl_app1.handleClick(data);
			getUISingleEntity(GL_ENTITY_ID)
			if (res.data && res.data.status >=300)
				gl_app1.$message.warning(messageI18n(res.data.message));
		});
}

function getUISingleEntity(entity_id){
  if (!entity_id)
     return null;
  var url=url_ui_single_entity.format(entity_id);
	axios.get(url)
		.then(res => {
			var data = null;
			var d = res.data.data;
			if (d) {
			   gl_ui_single_entity=d;
			   getUISingleEntityLinked(d);
			   setMessage(gl_ui_single_entity,gl_app.master_user.columns);
			}
			//if (res.data && res.data.status >=300)
				//gl_app1.$message.warning(res.data.message);
		});
}
function setMessage(ui_fields_list,columns){
  if(ui_fields_list&&columns)
    for (var i=0;i<ui_fields_list.length;i++){
      item=ui_fields_list[i];
      f=item.md_fields_name;
      if(item&&item.message_key&&item.message_key.trim().length>0&&f)
      for(var j=0;j<columns.length;j++){
        item1=columns[j];
        ff=item1.field;
        if(ff==f){
         item1.message_key=item.message_key;
        }

      }

    }
}
function getEntityRelation(frm_entity_ids,to_entity_ids){
   if (!entity_id)
     return null;
   var url=entity_rel_url;
   data={"$F_ENTITY_ID":frm_entity_ids,"$T_ENTITY_ID":to_entity_ids}
   axios.post(url,data)
		.then(res => {
			var data = null;
			var d = res.data.data;
			if (d) {
			   gl_entity_relations=d;
			}
            var res_data = res.data;
            if (gl_app&&res_data && res_data.status >= 300) {
                gl_app.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		});
}

function getUISingleEntityLinked(d){
   if(!d)
     return;
   len=d.length;
   ls=[]
   for(i=0;i<len;i++){
     item=d[i];
     l_field=item.linked_field_id
     if(!l_field)
       continue
     for(j=0;j<len;j++){
       item1=d[j];
       id=item1.ui_fields_id;
       if(id&&JSON.stringify(id)==JSON.stringify(l_field)){
         //item['linked_entity_id']=item1.entity_id;
         //item['linked_entity_code']=item1.md_entity_code;
         item['linked_md_field_name']=item1.md_fields_name;
         item['linked_md_field_id']=item1.md_fields_id;
         ls.push(item)
       }
     }
   }
   if(ls&&ls.length>0){
     gl_linked_entity_list=ls;
     //getEntityRelation();
   }

}

function get_curr_entity_metadata(entity_id) {
	axios.get(url_entity_current.format(entity_id))
		.then(res => {
			//var data=res.data.data[0];
			var data = null;
			var d = res.data.data;
			if (d) {
				data = d[0];
				gl_sys_flag = data['sys_flag'];
				gl_dialog_title = data['md_entity_name'];
				if (gl_app){
					gl_app.dialog_title = gl_dialog_title;
					if(gl_sys_flag&&gl_sys_flag=='N')
					  gl_app.show_summary=true
					else
					  gl_app.show_summary=false
					}
				label_gl = gl_dialog_title;

				if (gl_app&&res.data && res.data.status >=300)
					gl_app.$message.warning(messageI18n(res.data.message));
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

            var res_data = res.data;
            if (app&&res_data && res_data.status >= 300) {
                app.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})
}


function queryMetadata(url) {
    langu=language()
    gl_app.action_lbl='Action';
    if(langu&&langu=='zh'){
     gl_app.loading_text="拼命加载中，请稍候...";
     gl_app.action_lbl='操作';
    }else
     gl_app.loading_text="Please Wait,Data Loading...";
	if (gl_app)
		gl_app.loading = true;

	var parent_data_id = getUrlKey('parent_data_id');
	var parent_entity_id = getUrlKey('parent_entity_id');
    var readonly = getUrlKey('readOnly');
    if(readonly&&(readonly=='1'||readonly=='true'))
      gl_app.readOnly=true;
     else
      gl_app.readOnly=false;

	if(parent_data_id&&parent_entity_id){
        url+="&$PARENT_ENTITY_ID={0}".format(parent_entity_id)
        url+="&$parent_data_id={0}".format(parent_data_id)
        if (gl_app){
         gl_app.parent_entity_id=parent_entity_id
         gl_app.parent_data_id=parent_data_id
        }

    }
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
				width1=150;
				if(row){
                    rowCount=Object.keys(row).length
                    if(row&&rowCount>0){
                      width1=Math.round(1200/rowCount)
                      if(width1<150)
                       width1=150
                      else if(width1>500)
                       width1=500
                    }
				}
				for (var key in row) {
					var type1 = null;
					var dict0 = {
						field: key,
						title: key,
						type: type1,
						width:width1
					}
					cols[i] = dict0;
					i++;
				}
				for (var i = 0; i < len; i++) {
					var d = data[i];
					//赋值id为第一个序号的值，以便后续编辑，一般是key id的值，标识行的唯一性。
					d["$_clmn_id_"] = i + 1;
				}
				dict = {
					columns: cols,
					datas: data,
					size: len
				};
			}
			renderTable(dict);
            var res_data = res.data;
            if (gl_app&&res_data && res_data.status >= 300) {
                gl_app.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})
}

function number2string_list(list) {
	if (list) {
		var len = list.length;
		for (var i = 0; i < len; i++) {
			var item = list[i];
			item = number2string(item);
		}
	}
	return list;
}

function number2string(dict) {
	if (dict)
		for (f in dict) {
			var v = dict[f];
			if (v && (typeof v == 'object' || typeof v == 'number'))
				dict[f] = v.toString();
		}
	return dict
}

function str2dict(columns, dict) {
	if (dict && columns) {
		var len = columns.length;
		for (var i = 0; i < len; i++) {
			var item = columns[i];
			if(item&&item.field=="$parent_data_id")
			  item.visible=false
			else
			  item.visible=true
			if (item.lookup_flag == 'Y' && dict[item.field].indexOf("[") != -1 && dict[item.field].indexOf("]") != -1)
				dict[item.field] = eval("(" + dict[item.field] + ")");
		}
	}
	return dict
}

function queryData() {
	var id = this.entity_name.value;
	var s = url.format(id);
	queryMetadata(s);
}

function load_column_info(app) {
	if (gl_field_type) {
		var len = 0;
		var len1 = 0;
		if (app.master_user.columns) {
			len = app.master_user.columns.length;
		}
		if (gl_fields_list) {
			len1 = gl_fields_list.length;
		}
		for (var i = 0; i < len; i++) {
			var d = app.master_user.columns[i];
			for (var j = 0; j < len1; j++) {
				var f = gl_fields_list[j];
				if (d.field == f['md_fields_name']) {
					d["type"] = f["md_fields_type"];
					d["is_null"] = f["is_null"];
					d["is_key"] = f["is_key"];
					if(d.field=="$parent_data_id")
					 d['tab_visible']=false
					 else
					  d['tab_visible']=true

					if (f['is_key'] == 'Y' || f['md_fields_name'].toLowerCase() == 'last_update_date' || f['md_fields_name'].toLowerCase() == 'last_update_by' ||
						f['md_fields_name'].toLowerCase() == 'create_date' || f['md_fields_name'].toLowerCase() == 'create_by' ||
						f['md_fields_name'].toLowerCase() == 'tenant_id' )
						d['readonly'] = true
					else
						d['readonly'] = false
					var ent_look = f["lookup_entity"]
					d["lookup_type"] = f["lookup_type"];
					d["lookup_flag"] = f["lookup_flag"];
					d["md_fields_name_cn"] = f["md_fields_name_cn"];
					d["length"] = f["md_fields_length"];
					d["decimal"] = f["md_decimals_length"];
					var cn = f["md_fields_name_cn"];
					var en = f["md_fields_name_en"];
					if (en && en.trim() != "")
						d["title"] = en;
					if (cn && cn.trim() != ""&&language()=='zh')
						d["title"] = cn;
					d["lookup_entity"] = ent_look;
					if (ent_look && ent_look != "")
						get_entity_info_by_code(ent_look, d, f["lookup_type"]);
					break;
				}
			}
		}

        if(app)
          mapping_data_view_title(app.master_user.columns,gl_data_view);

	}
};

function insertData(data) {
	if (!data)
		return null;
	return axios.post(url_root + '/services/insertEntity', data);
};

function updateData(data) {
	if (!data)
		return null;
	return axios.post(url_root + '/services/updateEntity', data);
};

function deleteData(data) {
	if (!data)
		return null;
	return axios.post(url_root + '/services/deleteEntity', data);
};

function system_field_filter(dict) {
	//var new_dict=null;
	if (dict)
		for (field in dict) {
			if (field.toLowerCase() == 'last_update_date' || field.toLowerCase() == 'last_update_by' ||
				field.toLowerCase() == 'create_date' || field.toLowerCase() == 'create_by')
				delete dict[field];
		}
	return dict;
}

function renderTable(result) {
	if (!result) return;
	var cols = result.columns;
	var data1 = result.datas;
	data1 = number2string_list(data1);
	var field_types = result.field_types;
	var app = null;
	//主要内容
	if (gl_app) {
		app = gl_app;
		app.loading = true;
		app.currentPage = 1;
	} else {
		app = new Vue({
			el: "#app",
			data: {
				master_user: {
					sel: null, //选中行
					columns: [],
					data: [],
					ui_fields:[]
				},
				currentPage: 1, //默认显示页面为1
				pagesize: 10, //    每页的数据条数
				readOnly:false,
				table_height:450,
				lang:language(),
				loading_text:'Please Wait,Data Loading...',
				action_lbl:'Action',
				dialogFormVisible: false,
				formLabelWidth: '200px',
				dialog_title: "",
				selected_entity_name: "",
				row_sel: null,
				itemkey: null,
				itemkey1: null,
				loading: true,
				file: {},
				fileList: [],
				multipleSelection: [],
				show_summary:false,
				parent_entity_id:null,
				parent_data_id:null
			},
			mounted(){
                this.addEventListener()
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
				tip_show(val) {
				    if (!val) return;
				    var lang=language();
				    var title1=null;
				    var message1=null;
                    const h = this.$createElement;
                    var url_fomat_entity = entity_url_by_code.format("messages");
                    url_fomat_entity+="&message_key={0}".format(val);
                    axios.get(url_fomat_entity)
                        .then(res => {
                            var data = null;
                            var d = res.data.data;
                            if (d&&d.length>0) {
                                data = d[0];
                                //var entity_id = data['md_entity_id'];
                                //for_new_entity_id = entity_id;
                                //val="<a href='xxx'>"+val+"</a>"
                                if (lang&&lang=='zh'){
                                  title1='{0}[{1}]'.format(data.message_title,val)
                                  message1=h('div', { style: 'color: gray'}, this.message_format(val,data.messages,title1));
                                }else{
                                  title1='{0}[{1}]'.format(data.message_title_en,val)
                                  message1=h('div', { style: 'color: gray'}, this.message_format(val,data.messages_en,title1));
                                }
                                this.$notify({ title: title1,customClass:'notifyCustomClass',message:message1 });
                            }
                            if (gl_app1&&res.data && res.data.status >= 300)
                                gl_app1.$message.warning(messageI18n(res.data.message));
                        });
                 },
                 message_format(key,msg,title){
                    if(!msg)
                     msg="";
                    let newDatas = [];
                    too_long=false
                    let data=msg.split("\\n");
                    const h = this.$createElement;
                    for (let i in data) {
                        newDatas.push(h('p', null, data[i]));
                    }
                  return newDatas;
                 },
				getFile(item) {
					console.log(item.file)
					this.file = item.file
				},
				numberFormat(cellValue) {
					return cellValue ? this.stateFormat(cellValue)
						.toLocaleString() : "";
				},
				stateFormat(cellValue) {
					if (cellValue) {
						cellValue += "";
						if (!cellValue.includes(".")) cellValue += ".";
						return cellValue
							.replace(/(\d)(?=(\d{3})+\.)/g, ($0, $1) => {
								return $1 + ",";
							})
							.replace(/\.$/, "");
					}
				},
                handleCurrentSelectChange(val) {
                   if(val&&gl_app.master_user.sel!=val){
                      gl_app.master_user.sel = val;
                      row_id=null;
                      for (i in gl_app.master_user.columns){
                        col=gl_app.master_user.columns[i]
                        if(col&&col.is_key=='Y')
                          row_id=val[col.field]
                      }
                      if(row_id){
                        d={'row_id':row_id,'entity_id':GL_ENTITY_ID}
                        sendMessage2Parent('onSelectChange',d)
                       }
                      //gl_app.itemkey=Math.random();
                    }
                },
                addEventListener(){
                    // 接受父页面发来的信息
                    window.addEventListener("message", function(event){
                      var data = event.data;
                      switch (data.cmd) {
                        case 'parentMessage':
                            // 处理业务逻辑
                            app.$message('receive Message from Parent,message:{0}'.format(data));
                            break;
                        }
                    });
                },
				handleSelectionChange(val) {
					len=0
					if(val)
					  len=val.length;
					if(len>0)
					for (var i=len-1;i>=0;i--){
					  item=val[i];
					  active_flag=item.active_flag
					  if (active_flag && active_flag=='N')
					   val.splice(i,1)
					}
					app.multipleSelection = val;
					//console.log("---selected=", val);
				},
                cellStyle(row,column,rowIndex,columnIndex){//根据报警级别显示颜色
                    if(row.row&&row.row.active_flag=='N'){
                      return "color:#AAAAAA;font-size:12px;font-style:italic;"
                    }else {
                      //return "font-size:12px"
                    }
                },
				checkSelect (row,index) {
                  let isChecked = true;
                  if (row&&row.active_flag=='N') { // 判断里面是否存在某个参数
                    isChecked = false
                  } else {
                     isChecked = true
                  }
                  return isChecked
                },
				getSummaries(param, isManual = false) {
					const indexs = [0, 2, 3];
					if(gl_app&&!gl_app.show_summary ||!param)
					 return [];
					// console.log("---param=", param);
					const {
						columns,
						data
					} = param;
					if (!columns || columns.length <= 3 || !columns[3].property)
						return [];
					if (!isManual) {
						gl_grid_columns = param;
					}
					const sums = [];
					columns.forEach((column, index) => {
						if (index === 0) {
							sums[index] = "合计";
							return;
						} else if (indexs.includes(index)) {
							sums[index] = "";
							return;
						}
						var is_number = false;
						var is_int=false;
						if (column.property && gl_app && gl_app.master_user.columns) {
							cols = gl_app.master_user.columns;
							len = cols.length;
							for (var i = 0; i < len; i++) {
								var col = cols[i];
								if (column.property == col.field){
								   if (col.is_key == 'N'&&(!col.lookup_entity || col.lookup_entity.trim() == '')
								      &&(col.type=='int'||col.type=='decimal'||col.type=='bigint'||col.type=='number'||col.type=='money'||col.type=='numeric')){
									   is_number = true;
									   if(col.type=='int'||col.type=='bigint')
									    is_int=true;
									}
									break;
								}
							}
						}
						// console.log(data);
						const values = data.map((item) => Number(item[column.property]));
						// console.log(values);
						if (is_number && values.every((value) => /^(-)?([0-9]+)(\.\d{1,8})?$/.test(value))) {
							sums[index] = values.reduce((prev, curr) => {
								const value = Number(curr);
								if (!isNaN(value)) {
									return prev + curr;
								} else {
									return prev;
								}
							}, 0);
							var result=0;
							if(is_int)
							  result=this.stateFormat(sums[index].toFixed(0));
							else
							  result=this.stateFormat(sums[index].toFixed(2));

							sums[index] = result;

							// sums[index] += " 元";
						} else {
							sums[index] = "";
						}
					});
					return sums;
				},
				//添加数据
				add() {
					var set = {}
					if (app.master_user.columns) {
						let len = app.master_user.columns.length;
						var list = []
						if (len <= 0) {
							if (gl_field_type) {
								for (item in gl_field_type) {
									var label = item;
									if (gl_field_name_cn_dict && gl_field_name_cn_dict[item] && gl_field_name_cn_dict[item].trim() != "") {
										label = gl_field_name_cn_dict[item];
									}
									list.push({
										'field': item,
										'title': label,
										'type': gl_field_type[item],
										'lookup_entity': gl_field_lookup_entity_dict[item],
										"lookup_type": gl_field_lookup_type_dict[item],
										"lookup_flag": gl_field_lookup_flag_dict[item],
										"length":gl_field_length_dict[item],
										"decimal":gl_field_decimal_dict[item]
									});
								}
								app.master_user.columns = list;
								len = app.master_user.columns.length;
							}
						}
						for (var i = len - 1; i >= 0; i--) {
							var field = app.master_user.columns[i];
							var field_name = field.field;
							field.visible = true;
							if (field_name.toLowerCase() == 'last_update_date' || field_name.toLowerCase() == 'last_update_by' ||
								field_name.toLowerCase() == 'create_date' || field_name.toLowerCase() == 'create_by' ||
								field_name.toLowerCase() == '$parent_data_id' ||
								field_name.toLowerCase() == 'tenant_id' ) {
								field.visible = false;
							}
							set[field_name] = null;
						}
					}
					set.isSet = true;
					set.isNew = true;
					var new_dict = JSONbig.parse(JSONbig.stringify(set));
					load_column_info(app);
					app.master_user.sel = new_dict
					if (label_gl)
						app.dialog_title = label_gl + "(新增)";
					app.dialogFormVisible = true;
				},
				openDialog(row, index) {
				    //app.master_user.sel=row;
					app.cascadeSelector(row);
					var dict = JSONbig.parse(JSONbig.stringify(row));
					dict = number2string(dict);
					str2dict(app.master_user.columns, dict);
					app.master_user.sel = dict;
					row.isSet = true;
					//app.load_column_info();
					if (label_gl)
						app.dialog_title = label_gl;
			        //app.itemkey1 = Math.random();
					app.dialogFormVisible = true;
				},
				cascadeSelector(sel_row,field_name_selected){
				  gl_select_row=sel_row;
				  if(gl_linked_entity_list&&gl_linked_entity_list.length>0&&sel_row){
				     for (i in gl_linked_entity_list){
				         item=gl_linked_entity_list[i];
                         linked_md_field_name=item['linked_md_field_name'];
                         linked_md_field_id=item['linked_md_field_id'];
                         field_name=item["md_fields_name"];
                         data_id=sel_row[field_name];
				         cols=app.master_user.columns;
				         parent_code=null;
				         if(field_name_selected)//如果是下拉变化，则值更新变化的联动。
                            if(field_name_selected==linked_md_field_name)
                               sel_row[field_name]="";
                            else
                              continue;
				         if(cols)
				           for (k in cols){
				             co=cols[k];
				             ff=co.field;
				             if(linked_md_field_name&&linked_md_field_name==ff){
				               parent_code=co.lookup_entity;
                               parent_data_id=sel_row[linked_md_field_name];
                               sel_row['$parent_data_id-'+field_name]=parent_data_id;
				               break;
				              }
				           }
				           for (j in cols){
				             col=cols[j]
				             f=col.field
				             if(field_name&&field_name==f&&parent_code){
                               code=col.lookup_entity;
                               col.parent_entity_code=parent_code;
                               getLookupEntityByParentId(col,code,parent_code,parent_data_id);
                               break;
                             }
                           }
                     }
				  }
				},
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
				set_unfill_fields(index, data) {
					var is_not_ok = false;
					if (!data)
						return is_not_ok;
					var len = 0;
					if (app.master_user.columns)
						len = app.master_user.columns.length;
					for (var i = 0; i < len; i++) {
						var item = app.master_user.columns[i];
						for (field in data) {
							if ((data[field] == null || data[field] == '') && field == item.field && item.is_null == 'N') {
								if (item.readonly) //新建记录，不校验主键ID。
									continue
								var id = field + index;
								var dom = document.getElementById(id);
								dom.style.border = '1px solid #FF8800';
								is_not_ok = true;
								break;
							}

						}
					}
					return is_not_ok;
				},
				onchange(field_name, row, index,val=-1.0123456789) {
				    if (val!=-1.0123456789)
				       if(val&&val.value){
				         row[field_name]=val.value;
				         row[field_name+"_title"]=val.label;
				       }else
				         row[field_name]=val;
					app.cascadeSelector(row,field_name);
					row.isEdit = true;
					edit_gl = true;
					row.isSet = true;
					var id = field_name + index;
					var dom = document.getElementById(id);
					if(dom)
					 dom.style.border = '1px solid #33FF00';
					 app.cacl_rule(field_name,row)
					//console.log(field_name,row, index);
				},
				cacl_rule(field,data){
				    codes=[]
                    if(gl_rules_list&&gl_rules_list.length>0){
                     len=gl_rules_list.length
                     for(i=0;i<len;i++){
                        item=gl_rules_list[i];
                        f=item["input_params"]
                        if(f)
                          d=eval(f)
                          if(d&&d.length>0){
                              len1=d.length
                              for (var j=0;j<len1;j++){
                                item1=d[j]
                                if (item1 && item1==field)
                                 codes.push({"rule_code":item["rule_code"]})
                              }
                          }
                       }
                      if(codes&&codes.length>0)
                        app.ruleCompute(codes,data);
                      }
				},
				ruleCompute(rule_codes,input_data){
                    url=rule_compute_url;
                    data={"$_ENTITY_ID":GL_ENTITY_ID,"rule_category":"Computing","rules":rule_codes,"data":input_data}
                    axios.post(url, data).then(res => {
                            rule_dict=res.data;
                            update_fields=rule_dict["$rule_output"];
                            if(update_fields)
                              for (key in update_fields){
                                input_data[key]=update_fields[key];
                              }

                            var res_data = res.data;
                            if (app&&res_data && res_data.status >= 300) {
                                app.$message.warning({
                                    type: 'warning',
                                    message: messageI18n(res_data.message)
                                });
                                return;
                            }
                         }).catch(error => {
                          // this.$message.error(error.status)
                          this.$message.error('规则计算异常');
                          console.log(error)
                        })
				},
				ruleEntity(entity_id){
                    url=rule_entity_url;
                    data={"$_ENTITY_ID":entity_id,"rule_category":"Computing"}
                    axios.post(url, data).then(res => {
                            gl_rules_list=res.data.data;
                            var res_data = res.data;
                            if (app&&res_data && res_data.status >= 300) {
                                app.$message.warning({
                                    type: 'warning',
                                    message: messageI18n(res_data.message)
                                });
                                return;
                            }
                         }).catch(error => {
                          // this.$message.error(error.status)
                          this.$message.error('规则查询异常');
                          console.log(error)
                        })
				},
				data_mapping(data) {
					if (!data)
						return null
					var len = 0;
					var new_dict = JSONbig.parse(JSONbig.stringify(data));
					if (app.master_user.columns)
						len = app.master_user.columns.length;
					for (var i = 0; i < len; i++) {
						var item = app.master_user.columns[i];
						for (field in data) {
							if (field == item.field) {
								var f = field;
								if (item.is_key == 'Y') {
									delete new_dict[field];
									break;
								} else if (f.toLowerCase() == 'last_update_date' || f.toLowerCase() == 'last_update_by' ||
									f.toLowerCase() == 'tenant_id' || f.toLowerCase() == 'create_date' || f.toLowerCase() == 'create_by' ||
									f.toLowerCase() == 'isedit' || f.toLowerCase() == 'isset' || f.toLowerCase() == '$_clmn_id_') {
									delete new_dict[field];
								}
								break;
							}

						}
					}
					return new_dict;

				},
				data_key_mapping(data) {
					var key_list = [];
					if (!data)
						return null;
					var len = 0;
					if (app.master_user.columns)
						len = app.master_user.columns.length;
					var len1 = data.length;
					for (var j = 0; j < len1; j++) {
						var item1 = data[j];
						for (field in item1) {
							var skip = false;
							for (var i = 0; i < len; i++) {
								var item = app.master_user.columns[i];
								if (field == item.field && item.is_key == 'Y') {
									var key_dict = {};
									key_dict[field] = item1[field];
									key_list.push(key_dict);
									skip = true;
									break;
								}
							}
							if (skip) break;
						}
					}
					return key_list;
				},
				submit_update_data(row, index) {
					//请求操作,按需修改下
					let data = JSONbig.parse(JSONbig.stringify(app.master_user.sel));
					//判断必填是否填写。
					var is_filled_ok = app.set_unfill_fields(index, app.master_user.sel);
					if (is_filled_ok) {
						app.$message({
							type: 'warning',
							message: "必填字段不能为空，请填写"
						});
						return;
					}
					var data_upd_field = null;
					var data_add_field = null;
					let sel_data = app.master_user.sel;
					if (sel_data && sel_data.isNew) {
						var new_dict = sel_data;
						data_add_field = {
							"$_ENTITY_ID": GL_ENTITY_ID,
							"data": new_dict
						};
						if(app.parent_data_id&&app.parent_entity_id){
						  data_add_field['$PARENT_ENTITY_ID']=app.parent_entity_id
						  data_add_field['$parent_data_id']=app.parent_data_id
						}
					} else if (sel_data && sel_data.isEdit) {
						var new_dict = sel_data;
						var new_list = [];
						new_list.push(new_dict);
						var key_list = app.data_key_mapping(new_list);
						new_dict = app.data_mapping(new_dict);
						data_upd_field = {
							"$_ENTITY_ID": GL_ENTITY_ID,
							"data": [new_dict],
							"where": key_list
						};
					} else
						data_upd_field = null;
					axios.all([insertData(data_add_field), updateData(data_upd_field)])
						.then(axios.spread(function(acct, perms) {
							// 两个请求现在都执行完成
							var res_data = null;
							if (perms)
								res_data = perms.data
							else if (acct)
								res_data = acct.data;
							edit_gl = false;
							//console.log(acct, perms);
							if (res_data && res_data.status >= 300) {
								app.$message.warning({
									type: 'warning',
									message: messageI18n(res_data.message)
								});
							    console.log("校验未通过详情：", res_data.data);
								return;
							} else{
							     getI18nMessage("save_success_hint","").then((msg)=>{
                                    app.$message({
                                        type: 'success',
                                        message: msg
                                    });
                                });
                                //然后这边重新读取表格数据
                                app.readMasterUser();
                                app.dialogFormVisible = false;
                                app.master_user.sel = null;
                                row.isSet = false;
							}
							//row.isSet = false;
							if (gl_app1) {
								var curpage = app.currentPage;
								var psize = app.pagesize;
								gl_app1.handleClick(gl_select_data);
								app.currentPage = curpage;
								app.pagesize = psize;
							}
							//window.location.reload();
						}));
				},
				cancel_action(row, index) {
					if (row.isSet == "undefined")
						row.isSet = false
					row.isEdit = false;
					edit_gl = false;
					row.isSet = false;
					app.dialogFormVisible = false;
					app.readMasterUser();
					app.master_user.sel = null;
					return row.isSet;
				},
				delete_multi_record() {
					var data_list = app.multipleSelection;
					if (!data_list || data_list.length == 0) {
						app.$message({
							type: 'warning',
							message: "没有选中删除的记录，请选择再进行删除！"
						});
						return;
					}
					app.delete_submit(data_list, data_list.length);
				},
				delete_submit(data_list, index) {
					this.$confirm('你要删除当前选定数据, 是否确认?', '提示', {
							confirmButtonText: '确定',
							cancelButtonText: '取消',
							type: 'warning'
						})
						.then(() => {
							//点击确定的操作(调用接口)
							var data_upd_field = null;
							var key_list = app.data_key_mapping(data_list);
							//new_dict=app.data_mapping(new_dict);
							var new_data_list = [];
							if (key_list && gl_sys_flag == 'Y') {
								var len2 = key_list.length;
								for (var j = 0; j < len2; j++) {
									var data_dict = {
										'active_flag': 'N'
									};
									new_data_list.push(data_dict);
								}
							}
							var data_upd_field = null;
							var data_del_field = null;
							if (gl_sys_flag == 'Y') //为Y则失效数据，为N则删除
								data_upd_field = {
									"$_ENTITY_ID": GL_ENTITY_ID,
									"data": new_data_list,
									"where": key_list
								};
							else
								data_del_field = {
									"$_ENTITY_ID": GL_ENTITY_ID,
									"data": null,
									"where": key_list
								};
							axios.all([updateData(data_upd_field), deleteData(data_del_field)])
								.then(axios.spread(function(acct, perms) {
									// 两个请求现在都执行完成
                                    var res_data = null;
                                    if (perms)
                                        res_data = perms.data
                                    else if (acct)
                                        res_data = acct.data;
                                    if (res_data && res_data.status >= 300) {
                                        app.$message.warning({
                                            type: 'warning',
                                            message: messageI18n(res_data.message)
                                        });
                                        return;
                                    } else
                                        app.$message({
                                            type: 'success',
                                            message: "删除成功！"
                                        });
									//console.log(acct, perms);
									if (gl_app1) {
										var curpage = app.currentPage;
										var psize = app.pagesize;
										gl_app1.handleClick(gl_select_data);
										app.currentPage = curpage;
										app.pagesize = psize;
									}
									//window.location.reload();
								}));
							app.master_user.data.splice(index, 1);
						})
						.catch(() => {
							//点击取消的提示
							if(row)
							  app.master_user.sel = row;
							return;
						});
				},
				submit_delete_data(row, index) {
					if (index >= 0) {
						row.isSet = false;
						let sel_data = row;
						var new_list = [];
						new_list.push(sel_data);
						app.delete_submit(new_list, index);
						return;
					}
				},
				//修改
				pwdChange(row, index) {
					var dict = JSONbig.parse(JSONbig.stringify(row));
					app.master_user.sel = dict;
					if (gl_field_type) {
						app.master_user.types = gl_field_type; // 数据类型数据
					}
					row.isSet = true;
					this.$set(app.master_user.data, index, row);
					gl_app = app;

				}
			}
		});
		gl_app = app;
        if(gl_sys_flag&&gl_sys_flag=='N'){
          gl_app.show_summary=true;
        }else
          gl_app.show_summary=false
	}
	app.master_user.columns = cols; // 数据属性数据
    setMessage(gl_ui_single_entity,gl_app.master_user.columns);
	app.master_user.types = gl_field_type; // 数据类型数据
	app.master_user.data = data1; // 查询业务数据
	gl_app = app;
	if (app)
		load_column_info(app);
	app.dialog_title = label_gl;
	app.selected_entity_name = label_gl;
	app.loading = false;
	app.itemkey = Math.random();
	//app.$message('loading data ok');
}


function renderToolbar() {
    getUIElements();
	//主要内容
	var app = new Vue({
		el: "#app1",
		data() {
			return {
				options: [],
				select1: '',
				entity_name: "",
				entity_name1: "",
				select_value: "",
				showapp1: false,
				addFormVisible: false,
				table_options: [],
				form_data: {
					md_entity_code: null,
					md_entity_name: null,
					md_entity_name_en: null,
					md_tables_id: null,
					md_entity_desc: null
				}
			}
		},
		methods: {
			handleClick(data) {
				var value = "";
				var label = "";
				if (gl_app)
					gl_app.master_user.columns = null;
				if (data) {
					value = data.value;
					label = data.label;
				}
				gl_field_name_cn_dict = null;
				gl_select_data = data;
				var str_value = value.toString();
				var url = null;
				GL_ENTITY_ID = value.toString();
				getUISingleEntity(GL_ENTITY_ID);
				if (GL_ENTITY_ID)
				 gl_app.ruleEntity(GL_ENTITY_ID);
	            var template_code = getUrlKey('template_code');
				url = entity_info_url.format(GL_ENTITY_ID,template_code);
	            var _row_id_ = getUrlKey('_row_id_');
	            //var is_child = getUrlKey('is_child');
	            if(_row_id_)
	              url+='&$_row_id_={0}'.format(_row_id_)
				queryMetadata(url);
				let res = app.queryFields(url_fields.format(GL_ENTITY_ID));
				if (gl_app) {
					gl_app.dialog_title = label;
					label_gl = label;
				} else {
					label_gl = label;
				}
				gl_app.selected_entity_name = label;
				get_curr_entity_metadata(GL_ENTITY_ID);

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
                        var res_data = res.data;
                        if (app&&res_data && res_data.status >= 300) {
                            app.$message.warning({
                                type: 'warning',
                                message: messageI18n(res_data.message)
                            });
                            return;
                        }
					})

			},
			async queryFields(url) {
				let res = await axios.get(url)
					.then(res => {
						var dict1 = {};
						var dict2 = {};
						var dict3 = {};
						var dict4 = {};
						var dict5 = {};
						var dict6 = {};
						var dict7 = {};

                        var res_data = res.data;
                        if (app&&res_data && res_data.status >= 300) {
                            app.$message.warning({
                                type: 'warning',
                                message: messageI18n(res_data.message)
                            });
                            return;
                        }
						var data = res.data.data;
						if (data) {
							var len = 0;
							if (data)
								len = data.length;
							for (var i = 0; i < len; i++) {
								var d = data[i];
								dict1[d["md_fields_name"]] = d["md_fields_type"];
								dict2[d["md_fields_name"]] = d["lookup_entity"];
								dict3[d["md_fields_name"]] = d["lookup_type"];
								dict4[d["md_fields_name"]] = d["lookup_flag"];
								dict5[d["md_fields_name"]] = d["md_fields_name_cn"];
								dict6[d["md_fields_name"]] = d["md_fields_length"];
								dict7[d["md_fields_name"]] = d["md_decimals_length"];
							}
						}
						gl_field_type = JSONbig.parse(JSONbig.stringify(dict1));
						gl_field_lookup_entity_dict = JSONbig.parse(JSONbig.stringify(dict2));
						gl_field_lookup_type_dict = JSONbig.parse(JSONbig.stringify(dict3));
						gl_field_lookup_flag_dict = JSONbig.parse(JSONbig.stringify(dict4));
						gl_field_name_cn_dict = JSONbig.parse(JSONbig.stringify(dict5));
						gl_field_length_dict = JSONbig.parse(JSONbig.stringify(dict6));
						gl_field_decimal_dict = JSONbig.parse(JSONbig.stringify(dict7));
						gl_fields_list = data;
						if (gl_app)
							load_column_info(gl_app);
					});
			}

		}
	});
	gl_app1 = app;
	if (!gl_app)
		renderTable({
			columns: [],
			datas: [],
			size: 0
		});
	var entity_id = getUrlKey('entity_id');
	var entity_code = getUrlKey('entity_code');
	var head1 = getUrlKey('header');
	gl_field_name_cn_dict = null;
	if (head1 == '1') {
		queryEntity(app);
		app.showapp1 = true
	} else {
		app.showapp1 = false;
	}
	var data = null;
	var flag = false;
	if (entity_id && entity_id.trim()
		.length > 0) {
		data = {
			'value': entity_id,
			'label': ''
		};
		flag = false;
		app.handleClick(data);
	} else if (entity_code && entity_code.trim()
		.length > 0) {
		//data={'value':entity_code,'label':''};
		getCurrentEntityByCode(entity_code);
		flag = true;
	} else {
		var head1 = getUrlKey('header');
		if (head1 != '1')
			app.$message.warning('entity_id 或 entity_code不能为空。');
	}

}
function sendMessage2Parent(cmd,data){
        // 向父vue页面发送信息
        window.parent.postMessage({
            cmd: cmd,
            params: {
              success: true,
              data: data
            }
        }, '*');
 }

renderToolbar();
