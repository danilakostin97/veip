var ctx = document.getElementById('myChart').getContext('2d');
var mato=document.getElementById('mato').value, sko=mato=document.getElementById('sko').value;
var arr=document.getElementById('arr').value;
var myChart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: [],
        datasets: [{
            label: [arr[2]],
            backgroundColor: 'rgb(255,255,255)',
            borderColor: 'rgb(255, 99, 132)',
            data: []
        }]
    },

    // Configuration options go here
    options: {}
});
//Заполняем данными
  for (var x = -5; x<=5; x+=0.1) {
   myChart.data.labels.push(''+x.toFixed(2));
   myChart.data.datasets[0].data.push(f(x).toFixed(2));
  }
  //Обновляем
  myChart.update();

  function f(x) { //Вычисление нужной функции
   return Math.exp(-(Math.pow(x-mato, 2)/(2*Math.pow(sko,2))))*(1/(Math.sqrt(sko*Math.PI*2)));}
console.log(arr);