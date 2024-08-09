import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

const StockChart = ({ symbol }) => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.post('http://172.20.0.2:5000/predict', { symbol });
      const data = response.data;

      setChartData({
        labels: data.dates,
        datasets: [
          {
            label: 'Price',
            data: data.actual,
            fill: false,
            borderColor: 'blue',
          },
          {
            label: 'RSI',
            data: data.rsi,
            fill: false,
            borderColor: 'orange',
          },
          {
            label: 'SMA (Bollinger)',
            data: data.bollinger_bands.sma,
            fill: false,
            borderColor: 'green',
          },
          {
            label: 'Upper Band (Bollinger)',
            data: data.bollinger_bands.upper_band,
            fill: false,
            borderColor: 'red',
            borderDash: [5, 5],
          },
          {
            label: 'Lower Band (Bollinger)',
            data: data.bollinger_bands.lower_band,
            fill: false,
            borderColor: 'red',
            borderDash: [5, 5],
          },
          {
            label: 'MACD',
            data: data.macd.macd,
            fill: false,
            borderColor: 'purple',
          },
          {
            label: 'MACD Signal',
            data: data.macd.signal,
            fill: false,
            borderColor: 'pink',
          },
        ],
      });
    };

    fetchData();
  }, [symbol]);

  return chartData ? <Line data={chartData} /> : <p>Loading...</p>;
};

export default StockChart;
