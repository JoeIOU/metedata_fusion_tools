Vue.component("entity-select", {
        template: '\
        <span style="align:middle;">\
        <el-tooltip :content="label" placement="top" :disabled="!(label&&width&&width>0&&label.length>0&&label.length*20>width-50)">\
            <el-input :id="id" :style="style" v-model="inputData" :width="width" :is_null="is_null" :entity="entity" :url="url" :size="size" :multi_select="multi_select" :placeholder="placeholder" readonly :disabled="disabled"\
             @change="change">\
               <el-button slot="append" icon="el-icon-connection" :size="size" :disabled="disabled" @click="click"></el-button>\
            </el-input>\
        </el-tooltip>\
					<el-dialog :title="title" :visible.sync="dialogFormVisible" class="dialogCompClass"  width="800px" append-to-body>\
			            <el-row>\
				            <el-col :span="11">\
                                <el-input  class="com_search_input" v-model="searchText" style="width:100%" :placeholder="hint_text"  @keyup.enter.native="search_click">\
                                    <el-button slot="append" icon="el-icon-search"  type="primary" :size="size" @click="search_click"></el-button>\
                                </el-input>\
                           </el-col>\
				            <el-col :span="13">\
                           </el-col>\
			           </el-row><br>\
			            <el-row>\
				            <el-col :span="11"><span v-if="lang==\'zh\'">待选列表<span v-if="multi_select==false">(单选)</span><span v-else>(多选)</span>：</span><span v-else>Tobe Selecting<span v-if="multi_select==false">(Single)</span><span v-else>(multiple)</span>:</span>\
                                <el-table size="mini" :data="table_data.data.slice((currentPage-1)*pagesize,currentPage*pagesize)"\
                                          highlight-current-row\
                                          v-loading="loading"\
                                          element-loading-text="loading..."\
                                          element-loading-spinner="el-icon-loading"\
                                          element-loading-background="rgba(220, 220, 220, 0.8)" height="300" border style="width:100%"\
                                          :header-cell-style="{\'background-color\': \'#dddddd\',\'font-size\':\'12px\'}"\
                                          :cell-style="cellStyle" \
                                          @selection-change="handleSelectionChange" :key="itemkey1">\
                                    <el-table-column width="45" type="index" label="No."></el-table-column>\
                                    <el-table-column width="43" type="selection" :selectable="checkSelect" align="center" >\
                                    </el-table-column>\
                                    <el-table-column v-for="(v,i) in table_data.columns" :prop="v.field" :label="v.title" :type="v.type"\
                                                 :width="v.width" :formatter="stateFormat">\
                                        <template slot-scope="scope">\
                                          <span v-if="scope.row[\'disabled\']&&scope.row[\'disabled\']==true">\
                                           {{scope.row[v.field]}}\
                                          </span>\
                                          <span v-else>\
                                            {{scope.row[v.field]}}\
                                            </span>\
                                        </template>\
                                    </el-table-column>\
                                </el-table>\
                                <div class="pagination">\
                                    <el-pagination small\
                                                   @size-change="handleSizeChange"\
                                                   @current-change="handleCurrentChange"\
                                                   :current-page="currentPage"\
                                                   :page-sizes="[10, 30, 50, 100]"\
                                                   :page-size="pagesize"\
                                                   layout="sizes,prev, pager, next"\
                                                   :total="table_data.data.length">\
                                    </el-pagination>\
                                </div>\
                           </el-col>\
				           <el-col :span="2">\
				               <div style="display: table-cell;height:300px;width:80px;text-align:center;vertical-align:middle;">\
                                <el-button  style="padding:10px 10px; width:40px" type="primary" @click="to_right">>></el-button><p/>\
                                <el-button  style="padding:10px 10px; width:40px" type="primary" @click="to_left"><<</el-button>\
                                </div>\
                           </el-col>\
                           <el-col :span="11"><span v-if="lang==\'zh\'">已选列表：</span><span v-else>(Selected)</span>\
                                    <el-table size="mini" :data="table_data.data_sel"\
                                              highlight-current-row\
                                              v-loading="loading"\
                                              element-loading-text="loading..."\
                                              element-loading-spinner="el-icon-loading"\
                                              element-loading-background="rgba(220, 220, 220, 0.8)" height="300" border style="width:100%"\
                                              :header-cell-style="{\'background-color\': \'#dddddd\',\'font-size\':\'12px\'}"\
                                              :cell-style="{\'font-size\':\'12px\'}" \
                                              @selection-change="handleSelectionChange1" :key="itemkey2">\
                                        <el-table-column width="45" type="index" label="No."></el-table-column>\
                                        <el-table-column width="43" type="selection" align="center" >\
                                        </el-table-column>\
                                        <el-table-column v-for="(v,i) in table_data.columns" :prop="v.field" :label="v.title" :type="v.type"\
                                                     :width="v.width" :formatter="stateFormat">\
                                            <template slot-scope="scope">\
                                                {{scope.row[v.field]}}\
                                            </template>\
                                        </el-table-column>\
                                    </el-table>\
                           </el-col>\
			           </el-row>\
                        <div slot="footer" class="dialog-footer">\
                            <el-button @click="cancel">\
                            <span v-if="lang==\'zh\'">取消</span>\
                            <span v-else>Cancel</span>\
                            </el-button>\
                            <el-button type="primary" @click="submit_data">\
                            <span v-if="lang==\'zh\'">确定</span>\
                            <span v-else>OK</span>\
                            </el-button>\
                        </div>\
                    </el-dialog>\
        </span>\
        ',
        props: {
            id: {
                type: [String, Number],
                default: '',
                desc: 'ID'
            },
            parent_data_id: {
                type: [String, Number],
                default: null,
                desc: '父类数据实例ID'
            },
            parent_entity_code: {
                type: String,
                default: null,
                desc: '父类实体code'
            },
            value: {
                type: [String, Number],
                default: '',
                desc: '值'
            },
            title: {
                type: String,
                default: '请选择...',
                desc: '对话框标题'
            },
            model: {
                type: [String, Number],
                default: '',
                desc: '绑定'
            },
            width: {
                type: [String, Number],
                default: '200',
                desc: '宽度'
            },
            style: {
                type: String,
                default: '',
                desc: '样式'
            },
            placeholder: {
                type: String,
                default: '',
                desc: '标识符'
            },
            entity: {
                type: String,
                default: '',
                desc: '元数据实体md_entity_code'
            },
            multi_select: {
                type: String,
                default: false,
                desc: '多选标识，true为多选'
            },
            is_null: {
                type: String,
                default: 'Y',
                desc: '是否为空，Y可以，N不可'
            },
            label: {
                type: String,
                default: "",
                desc: '标签'
            },
            url: {
                type: String,
                default: '',
                desc: '元数据实体md_entity_code'
            },
            size:{
              type: String,
              default: ()=>{ return null }
            },
            disabled: {
                type: String,
                default: false,
                desc: '失效标识'
            }
        },
        data() {
            return {
                focused: false,
                id:null,
                value:null,
                old_value:null,
                parent_data_id:null,
                parent_entity_code:null,
                model:"",
                placeholder:'',
                style:'',
                hint_text:"",
                disabled:false,
                size:"",
                width:"",
                searchText:"",
                entity:"",
                is_null:"Y",
                label:"",
                multi_select:false,
				itemkey1: null,
				itemkey2: null,
				lang:"en",
                url:"",
                selected_list:null,
                multipleSelection:[],
                multipleSelection1:[],
                table_data: {
					sel: null, //选中行
					columns: [],
					data: [],
					data_sel:[]
				},
				currentPage: 1, //默认显示页面为1
				pagesize: 10, //    每页的数据条数
				dialogFormVisible: false,
				title :'请选择...',
				loading: false,
            }
        },
        created(){
          this.style="width:"+this.width+"px;"+this.style;
          this.lang=language();
          this.model=this.value;
          //this.load_selected();
          if(this.label)
            this.model=this.label;
           if (this.lang=='zh')
            this.hint_text="请输入名称查询，前后缀加\'%\'为模糊查询"
           else
            this.hint_text="input search string,prefix or suffix with \'%\' is fuzzy search."

        },
        mounted(){
        },
        computed: {
           //data里的数据
            inputData: {
                get() {
                      val=this.value;
                      if(!val||val==''){//val为空，表示清空了，label的值,已选项也要清空。
                       this.label='';
                       this.multipleSelection1=[];
                       this.table_data.data_sel=[];
                       }
                      if(this.label&&this.label!='')
                        val=this.label;
                      if(this.old_value!=this.value)  {
                         this.load_selected();
                         this.old_value=this.value;
                      }
                      return val;
                },
                set(val){
                  this.value=val;
                }
            },
            output_value: {
                get() {
                      val=this.value;
                },
                set(){
                }
            },
        },
        methods: {
        //每页下拉显示数据
        handleSizeChange: function(size) {
            this.pagesize = size;
            /*console.log(this.pagesize) */
        },
        cellStyle(row,column,rowIndex,columnIndex){//根据报警级别显示颜色
            if(row.row&&row.row.disabled){
              return "color:#AAAAAA;font-size:12px;font-style:italic;"
            }else {
              return "font-size:12px"
            }
        },
        checkSelect (row,index) {
          let isChecked = true;
          if (row&&!row.disabled) { // 判断里面是否存在某个参数
            isChecked = true
          } else {
             isChecked = false
          }
          return isChecked
        },
        //点击第几页
        handleCurrentChange: function(currentPage) {
            this.currentPage = currentPage;
            /*console.log(this.currentPage) */
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
         change(val){
           //console.log("change:"+val+",value:"+this.value);
               this.$emit('change',{value:val,label:this.label})
         },
         cancel(){
           this.table_data.data_sel= JSONbig.parse(JSONbig.stringify(this.selected_list));
           this.dialogFormVisible=false;
         },
         submit_data(){
           ls=this.table_data.data_sel
           this.selected_list=JSONbig.parse(JSONbig.stringify(this.table_data.data_sel));
           msg="必填项，请至少选中一项才能提交。"
           if (this.lang!='zh')
            msg="required fields,please select at least one."
           if(!ls||ls.length==0&&this.is_null&&this.is_null=='N'){
            this.$message({
                type: 'warning',
                message: msg
            });
             return;
           }
          lb=null
          values=[]
          item=null;
          for (i in ls){
            item=ls[i]
            values.push(item.value) ;
            if (this.lang=='zh')
              labl=item.label
            else
              labl=item.label_en
            if(!labl&&labl.trim().length<=0)
              labl=item.value
             if(!lb)
               lb=labl
             else
               lb+="," +labl
          }

          this.label=lb;
          this.value=null;
          if(ls)
              if (ls.length==0)
                   this.value=null
              else if (ls.length==1&&item)
                   this.value=item.value
              else
                   this.value=values

           //this.$emit('change',this.value,this.label);
           this.$emit('change',{value:this.value,label:this.label})
          this.dialogFormVisible=false;
         },
         click(val){
           //console.log("click:"+val+",value:"+this.value);
           this.load_data(this.entity);
           this.searchText="";
           this.dialogFormVisible=true;
           this.loading=true;
           this.load_selected();
           this.$emit('click',this.value);
         },
         click_clear(val){
           this.value="";
           this.label="";
           this.multipleSelection1=null;
           this.table_data.data_sel=null;
           this.dialogFormVisible=false;
         },
         search_click(val){
           condition=null
           ss=this.searchText;
           if (!ss||ss.trim().length<=0)
               condition=null
           else {
                   if(ss.indexOf('%')<0)
                     ss=ss+'%'
                   if(this.lang=='zh')
                     condition={"label":ss}
                   else
                     condition={"label_en":ss}
               }
           this.load_data(this.entity,condition)
         },
         to_left(val){
           var select_list=this.multipleSelection1;
           msg="请至少从右列表选择一个需要清除的选项。"
           if (this.lang!='zh')
            msg="select one from right for clear."
           if(!select_list||select_list.length==0){
            this.$message({
                type: 'warning',
                message: msg
            });
             return;
           }
           ls=this.table_data.data_sel
           if(select_list)
           for (i in select_list){
             item=select_list[i]
             if(ls)
             for (j in ls){
               item1=ls[j]
               if (item1.value==item.value)
                 ls.splice(j,1);
             }
           }
           this.multipleSelection1=[];
           this.itemkey2=Math.random();
         },
         to_right(val){
           select_list=this.multipleSelection;
           select_list1=this.table_data.data_sel;
           msg="请从左边列表选择至少一个选项。"
           if (this.lang!='zh')
            msg="please select at least one from left."
           if(!select_list||select_list.length==0){
            this.$message({
                type: 'warning',
                message: msg
            });
             return;
           }
           if(!this.multi_select||this.multi_select=='false'){
             msg="单选，只能选择一个选项哦，请重新选择。"
             if (this.lang!='zh')
              msg="please select only one from left."
             if(select_list&&select_list.length>1){
                this.$message({
                    type: 'warning',
                    message: msg
                });
                 return;
             }

             msg="单选，新选择项，已覆盖之前已选项。"
             if (this.lang!='zh')
               msg="only one selected,and will cover the exist."
             if(select_list&&select_list.length==1&&select_list1&&select_list1.length>0){
                if(select_list[0].value!=select_list1[0].value)//值不相同，则如下提示
                    this.$message({
                        type: 'warning',
                        message: msg
                    });
                else{
                     msg="跟已选择的相同,请勿重复选择，请知。"
                     if (this.lang!='zh')
                       msg="the same as the selected."
                    this.$message({
                        type: 'warning',
                        message: msg
                    });
                }
             }

           }
           if((!this.multi_select||this.multi_select=='false')&&this.table_data.data_sel)
             this.table_data.data_sel=[]
            list_sel=this.table_data.data_sel;
            if(!list_sel)
              list_sel=[]
           if(select_list)
           for (i in select_list){
             item=select_list[i]
             is_exist=false;
             for (j in list_sel){
                   item1=list_sel[j]
                   if (item1&&item1.value==item.value){
                     is_exist=true;
                     break;
                   }
             }
             if(!is_exist){
               list_sel.push(item);
             }
           }
           this.table_data.data_sel=list_sel;
           this.itemkey2=Math.random();
         },
         load_data(code,whereCondition=null,selected=false){
            url_formated=null;
            if(!this.url)
             url_formated=url_root+"/services/findLookupByEntityCode?entity_code={0}&lookup_code={1}";
            else
             url_formated=this.url;

            var url_entity= url_formated.format(code,code);
            where=null
            if(whereCondition)
              where={"entity_code":code,"lookup_code":code,"where":whereCondition}
             else
              where={"entity_code":code,"lookup_code":code}

            if(this.parent_data_id&&this.parent_entity_code&&this.parent_entity_code.trim().length>0&&!selected){
              where["$PARENT_ENTITY_CODE"]=this.parent_entity_code;
              where["$parent_data_id"]=this.parent_data_id;
            }
            this.url= url_entity;
            //console.log("v-model:"+this.value+";Entity:"+this.entity+",url:"+this.url_entity);

            if(selected){
              this.table_data.data_sel=[];
              this.selected_list=[];
            }else{
              this.table_data.data=[];
            }
            if(!selected||(selected&&whereCondition))
                axios.post(url_entity,where)
                    .then(res => {
                        var data = res.data.data;
                        if(data){
                            this.title=data['entity_code']
                            if(this.lang=='zh'&&data['entity_name'])
                              this.title=data['entity_name']
                             else if(data['entity_name_en'])
                              this.title=data['entity_name_en']
                        }
                        var d = data.data;
                        var ddd = this.data_select_options_mapping(code, null, d,selected);
                        var res_data = res.data;
                        if (res_data && res_data.status >= 300) {
                            this.$message.warning({
                                type: 'warning',
                                message: res_data.message
                            });
                            return;
                        }
                        return d;
                    });
         },
         load_selected(){
           v=this.value;
           this.table_data.data_sel=[];
           this.selected_list=[];
           if (!v||v==""||v.length<=0){
             v='';
             this.label='';
             this.title='';
             return;
           }
           d=v;
           if(v){
            v=JSONbig.stringify(v)
            if (v && v.indexOf("[") != -1 && v.indexOf("]") != -1)
				d = eval("(" + v+ ")");
			}
           condition=null
           if (v||v.length>0){
              condition={"value":d}
           }

           this.load_data(this.entity,condition,true)
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
            this.multipleSelection = val;
            //console.log("---selected=", val);
         },
         handleSelectionChange1(val) {
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
            this.multipleSelection1 = val;
            //console.log("---selected=", val);
         },
        data_select_options_mapping(code, lookup_type, d,selected) {
            var re = [];
            if (!d){
                  if(selected){
                      this.table_data.data_sel=null;
                      this.selected_list=null;
                   }else{
                    this.table_data.data=null;
                   }
                 return null;
            }
            var len = d.length;
            lang=language();
            key1 = null;
            label1 = null;
            value1 = null;
            label_en1=null;
            desc=null;
            disabled1 = false;
            for (var i = 0; i < len; i++) {
                var item = d[i];
                if (code && code.toLowerCase() == 'lookup_classify' && lookup_type && lookup_type.trim() != "") {
                    key1 = "lookup_item_code";
                    label1 = "lookup_item_name";
                    label_en1 = 'lookup_item_name_en';
                    value1 = "lookup_item_code";
                    desc = '';
                    disabled1 = false;
                } else {
                    key1 = 'key';
                    label1 = 'label';
                    label_en1 = 'label_en';
                    value1 = 'value';
                    desc = 'desc';
                    disabled1 = item['disabled'];
                }
                if (item && item['active_flag'] == 'N')
                    disabled1 = true;
                new_label=item[label1];
                if(label_en1&&item[label_en1]&&lang=='en')
                  new_label=item[label_en1]
                if (!new_label || new_label ==null || new_label=="")
                  new_label=item[key1]

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
            var cols=[]
            labl=null;
            key_title=null;
            value_title=null;
            name_title=null;
            desc_title=null;
            if (lang=='zh'){
                labl=label1;
                key_title="ID/Code";
                value_title="值/编码";
                name_title="名称"
                desc_title="描述";
             }else{
                labl=label_en1
                key_title="ID/Code";
                value_title="Value/Code";
                name_title="Name"
                desc_title="Remark";
             }
            col={"field":key1,"title":key_title,"type":"varchar","width":""}
            cols.push(col)
            col={"field":labl,"title":name_title,"type":"varchar","width":""}
            cols.push(col)
            col={"field":value1,"title":value_title,"type":"varchar","width":""}
            cols.push(col)
            col={"field":desc,"title":desc_title,"type":"varchar","width":""}
            cols.push(col)
            if(selected){
                  //this.table_data.columns=cols;
                  this.table_data.data_sel=re;
                  if (re)
                     this.selected_list=JSONbig.parse(JSONbig.stringify(re));
                   else
                     this.selected_list=null;
                  lb=this.value;
                  if (re&&re.length>0){
                      lb=null;
                      for (i in re){
                        item=re[i]
                        //values.push(item.value) ;
                        if (this.lang=='zh')
                          labl=item.label
                        else
                          labl=item.label_en
                        if(!labl&&labl.trim().length<=0)
                          labl=item.value
                         if(!lb)
                           lb=labl
                         else
                           lb+="," +labl
                      }
                  }
                  this.label=lb;
                  this.itemkey2 = Math.random();
            }else{
                this.table_data.columns=cols;
                this.table_data.data=re;
                //this.itemkey1 = Math.random();
            }
            this.loading=false;
            return re;
        }
       }
    })
function number2string(dict) {
	if (dict)
		for (f in dict) {
			var v = dict[f];
			if (v && (typeof v == 'object' || typeof v == 'number'))
				dict[f] = v.toString();
		}
	return dict
}
