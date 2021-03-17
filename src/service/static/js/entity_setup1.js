var url = url_root + "/services/findEntitySetup?$_ENTITY_ID={0}";
var login_url = url_root + "/login?user_account=test1&user_name=Joe.Lin";
var url_entity = url_root + "/services/queryEntityByCodeOrID?$_ENTITY_CODE=md_entities";
var url_field = url_root + "/services/queryFieldsByCodeOrID?$_ENTITY_CODE=md_fields";
var app_gl = null;
var label_gl=null;
var edit_gl=false;
var GL_ENTITY_ID=null;
var GL_FIELD_ID=null;
var GL_TENANT_ID=null;

axios.get(url_entity)
.then(res => {
	var rs = JSONbig.stringify(res);
	var data=res.data.data[0];
	var entity_id=data['md_entity_id'];
	GL_ENTITY_ID=entity_id;
	//console.log(rs);
});
axios.get(url_field)
.then(res => {
	var rs = JSONbig.stringify(res);
	var data=res.data.data[0];
	var entity_id=data['md_entity_id'];
	GL_FIELD_ID=entity_id;
	//console.log(rs);
});
function queryMetadata(url,id) {
	axios.get(url).then(res => {
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
			var row=data[0];
			for (var key in row) {
				var type1=null;
				var vis=true;
				var read_only=true;
				var width1=null;
				var title_str=key;
				if (key.indexOf("md_") != -1)
					title_str=key.substring(3);
				if (key==='md_entity_id' ||key==='md_entity_code'||key==='md_entity_name'||key==='md_tables_id'||key==='md_columns_id'||key==='md_entity_name_en'||key==='md_entity_desc')
					vis=false
				if(key==='md_fields_id' ||key==='md_fields_length'||key==='md_decimals_length'||key==='md_columns_length'||key==='md_dec_length')
					type1='int'
				else if(key==='' ||key==='')
					type1='varchar'
				else
					type1='varchar'
				if(key==='md_fields_type'||key==='md_fields_name' ||key==='md_fields_name_en'||key==='md_fields_length'||key==='md_decimals_length'
					||key==='md_entity_name_en' ||key==='md_entity_desc'||key==='md_fields_desc'||key==='lookup_flag'||key==='default_value'
					||key=="is_null"||key=="is_indexed"||key=="is_unique"||key=="public_flag"){
					read_only=false;
			}
			if(key==='md_fields_name'||key==='md_fields_name_en'||key==='md_fields_type'||key==='md_entity_name_en' ||key==='md_entity_desc'||key==='md_fields_desc')
				width1=150;
			var dict0 = {
				field: key, title: title_str,type:type1,width:width1,visible:vis,readonly:read_only
			}
			cols[i] = dict0;
			i++;
		}
		for (var i=0;i<len;i++){
			var d=data[i];
				//赋值id为第一个序号的值，以便后续编辑，一般是key id的值，标识行的唯一性。
				d["id"]=i+1;
			}
			dict = {
				columns: cols,
				datas: data,
				size: len
			};
		}
		renderTable(dict,id);
	}
	)
}
function getUrlKey (name) {
	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.href) || [, ""])[1].replace(/\+/g, '%20')) || null
}
function queryData() {
	let id = getUrlKey('entity_id');
	if (!id)
	   id=-1
	var s=url.format(id);
	queryMetadata(s,id);
}
function renderTable(result,id) {
	if (!result) return;
	var cols = result.columns;
	var data1 = result.datas;
	var field_types = result.field_types;
	var gl_entity_id=id;
	var app = null;
	//主要内容
	if (app_gl) {
		app = app_gl;
		app.currentPage = 1;
	}
	else {
		app = new Vue({
			el: "#app",
			data: {
				master_user: {
					sel: null,//选中行
					columns: [],
					data: []
				},
				options: [{
					value: 'int',
					label: '整数型'
				}, {
					value: 'bigint',
					label: '长整型'
				}, {
					value: 'decimal',
					label: '货币型'
				}, {
					value: 'char',
					label: '字符型'
				}, {
					value: 'varchar',
					label: '文本型'
				}, {
					value: 'timestamp',
					label: '日期型'
				}],
				test11: true,
				$_ENTITY_ID:gl_entity_id
			},
			methods: {
				//添加账号
				addUser() {
					for (let i of app.master_user.data) {
						if (i.isSet) return app.$message.warning("Please save what you are editing first.");
					}
					let j = {
						id: 0,
						"type": "",
						"addport": "",
						"isSet": true,
						"_temporary": true
					};
					app.master_user.data.push(j);
					app.master_user.sel = JSONbig.parse(JSONbig.stringify(j));
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
				onchange(field_name,row, index){
					row.isEdit=true;
					edit_gl=true;
					row.isSet=true;
					var id=field_name+index;
					var dom=document.getElementById(id);
                     //dom.style.backgroundColor="#FFEE00";
                     dom.style.border = '1px solid #33FF00';
                 },
                 setStyle(row,index,del_flag){
                 	for (item in row){
                 		var id=item+index;
                 		var dom=document.getElementById(id);
                        if (dom && del_flag){
                            if (row.isDel)
                                dom.style.textDecoration = 'none'
                            else
                                dom.style.textDecoration = 'line-through'
                        }else if(dom && !dom.hasAttribute("disabled")){
                            dom.value='';
                            dom.style.border = null;
                            row.isEdit=false;
                        }
                 	}
                 	if (del_flag)
                 		if (row.isDel==null)
                 			row.isDel=true
                 		else
                 			row.isDel=!row.isDel;
                 	},
				//修改
				pwdChange(row, index, cg) {
					//是否是取消操作
					if (!cg) {
						if (row.md_fields_id){
							//delete
							app.setStyle(row,index,true);
                            //app.master_user.data.splice(index, 1);
                            //row.isEdit=false;
                            return;
                        }else{
                            //cancel
                            if (row.isSet== "undefined")
                            	row.isSet = false
                            //app.master_user.sel =row;
                            app.setStyle(row,index);
                            return row.isSet = !row.isSet;
                        }
                    }else {
						//load data
						//app.master_user.sel = JSONbig.parse(JSONbig.stringify(row));
						row.isSet = true;
						this.$set(app.master_user.data,index,row);
					}
				},
				close(){
					if(edit_gl){
						this.$confirm('你有编辑内容未保存，关闭将会丢失, 是否确认关闭?', '警告', {
							confirmButtonText: '确定',
							cancelButtonText: '取消',
							type: 'warning'
						}).then(() => {
                                //点击确定的操作(调用接口)
                                window.close();
                            }).catch(() => {
                                //点击取消的提示
                                return ;
                            });
                            return;
                        }else
                        window.close();
                    },
                    insertData(data) {
                         if(!data)
                           return null;
                         return axios.post(url_root+'/services/insertEntity', data);
                    },
                    updateData(data) {
                         if(!data)
                           return null;
                         return axios.post(url_root+'/services/updateEntityBatch',data);
                    },
                    set_unfill_fields(index,item){
                          var  is_not_ok=false;
                          if (item.md_fields_name==null||item.md_fields_name=='' ){
                            var id="md_fields_name"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                          }
                          if (item.md_fields_name_en==null||item.md_fields_name_en==''){
                            var id="md_fields_name_en"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                          }
                          if (item.md_fields_type==null||item.md_fields_type==''){
                            var id="md_fields_type"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                          }
                          if (item.is_null==null||item.is_null==''){
                            var id="is_null"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                          }
                          if (item.lookup_flag==null||item.lookup_flag==''){
                            var id="lookup_flag"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                          }
                          if (item.public_flag==null||item.public_flag==''){
                            var id="public_flag"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                          }
                          if ((item.md_fields_length==null||item.md_fields_length==''||item.md_fields_length<1) && !(item.md_fields_type=='timestamp' ||item.md_fields_type=='datetime'||item.md_fields_type=='date')){
                            var id="md_fields_length"+index;
                            var dom=document.getElementById(id);
                            dom.style.border = '1px solid #FF8800';
                            is_not_ok=true;
                            }
                          return is_not_ok;
                    },
                    submitData(){
                    	let data=app.master_user.data ;
                        let data_add_field=null;
                        let data_upd_field=null;
                        let data_upd_entity=null;
                    	if (data){
                    	    var update_data_list=[];
                    	    var update_where_list=[];
                    	    var insert_data_list=[];
                    	    var warning_data_list=[];
                    		let len=data.length;
                    		var is_not_ok=null;
                    		for (var i=0;i<len;i++){
                    			var item=data[i];
                    			var new_item= {"md_fields_name":item.md_fields_name,"md_fields_name_en":item.md_fields_name_en,
                    			  "md_fields_type":item.md_fields_type,"md_fields_desc":item.md_fields_desc,"md_fields_length":item.md_fields_length,
                    			  "md_decimals_length":item.md_decimals_length,"lookup_flag":item.lookup_flag,"default_value":item.default_value,
                    			  "is_null":item.is_null,"is_indexed":item.is_indexed,"is_unique":item.is_unique,"public_flag":item.public_flag,'active_flag':'Y'};
                    			if(item&&item.isEdit&&item.md_fields_id){//修改
                    			  //delete new_item.md_fields_id;
                    			  update_data_list.push(new_item);
                    			  update_where_list.push({"md_fields_id":item.md_fields_id});
                    			  is_not_ok=app.set_unfill_fields(i,new_item);
                    			}else if(item&&item.isEdit){//新增
                    			  if (!GL_TENANT_ID)
                    			   continue;
                    			  new_item.tenant_id=GL_TENANT_ID;
                    			  new_item.md_entity_id=item.md_entity_id;
                    			  new_item.md_columns_id=item.md_columns_id;
                    			  insert_data_list.push(new_item);
                    			  is_not_ok=app.set_unfill_fields(i,new_item);
                    			}else if(item&&item.isDel&&item.md_fields_id){//删除
                    			  new_item.active_flag='N';
                    			  update_data_list.push(new_item);
                    			  update_where_list.push({"md_fields_id":item.md_fields_id});
                    			  is_not_ok=app.set_unfill_fields(i,new_item);
                    			}
                            }
                            if(is_not_ok){
                                  app.$message({type: 'warning',message: "some fields should be null,please fill in again."});
                                  return;
                             }
                             data_upd_field={"$_ENTITY_ID":GL_FIELD_ID,"data":update_data_list,"where":update_where_list};
                             data_add_field={"$_ENTITY_ID":GL_FIELD_ID,"data":insert_data_list};
                            let sel_data = app.master_user.sel;
                             if(sel_data&&sel_data.isEdit){
                                var new_entity={"md_entity_code":sel_data.md_entity_code,"md_entity_name":sel_data.md_entity_name,"md_entity_desc":sel_data.md_entity_desc,"md_entity_name_en":sel_data.md_entity_name_en}
                                var where_dict={"md_entity_id":sel_data.md_entity_id};
                                data_upd_entity={"$_ENTITY_ID":GL_ENTITY_ID,"data":[new_entity],"where":[where_dict]};
                             }else
                                data_upd_entity=null;
                            //console.log("updateFields=="+JSONbig.stringify(data_upd_field));
                            //console.log("insertFields=="+JSONbig.stringify(data_add_field));
                            //console.log("updateEntity=="+JSONbig.stringify(data_upd_entity));
                            axios.all([app.insertData(data_add_field), app.updateData(data_upd_field), app.updateData(data_upd_entity)])
                              .then(axios.spread(function (acct, perms) {
                                  // 两个请求现在都执行完成
                                  app.$message({type: 'success',message: "Save success."});
                                  //row.isSet = false;
                                  edit_gl=false;
                                  console.log(acct,perms);
                                  window.location.reload();
                              }));
                      }
                  }

              }
          });
app_gl = app;
}
app.master_user.columns = cols;
	// 数据属性数据
	app.master_user.data = data1;
	let d=null;
	let len=data1.length;
	if (data1){
		d=data1[0];
		for (var i=0;i<len;i++){
			var item=data1[i];
			if (item['md_entity_id']!=null){
				d=item;
				break;
			}
		}
	}
	// 查询业务数据
	if (data1 && d)
		app.master_user.sel = JSONbig.parse(JSONbig.stringify(d));
	app.$message('loading data ok');
}
queryData();
