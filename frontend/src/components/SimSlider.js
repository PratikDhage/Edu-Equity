import React, { useState } from 'react';
import axios from 'axios';
import Slider from 'react-slider';

const SimSlider = () => {
  const [value, setValue] = useState(0);
  const [result, setResult] = useState(null);

  const simulate = async () => {
    const features = { class_rooms: 10 + value, total_teachers: 20, class_students: 300, student_teacher_ratio: 15 };
    const res = await axios.post('http://localhost:8000/api/predict', features);
    setResult(res.data);
  };

  return (
    <div className="slider-container">
      <h3>Simulate Teacher Boost ({value}%)</h3>
      <Slider value={value} onChange={setValue} min={0} max={50} />
      <button onClick={simulate}>Run Sim</button>
      {result && <p>Predicted: {result.predicted_students} students (+{result.uplift.toFixed(0)} uplift)</p>}
    </div>
  );
};

export default SimSlider;
