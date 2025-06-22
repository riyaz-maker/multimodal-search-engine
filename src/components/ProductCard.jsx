function ProductCard({ product }) {
  const imageUrl = `http://localhost:8001/${product.image_path}`;

  return (
    <div className="product-card">
      <img src={imageUrl} alt={product.prod_name} className="product-image" loading="lazy" />
      <div className="product-info">
        <h3 className="product-name">{product.prod_name}</h3>
      </div>
    </div>
  );
}

export default ProductCard;