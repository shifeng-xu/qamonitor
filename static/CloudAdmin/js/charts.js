
var Charts = function () {

    return {
        initCharts: function (datadict) {
            bugsAllByDayList=[]; //数据列表[[1,数据1],[2,数据2]]
            bugsUnFixByDayList=[];

            bugsByQaList=[];
            bugsByQaList_all=[];
            bugsByRdList=[];
            bugsByRdList_all=[];
            DayList=[]; //日期列表[[1，日期1],[2，日期2]]
            QaList=[];//qa列表[[1，qa1],[2，qa2]]
            RdList=[];//qa列表[[1，rd1],[2，rd2]]



            var bugsAllByDayDic = new Array();//通过申明一个Array来做一个字典

            for(var key in datadict){
                    if(key=='bugsAllByDay') //每天新提的bug数
                    {
                         var index=0
                        bugsAllByDayDic=datadict[key]
                        for(var key in bugsAllByDayDic){
                            datenew=bugsAllByDayDic[key]
                            DayList[index]=[index+1,key]
                            bugsAllByDayList[index]=[index+1,datenew]
                            index++
                        }
                    }//bugsUnFixByDay
                    if(key=='bugsUnFixByDay')  //截止当天未关闭的bug数
                        {
                             var index=0
                            bugsUnFixByDayDic=datadict[key]
                            for(var key in bugsUnFixByDayDic){
                                datenew=bugsUnFixByDayDic[key]
                                DayList[index]=[index+1,key]
                                bugsUnFixByDayList[index]=[index+1,datenew]
                                index++
                            }
                        }//repairedRateTotal
                    if(key=='repairedRateTotal')  //项目总修复率
                            {
                                repairedRateTotal_Pie=datadict[key]
                            }

                     if(key=='qaRepairedRateDict') {
                         var index = 0
                         bugsByQaListDic = datadict[key]
                         for (var key in bugsByQaListDic) {
                             qanew = bugsByQaListDic[key]
                             QaList[index] = [index + 1, key]
                             bugsByQaList[index] = [index + 1, "       "+qanew]
                             index++

                         }
                     }
                     if(key=='rdRepairedRateDict') {
                         var index = 0
                         bugsByRdListDic = datadict[key]
                         for (var key in bugsByRdListDic) {
                             rdnew = bugsByRdListDic[key]
                             RdList[index] = [index + 1, key]
                             bugsByRdList[index] = [index + 1, "       "+rdnew]
                             index++

                         }
                     }

                     if(key=='qaAllBugsDict') {
                         var index = 0
                         bugsByQaListDic_all = datadict[key]
                         for (var key in bugsByQaListDic_all) {
                             qanew = bugsByQaListDic_all[key]
                             QaList[index] = [index + 1, key]
                             bugsByQaList_all[index] = [index + 1, "       "+qanew]
                             index++

                         }
                     }

                     if(key=='rdAllBugsDict') {
                         var index = 0
                         bugsByRdListDic_all = datadict[key]
                         for (var key in bugsByRdListDic_all) {
                             rdnew = bugsByRdListDic_all[key]
                             RdList[index] = [index + 1, key]
                             bugsByRdList_all[index] = [index + 1, "       "+rdnew]
                             index++

                         }
                     }

                     }


            if (!jQuery.plot) {
                return;
            }

            var data = [];
            var maximum = 300;
            function getRandomData() {
                if (data.length) {
					data = data.slice(1);
				}
				while (data.length < maximum) {
					var previous = data.length ? data[data.length - 1] : 50;
					var y = previous + Math.random() * 10 - 5;
					data.push(y < 0 ? 0 : y > 100 ? 100 : y);
				}
				// zip the generated y values with the x values
				var res = [];
				for (var i = 0; i < data.length; ++i) {
					res.push([i, data[i]])
				}
				return res;
            }
			/* Basic Chart */
            function chart1() {
                var d1 = [];
                for (var i = 0; i < Math.PI * 2; i += 0.25)
                    d1.push([i, Math.sin(i)]);

                var d2 = [];
                for (var i = 0; i < Math.PI * 2; i += 0.25)
                    d2.push([i, Math.cos(i)]);

                var d3 = [];
                for (var i = 0; i < Math.PI * 2; i += 0.1)
                    d3.push([i, Math.tan(i)]);

                $.plot($("#chart_1"), [{
                            label: "sin(x)",
                            data: d1
                        }, {
                            label: "cos(x)",
                            data: d2
                        }, {
                            label: "tan(x)",
                            data: d3
                        }
                    ], {
                        series: {
                            lines: {
                                show: true
                            },
                            points: {
                                show: true
                            }
                        },
                        xaxis: {
                            ticks: [0, [Math.PI / 2, "\u03c0/2"],
                                [Math.PI, "\u03c0"],
                                [Math.PI * 3 / 2, "3\u03c0/2"],
                                [Math.PI * 2, "2\u03c0"]
                            ]
                        },
                        yaxis: {
                            ticks: 10,
                            min: -2,
                            max: 2
                        },
                        grid: {
							borderWidth: 0
                        },
					colors: ["#70AFC4", "#D9534F", "#A8BC7B", "#F0AD4E"]
                    });

            }

            /* Interactive Chart */
            function chart2(DayList,bugsAllByDayList,bugsUnFixByDayList) {

                var plot = $.plot($("#chart_2"), [{

                            data: bugsAllByDayList,
                            label: "当日新增Bug数"
                        },

                    {
                            data: bugsUnFixByDayList,
                            label: "截止当天未关闭的bug数"
                        }
                    ], {
                        series: {
                            lines: {
                                show: true,
                                lineWidth: 2,
                                fill: true,
                                fillColor: {
                                    colors: [{
                                            opacity: 0.05
                                        }, {
                                            opacity: 0.01
                                        }
                                    ]
                                }
                            },
                            points: {
                                show: true
                            },
                            shadowSize: 2
                        },
                        grid: {
                            hoverable: true,
                            clickable: true,
                            tickColor: "#eee",
                            borderWidth: 0
                        },
                        colors: ["#DB5E8C", "#F0AD4E", "#5E87B0"],
                        /*xaxis: {
                            ticks: 11,
                            tickDecimals: 0
                        },*/
                        //xaxis: { tickFormatter: function(n, o) {var d = new Date(); d.setTime(n); return (d.getMonth()+1) + "-" + d.getDate();}},
                        xaxis: {
                         axisLabelUseCanvas: true,
                         ticks: DayList
                     },  //指定固定的显示内容
                        yaxis: {
                            ticks: 11,
                            tickDecimals: 0
                        }
                    });


                function showTooltip(x, y, contents) {
                    $('<div id="tooltip">' + contents + '</div>').css({
                            position: 'absolute',
                            display: 'none',
                            top: y + 5,
                            left: x + 15,
                            border: '1px solid #333',
                            padding: '4px',
                            color: '#fff',
                            'border-radius': '3px',
                            'background-color': '#333',
                            opacity: 0.80
                        }).appendTo("body").fadeIn(200);
                }

                var previousPoint = null;
                $("#chart_2").bind("plothover", function (event, pos, item) {
                    $("#x").text(pos.x.toFixed(2));
                    $("#y").text(pos.y.toFixed(2));

                    if (item) {
                        if (previousPoint != item.dataIndex) {
                            previousPoint = item.dataIndex;

                            $("#tooltip").remove();

                            var x = item.datapoint[0].toFixed(2),
                                y = item.datapoint[1].toFixed(2);


                            showTooltip(item.pageX, item.pageY, item.series.label + " = " + y);
                            //showTooltip(item.pageX, item.pageY, item.series.label + " of " + x + " = " + y);
                        }
                    } else {
                        $("#tooltip").remove();
                        previousPoint = null;
                    }
                });
            }

            /* Tracking Curves */
            function chart3() {
                var sin = [],
                    cos = [];
                for (var i = 0; i < 14; i += 0.1) {
                    sin.push([i, Math.sin(i)]);
                    cos.push([i, Math.cos(i)]);
                }

                plot = $.plot($("#chart_3"), [{
                            data: sin,
                            label: "sin(x) = -0.00"
                        }, {
                            data: cos,
                            label: "cos(x) = -0.00"
                        }
                    ], {
                        series: {
                            lines: {
                                show: true
                            }
                        },
                        crosshair: {
                            mode: "x"
                        },
                        grid: {
                            hoverable: true,
							borderWidth: 0,
                            autoHighlight: false
                        },
                        yaxis: {
                            min: -1.2,
                            max: 1.2
                        },
						colors: ["#A8BC7B", "#FCD76A", "#F38630"],
                    });

                var legends = $("#chart_3 .legendLabel");
                legends.each(function () {
                    $(this).css('width', $(this).width());
                });

                var updateLegendTimeout = null;
                var latestPosition = null;

                function updateLegend() {
                    updateLegendTimeout = null;

                    var pos = latestPosition;

                    var axes = plot.getAxes();
                    if (pos.x < axes.xaxis.min || pos.x > axes.xaxis.max || pos.y < axes.yaxis.min || pos.y > axes.yaxis.max) return;

                    var i, j, dataset = plot.getData();
                    for (i = 0; i < dataset.length; ++i) {
                        var series = dataset[i];

                        for (j = 0; j < series.data.length; ++j)
                            if (series.data[j][0] > pos.x) break;

                        var y, p1 = series.data[j - 1],
                            p2 = series.data[j];
                        if (p1 == null) y = p2[1];
                        else if (p2 == null) y = p1[1];
                        else y = p1[1] + (p2[1] - p1[1]) * (pos.x - p1[0]) / (p2[0] - p1[0]);

                        legends.eq(i).text(series.label.replace(/=.*/, "= " + y.toFixed(2)));
                    }
                }

                $("#chart_3").bind("plothover", function (event, pos, item) {
                    latestPosition = pos;
                    if (!updateLegendTimeout) updateLegendTimeout = setTimeout(updateLegend, 50);
                });
            }

            /* Auto updating Chart */
            function chart4() {
                var options = {
                    series: {
                        shadowSize: 1
                    },
                    lines: {
                        show: true,
                        lineWidth: 1.5,
                    },
                    yaxis: {
                        min: 0,
                        max: 100,
                        tickFormatter: function (v) {
                            return v + "%";
                        }
                    },
                    xaxis: {
                        show: false
                    },
                    colors: ["#D9534F"],
                    grid: {
                        tickColor: "#a8a3a3",
                        borderWidth: 0
                    }
                };

                var updateInterval = 30;
                var plot = $.plot($("#chart_4"), [getRandomData()], options);

                function update() {
                    plot.setData([getRandomData()]);
                    plot.draw();
                    setTimeout(update, updateInterval);
                }
                update();
            }

            /* Bars with controls */

            function chart5(bugsByQaList,bugsByRdList,bugsByQaList_all,bugsByRdList_all) {
                /*var d1 = [];
                for (var i = 0; i <= 2; i += 1)
                    d1.push([i, parseInt(Math.random() * 30)]);

                var d2 = [];
                for (var i = 0; i <= 2; i += 1)
                    d2.push([i, parseInt(Math.random() * 30)]);

                var d3 = [];
                for (var i = 0; i <= 2; i += 1)
                    d3.push([i, parseInt(Math.random() * 30)]);*/


                var stack = 0,
                    bars = true,
                    lines = false,
                    steps = false;

                function plotWithOptions() {
                    $.plot($("#chart_qa"), [bugsByQaList], {
                        series: {
                            stack: stack,
                            lines: {
                                show: lines,
                                fill: true,
                                steps: steps
                            },
                            bars: {
                                show: bars,
                                barWidth: 0.6
                            }
                        },

                        grid: {
                            borderWidth: 0,
                            hoverable: true,
							borderWidth: 0,
                            autoHighlight: false
                        },
                        //colors: ["#70AFC4", "#F0AD4E", "#A8BC7B"],
                        colors: ["#70AFC4"],
                        xaxis: {
                            mode: "categories",
                            ticks: QaList
                            //            tickLength: 2
                        },
                    });
                    $.plot($("#chart_rd"), [bugsByRdList], {
                        series: {
                            stack: stack,
                            lines: {
                                show: lines,
                                fill: true,
                                steps: steps
                            },
                            bars: {
                                show: bars,
                                barWidth: 0.6
                            }
                        },

                        grid: {
                            borderWidth: 0,
                            hoverable: true,
							borderWidth: 0,
                            autoHighlight: false
                        },
                        //colors: ["#70AFC4", "#F0AD4E", "#A8BC7B"],
                        colors: ["#F0AD4E"],
                        xaxis: {
                            mode: "categories",
                            ticks: RdList
                            //            tickLength: 2
                        },
                    });

                    $.plot($("#chart_qa_bugs"), [bugsByQaList_all], {
                        series: {
                            stack: stack,
                            lines: {
                                show: lines,
                                fill: true,
                                steps: steps
                            },
                            bars: {
                                show: bars,
                                barWidth: 0.6
                            }
                        },

                        grid: {
                            borderWidth: 0,
                            hoverable: true,
							borderWidth: 0,
                            autoHighlight: false
                        },

                        //colors: ["#70AFC4", "#F0AD4E", "#A8BC7B"],
                        colors: ["#A2CD5A"],
                        xaxis: {
                            mode: "categories",
                            ticks: QaList
                            //            tickLength: 2
                        },
                    });

                    $.plot($("#chart_rd_bugs"), [bugsByRdList_all], {
                        series: {
                            stack: stack,
                            lines: {
                                show: lines,
                                fill: true,
                                steps: steps
                            },
                            bars: {
                                show: bars,
                                barWidth: 0.6
                            }
                        },

                        grid: {
                            borderWidth: 0,
                            hoverable: true,
							borderWidth: 0,
                            autoHighlight: false
                        },
                        //colors: ["#70AFC4", "#F0AD4E", "#A8BC7B"],
                        colors: ["#6C7B8B"],
                        xaxis: {
                            mode: "categories",
                            ticks: RdList
                            //            tickLength: 2
                        },
                    });



                }

                function showTooltip(x, y, contents) {
                    $('<div id="tooltip">' + contents + '</div>').css({
                            position: 'absolute',
                            display: 'none',
                            top: y + 5,
                            left: x + 15,
                            border: '1px solid #333',
                            padding: '4px',
                            color: '#fff',
                            'border-radius': '3px',
                            'background-color': '#333',
                            opacity: 0.80
                        }).appendTo("body").fadeIn(200);
                }

                var previousPoint = null;
                $("#chart_qa").bind("plothover", function (event, pos, item) {
                    if (item) {
		                if (previousPoint != item.dataIndex) {
		                    previousPoint = item.dataIndex;
		                    $("#tooltip").remove();
		                    var y = item.datapoint[1].toFixed(0);

		                    var tip = "修复率：";
		                    showTooltip(item.pageX, item.pageY,tip+y+"%");

                        }
                    } else {
                        $("#tooltip").remove();
                        previousPoint = null;
                    }
                });

                var previousPoint = null;
                $("#chart_rd").bind("plothover", function (event, pos, item) {
                    if (item) {
		                if (previousPoint != item.dataIndex) {
		                    previousPoint = item.dataIndex;
		                    $("#tooltip").remove();
		                    var y = item.datapoint[1].toFixed(0);

		                    var tip = "修复率：";
		                    showTooltip(item.pageX, item.pageY,tip+y+"%");

                        }
                    } else {
                        $("#tooltip").remove();
                        previousPoint = null;
                    }
                });

                var previousPoint = null;
                $("#chart_rd_bugs").bind("plothover", function (event, pos, item) {
                    if (item) {
		                if (previousPoint != item.dataIndex) {
		                    previousPoint = item.dataIndex;
		                    $("#tooltip").remove();
		                    var y = item.datapoint[1].toFixed(0);

		                    var tip = "Bug数：";
		                    showTooltip(item.pageX, item.pageY,tip+y);

                        }
                    } else {
                        $("#tooltip").remove();
                        previousPoint = null;
                    }
                });

                var previousPoint = null;
                $("#chart_qa_bugs").bind("plothover", function (event, pos, item) {
                    if (item) {
		                if (previousPoint != item.dataIndex) {
		                    previousPoint = item.dataIndex;
		                    $("#tooltip").remove();
		                    var y = item.datapoint[1].toFixed(0);

		                    var tip = "Bug数：";
		                    showTooltip(item.pageX, item.pageY,tip+y);

                        }
                    } else {
                        $("#tooltip").remove();
                        previousPoint = null;
                    }
                });



                $(".stackControls input").click(function (e) {
                    e.preventDefault();
                    stack = $(this).val() == "With stacking" ? true : null;
                    plotWithOptions();
                });
                $(".graphControls input").click(function (e) {
                    e.preventDefault();
                    bars = $(this).val().indexOf("Bars") != -1;
                    lines = $(this).val().indexOf("Lines") != -1;
                    steps = $(this).val().indexOf("steps") != -1;
                    plotWithOptions();
                });

                plotWithOptions();
            }
			 /* Horizontal bar chart */
            function chart6() {
				 var data1 = [
							[5, 0], [10, 10], [20, 20], [30, 30], [40, 40], [50, 50], [60, 60]
						];
					 
						var options = {
								series:{
									bars:{
											show: true
										}
								},
								bars:{
									horizontal:true,
									barWidth:6
								},
								grid:{
									borderWidth: 0
								},
								colors: ["#F38630"]
						};
					 
						$.plot($("#chart_6"), [data1], options); 

            }
			
			/* Select chart */
            function chart7() {
				 // setup plot
				function getData(x1, x2) {

					var d = [];
					for (var i = 0; i <= 100; ++i) {
						var x = x1 + i * (x2 - x1) / 100;
						d.push([x, Math.cos(x * Math.sin(x))]);
					}

					return [
						{ label: "cos(x sin(x))", data: d }
					];
				}

				var options = {
					grid: {
						hoverable: true,
						clickable: true,
						tickColor: "#f7f7f7",
						borderWidth: 0,
						labelMargin: 10,
						margin: {
							top: 0,
							left: 5,
							bottom: 0,
							right: 0
						}
					},
					legend: {
						show: false
					},
					series: {
						lines: {
							show: true
						},
						shadowSize: 0,
						points: {
							show: true
						}
					},
					colors: ["#D9534F"],
					yaxis: {
						ticks: 10
					},
					selection: {
						mode: "xy",
						color: "#F1ADAC"
					}
				};

				var startData = getData(0, 3 * Math.PI);

				var plot = $.plot("#placeholder", startData, options);

				// Create the overview plot

				var overview = $.plot($("#overview"), startData, {
					legend: {
						show: false
					},
					series: {
						lines: {
							show: true,
							lineWidth: 1
						},
						shadowSize: 0
					},
					xaxis: {
						ticks: 4
					},
					yaxis: {
						ticks: 3,
						min: -2,
						max: 2
					},
					colors: ["#D9534F"],
					grid: {
						color: "#999",
						borderWidth: 0,
					},
					selection: {
						mode: "xy",
						color: "#F1ADAC"
					}
				});

				// now connect the two

				$("#placeholder").bind("plotselected", function (event, ranges) {

					// clamp the zooming to prevent eternal zoom

					if (ranges.xaxis.to - ranges.xaxis.from < 0.00001) {
						ranges.xaxis.to = ranges.xaxis.from + 0.00001;
					}

					if (ranges.yaxis.to - ranges.yaxis.from < 0.00001) {
						ranges.yaxis.to = ranges.yaxis.from + 0.00001;
					}

					// do the zooming

					plot = $.plot("#placeholder", getData(ranges.xaxis.from, ranges.xaxis.to),
						$.extend(true, {}, options, {
							xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
							yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
						})
					);

					// don't fire event on the overview to prevent eternal loop

					overview.setSelection(ranges, true);
				});

				$("#overview").bind("plotselected", function (event, ranges) {
					plot.setSelection(ranges);
				});

				// Add the Flot version string to the footer

				$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");

            }

            //graph
            //chart1();
            /*var pageviews = [
                    [30, 10],
                    [29, 24],
                    [28, 38],
                    [27, 32],
                    [26, 31],
                    [25, 25],
                    [24, 35],
                    [23, 46],
                    [22, 36],
                    [21, 48],
                    [20, 38],
                    [19, 60],
                    [18, 63],
                    [17, 72],
                    [16, 58],
                    [15, 65],
                    [14, 50],
                    [13, 32],
                    [12, 40],
                    [11, 35],
                    [10, 30],
                    [9, 35],
                    [8, 50],
                    [7, 53],
                    [6, 42],
                    [5, 34],
                    [4, 22],
                    [3, 15],
                    [2, 20],
                    [1, 5]
                ];*/
            //chart2(DayList,bugsAllByDayList,bugsUnFixByDayList);
			//chart7();
            //chart3();
            //chart4();
            //chart5(bugsByQaList,bugsByRdList,bugsByQaList_all,bugsByRdList_all);
			//chart6();
        },

        initPieCharts: function (datadict) {

            repairedRateTotal_Pie=0;
            var statusCount_Data=[]
            for(var key in datadict){
                if(key=='repairedRateTotal')  //项目总修复率
                    {
                        repairedRateTotal_Pie=datadict[key];
                       // break;
                    }
                if(key=='bugStatusDict')  //各个状态的bug饼图
                    {
                        var index=0
                        bugStatusDict=datadict[key]
                        for(var key in bugStatusDict){
                            statusNum=bugStatusDict[key]
                            statusCount_Data.push({label:key,data:statusNum})
                            index++
                        }
                        //break;
                    }


            }
            //repairedRateTotal_Pie=60;
            var repairedRateTotal_Data=[{label:"已修复",data:repairedRateTotal_Pie},{label:"未修复",data:100-repairedRateTotal_Pie}]; //[修复，未修复]
            //var repairedRateTotal_Data=[60,100-60]; //[修复，未修复]
            var data = [];
            var series = Math.floor(Math.random() * 9) + 1;
            series = series < 6 ? 6 : series;
            
            for (var i = 0; i < series; i++) {
                data[i] = {
                    label: "Series" + (i + 1),
                    data: Math.floor(Math.random() * 100)
                }
            }

            /* DEFAULT */
            $.plot($("#pie_chart"), repairedRateTotal_Data, {
                    series: {
                        pie: {
                            show: true
                        }
                    },
                legend: {
						show: false //不显示图例
			},
					colors: ["#A8BC7B","#F0AD4E"]
					//colors: ["#D9534F", "#A8BC7B", "#F0AD4E", "#70AFC4", "#DB5E8C", "#FCD76A", "#A696CE"]
                });

            /* DONUT */
            $.plot($("#donut"), statusCount_Data, {
                    series: {
                        pie: {
                            innerRadius: 0.6,
                            show: true
                        }
                    },
                legend: {
						show: false //不显示图例
			    },

					colors: ["#00BFFF", "#00CD66", "#68838B", "#68228B", "#8B3A62", "#8B8B00", "#5D478B","#9ACD32","#9E9E9E","#7B68EE"]
                });

        },
		
        initOtherCharts: function () {
			function chartGrow() {               
                var data = [[0, 2.5],[1, 3.5], [2, 2], [3, 3], [4, 4],[5, 3.5], [6, 3.5], [7, 1], [8, 2], [9, 3], [10, 4],[11, 5], [12, 4], [13, 3], [14, 5], [15, 3.5],[16, 5], [17, 4], [18, 5], [19, 6],[20, 5], [21, 4], [22, 3], [23, 5], [24, 4], [25, 3],[26, 2], [27, 1], [28, 2], [29, 2],[30, 3], [31, 2]];

                var plot = $.plot($("#chart_grow"), [{
                            data: data,
                            label: "Monthly Sales"
                        }], {
                        series: {
                            lines: {
                                show: true,
                                lineWidth: 2,
                                fill: true,
                                fillColor: {
                                    colors: [{
                                            opacity: 0.05
                                        }, {
                                            opacity: 0.01
                                        }
                                    ]
                                }
                            },
                            points: {
                                show: true
                            },
                            shadowSize: 2,
							grow: { active: true, duration: 1500 }
                        },
                        grid: {
                            hoverable: true,
                            clickable: true,
                            tickColor: "#eee",
                            borderWidth: 0
                        },
                        colors: ["#D9534F"],
                        xaxis: {
                            ticks: 11,
                            tickDecimals: 0
                        },
                        yaxis: {
                            ticks: 11,
                            tickDecimals: 0
                        }
                    });


                function showTooltip(x, y, contents) {
                    $('<div id="tooltip">' + contents + '</div>').css({
                            position: 'absolute',
                            display: 'none',
                            top: y + 5,
                            left: x + 15,
                            border: '1px solid #333',
                            padding: '4px',
                            color: '#fff',
                            'border-radius': '3px',
                            'background-color': '#333',
                            opacity: 0.80
                        }).appendTo("body").fadeIn(200);
                }

                var previousPoint = null;
                $("#chart_2").bind("plothover", function (event, pos, item) {
                    $("#x").text(pos.x.toFixed(2));
                    $("#y").text(pos.y.toFixed(2));

                    if (item) {
                        if (previousPoint != item.dataIndex) {
                            previousPoint = item.dataIndex;

                            $("#tooltip").remove();
                            var x = item.datapoint[0].toFixed(2),
                                y = item.datapoint[1].toFixed(2);

                            showTooltip(item.pageX, item.pageY, item.series.label + " of " + x + " = " + y);
                        }
                    } else {
                        $("#tooltip").remove();
                        previousPoint = null;
                    }
                });
            }
			//Run the graph
			chartGrow();
        }
    };

}();