var entity_info_url = url_root + "/services/findUIEntity?$_ENTITY_ID={0}&ui_template_code={1}";
var ui_template_info_url = url_root + "/services/queryUIElements?ui_template_code={0}&entity_id={1}";
var ui_fields_url = url_root + "/services/queryFieldsByCodeOrID";
var GL_APP = null;
var gl_fields_list=null;
var gl_linked_entity_list=null;
var gl_rules_list=null;

function getEntityFields(entity_ids,ui_data){
    if(!entity_ids)
      return null;
    url=ui_fields_url
    params={"$_ENTITY_ID":entity_ids}
	axios.post(url,params)
		.then(res => {
			var data = res.data.data;
			if(GL_APP){
//			 GL_APP.view_data.columns=data;
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
	var entity_id = getUrlKey('entity_id');
	var template_code = getUrlKey('template_code');
	var header_title_show = getUrlKey('header');
	if(GL_APP&&(!header_title_show||header_title_show=='1'))
	  GL_APP.header_title_show=true
	else if(GL_APP)
	  GL_APP.header_title_show=false
    if(!template_code||!entity_id)
      return null;
	var parent_entity_id = getUrlKey('parent_entity_id');
	var parent_id = getUrlKey('parent_id');
	var _row_id_ = getUrlKey('_row_id_');
	if(is_child&&is_child=='1'&&parent_id)
	  _row_id_=parent_id
	var is_child = getUrlKey('is_child');
    var url=ui_template_info_url.format(template_code,entity_id)
    load_data(parent_entity_id,entity_id,template_code,_row_id_,is_child=='1');
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
function load_data(parent_entity_id,entity_id,template_code,_row_id_,is_child=false){
	if(!entity_id || !template_code)
	  return;
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
                if (cn && cn.trim() != ""&&language()=='zh')
                    d["title"] = cn;
                d["lookup_entity"] = ent_look;
                list_fileds.push(d);
                break;
          }
        }
        app.view_data.columns=list_fileds;

};
function load(){
	    getUIElements();
        app=new Vue({
            el: "#app",
            data: {
              formLabelWidth:200,
              itemkey1 :0,
              itemkey2:0,
              lang:'en',
              readOnly:false,
              header_title_show:true,
              view_data:{
                 sel:[],
                 columns:[],
                 ui_fields:[]
              }
            },
            computed: {
            },
            methods: {

				cancel_action(row, index) {
					if (row.isSet == "undefined")
						row.isSet = false
					row.isEdit = false;
					edit_gl = false;
					row.isSet = false;
					app.view_data.sel = null;
					return row.isSet;
				},
				submit_data(row, index) {
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
            }
        });
        app.lang=language();
        GL_APP=app;
        var header_title_show = getUrlKey('header');
        if(GL_APP&&(!header_title_show||header_title_show=='1'))
          GL_APP.header_title_show=true
        else if(GL_APP)
          GL_APP.header_title_show=false
}
function next(){
   if (confirm("Next Step?")) {

    return true;
  }
 }
load();
