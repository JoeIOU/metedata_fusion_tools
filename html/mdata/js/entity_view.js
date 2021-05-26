var entity_info_url = url_root + "/services/findUIEntity?$_ENTITY_ID={0}&ui_template_code={1}";
var ui_template_info_url = url_root + "/services/queryUIEntities?ui_template_code={0}";
var ui_fields_url = url_root + "/services/queryFieldsByCodeOrID";
var url_ui_entity_edit="ui_entity_edit.html?entity_id={0}&parent_entity_id={1}&parent_data_id={3}&template_code={4}&header=0&readOnly={5}"
var url_ui_entity_table="ui_entity_table.html?entity_id={0}&parent_entity_id={1}&parent_data_id={3}&template_code={4}&header=0&readOnly={5}"
var GL_APP = null;
var gl_fields_list=null;

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
                        node.url=url;
                    }
                }
                mmm={}
                mmm.map=map;
                mmm.data_tree=tree
                mmm.data=list
                if(GL_APP){
                 GL_APP.view_data.data=list
                 GL_APP.view_data.data_tree=tree
                 GL_APP.view_data.map=map
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
			if(GL_APP&&data)
			GL_APP.view_data.sel=data[0];
			var cols = [];
			var dict = {
				columns: [],
				datas: [],
				size: 0
			};

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
//					if (ent_look && ent_look != "")
//						get_entity_info_by_code(ent_look, d, f["lookup_type"]);
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
              lang:'en',
              title:'',
              view_data:{
               sel:[],
               columns:[],
               data:[],
               map:null,
               data_tree:[]
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
                            map=app.view_data.map
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
          app.view_data.data=entity_tree.data;
          app.view_data.map=entity_tree.map;
          app.view_data.data_tree=entity_tree.data_tree;
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
