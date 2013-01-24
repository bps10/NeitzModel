////////////////////////////
// locations:plots        //
//   5:image    1:MTF     //
//   6:DOG      2:plot2   //
//   7:plot6    3:plot3   //
//   8:button   4:plot4   //
////////////////////////////


// dimensions //
var margin = {top: 70, right: 20, bottom: 30, left: 40},
    width = 900 - margin.left - margin.right,
    height = 1470 - margin.top - margin.bottom,
    xaxisWidth = 350, yaxisWidth = 250;



// scales //
var x1 = d3.scale.linear()
    .range([0, xaxisWidth]);
    
var y1 = d3.scale.linear()
    .range([yaxisWidth, 0]);
    
var x2 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y2 = d3.scale.log()
    .range([yaxisWidth, 0]);

var x3 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y3 = d3.scale.log()
    .range([yaxisWidth, 0]);

var x4 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y4 = d3.scale.log()
    .range([yaxisWidth, 0]);
	
var x5 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y5 = d3.scale.log()
    .range([yaxisWidth, 0]);

var x6 = d3.scale.linear()
    .range([0, xaxisWidth]);
    
var y6 = d3.scale.linear()
    .range([yaxisWidth, 0]);


// axes handles //	
var xAxis = d3.svg.axis()
    .scale(x1)
    .ticks(5)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y1)
    .ticks(5)
    .orient("left");
	
var xAxis2 = d3.svg.axis()
    .scale(x2)
    .ticks(2)
    .orient("bottom");

var yAxis2 = d3.svg.axis()
    .scale(y2)
    .ticks(5)
    .orient("left");

var xAxis3 = d3.svg.axis()
    .scale(x3)
    .ticks(2)
    .orient("bottom");

var yAxis3 = d3.svg.axis()
    .scale(y3)
    .ticks(5)
    .orient("left");

var xAxis4 = d3.svg.axis()
    .scale(x4)
    .ticks(2)
    .orient("bottom");

var yAxis4 = d3.svg.axis()
    .scale(y4)
    .ticks(2)
    .orient("left");

var xAxis5 = d3.svg.axis()
    .scale(x5)
    .ticks(2)
    .orient("bottom");

var yAxis5 = d3.svg.axis()
    .scale(y5)
    .ticks(5)
    .orient("left");

var xAxis6 = d3.svg.axis()
    .scale(x6)
    .ticks(5)
    .orient("bottom");

var yAxis6 = d3.svg.axis()
    .scale(y6)
    .ticks(5)
    .orient("left");	



var line = d3.svg.line()
.x(function(d) { return x1(d.x); })
.y(function(d) { return y1(d.y); });

var line2 = d3.svg.line()
.x(function(d) { return x2(d.x); })
.y(function(d) { return y2(d.y); });

var lineFFT = d3.svg.line()
.x(function(d) { return x3(d.x); })
.y(function(d) { return y3(d.y); });

var line4 = d3.svg.line()
.x(function(d) { return x4(d.x); })
.y(function(d) { return y4(d.y); });

var linePow = d3.svg.line()
.x(function(d) { return x5(d.x); })
.y(function(d) { return y5(d.y); });

var lineDoG = d3.svg.line()
.x(function(d) { return x6(d.x); })
.y(function(d) { return y6(d.y); });

var opt1 = ['onAxis : 1m'],
opt2 = ['onAxis : 20ft'],
spacing=2,
updateEvent = {};


function dataFormatter(input,xstart) {
    var dat = []
    for (var i=0; i<input.length; i++) {
        dat.push({"x": i+xstart, "y": input[i]});
        };
    return dat
};

function dogFormatter(xvals, DOG) {
    var dat = []
    for (var i=0; i<xvals.length; i++) {
        dat.push({"x": xvals[i], "y": DOG[i]})
    };
    return dat;
};


var dataDif = dataFormatter(dataDif,0);
    data = dataFormatter(dataOpt,0),
    data2 = dataFormatter(dataOptB,0),
    dataFFT = dataFormatter(DOG_fft,1),
    dataPow = dataFormatter(powerLaw,1),
    retPowDiffract = dataFormatter(retPowDiffract,1),
    retPowOpt1 = dataFormatter(retPowOpt1,1),
    retPowOpt2 = dataFormatter(retPowOpt2,1),
    conePowDiffract = dataFormatter(conePowDiffract,1),
    conePowOpt1 = dataFormatter(conePowOpt1,1),
    conePowOpt2 = dataFormatter(conePowOpt2,1);

//console.log(retPowDiffract);

