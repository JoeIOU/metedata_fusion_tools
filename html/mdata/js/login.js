    login_url= url_root + "/login";
    function getQueryVariable(variable)
    {
     var query = window.location.search.substring(1);
     var vars = query.split("&");
     for (var i=0;i<vars.length;i++) {
       var pair = vars[i].split("=");
       if(pair[0] == variable){return pair[1];}
     }
     return(false);
   }
   var app = new Vue({
    el: "#app1",
    data() {
      return {
        options: [],
        select1: '',
        entity_name: "",
        entity_name1: "",
        form: {
          username:"",
          password:""
        }
      }
    },
    methods: {
      handleClick(value) {
        queryMetadata(url.format(value),value);
        let res = this.queryFields(url_fields.format(value));
      },
      login(){
                //var instance=app.verify();
                //根据api接口获取token
                var url = login_url;
                axios.post(url, app.form).then(res => {
                      // console.log(res.data);
                      let data = res.data;
                      // 把一个用户存储到localStorage
                      data=JSONbig.parse(JSONbig.stringify(data));
                      localStorage.setItem('token', data.token);
                      localStorage.setItem('expire_time', data.expire_time);
                      var token = localStorage.getItem('token');
                      res.headers['Authorization'] = token;
                      this.$message.success('登录成功');
                     // 跳转到首页，这里使用vue-router实现
                     var href1=getQueryVariable('url');
                     if (!href1||href1=='null')
                       window.location.replace("index.html");
                     else{
                       href1=unescape(href1);
                       window.location.href=href1;
                         // window.open(href1,"_blank");
                         // window.close();
                       }

                     }).catch(error => {
                      // this.$message.error(error.status)
                      this.loading = false
                      this.loginBtn = "登录"
                      this.$message.error('账号或密码错误');
                      console.log(error)
                    })
                   },
                   reset(){
                     app.form.username='';
                     app.form.password='';
                   },
                   handleCommand(command) {
                    this.$message('click on item ' + command);
                  }
                }
              });
