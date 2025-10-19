import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ClusterChart = ({ data }) => {
  const chartData = {
    labels: data.map(d => `Cluster ${d.cluster}`),
    datasets: [{ label: 'Students', data: data.map(d => d.class_students), backgroundColor: 'rgba(75,192,192,0.6)' }]
  };
  return <div className="chart-container"><Bar data={chartData} options={{ responsive: true }} /></div>;
};

export default ClusterChart;