var dataDoG = dogFormatter(DOG_xvals,DOG);
    

    
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x1.domain(d3.extent(data, function(d) { return d.x; }));
    y1.domain(d3.extent(data, function(d) { return d.y; }));

    x2.domain(d3.extent(retPowDiffract, function(d) { return d.x; }));
    y2.domain([Math.pow(10,-5), Math.pow(10,0)]);

    x3.domain(d3.extent(dataFFT, function(d) { return d.x; }));
    y3.domain([Math.pow(10,-5), Math.pow(10,0)]);

    x4.domain(d3.extent(conePowDiffract, function(d) { return d.x; }));
    y4.domain([Math.pow(10,-6), Math.pow(10,-1)]);

    x5.domain(d3.extent(dataPow, function(d) { return d.x; }));
    y5.domain(d3.extent(dataPow, function(d) { return d.y; }));

    x6.domain(d3.extent(dataDoG, function(d) { return d.x; }));
    y6.domain(d3.extent(dataDoG, function(d) { return d.y; }));
    
    // figure 1 lines //	
    
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(470,250)")
    .call(xAxis)
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/deg)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(460,-10)")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("modulation");

    svg.append("path")
    .datum(dataDif)
    .attr("transform", "translate(470,-10)")
    .attr("class", "diff")
    .attr("data-legend","diffraction")
    .attr("d", line);
    
    svg.append("path")
    .datum(data)
    .attr("transform", "translate(470,-10)")
    .attr("class", "line")
    .attr("data-legend",opt1)
    .attr("d", line);

    svg.append("path")
    .datum(data2)
    .attr("transform", "translate(470,-10)")
    .attr("class", "line2")
    .attr("data-legend",opt2)
    .attr("d", line);

    svg.append("g")
    .attr("class","legend")
    .attr("transform","translate(700,20)")
    .style("font-size","16px")
    .call(d3.legend);


    // figure 2 //

    svg.append("svg:clipPath")
    .attr("id", "clipper")
    .append("svg:rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", xaxisWidth)
    .attr("height", yaxisWidth);

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(470,600)")
    .call(xAxis2)    
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/deg)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(460,340)")
    .call(yAxis2)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -50)
    .attr("x", -150)
    .text("density");

    svg.append("path")
    .datum(retPowDiffract)
    .attr("transform", "translate(470,340)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "diff")
    .attr("d", line2);

    svg.append("path")
    .datum(retPowOpt1)
    .attr("transform", "translate(470,340)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "line")
    .attr("d", line2);

    svg.append("path")
    .datum(retPowOpt2)
    .attr("transform", "translate(470,340)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "line2")
    .attr("d", line2);

    // figure 3 //

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(470,950)")
    .call(xAxis3)
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/deg)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(460,690)")
    .call(yAxis3)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -50)
    .attr("x", -150)
    .text("density");
	
    svg.append("path")
    .datum(dataFFT)
    .attr("transform", "translate(470,690)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "lineDoG")
    .attr("d", lineFFT);

    // figure 4 //

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(470,1300)")
    .call(xAxis4)    
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/degree)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(460,1040)")
    .call(yAxis4)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -50)
    .attr("x", -150)
    .text("density");

    svg.append("path")
    .datum(conePowDiffract)
    .attr("transform", "translate(470,1040)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "diff")
    .attr("d", line4);

    svg.append("path")
    .datum(conePowOpt1)
    .attr("transform", "translate(470,1040)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "line")
    .attr("d", line4);

    svg.append("path")
    .datum(conePowOpt2)
    .attr("transform", "translate(470,1040)")
    .attr("clip-path", "url(#clipper)")
    .attr("class", "line2")
    .attr("d", line4);


    // loc 6, figure 5 //
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(40,600)")
    .call(xAxis5)    
    .append("text")
    .attr("y", 50)
    .attr("x", 65)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/degree)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(30,340)")
    .call(yAxis5)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -50)
    .attr("x", -150)
    .text("density");

    svg.append("path")
    .datum(dataPow)
    .attr("transform", "translate(40, 340)")
    .attr("class", "lineDoG")
    .attr("d", linePow);

    d3.select("body").append("text")
    .attr("id", "powLaw")
    .text("power law, n = " + power);

    // loc7, fig6 //
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(40,950)")
    .call(xAxis6)    
    .append("text")
    .attr("y", 50)
    .attr("x", 115)
    .style("text-anchor", "beginning")
    .text("distance (arcmin)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(30,690)")
    .call(yAxis6)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -50)
    .attr("x", -150)
    .text("amplitude");

    svg.append("path")
    .datum(dataDoG)
    .attr("transform", "translate(40,690)")
    .attr("class", "lineDoG")
    .attr("d", lineDoG);

    // loc8, options //

    
                  
    d3.select("#powerInput").on("change", changePower);
	d3.select("#coneInput").on("change", changeCone);
    d3.select("#opticSetting1").on("change",changeOpt1);
    d3.select("#opticSetting2").on("change",changeOpt2);
    
    
    function changeOpt1() {
        opt1 = this.value.split(" : ")
    }
    
    function changeOpt2() {
        opt2 = this.value.split(" : ")
    }

    function changeCone() {
        spacing = this.value;
        console.log(spacing);
        
        d3.select("#cone_val").remove();
        
        d3.select("#cone_text").append("span")
        .attr("id", "cone_val")
        .style("color", "black")
        .text(spacing + " arcmin");
        
    };


    function changePower() {
        power = this.value;
        
        d3.select("#power_val").remove();
        
        d3.select("#power_text").append("span")
        .attr("id", "power_val")
        .style("color", "black")
        .text(power);
        
    };





