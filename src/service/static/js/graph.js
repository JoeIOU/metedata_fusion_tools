function relation_show(data){
                var neo4jd3 = new Neo4jd3('#neo4jd3', {
                    highlight: [
                        {
                            class: 'Entity',
                            property: 'name',
                            value: 'neo4jd3'
                        }, {
                            class: 'Model',
                            property: 'name',
                            value: 'model'
                        }
                    ],
                    icons: {
                        'zoomFit': 'arrows-alt',
                        'zoomIn': 'search-plus',
                        'zoomOut': 'search-minus'
                    },
                    images: {
                    },
                    minCollision: 60,
<!--                    neo4jDataUrl: data,-->
                    neo4jData: data,
                    nodeRadius: 25,
                    onNodeDoubleClick: function(node) {
                        switch(node.id) {
                            case '25':
                                // Google
                                window.open(node.properties.url, '_blank');
                                break;
                            default:
                                var maxNodes = 5,
                                    data = neo4jd3.randomD3Data(node, maxNodes);
                                neo4jd3.updateWithD3Data(data);
                                break;
                        }
                    },
                    onRelationshipDoubleClick: function(relationship) {
                        console.log('double click on relationship: ' + JSON.stringify(relationship));
                    },
                    zoomFit: true
                });
            }

        function showModel(title,flag) {
            $.get("/relation/" + encodeURIComponent(title)+"/"+ encodeURIComponent(flag),
                    function (data) {
                        if (!data) return;
                        rel_list(data);
                    }, "json");
            return false;
        }
        function rel_list(data){
                        $("#title").text(data.title);
                        $("#poster").attr("src","/static/imgs/001.png");
                        const $list = $("#crew").empty();
                        data.cast.forEach(function (cast) {
                        if (cast.REL_TABLE){
                            $list.append($("<li>--["+cast.REL_TYPE+"] --<b>" + cast.REL_TABLE + "</b> ("+cast.REL_PK+" : "+cast.REL_FK+ ")</li>"));
                            }else{
                            $list.append($("<li>" + "Nothing"+ "</li>"));
                            }
                        });
        }
        function showGraph(title,flag) {
            $.get("/graph/" + encodeURIComponent(title)+"/"+ encodeURIComponent(flag),
                    function (data) {
                        if (!data) return;
                        relation_show(data);
                    }, "json");
            return false;
        }
        function highlight_row(row){
                row.addClass('success')      //为选中项添加高亮
                .siblings().removeClass('success')//去除其他项的高亮形式
                .end();
        }
        function search() {
            var query=$("#search").find("input[name=search]").val();
            var flag_input=$('input[name="flag_input"]:checked').val();
            $.get("/search?q=" + encodeURIComponent(query),
                    function (data) {
                        const t = $("table#results tbody").empty();
                        if (!data || data.length == 0) return;
                        data.forEach(function (movie) {
                            $("<tr><td class='movie'>" + movie.title + "</td><td>" + movie.released + "</td><td>" + movie.name + "</td></tr>").appendTo(t)
                                    .click(function() { showModel($(this).find("td.movie").text(),flag_input);showGraph($(this).find("td.movie").text(),flag_input);highlight_row($(this));})
                        });
                        showModel(data[0].title,flag_input);
                        showGraph(data[0].title,flag_input);
                    }, "json");
            return false;
        }
        function search1() {
            var query=$("#search1").find("input[name=search1]").val();
            var query1=$("#search1").find("input[name=search2]").val();
            var flag_input=$('input[name="flag_input"]:checked').val();
            $.get("/search_shortest_path?q=" + encodeURIComponent(query)+"&to="+encodeURIComponent(query1),
                    function (data) {
                        if (!data || data.length == 0) return;
                        relation_show(data);
                    }, "json");
            return false;
        }

    $(function () {

        $("#search").submit(search);
        $("#search1").submit(search1);
    })
