import ProductCard from './ProductCard';

function ResultsList({ results }) {
  if (!results || results.length === 0) {
    return null;
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