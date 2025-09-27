import { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function Recommendations() {
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    const fetchRecs = async () => {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://localhost:5000/api/recommendations', { headers: { Authorization: `Bearer ${token}` } });
      setRecs(res.data);
    };
    fetchRecs();

    socket.on('new-recommendation', (rec) => {
      setRecs((prev) => [...prev, rec]);
    });

    return () => socket.off('new-recommendation');
  }, []);

  return (
    <div>
      <h2>Your Personalized Recommendations</h2>
      <ul className="recommendation-list">
        {recs.map((rec, index) => (
          <li key={index} className="recommendation-item">
            {rec.product} - Why? {rec.reason} (from AI)
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;