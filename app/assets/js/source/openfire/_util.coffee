## nuffin' yet

## openfire user controllers
class ActivityGraph
    constructor: (@graphId, @graphType) ->
        @setup_bar()
        @setup_bubble()
        @setup_line()


    setup_bar: () ->
        data = [ 1, 2, 4, 8, 9, 10, 14, 17 ]

        x = d3.scale.linear()
                .domain([ 0, d3.max(data) ])
                .range([ 0, 420 ])

        y = d3.scale.ordinal()
                .domain(data)
                .rangeBands([ 0, 120 ])

        chart = d3.select("#spark-graph").append("svg")
                .attr("class", "chart")
                .attr("width", 250)
                .attr("height", 140)
                .append("g")
                .attr("transform", "translate(10,15)")

        chart.selectAll("rect").data(data).enter().append("rect")
            .attr("y", y)
            .attr("width", x)
            .attr "height", y.rangeBand()

        chart.selectAll("line").data(x.ticks(10)).enter().append("line")
            .attr("x1", x)
            .attr("x2", x)
            .attr("y1", 0)
            .attr("y2", 120)
            .style "stroke", "#ccc"

        chart.selectAll("text").data(data).enter().append("text")
            .attr("x", x)
            .attr("y", (d) ->
                y(d) + y.rangeBand() / 2
            ).attr("dx", -3)
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .text(String)
            .style "fill", "#fff"

        chart.selectAll(".rule").data(x.ticks(10)).enter().append("text")
            .attr("class", "rule")
            .attr("x", x)
            .attr("y", 0)
            .attr("dy", -3)
            .attr("text-anchor", "middle")
            .text(String)
            .style "fill", "#000"

        chart.append("line")
            .attr("y1", 0)
            .attr("y2", 120)
            .style "stroke", "#000"


    setup_bubble: () ->
        chart = d3.select("#category-graph").append("svg")
            .attr("class", "bubble")
            .attr("width", 250)
            .attr("height", 140)

        for d in [0...10]
            x = Math.floor(Math.random() * 200)
            y = Math.floor(Math.random() * 140)
            chart.append("circle")
                .attr("r", Math.floor(Math.random() * 30))
                .attr("cx", x)
                .attr("cy", y)
                .attr "fill", "SteelBlue"

            chart.append("text")
                .attr("dx", x)
                .attr("dy", y)
                .text(Math.floor(Math.random() * 100))


    setup_line: () ->

        #data = [ 6, 4, 7, 1, 14, 22, 18, 13, 15, 22, 9, 6, 16 ]
        data = (Math.floor(Math.random() * 50) for i in [0...10])
        w = 250
        h = 140
        margin = 20
        y = d3.scale.linear().domain([ 0, d3.max(data) ]).range([ 0 + margin, h - margin ])
        x = d3.scale.linear().domain([ 0, data.length ]).range([ 0 + margin, w - margin ])

        graph = d3.select("#backers-graph").append("svg:svg")
            .attr("width", w)
            .attr("height", h)

        g = graph.append("svg:g")
            .attr("transform", "translate(0, 140)")

        line = d3.svg.line().x((d, i) -> x i).y((d) -> -1 * y(d))

        g.append("svg:path")
            .attr "d", line(data)

        g.append("svg:line")
            .attr("x1", x(0)).attr("y1", -1 * y(0)).attr("x2", x(w)).attr "y2", -1 * y(0)

        g.append("svg:line")
            .attr("x1", x(0))
            .attr("y1", -1 * y(0))
            .attr("x2", x(0)).attr "y2", -1 * y(d3.max(data))

        g.selectAll(".xLabel").data(x.ticks(5)).enter().append("svg:text")
            .attr("class", "xLabel")
            .text(String)
            .attr("x", (d) -> x d)
            .attr("y", 0)
            .attr("text-anchor", "middle")

        g.selectAll(".yLabel").data(y.ticks(4)).enter().append("svg:text")
            .attr("class", "yLabel")
            .text(String)
            .attr("x", 0)
            .attr("text-anchor", "right")
            .attr("dy", 4)
            .attr("y", (d) -> -1 * y(d))

        g.selectAll(".xTicks").data(x.ticks(5)).enter().append("svg:line")
            .attr("class", "xTicks")
            .attr("x1", (d) -> x d)
            .attr("y1", -1 * y(0))
            .attr("x2", (d) -> x d)
            .attr("y2", -1 * y(-0.3))

        g.selectAll(".yTicks").data(y.ticks(4)).enter().append("svg:line")
            .attr("class", "yTicks")
            .attr("y1", (d) -> -1 * y(d))
            .attr("x1", x(-0.3))
            .attr("y2", (d) -> -1 * y(d))
            .attr("x2", x(0))


window.ActivityGraph = ActivityGraph
