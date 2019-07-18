trace1 = {
x: [0],
y: [0],
hoverinfo: 'text+name',
marker: {
  color: '850000',
  size: 28
},
name: 'performance',
showlegend: false,
text: 175,
type: 'scatter',
uid: '5637dc'
};
trace2 = {
hole: 0.5,
hoverinfo: 'label',
labels: ['76-100', '51-75', '0-50',''],
marker: {colors: ['rgb(51,255,51)', 'rgb(255,255,77)', 'rgb(255,0,0)','rgba(255, 255, 255, 0)']},
rotation: 90,
showlegend: false,
text: ['Good', 'Average', 'Bad',''],
textinfo: 'text',
textposition: 'inside',
type: 'pie',
uid: 'e3117f',
values: [16.666666667,16.666666667,16.666666667,50]
};
data = [trace1, trace2];
layout = {
autosize: false,
height: 600,
shapes: [
  {
    fillcolor: '850000',
    line: {color: '850000'},
    path: 'M -.0 -0.025 L .0 0.025 L 0.498097349045872 0.04357787137382908 Z',
    type: 'path'
  }
],
title: '<b>Performace</b> <br>Section',
width: 500,
xaxis: {
  autorange: false,
  range: [-1, 1],
  showgrid: false,
  showticklabels: false,
  type: 'linear',
  zeroline: false
},
yaxis: {
  autorange: false,
  range: [-1, 1],
  showgrid: false,
  showticklabels: false,
  type: 'linear',
  zeroline: false
}
};
Plotly.plot('pie_div', {
data: data,
layout: layout
});
