import React from 'react';

const StockSelector = ({ setSelectedStock }) => {
  const handleSelect = (e) => {
    setSelectedStock(e.target.value);
  };

  return (
    <select onChange={handleSelect}>
      <option value="">Select a stock</option>
      <option value="AAPL">Apple (AAPL)</option>
      <option value="GOOGL">Google (GOOGL)</option>
      <option value="MSFT">Microsoft (MSFT)</option>
      {/* Add more stock options here */}
    </select>
  );
};

export default StockSelector;
