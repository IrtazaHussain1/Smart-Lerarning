function makeplottest() {
  Plotly.d3.csv("{% static \"Data/PF_SP18_BCS_B.csv\" %}", function(data){ processDatatest(data)  }  );
};

function processDatatest(allRows) {

    console.log(allRows);
    var xtest = [], ytest = [],ztest=[],atest=[];

    for (var i=0; i< allRows.length; i++) {
        row = allRows[i];
        xtest.push( row['Name'] );
        ytest.push( row['Quiz (15)'] );
        ztest.push(row['CA (10)']);
        atest.push(row['ST (25)']);
    }
    console.log( 'X',xtest, 'Y',ytest, 'Z',ztest,'A', atest );
    makePlotlytest( xtest, ytest, ztest,atest );
}

function makePlotlytest( x, y,z,a ){
    var plotDiv = document.getElementById("plot");
    var traces = {
        x: x,
        y: y,
        name:'Quiz',
        type:'bar'
    };
    var traces1 = {
        x: x,
        y: z,
        name:'Assignment',
        type:'bar'
    };
    var traces2 = {
        x: x,
        y: a,
        name:'Sessional',
        type:'bar'
    };
    var data=[traces,traces1,traces2];
    var layout={barmode:'group',
      title:'Total Performance Section B'
  };

    Plotly.newPlot('test_view', data,layout,
     {responsive: true});
};


    makeplottest();