import { useState } from 'react';

function SearchBar({ onSearch, isLoading }) {
  const [textQuery, setTextQuery] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(textQuery, imageFile);
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={textQuery}
        onChange={(e) => setTextQuery(e.target.value)}
        placeholder="e.g., 'red summer dress' or 'darker color'"
        className="text-input"
      />
      <label htmlFor="image-upload" className="image-upload-label">
        {imagePreview ? 'Change Image' : 'Upload Image'}
      </label>
      <input
        id="image-upload"
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="image-input"
      />
      <button type="submit" disabled={isLoading} className="search-button">
        {isLoading ? 'Searching...' : 'Search'}
      </button>
      {imagePreview && <img src={imagePreview} alt="Preview" className="image-preview" />}
    </form>
  );
}

export default SearchBar;