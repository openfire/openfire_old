## nuffin' yet

## openfire user controllers
class ActivityGraph
    constructor: (@graphId, @graphType) ->
        @setup_bar()
        @setup_bubble()


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


window.ActivityGraph = ActivityGraph
