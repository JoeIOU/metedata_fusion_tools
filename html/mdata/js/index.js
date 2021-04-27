//主要内容
var systemSetup_url="system_setup.html?tab={0}";
function load_data(){
    var app = new Vue({
      el: "#app1",
      data() {
        return {
          options: [],
          search_text:'',
          select1: '',
          user_name: "",
          account_number: "",
          activeIndex: '1',
          card_images:["https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=2652206393,3109958128&fm=26&gp=0.jpg",
          "https://www.edrawsoft.cn/images/flowchart/images/bianpinghuapptmuban.png",
          "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3028339432,10020054&fm=26&gp=0.jpg",
          "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2230719646,832164230&fm=26&gp=0.jpg"],
          card_title:['元数据管理','业务配置管理','租户管理','权限管理'],
          currentDate: new Date(),
          defaultProps: {
            children: 'children',
            label: 'label'
          }
        }
      },
      methods: {
        login(){
          var url=url_root+"/services/user";
          axios.get(url)
          .then(res => {
            var re=JSONbig.parse(JSONbig.stringify(res));
            var data=re.data.data;
            app.user_name=data['user_name'];
            app.account_number=data['account_number'];
            console.log(res);
          });
        },
        handleSelect(key, keyPath) {
            var tab="";
            switch (key) {
                case 'metadata':
                    tab="metadata";
                    break;
                case 'chart':
                    tab="chart";
                    break;
                case 'users':
                    tab="users";
                    break;
                case 'tenant':
                    tab="tenant";
                    break;
                case 'group':
                    tab="group";
                    break;
                case '':
                    tab="";
                    break;
                case '':
                    tab="";
                    break;
                case 'login':
                    tab="";
                    break;
                case 'logout':
                    tab="";
                    break;
                case '':
                    tab="";
                    break;
                default:
                    tab=key;
            }
             url=systemSetup_url.format(tab);

            switch (key) {
                case 'login':
                    tab="";
                    url="login.html"
                    break;
                case 'logout':
                    tab="";
                    url="logout.html"
                    break;
                case 'business_maintain':
                    tab="";
                    url="entity_edit.html?header=1"
                    break;
                case '':
                    tab="";
                    break;
            }
             window.open(url,tab) ;// 新窗口打开外链接
             console.log(key, keyPath);
        },
        handleOpen(){
        },
        handleClose (){
        },
        card_handle(index){
              var tab="";
             if (index==0){
               tab='metadata';
             }else if(index==2){
               tab='tenant';
             }else if(index==3){
               tab='privilege';
             }else if(index==1){
               tab='process';
             }else{

             };
             url=systemSetup_url.format(tab);
             window.open(url,tab) ;// 新窗口打开外链接
       },
       handleNodeClick(data) {
        console.log(data);
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
        if (command=='logout')
         window.location.href='login.html';
     }
        }
      });
    app.login();
 }
 load_data();
