import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import Card from './components/Card';
import './css/styles.css';

const App = () => {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const res = await axios.get("http://127.0.0.1:8000/posts");
        setData(res.data);
      } catch (err) {
        setError("Failed to load data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredData = data.filter(item => 
    item.title.toLowerCase().includes(search.toLowerCase()) ||
    item.body.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <Header />
      <div className="container">
        <div className="search-box">
          <input 
            type="text" 
            placeholder="Search posts..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
        </div>
        {loading && <p className="message">Loading data...</p>}
        {error && <p className="message" style={{color: 'red'}}>{error}</p>}
        {!loading && !error && filteredData.length === 0 && (
          <p className="message">No posts found.</p>
        )}
        {!loading && !error && filteredData.length > 0 && (
          <div className="card-container">
            {filteredData.map((elem, idx) => (
              <Card key={elem.id || idx} title={elem.title} body={elem.body} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
