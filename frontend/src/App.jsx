import { useState } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import ResultsList from './components/ResultsList';
import './App.css';

function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (textQuery, imageFile) => {
    if (!textQuery && !imageFile) {
      setError("Please enter a text query or upload an image.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults([]);

    const formData = new FormData();
    if (textQuery) {
      formData.append('text_query', textQuery);
    }
    if (imageFile) {
      formData.append('image_query', imageFile);
    }
    formData.append('top_k', 12);

    try {
      const response = await axios.post('http://localhost:8000/search/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data.results);
    } catch (err) {
      setError("An error occurred during the search. Please check the API server and try again.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Multimodal E-commerce Search</h1>
        <p>Search with text, an image, or both!</p>
      </header>
      <main>
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        {error && <p className="error-message">{error}</p>}
        {isLoading && <div className="loader"></div>}
        {/* Pass isLoading to ResultsList */}
        <ResultsList results={results} isLoading={isLoading} /> 
      </main>
    </div>
  );
}

export default App;