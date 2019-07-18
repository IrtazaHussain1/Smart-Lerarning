$(document).ready(fucntion(){
  d3.json("{% url 'dashboard_app:inter_graph' %}", function(error, in_data){
        var c= [];
      for(i in in_data['pref_class_count']){
        c[i]=[in_data['pref_class_count'][i]['G_count'],in_data['pref_class_count'][i]['A_count'],in_data['pref_class_count'][i]['B_count']];
      }
      console.log("this is c: ",c[0]);

      var data = [{
          values: c[1],
          labels: ['Good', 'Avrage', 'bad' ],
          text: 'CSD101',
          textposition: 'inside',
          domain: {column: 0},
          name: 'Student Performance',
          hoverinfo: 'label+percent+name',
          hole: .5,
          type: 'pie',
          marker:{
            colors:['#00ff04', '#ffff00', '#ff2700']
          }
          },{
            values: c[0],
            labels: ['Good', 'Avrage', 'bad' ],
            text: 'CSD202',
            textposition: 'inside',
            domain: {column: 1},
            name: 'Student Performance',
            hoverinfo: 'label+percent+name',
            hole: .5,
            type: 'pie',
            marker:{
              colors:['#00ff04', '#ffff00', '#ff2700']
            }
          }

          ];

          var layout = {
          title: 'Class All performance',
          annotations: [
            {
              font: {
                size: 20
              },
              showarrow: false,
              text: 'CSD101',
              x: 0.14,
              y: 0.5
            },
            {
              font: {
                size: 20
              },
              showarrow: false,
              text: 'CSD202',
              x: 0.87,
              y: 0.5
            }
          ],
          height: 400,
          width: 600,
          showlegend: true,
          grid: {rows: 1, columns: 2}
          };

          Plotly.newPlot('pie_div1', data, layout);
    });
          
}


