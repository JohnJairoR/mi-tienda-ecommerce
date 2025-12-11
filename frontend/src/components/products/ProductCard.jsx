import { ShoppingCart, Star } from 'lucide-react';
import { Link } from 'react-router-dom';
import useCartStore from '../../store/cartStore';

const ProductCard = ({ product }) => {
  const { addItem } = useCartStore();

  const handleAddToCart = (e) => {
    e.preventDefault();
    addItem(product, 1);
  };

  const discount = product.compare_price
    ? Math.round(((product.compare_price - product.price) / product.compare_price) * 100)
    : 0;

  return (
    <Link
      to={`/products/${product.slug}`}
      className="group bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
    >
      {/* Image */}
      <div className="relative overflow-hidden aspect-square">
        <img
          src={product.image_url || 'https://via.placeholder.com/400'}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
        />

        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-2">
          {product.is_featured && (
            <span className="bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
              <Star className="h-3 w-3 fill-current" />
              Destacado
            </span>
          )}
          {discount > 0 && (
            <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
              -{discount}%
            </span>
          )}
        </div>

        {/* Stock Badge */}
        {product.stock < 10 && product.stock > 0 && (
          <div className="absolute bottom-3 left-3">
            <span className="bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full">
              ¡Solo {product.stock} disponibles!
            </span>
          </div>
        )}

        {product.stock === 0 && (
          <div className="absolute inset-0 bg-black bg-opacity-60 flex items-center justify-center">
            <span className="bg-red-600 text-white text-sm font-bold px-4 py-2 rounded-lg">
              Agotado
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Name */}
        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition line-clamp-2 mb-2">
          {product.name}
        </h3>

        {/* Description */}
        <p className="text-sm text-gray-600 line-clamp-2 mb-3">
          {product.description}
        </p>

        {/* Price & Button */}
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold text-gray-900">
                ${product.price.toFixed(2)}
              </span>
              {product.compare_price && (
                <span className="text-sm text-gray-500 line-through">
                  ${product.compare_price.toFixed(2)}
                </span>
              )}
            </div>
          </div>

          {product.stock > 0 && (
            <button
              onClick={handleAddToCart}
              className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition transform hover:scale-105 active:scale-95"
              title="Agregar al carrito"
            >
              <ShoppingCart className="h-5 w-5" />
            </button>
          )}
        </div>

        {/* SKU */}
        {product.sku && (
          <p className="text-xs text-gray-400 mt-2">SKU: {product.sku}</p>
        )}
      </div>
    </Link>
  );
};

export default ProductCard;