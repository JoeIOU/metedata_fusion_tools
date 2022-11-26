var root_url_graph = "http://localhost:8080/md/graph";
var entitySetup_url = "entity_setup1.html?entity_id={0}&isReadonly=1";
var entity_info_list = url_root + "/services/queryEntityList";
var gl_app = null;
var gl_data = null;

function relation_show(label, data) {
	label = '#' + label;
	var neo4jd3 = new Neo4jd3(label, {
		highlight: [{
			class: 'Entity',
			property: 'name',
			value: 'modelShow'
		}],
		icons: {
			'zoomFit': 'arrows-alt',
			'zoomIn': 'search-plus',
			'zoomOut': 'search-minus'
		},
		images: {},
		minCollision: 60,
		//neo4jDataUrl: data,
		neo4jData: data,
		nodeRadius: 25,
		onNodeDoubleClick: function(node) {
			var id = node.properties._id;
			var url = entitySetup_url
			url = url.format(id);
			window.open(url, 'metedata');
		},
		onRelationshipDoubleClick: function(relationship) {
			console.log('double click on relationship: ' + JSON.stringify(relationship));
		},
		zoomFit: true
	});
}

function showModel(app, title, flag) {
	axios.get(root_url_graph + "/relation/" + encodeURIComponent(title) + "/" + encodeURIComponent(flag))
		.then(res => {
			var data = []
			if (res.data)
				data = res.data;
			rel_list(app, data);
			if (app && app.currentRow)
				showGraph(app.currentRow.entity_name, app.radio);
			return false;
		})
}

function rel_list(app, data) {
	list = []
	if (data) {
		app.title = data.title;
		let data1 = data.cast;
		if (data1) {
			let len = data1.length;
			d = data1[0];
			for (var i = 0; i < len; i++) {
				var item = data1[i];
				var set = {
					rel_id: item["relation_id"],
					rel_type: item["relation_type"],
					rel_name: item["name"],
					father_name: item["from_entity_name"],
					father_field: item["from_fields_name"],
					child_name: item["to_entity_name"],
					child_field: item["to_fields_name"],
					rel_desc: item["relation_desc"]
				}
				list.push(set);
			}
		}
	}
	app.rel_table.table_datas = list;
}

function showGraph(title, flag) {
	axios.get(root_url_graph + "/graph/" + encodeURIComponent(title) + "/" + encodeURIComponent(flag))
		.then(res => {
			if (!res.data) return;
			var data = res.data;
			var label = 'neo4jd3';
			gl_data = data;
			relation_show(label, data);
		})
	return false;
}

function highlight_row(row) {
	row.addClass('success') //为选中项添加高亮
		.siblings()
		.removeClass('success') //去除其他项的高亮形式
		.end();
}

function entity_data_format(data) {
	if (!data)
		return []
	//    var len =data.length;
	var list = data;
	return list;

}

function search(app, str) {
	axios.get(root_url_graph + "/search?q=" + encodeURIComponent(str))
		.then(res => {
			app.entity_table.table_datas = res.data;
			if (res.data) {
				app.handleCurrentChange(res.data[0]);
				app.$refs.interfaceTable.setCurrentRow(res.data[0])
			}
		})
	return false;
}

function search_rel(app) {
	axios.get(root_url_graph + "/search_shortest_path?q=" + encodeURIComponent(app.from_text) + "&to=" + encodeURIComponent(app.to_text) + "&flag=" + encodeURIComponent(app.radio))
		.then(res => {
			var data = res.data;
			if (!data || data.length == 0) return;
			var label = 'neo4jd3';
			gl_data = data;
			relation_show(label, data);
			app.select_entity_model = app.from_text + "::" + app.to_text;
		})
	return false;
}

function queryEntity(app) {
	var data = null;
	axios.get(entity_info_list)
		.then(res => {
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
			app.options1 = options;
		})
}

function data_load() {
	var app = new Vue({
		el: "#app",
		data: {
			radio: 0,
			title: "Details",
			search_text: "",
			from_text: "",
			to_text: "",
			currentRow: null,
			select_entity: null,
			select_entity_model: null,
			dialogTableVisible: true,
			rel_table: {
				table_columns: [{
						field: "rel_id",
						title: "实体关系ID",
						width: 100
					},
					{
						field: "rel_type",
						title: "实体关系类型"
					},
					{
						field: "rel_name",
						title: "实体关系名称"
					},
					{
						field: "father_name",
						title: "父实体名称"
					},
					{
						field: "father_field",
						title: "父实体属性"
					},
					{
						field: "child_name",
						title: "子实体名称"
					},
					{
						field: "child_field",
						title: "子实体属性"
					},
					{
						field: "rel_desc",
						title: "实体关系描述"
					}
				],
				table_datas: [{
					rel_id: '',
					rel_type: '',
					rel_name: '',
					father_name: '',
					father_field: '',
					child_name: "",
					child_field: "",
					rel_desc: ""
				}]
			},
			entity_table: {
				table_columns: [{
						field: "entity_id",
						title: "实体ID"
					},
					{
						field: "schema",
						title: "实体分类"
					},
					{
						field: "entity_code",
						title: "实体编码"
					},
					{
						field: "entity_name",
						title: "实体名称"
					},
					{
						field: "entity_desc",
						title: "实体描述",
						width: 100
					}
				],
				table_datas: [{
					entity_id: '',
					schema: '',
					entity_code: '',
					entity_name: '',
					entity_desc: ''
				}]
			},
			options: [],
			options1: []
		},
		methods: {
			handleCurrentChange(val) {
				app.currentRow = val;
				if (val && val.entity_name){
					app.select_entity = val.entity_name;
				    app.select_entity_model = val.entity_name;
				    showModel(app, val.entity_name, app.radio);
				}
			},
			redioChange(val) {
				showModel(app, app.currentRow.entity_name, app.radio);
			},
			search() {
				var str = app.search_text;
				search(app, str);
			},
			hadleRelShortest() {
				search_rel(app);
			},
			showMax() {
				if (gl_data) {
					app.dialogTableVisible = true;
					var label = 'neo4jd31';
					relation_show(label, gl_data);
				}
			}
		}
	});
	gl_app = app;
	app.radio = 0;
	app.dialogTableVisible = false;
	queryEntity(app);
	//app.$message('loading data ok');
}
data_load();
