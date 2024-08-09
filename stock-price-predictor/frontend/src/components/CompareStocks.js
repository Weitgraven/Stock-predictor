import React, { useState } from 'react';
import axios from 'axios';
import StockChart from './StockChart';

const CompareStocks = () => {
  const [symbols, setSymbols] = useState(['AAPL', 'GOOGL']);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/compare', { symbols });
      setComparisonData(response.data);
    } catch (err) {
      console.error('Failed to fetch comparison data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div>
        {symbols.map((symbol, index) => (
          <input
            key={index}
            value={symbol}
            onChange={(e) => {
              const newSymbols = [...symbols];
              newSymbols[index] = e.target.value;
              setSymbols(newSymbols);
            }}
          />
        ))}
        <button onClick={handleCompare} disabled={loading}>Compare</button>
      </div>
      {comparisonData && symbols.map((symbol, index) => (
        <div key={index}>
          <h3>{symbol}</h3>
          <StockChart symbol={symbol} />
        </div>
      ))}
    </div>
  );
};

export default CompareStocks;
