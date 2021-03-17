//主要内容
var url_root = "http://127.0.0.1:8888/md";
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
			}
			catch (e) {
				/* Ignore */
				console.log(e);
			}
		}
		return data;
	}
	];
}
//long类型转换设置
axios_long_parse();
//cookie认证传递
axios.defaults.withCredentials = true;
// 首先对拦截器的请求进行设置，并在方法中return config，此处为固定格式
axios.interceptors.request.use(config => {
  // 表示在配置中的设置头消息的字段Authorization为从本地获取的token值
    var AUTH_TOKEN=localStorage.getItem('token');
    if (!AUTH_TOKEN||AUTH_TOKEN=='null'){
           cur_url=escape(window.location.href);
           window.location.replace("login.html?"+'url='+cur_url);
           return
    }
    // 在实例已创建后修改默认值
    var basicAuth = 'Basic ' + btoa(AUTH_TOKEN+":");
    config.headers.Authorization = basicAuth;
    axios.defaults.headers.common['Authorization'] = basicAuth;
  return config
});

Vue.prototype.$http = axios;
