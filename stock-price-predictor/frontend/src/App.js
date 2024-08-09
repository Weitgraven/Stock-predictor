import React, { useState } from 'react';
import StockSelector from './components/StockSelector';
import StockChart from './components/StockChart';
import CompareStocks from './components/CompareStocks';
import Education from './components/Education';
import './App.css';

function App() {
  const [selectedStock, setSelectedStock] = useState(null);
  const [comparisonMode, setComparisonMode] = useState(false);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Stock Price Predictor</h1>
        <button onClick={() => setComparisonMode(!comparisonMode)}>
          {comparisonMode ? "Single Stock Mode" : "Compare Stocks Mode"}
        </button>
        {comparisonMode ? (
          <CompareStocks />
        ) : (
          <>
            <StockSelector setSelectedStock={setSelectedStock} />
            {selectedStock && <StockChart symbol={selectedStock} />}
          </>
        )}
        <Education />
      </header>
    </div>
  );
}

export default App;
