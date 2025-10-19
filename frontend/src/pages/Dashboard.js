import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapView from '../components/MapView';
import ClusterChart from '../components/ClusterChart';
import SimSlider from '../components/SimSlider';
import { TextField, Button } from '@mui/material';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [stateCode, setStateCode] = useState('');

  useEffect(() => {
    axios.get(`http://localhost:8000/api/clusters?state_code=${stateCode}`).then(res => setData(res.data));
  }, [stateCode]);

  return (
    <div className="dashboard">
      <div className="filter">
        <TextField label="State Code (e.g., UP)" value={stateCode} onChange={e => setStateCode(e.target.value)} />
        <Button variant="contained" onClick={() => {}}>Refresh</Button>
      </div>
      <MapView data={data} />
      <ClusterChart data={data} />
      <SimSlider />
    </div>
  );
};

export default Dashboard;
