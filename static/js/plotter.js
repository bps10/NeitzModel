////////////////////////////
// locations:plots        //
//   5:image    1:plot1   //
//   6:plot5    2:plot2   //
//   7:plot6    3:plot3   //
//   8:button   4:plot4   //
////////////////////////////


// dimensions //
var margin = {top: 70, right: 20, bottom: 30, left: 40},
    width = 900 - margin.left - margin.right,
    height = 1500 - margin.top - margin.bottom,
    xaxisWidth = 350, yaxisWidth = 250;



// scales //
var x1 = d3.scale.linear()
    .range([0, xaxisWidth]);
    
var y1 = d3.scale.linear()
    .range([yaxisWidth, 0]);
    
var x2 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y2 = d3.scale.linear()
    .range([yaxisWidth, 0]);

var x3 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y3 = d3.scale.linear()
    .range([yaxisWidth, 0]);

var x4 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y4 = d3.scale.linear()
    .range([yaxisWidth, 0]);
	
var x5 = d3.scale.log()
    .range([0, xaxisWidth]);
    
var y5 = d3.scale.linear()
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
    .ticks(5)
    .orient("bottom");

var yAxis2 = d3.svg.axis()
    .scale(y2)
    .ticks(5)
    .orient("left");

var xAxis3 = d3.svg.axis()
    .scale(x3)
    .ticks(5)
    .orient("bottom");

var yAxis3 = d3.svg.axis()
    .scale(y3)
    .ticks(5)
    .orient("left");

var xAxis4 = d3.svg.axis()
    .scale(x4)
    .ticks(5)
    .orient("bottom");

var yAxis4 = d3.svg.axis()
    .scale(y4)
    .ticks(5)
    .orient("left");

var xAxis5 = d3.svg.axis()
    .scale(x5)
    .ticks(5)
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


function dataFormater(input) {
    var dat = []
    for (var i=0; i<input.length; i++) {
        dat.push({"x": i, "y": input[i]});
        };
    return dat
};


var dataDif = dataFormater(dataDif);
    data = dataFormater(dataOpt),
    data2 = dataFormater(dataOptB);
    

    
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x1.domain(d3.extent(data, function(d) { return d.x; }));
    y1.domain(d3.extent(data, function(d) { return d.y; }));

    x2.domain([Math.pow(10,2),Math.pow(10,6.6)]);
    y2.domain([0,25]);

    x3.domain([Math.pow(10,2),Math.pow(10,6.6)]);
    y3.domain([0,25]);    

    x4.domain([Math.pow(10,2),Math.pow(10,6.6)]);
    y4.domain([0,25]); 

    x5.domain([Math.pow(10,2),Math.pow(10,6.6)]);
    y5.domain([0,25]); 

    x6.domain([-15,15]);
    y6.domain([-0.3,1]); 
    
    // x,y axes //	
    
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(450,250)")
    .call(xAxis)
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/deg)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(440,-10)")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("modulation");

    // figure 1 lines //
    svg.append("path")
    .datum(dataDif)
    .attr("transform", "translate(450,-10)")
    .attr("class", "diff")
    .attr("d", line);
    
    svg.append("path")
    .datum(data)
    .attr("transform", "translate(450,-10)")
    .attr("class", "line")
    .attr("d", line);

    svg.append("path")
    .datum(data2)
    .attr("transform", "translate(450,-10)")
    .attr("class", "line2")
    .attr("d", line);
    
    
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(450,600)")
    .call(xAxis2)    
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/deg)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(440,340)")
    .call(yAxis2)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("density");
    

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(450,950)")
    .call(xAxis3)
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/deg)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(440,690)")
    .call(yAxis3)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("density");
	
	
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(450,1300)")
    .call(xAxis4)    
    .append("text")
    .attr("y", 50)
    .attr("x", 75)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/degree)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(440,1040)")
    .call(yAxis4)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("density");

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(30,600)")
    .call(xAxis5)    
    .append("text")
    .attr("y", 50)
    .attr("x", 65)
    .style("text-anchor", "beginning")
    .text("spatial frequency (cycles/degree)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(20,340)")
    .call(yAxis5)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("density");

    // loc7, fig6 //	
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(30,950)")
    .call(xAxis6)    
    .append("text")
    .attr("y", 50)
    .attr("x", 115)
    .style("text-anchor", "beginning")
    .text("distance (arcmin)");
    

    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(20,690)")
    .call(yAxis6)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -150)
    .text("amplitude");
	

    // loc8, options //	

                  

	d3.select("#coneInput").on("change", changeCone);
    d3.select("#opticSetting1").on("change",changeOpt1);
    d3.select("#opticSetting2").on("change",changeOpt2);
    //d3.select("#runButton").on("click", update);
    
    
    var Opt1 = ['offAxis','40deg'],
        Opt2 = ['offAxis','20deg'],
        spacing=2,
        updateEvent = {};
    
    function changeOpt1() {
        Opt1 = this.value.split(" : ")
    }
    
    function changeOpt2() {
        Opt2 = this.value.split(" : ")
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


    
	



