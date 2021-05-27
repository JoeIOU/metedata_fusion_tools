var entity_info_url = url_root + "/services/findUIEntity?$_ENTITY_ID={0}&ui_template_code={1}";
var ui_template_info_url = url_root + "/services/queryUIEntities?ui_template_code={0}";
var ui_template_fields_info_url = url_root + "/services/queryUIElements?ui_template_code={0}&entity_id={1}";
var ui_fields_url = url_root + "/services/queryFieldsByCodeOrID";
var url_ui_entity_edit="ui_entity_edit.html?entity_id={0}&parent_entity_id={1}&parent_data_id={3}&template_code={4}&header=0&readOnly={5}"
var url_ui_entity_table="ui_entity_table.html?entity_id={0}&parent_entity_id={1}&parent_data_id={3}&template_code={4}&header=0&readOnly={5}"
var entity_rel_url = url_root + "/services/findEntityRelation";
var rule_compute_url = url_root + "/services/computeRules";
var rule_entity_url = url_root + "/services/findEntityRules";
var GL_APP = null;
var gl_fields_list=null;
var gl_linked_entity_list=null;
var gl_rules_list =null;
var gl_ui_single_entity=null;
var gl_linked_entity_list=null;
var gl_lookup_dict = {};
var gl_entity_relations=null;
var gl_delect_row=null;
var GL_ENTITY_ID =null;
var lang=null;

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
function getEntityFields(entity_ids,ui_data){
    if(!entity_ids)
      return null;
    url=ui_fields_url
    params={"$_ENTITY_ID":entity_ids}
	axios.post(url,params)
		.then(res => {
			var data = res.data.data;
			if(GL_APP){
//			 GL_APP.template_view_data.columns=data;
//			 gl_fields_list = data;
			 load_column_info(GL_APP,data,ui_data);
			}
            var res_data = res.data;
            if (GL_APP&&res_data && res_data.status >= 300) {
                GL_APP.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})
}
function getUIElements(){
	var template_code = getUrlKey('template_code');
    if(!template_code)
      return null;
	//var entity_id = getUrlKey('entity_id');
    var url=ui_template_info_url.format(template_code)
	var _row_id_ = getUrlKey('_row_id_');
	axios.get(url)
		.then(res => {
			var data = res.data.data;
            tree=listToTree(data)
            load(tree);
            var res_data = res.data;
            if (GL_APP&&res_data && res_data.status >= 300) {
                GL_APP.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})
}

function getSingleUIElements(parent_entity_id,entity_id,template_code,row_id,isChild=false){
//	var entity_id = getUrlKey('entity_id');
//	var template_code = getUrlKey('template_code');
	var header_title_show = '0';
	if(GL_APP&&(!header_title_show||header_title_show=='1'))
	  GL_APP.header_title_show=true
	else if(GL_APP)
	  GL_APP.header_title_show=false
    if(!template_code||!entity_id)
      return null;
//	var parent_entity_id = getUrlKey('parent_entity_id');
//	var parent_id = getUrlKey('parent_id');
//	var _row_id_ = getUrlKey('_row_id_');
//    var _row_id_=row_id
//	if(isChild&&row_id)
//	  _row_id_=row_id
    var url=ui_template_fields_info_url.format(template_code,entity_id)
    load_data(parent_entity_id,entity_id,template_code,row_id,isChild);
	axios.get(url)
		.then(res => {
			var data = res.data.data;
			if(GL_APP&&data)
			  GL_APP.view_data.ui_fields=data;
			else
			  GL_APP.view_data.ui_fields=[];
            entity_ids=[]
            if(entity_id)
             entity_ids.push(entity_id)
            primary_entity_id=null
	        if(entity_ids)
	         getEntityFields(entity_ids,data);
            var res_data = res.data;
            if (GL_APP&&res_data && res_data.status >= 300) {
                GL_APP.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})
}
function listToTree(list) {
                var map = {}, node, tree= [], i;
	            var readOnly = getUrlKey('readOnly');
	            var _row_id_ = getUrlKey('_row_id_');
	            var template_code = getUrlKey('template_code');
                for (i = 0; i < list.length; i++) {
                    map[list[i].entity_id] = list[i];
                    list[i].children = [];
                }
                for (i = 0; i < list.length; i++) {
                    node = list[i];
                    parent_entity_id=node.parent_entity_id;
                    entity_id=node.entity_id;
                    if (node.parent_entity_id&&node.parent_entity_id>0) {
                        node1=map[node.parent_entity_id]
                        node1.children.push(node);
                        //tree.push(node);
                        isChild=true;
                        if(node1.parent_entity_id)//如果父类还有父类，则当前parent_id赋予null，当前节点父类变动时，再进行互动。
                          _row_id_=null
                        url=generate_url(parent_entity_id,entity_id,template_code,_row_id_,isChild,readOnly)
                        node.url=url;
                    } else {
                        tree.push(node);
                        url=generate_url(parent_entity_id,entity_id,template_code,_row_id_,false,readOnly)
                        getSingleUIElements(parent_entity_id,entity_id,template_code,_row_id_,false)
                        node.url=url;
                    }
                }
                mmm={}
                mmm.map=map;
                mmm.data_tree=tree
                mmm.data=list
                if(GL_APP){
                 GL_APP.template_view_data.data=list
                 GL_APP.template_view_data.data_tree=tree
                 GL_APP.template_view_data.map=map
                 }
                return mmm;
}

function generate_url(parent_entity_id,entity_id,template_code,_row_id_,isChild=false,isReadOnly='0'){
	if(!entity_id || !template_code)
	  return '';
     page_str='ui_entity_edit.html'
     if(isChild)
       page_str='ui_entity_table.html'
     url=page_str+"?entity_id={0}&template_code={1}&header=0"

	url=url.format(entity_id,template_code);
	if(isChild){
	  url+="&parent_data_id={0}";
	  if(_row_id_)
	    url=url.format(_row_id_);
	  else
	    url=url.format('null');
	}else if(_row_id_)
	  url+="&_row_id_={0}".format(_row_id_);
	if(isChild&&parent_entity_id)
	  url+="&parent_entity_id={0}".format(parent_entity_id);
	if(isReadOnly&&(isReadOnly=='1'||isReadOnly=='true'))
	  url+="&readOnly={0}".format('1');
	 else
	  url+="&readOnly={0}".format('0');
	return url;
}

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
function load_data(parent_entity_id,entity_id,template_code,_row_id_,is_child=false){
	if(!entity_id || !template_code)
	  return;
	GL_ENTITY_ID=  entity_id;
	entity_info_url=entity_info_url.format(entity_id,template_code);
	if(_row_id_&&is_child){
	  entity_info_url+="&$parent_data_id={0}".format(_row_id_);
	}else if(_row_id_)
	  entity_info_url+="&$_row_id_={0}".format(_row_id_);
	if(is_child&&parent_entity_id)
	  entity_info_url+="&$PARENT_ENTITY_ID={0}".format(parent_entity_id);
	url = entity_info_url;
	axios.get(url)
		.then(res => {
			var data = res.data.data;
			if(GL_APP&&data&&data.length>0)
			   GL_APP.view_data.sel=data[0];
			else
			   GL_APP.view_data.sel=[];

            var res_data = res.data;
            if (GL_APP&&res_data && res_data.status >= 300) {
                GL_APP.$message.warning({
                    type: 'warning',
                    message: messageI18n(res_data.message)
                });
                return;
            }
		})

}

function load_column_info(app,data,ui_data) {
		var len1 = 0;
		var len=0;
        var readOnly = getUrlKey('readOnly');
        if(GL_APP&&readOnly&&(readOnly=='1'||readOnly=='true'))
           GL_APP.readOnly=true;
        else if(GL_APP)
           GL_APP.readOnly=false;
		if(data)
		  len1=data.length;
		if(ui_data)
		  len=ui_data.length;
        list_fileds=[]
        for(var i = 0; i < len; i++){
          item=ui_data[i]
          e_id=item['entity_id']
          f_id=item['md_fields_id']
          ui_fields_name_cn=item['ui_fields_name_cn']
          ui_fields_name_en=item['ui_fields_name_en']
          for (var j = 0; j < len1; j++) {
                var f = data[j];
                e_id1=f['md_entity_id']
                f_id1=f['md_fields_id']
                if (!(e_id&&f_id&&f_id==f_id1&&e_id==e_id1))
                  continue
                d={}
                d["$_clmn_id_"] = j + 1;
                d.field = f['md_fields_name'];
                d["type"] = f["md_fields_type"];
                d["is_null"] = f["is_null"];
                d["is_key"] = f["is_key"];
                if (f['is_key'] == 'Y' || f['md_fields_name'].toLowerCase() == 'last_update_date' || f['md_fields_name'].toLowerCase() == 'last_update_by' ||
                    f['md_fields_name'].toLowerCase() == 'create_date' || f['md_fields_name'].toLowerCase() == 'create_by' ||
                    f['md_fields_name'].toLowerCase() == 'tenant_id' )
                    d['readonly'] = true
                else if (GL_APP&&GL_APP.readOnly)
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
                if(ui_fields_name_en)
                    d["title"] = ui_fields_name_en;
                if (cn && cn.trim() != ""&&language()=='zh')
                  if(ui_fields_name_cn)
                    d["title"] = ui_fields_name_cn;
                  else
                    d["title"] = cn;

                d["lookup_entity"] = ent_look;
                list_fileds.push(d);
                break;
          }
        }
        app.view_data.columns=list_fileds;

};
function load(entity_tree){
        app=new Vue({
            el: "#app",
            data: {
              formLabelWidth:200,
              itemkey1 :0,
              itemkey2:0,
              itemkey_form:0,
              lang:'en',
              title:'',
              template_view_data:{
               sel:[],
               columns:[],
               data:[],
               map:null,
               data_tree:[]
              },
              view_data:{
               sel:[],
               columns:[],
               data:[],
               ui_fields:[]
              }
            },
            mounted() {
                  function reinitIframe(){
                    class_name="mmtx_iframe_class";
                    results=document.getElementsByClassName(class_name);
                    if(results&&results.length>0) {
                        for (i in results){
                              var iframe=results[i];
                              //var iframe = document.getElementById("iframe_form");
                              try{
                                  var bHeight = iframe.contentWindow.document.body.scrollHeight;
                                  var dHeight = iframe.contentWindow.document.documentElement.scrollHeight;
                                  var height = Math.min(bHeight, dHeight);
                                  iframe.height = height;
                                 /* console.log(iframe.contentWindow);
                                  console.log(bHeight,dHeight);*/
                              }catch (ex){}
                        }
                   }
                  };
                  setInterval(reinitIframe,200);
                  this.iframeInit();
            },
            methods: {
				cancel_action(row, index) {
					if (row.isSet == "undefined")
						row.isSet = false
					row.isEdit = false;
					edit_gl = false;
					row.isSet = false;
					app.template_view_data.sel = null;
					return row.isSet;
				},
				submit_update_data(row, index) {
					//请求操作,按需修改下
					let data = JSONbig.parse(JSONbig.stringify(app.view_data.sel));
					//判断必填是否填写。
					var is_filled_ok = app.set_unfill_fields(index, app.view_data.sel);
					if (is_filled_ok) {
						app.$message({
							type: 'warning',
							message: "必填字段不能为空，请填写"
						});
						return;
					}
					var data_upd_field = null;
					var data_add_field = null;
					let sel_data = app.view_data.sel;
					if (sel_data && sel_data.isNew) {
						var new_dict = sel_data;
						data_add_field = {
							"$_ENTITY_ID": GL_ENTITY_ID,
							"data": new_dict
						};
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
                                //app.readMasterUser();
                                //app.dialogFormVisible = false;
                                //app.view_data.sel = null;
                                app.itemkey_form=Math.random();
                                row.isSet = false;
							}
							//window.location.reload();
						}));
				},
				set_unfill_fields(index, data) {
					var is_not_ok = false;
					if (!data)
						return is_not_ok;
					var len = 0;
					if (app.view_data.columns)
						len = app.view_data.columns.length;
					for (var i = 0; i < len; i++) {
						var item = app.view_data.columns[i];
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
				data_key_mapping(data) {
					var key_list = [];
					if (!data)
						return null;
					var len = 0;
					if (app.view_data.columns)
						len = app.view_data.columns.length;
					var len1 = data.length;
					for (var j = 0; j < len1; j++) {
						var item1 = data[j];
						for (field in item1) {
							var skip = false;
							for (var i = 0; i < len; i++) {
								var item = app.view_data.columns[i];
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
				data_mapping(data) {
					if (!data)
						return null
					var len = 0;
					var new_dict = JSONbig.parse(JSONbig.stringify(data));
					if (app.view_data.columns)
						len = app.view_data.columns.length;
					for (var i = 0; i < len; i++) {
						var item = app.view_data.columns[i];
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
				cascadeSelector(sel_row,field_name_selected){
				  gl_select_row=sel_row;
				  if(gl_linked_entity_list&&gl_linked_entity_list.length>0&&sel_row){
				     for (i in gl_linked_entity_list){
				         item=gl_linked_entity_list[i];
                         linked_md_field_name=item['linked_md_field_name'];
                         linked_md_field_id=item['linked_md_field_id'];
                         field_name=item["md_fields_name"];
                         data_id=sel_row[field_name];
				         cols=app.view_data.columns;
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
                iframeInit() {
                    // 接受子级返回数据
                    window.addEventListener(
                      'message',
                      (e) => {
                        console.log(e.data)
                        var data = e.data;
                        switch (data.cmd) {
                          case 'onSelectChange':
                            // 处理业务逻辑
                            map=app.template_view_data.map
                            if(map&&data&&data.params&&data.params.data){
                              entity_id= data.params.data.entity_id;
                              row_id= data.params.data.row_id;
                              node=map[entity_id];
                              if(node&&node.children&&node.children.length>0){
                                children=node.children
                                for(i in children){
                                  child=children[i]
                                  url=child.url
                                  if(url&&row_id){
                                     url=replaceUrlParamVal(url,'parent_data_id',row_id);
                                     if(url)
                                      child.url=url;
                                  }
                                }
                              }
//                            msg='receive Message from Parent,message:{0}'.format(JSON.stringify(data))
//                            app.$message(msg);
                            }
                            break;
                        }
                      },
                      false
                    )
                }
            }
        });
        app.lang=language();
        var doc_title=''
        if(app.lang=='zh')
          doc_title = '{0}-业务视图';
        else
          doc_title = '{0}-Business View';

	    var entity_id = getUrlKey('_row_id_');
	    if(!entity_id)
	      entity_id='null'
        document.title = doc_title.format(entity_id);
        if(entity_tree){
          app.template_view_data.data=entity_tree.data;
          app.template_view_data.map=entity_tree.map;
          app.template_view_data.data_tree=entity_tree.data_tree;
        }
        if(entity_tree&&entity_tree.data&&entity_tree.data.length>0)
           app.title=entity_tree.data[0].ui_template_name
        GL_APP=app;
}

function replaceUrlParamVal(url,paramName, replaceWith) {
	var oUrl = url;
	var re = eval('/(' + paramName + '=)([^&]*)/gi');
	var nUrl = "";
	var rep_str = paramName + '=' + replaceWith;
	if (oUrl.indexOf(paramName + "=") < 0) {
		if (oUrl.indexOf("?") < 0)
			nUrl = oUrl + "?" + rep_str;
		else
			nUrl = oUrl + "&" + rep_str;
	} else
		nUrl = oUrl.replace(re, rep_str);
	return nUrl;
}
function next(){
   if (confirm("Next Step?")) {

    return true;
  }
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
function messageReceive(){
    // 接受子级返回数据
    window.addEventListener(
      'message',
      (e) => {
        console.log(e.data)
        // alert('iframe页面token失效了')
        // 外部vue向iframe内部传数据
        iframe.contentWindow.postMessage(JSON.stringify({
          token: getToken()
        }), this.src)
      },
      false
    )
}
getUIElements();
