//主要内容
var url_root = "http://localhost:8888/md";

/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function(exp, newStr) {
	return this.replace(new RegExp(exp, "gm"), newStr);
};

String.prototype.format = function(args) {
	var result = this;
	if (arguments.length < 1) {
		return result;
	}

	var data = arguments; //如果模板参数是数组
	if (arguments.length == 1 && typeof(args) == "object") {
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
	if (arguments.length == 1 && typeof(args) == "object") {
		// 如果模板参数是对象
		data = args;
	}
	for (var key in data) {
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
			} catch (e) {
				/* Ignore */
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
// 首先对拦截器的请求进行设置，并在方法中return config，此处为固定格式
axios.interceptors.request.use(config => {
	if (window.location.href.indexOf("/login.html") >= 0)
		return config
	// 表示在配置中的设置头消息的字段Authorization为从本地获取的token值
	var AUTH_TOKEN = localStorage.getItem('token');
	var expire_time = localStorage.getItem('expire_time');
	var x = new Date()
	var utc_timestamp = x.getTime() + x.getTimezoneOffset() * 60 * 1000;
	if (!AUTH_TOKEN || !expire_time || utc_timestamp > expire_time) {
		cur_url = escape(window.location.href);
		window.location.replace("login.html?" + 'url=' + cur_url);
		return config
	}
	// 在实例已创建后修改默认值
	var basicAuth = 'Basic ' + btoa(AUTH_TOKEN + ":");
	config.headers.Authorization = basicAuth;
	axios.defaults.headers.common['Authorization'] = basicAuth;
	return config
});

function login_redirect(config) {
	cur_url = escape(window.location.href);
	window.location.replace("login.html?" + 'url=' + cur_url);
	return config
}
//替换指定传入参数的值,paramName为参数,replaceWith为新值
function replaceParamVal(paramName, replaceWith) {
	var oUrl = this.location.href.toString();
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
	//    this.location = nUrl;
	//    window.location.href=nUrl;
	history.replaceState(null, null, nUrl);
}

function getUrlKey(name) {
	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)')
		.exec(location.href) || [, ""])[1].replace(/\+/g, '%20')) || null
}

Vue.component("currency-input", {
        template: '\
            <div class="el-input el-input--small">\
                <input class="el-input__inner"\
                    v-bind:id="id"\
                    v-bind:decimal="decimal"\
                    v-bind:maxlength="maxlength"\
                    v-bind:disabled="disabled"\
                    v-bind:value="formatValue"\
                    ref="input"\
                    v-on:input="updatevalue($event.target.value)"\
                    v-on:blur="onBlur"\
                    v-on:change="onChange"\
                    v-on:focus="selectAll"/>\
            </div>\
        ',
        props: {
            value: {
                type: [String, Number],
                default: '',
                desc: '数值'
            },
            id: {
                type: [String, Number],
                default: '',
                desc: 'id'
            },
            symbol: {
                type: String,
                default: '',
                desc: '货币标识符'
            },
            disabled: {
                type: String,
                default: '',
                desc: '失效标识'
            },
            decimal: {
                type: Number,
                default: 2,
                desc: '小数位'
            },
            maxlength: {
                type: Number,
                default: 20,
                desc: '最大长度'
            }
        },
        data() {
            return {
                focused: false,
            }
        },
        created(){
          console.log("ID:"+this.id+";Value:"+this.value);
        },
        computed: {
            formatValue() {
                if(!this.value)
                     return null;
                if (this.focused) {
                    return accounting.unformat(this.value);
                } else {
                     return accounting.formatMoney(this.value, this.symbol, this.decimal);
                }
            }
        },
        methods: {
            updatevalue(value) {
                var v=value;
                v=this.handle_input(value);
                var formatvalue = accounting.unformat(v);
                this.$emit("input", formatvalue)
            },
            handle_input(value){
                if(!value)
                  return;
                var new_value=value;
                var len=value.toString().replace("-","").replace(".","").length;
                var idx=value.toString().indexOf(".");
                var _idx=value.toString().indexOf("-");
                this.maxlength=parseInt(this.maxlength);
                if(!this.maxlength||this.maxlength<=0)
                  this.maxlength=20;
                if(this.maxlength && len>this.maxlength){
                  pdx=0;
                  if(_idx>=0)
                   pdx=1;
                  sValue= value.toString();
                  if(idx>=0&&idx<this.maxlength)
                     new_value=sValue.slice(0,this.maxlength+pdx+1);
                  else
                     new_value=sValue.slice(0,this.maxlength+pdx);
                }
                if(new_value)
                 new_value=parseFloat(new_value);
                if(this.decimal==0)
                  new_value=parseInt(new_value);
                //this.isEdit=false;
                return new_value;

            },
            onBlur() {
                this.focused = false;
                this.$emit("blur");
                this.dispatch("ElFormItem", "el.form.blur", [this.value]);
            },
            onChange($event) {
                this.$emit('change', $event.target.checked)
            },
            selectAll(event) {
                this.focused = true;
                //this.isEdit=true;
                setTimeout(() => {
                    //event.target.select()
                }, 0)
            },
            dispatch(componentName, eventName, params) {
              var parent = this.$parent || this.$root;
              var name = parent.$options.componentName;
              while (parent && (!name || name !== componentName)) {
                parent = parent.$parent;
                if (parent) {
                  name = parent.$options.componentName;
                }
              }
              if (parent) {
                parent.$emit.apply(parent, [eventName].concat(params));
              }
            }
        },
    })
function language(){
    var lang=null;
　　var type = navigator.appName;
　　if (type == "Netscape"){
    　　 lang = navigator.language;//获取浏览器配置语言，支持非IE浏览器
　　}else{
    　　 lang = navigator.userLanguage;//获取浏览器配置语言，支持IE5+ == navigator.systemLanguage
　　};
　　 lang = lang.substr(0, 2);//获取浏览器配置语言前两位
　　if (lang == "zh"){
   　　 lang="zh"
　　    //window.location.replace('url');//中文编码时打开链接
　　}else if (lang == "en"){
   　　 lang="en"
　　}else{//其他语言编码时打开以下链接
   　　 lang="en"
   }
   return lang;
  }

Vue.prototype.$http = axios;
