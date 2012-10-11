## nuffin' yet

## openfire user controllers
class ActivityGraph
    constructor: (@graphId, @graphType) ->
        @setup_time_series()
        @setup_pie_chart()
        @setup_projects_funded()

    setup_time_series: () ->
        data = [
            values: [ [1, 10], [2, 200], [3, 300], [4, 750], [5, 890], [6, 1000], [7, 2000], [8, 4500] ]
            key: 'Total $'
        ,
            values: [ [1, 1], [2, 3], [3, 6], [4, 9], [5, 10], [6, 14], [7, 19], [8, 28] ]
            key: 'Donations'
            bar: true
        ]

        chart = nv.models.linePlusBarChart()
        .margin(top: 20, right: 40, bottom: 35, left: 25)
        .x((d, i) ->
            i
        ).y((d) ->
            d[1]
        ).color(d3.scale.category10().range())

        chart.xAxis.showMaxMin(false)
        .axisLabel('Last 8 Days')
        .tickFormat (d) ->
            dx = data[0].values[d] and data[0].values[d][0] or 0
            return d3.format(",f")(d)

        chart.y1Axis.tickFormat d3.format(",f")
        chart.y2Axis.tickFormat (d) ->
            "$" + d3.format(",f")(d)

        chart.bars.forceY [0]
        d3.select('#spark-graph svg').datum(data).transition().duration(500).call(chart)
        nv.utils.windowResize chart.update
        return chart


    setup_pie_chart: () ->
        data = [
            key: 'Donations by Category'
            values: [
                label: 'politics'
                value: 300
            ,
                label: 'conservation'
                value: 100
            ,
                label: 'health care'
                value: 200
            ,
                label: 'business'
                value: 700
            ,
                label: 'law'
                value: 900
            ,
                label: 'technology'
                value: 2000
            ,
                label: 'economy'
                value: 300
            ]
        ]

        chart = nv.models.pieChart()
        .margin(top: 0, right: 0, bottom: 0, left: 0)
        .x((d) ->
            d.label
        ).y((d) ->
            d.value
        ).showLabels(true)

        d3.select("#category-graph svg").datum(data).transition().duration(1200).call chart

        return chart

    setup_projects_funded: () ->
        data = [
            values: [ {'x': 1, 'y': 3}, {'x': 2, 'y': 4}, {'x': 3, 'y': 6}, {'x': 4, 'y': 10}, {'x': 5, 'y': 11}, {'x': 6, 'y': 12}, {'x': 7, 'y': 15}, {'x': 8, 'y': 20} ]
            key: 'Total Projects'
        ,
            values: [ {'x': 1, 'y': 0}, {'x': 2, 'y': 1}, {'x': 3, 'y': 1}, {'x': 4, 'y': 2}, {'x': 5, 'y': 3}, {'x': 6, 'y': 5}, {'x': 7, 'y': 7}, {'x': 8, 'y': 10} ]
            key: 'Funded Projects'
        ]

        chart = nv.models.lineChart()
        chart.xAxis.axisLabel('Months').tickFormat d3.format(",d")
        chart.yAxis.tickFormat d3.format(",d")
        chart.margin(top: 20, right: 20, bottom: 35, left: 25)

        d3.select("#project-graph svg").datum(data).transition().duration(500).call chart

        nv.utils.windowResize chart.update
        return chart

window.ActivityGraph = ActivityGraph
