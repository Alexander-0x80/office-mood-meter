(function(){
    'use strict';

    var CHART_RANGE = ["#00c90d", "#4282d3", "#ffec00", "#ffaa00", "#ff2800"];

    var dispatch = d3.dispatch("update"),   /* Event listener */
        levels = d3.selectAll("#level > div"),
        connection = new WebSocket("ws://localhost:8080/socket"),
        chart_data = [1,0,0,0,0];
    
    createChart(chart_data,CHART_RANGE);

    /* Event Handlers */

    connection.onopen = function(){
        console.log("Connected..");
    };

    connection.onmessage = function(e){
        if (e.data == "{}") return;
        chart_data = [
            count(e.data,1),
            count(e.data,2),
            count(e.data,3),
            count(e.data,4),
            count(e.data,5)
        ];

        dispatch.update();
    };

    if (levels) {
        levels.on('click',updateChart);
    }


    /* Callbacks */

    function updateChart(){
         d3.xhr("/update")
            .post('value=' + d3.select(this).text());
    }


    /* Methods */

    function count(data,value) {
        var ocr = 0;
        for (var key in data)
            if (data.hasOwnProperty(key) && (data[key] == value)) ocr++;
        
        return ocr;
    }


    /* d3.js */
    function createChart(data,range_c){
        console.log(data);
        var width  = 960,
            height = 500,
            radius = Math.min(width,height) /2,
            color  = d3.scale.ordinal().range(range_c),
            pie = d3.layout.pie().sort(null),
            arc = d3.svg.arc()
                    .innerRadius(radius - 100)
                    .outerRadius(radius - 20),
            svg = d3.select("#charts").append("svg")
                    .attr("width",width)
                    .attr("height",height)
                    .append("g")
                    .attr("transform","translate("+ width /2 +","+ height /2 +")" ),
            path = svg.selectAll("path")
                    .data(pie(data))
                    .enter().append("path")
                    .attr("fill",function(d, i) { return color(i); })
                    .attr("d",arc)
                    .each(function(d) { this._current = d; });

            /* Emit update event */
            dispatch.on('update',change);

            function change() {
                path = path.data(pie(chart_data));
                path.transition().duration(750).attrTween("d", arcTween);
            }

            function arcTween(a) {
                var i = d3.interpolate(this._current, a);
                this._current = i(0);
                return function(t) {
                    return arc(i(t));
                };
            }
    }

})();