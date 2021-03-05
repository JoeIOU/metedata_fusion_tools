var url_root = "http://127.0.0.1:8888/md";
var url = url_root + "/services/findEntity?$_ENTITY_ID={0}";
var url_fields = url_root + "/services/findEntity?$_ENTITY_ID=30017&md_entity_id={0}";
var login_url = url_root + "/login?user_account=admin&user_name=Joe.Lin";
var app_gl = null;
var gl_field_type=null;
var label_gl=null;

/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function (exp, newStr) {
	return this.replace(new RegExp(exp, "gm"), newStr);
};

String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments;		//如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        //如果模板参数是对象
        data = args;
    }
    for (var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replace("{" + key + "}", value);
        }
}
    return result;
}
/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function(args) {
	var result = this;
	if (arguments.length < 1) {
		return result;
	}

	var data = arguments; // 如果模板参数是数组
	if (arguments.length == 1 && typeof (args) == "object") {
		// 如果模板参数是对象
		data = args;
	}
	for ( var key in data) {
		var value = data[key];
		if (undefined != value) {
			result = result.replaceAll("\\{" + key + "\\}", value);
		}
	}
	return result;
}

function axios_long_parse() {
    axios.defaults.transformResponse = [(data, headers) => {
        /*eslint no-param-reassign:0*/
        if (typeof data === 'string' && headers["content-type"] === "application/json") {
            try {
                data = JSONbig.parse(data);
            } catch (e) { /* Ignore */
                console.log(e);
            }
        }
        return data;
    }];
}

//long类型转换设置
axios_long_parse();
//cookie认证传递
axios.defaults.withCredentials = true;
//让ajax携带cookie
axios.get(login_url)
    .then(res => {
        var rs = JSON.stringify(res);
        console.log(rs);
    })

function queryEntity(app) {
    var data = null;
//    var result = "{0} 今年 {1} {2} {1}".format("张三", 20);
    var url1 = url.format("30015");
    axios.get(url1).then(res => {
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
//                    try{
//                      if(gl_field_type)
//                        type1=gl_field_type[key];
//                    } catch (e) {
//                        console.log(e);
//                    }
                    var dict0 = {
                        field: key, title: key,type:type1
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
            renderTable(dict);
        }
    )
}


function queryData() {
    var id = this.entity_name.value;
    var s=url.format(id);
    queryMetadata(s);
}

function renderTable(result) {
    if (!result) return;
    var cols = result.columns;
    //alert("getCols:"+JSON.stringify(cols));
    var data1 = result.datas;
    var field_types = result.field_types;
    var app = null;
    //主要内容
    if (app_gl) {
        app = app_gl;
        app.currentPage = 1;
    } else {
        app = new Vue({
            el: "#app",
            data: {
                master_user: {
                    sel: null,//选中行
                    columns: [],
                    //types:[],
                    data: [],
                    dialog_title:"Demo"
                },
                currentPage: 1, //默认显示页面为1
                pagesize: 10 ,//    每页的数据条数
                //dialogTableVisible: false,
                dialogFormVisible: false,
                formLabelWidth: '200px',
                timer_time:''
            },
            methods: {
                //每页下拉显示数据
                handleSizeChange: function (size) {
                    this.pagesize = size;
                    /*console.log(this.pagesize) */
                },
                //点击第几页
                handleCurrentChange: function (currentPage) {
                    this.currentPage = currentPage;
                    /*console.log(this.currentPage) */
                },
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
                    app.master_user.sel = JSON.parse(JSON.stringify(j));
                },
                openDialog(row, index){
                 app.master_user.sel = row;
                 if(gl_field_type){
                      var len=0;
                      if(app.master_user.columns){
                        len=app.master_user.columns.length;
                      }
                      for (var i=0;i<len;i++){
                          var d=app.master_user.columns[i];
                          d["type"]=gl_field_type[d.field];
                      }
                  }
                 //app.master_user.columns = app.master_user.columns; // 数据属性数据

                 alert("gl_field_type:"+JSON.stringify(gl_field_type)+"\r\n"+"app.master_user.columns:"+JSON.stringify(app.master_user.columns));
//                 alert();
                 if(label_gl)
                   app.master_user.dialog_title=label_gl;
                 app.dialogFormVisible = true;
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
                //修改
                pwdChange(row, index, cg) {
                    //点击修改 判断是否已经保存所有操作
                    for (let i of app.master_user.data) {
                        if (i.isSet && i.id != row.id) {
                            app.$message.warning("Please save what you are editing first.");
                            return false;
                        }
                    }
                    //是否是取消操作
                    if (!cg) {
                        if (!row.isSet){
                            row.isSet=false;
                            this.$confirm('你将要删除当前行数据, 是否确认?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                              }).then(() => {
                                //点击确定的操作(调用接口)
                                app.master_user.data.splice(index, 1);
                                app.$message('delete success,row='+(index+1));
                              }).catch(() => {
                                //点击取消的提示
                                return ;
                              });
                            return;
                        }
                        if (row.isSet== "undefined")
                          row.isSet = false
                        app.master_user.sel = row;
                        return row.isSet = !row.isSet;
                    }
                    //提交数据
                    if (row.isSet) {
                        //请求操作,按需修改下
                        (function () {
                            let data = JSON.parse(JSON.stringify(app.master_user.sel));
                            for (let k in data) row[k] = data[k];
                            app.$message({
                                type: 'success',
                                message: "Save success."
                            });
                            //然后这边重新读取表格数据
                            app.readMasterUser();
                            app.master_user.sel=null;
                            row.isSet = false;
                        })();
                    } else {
                        app.master_user.sel = JSON.parse(JSON.stringify(row));
                        if(gl_field_type){
                              app.master_user.types = gl_field_type; // 数据类型数据
                              var len=0;
                              if(app.master_user.columns){
                                len=app.master_user.columns.length;
                              }
                              for (var i=0;i<len;i++){
                                  var d=app.master_user.columns[i];
                                  d["type"]=gl_field_type[d.field];
                              }
                          }
                        row.isSet = true;
                        this.$set(app.master_user.data,index,row);
                    }
                }
            }
        });
        app_gl = app;
    }
    //alert("field_types:"+JSON.stringify(gl_field_type));
    app.master_user.columns = cols; // 数据属性数据
    app.master_user.types = gl_field_type; // 数据类型数据
    app.master_user.data = data1; // 查询业务数据
    app.$message('loading data ok');
}

function renderToolbar() {
    //主要内容
    var app = new Vue({
        el: "#app1",
        data() {
            return {
                options: [],
                select1: '',
                entity_name: "",
                entity_name1: "",
                date1:""
            }
        },
        methods: {
            handleClick(data) {
                const { value, label } = data;
                queryMetadata(url.format(value),value);
                let res = this.queryFields(url_fields.format(value));
                if (app_gl){
                  app_gl.master_user.dialog_title=label;
                  label_gl=label;
                  //alert(label);
                }else{
                 label_gl=label;
                }
            },
            async queryFields(url) {
                let res=await axios.get(url).then(res =>{
                    var dict1={};
                    var data = res.data.data;
                    if (data) {
                        var len = 0;
                        if (data)
                            len = data.length;
                        for (var i=0;i<len;i++){
                         var d=data[i];
                         dict1[d["md_fields_name"]]=d["md_fields_type"];
                        }
                    }
                    gl_field_type=dict1;
                    }
                );
            },
            handleCommand(command) {
                this.$message('click on item ' + command);
            }
        }
    });
    queryEntity(app);
}

renderToolbar();
