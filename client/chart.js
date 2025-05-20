import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';

const ChartDashboard = () => {
  // Sample dataset
  const rawData = [
    { month: 'Jan', sales: 30, profit: 10, volume: 200 },
    { month: 'Feb', sales: 50, profit: 20, volume: 220 },
    { month: 'Mar', sales: 70, profit: 25, volume: 250 },
    { month: 'Apr', sales: 40, profit: 15, volume: 180 }
  ];

  const chartTypes = ['heatmap', 'bar', 'bubble'];
  const xFields = ['month'];
  const yFields = ['sales', 'profit', 'volume'];

  // State for dropdown selections
  const [chartType, setChartType] = useState('heatmap');
  const [xAxisField, setXAxisField] = useState('month');
  const [yAxisField, setYAxisField] = useState('sales');
  const [series, setSeries] = useState([]);
  const [options, setOptions] = useState({});

  // Build chart options & series on load and dropdown change
  useEffect(() => {
    const buildChart = () => {
      const xCategories = rawData.map(item => item[xAxisField]);

      let newSeries = [];

      if (chartType === 'heatmap') {
        newSeries = [
          {
            name: yAxisField,
            data: rawData.map(item => ({
              x: item[xAxisField],
              y: item[yAxisField]
            }))
          }
        ];
      } else if (chartType === 'bar') {
        newSeries = [
          {
            name: yAxisField,
            data: rawData.map(item => item[yAxisField])
          }
        ];
      } else if (chartType === 'bubble') {
        newSeries = [
          {
            name: yAxisField,
            data: rawData.map((item, i) => ({
              x: i + 1,
              y: item[yAxisField],
              z: item.volume || 50
            }))
          }
        ];
      }

      const newOptions = {
        chart: { type: chartType },
        xaxis: {
          categories: chartType !== 'bubble' ? xCategories : undefined,
          title: { text: xAxisField }
        },
        yaxis: { title: { text: yAxisField } },
        dataLabels: { enabled: true },
        plotOptions: chartType === 'heatmap' ? {
          heatmap: {
            colorScale: {
              ranges: [
                { from: 0, to: 20, color: '#00A100' },
                { from: 21, to: 60, color: '#128FD9' },
                { from: 61, to: 100, color: '#FFB200' }
              ]
            }
          }
        } : {}
      };

      setOptions(newOptions);
      setSeries(newSeries);
    };

    buildChart();
  }, [chartType, xAxisField, yAxisField]);

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <label>
          Chart Type:
          <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
            {chartTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </label>

        <label>
          X Axis:
          <select value={xAxisField} onChange={(e) => setXAxisField(e.target.value)}>
            {xFields.map(field => (
              <option key={field} value={field}>{field}</option>
            ))}
          </select>
        </label>

        <label>
          Y Axis:
          <select value={yAxisField} onChange={(e) => setYAxisField(e.target.value)}>
            {yFields.map(field => (
              <option key={field} value={field}>{field}</option>
            ))}
          </select>
        </label>
      </div>

      <Chart options={options} series={series} type={chartType} height={400} />
    </div>
  );
};

export default ChartDashboard;
