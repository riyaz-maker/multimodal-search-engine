import ProductCard from './ProductCard';
function ResultsList({ results, isLoading }) {
  if (isLoading) {
    return null;
  }
  
  if (!results || results.length === 0) {
    return <p className="no-results">No products found. Try a different search!</p>;
  }

  return (
    <div className="results-list">
      {results.map((product) => (
        <ProductCard key={product.article_id} product={product} />
      ))}
    </div>
  );
}

export default ResultsList;