import React from 'react';
import Chart from 'react-apexcharts';

const HeatmapChart = () => {
  const options = {
    chart: {
      type: 'heatmap',
      toolbar: { show: false }
    },
    plotOptions: {
      heatmap: {
        shadeIntensity: 0.5,
        colorScale: {
          ranges: [
            { from: 0, to: 30, color: '#00A100', name: 'Low' },
            { from: 31, to: 70, color: '#128FD9', name: 'Medium' },
            { from: 71, to: 100, color: '#FFB200', name: 'High' }
          ]
        }
      }
    },
    dataLabels: {
      enabled: true
    },
    xaxis: {
      type: 'category'
    }
  };

  const series = [
    {
      name: 'Metric 1',
      data: [
        { x: 'Jan', y: 22 },
        { x: 'Feb', y: 45 },
        { x: 'Mar', y: 78 },
        { x: 'Apr', y: 40 }
      ]
    },
    {
      name: 'Metric 2',
      data: [
        { x: 'Jan', y: 60 },
        { x: 'Feb', y: 35 },
        { x: 'Mar', y: 90 },
        { x: 'Apr', y: 70 }
      ]
    }
  ];

  return (
    <div>
      <Chart options={options} series={series} type="heatmap" height={350} />
    </div>
  );
};

export default HeatmapChart;

//npm install apexcharts react-apexcharts
