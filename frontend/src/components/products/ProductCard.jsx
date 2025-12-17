import { Link } from 'react-router-dom';
import { ShoppingCart } from 'lucide-react';
import { useCart } from '../../store/CartContext';

const ProductCard = ({ product }) => {
  const { addToCart } = useCart();

  const handleAddToCart = (e) => {
    e.preventDefault(); // Evitar que navegue al hacer clic en el botón
    e.stopPropagation();
    addToCart(product, 1);

    // Mostrar feedback al usuario
    const button = e.currentTarget;
    const originalText = button.innerHTML;
    button.innerHTML = '✓ Agregado';
    button.classList.add('bg-green-600');

    setTimeout(() => {
      button.innerHTML = originalText;
      button.classList.remove('bg-green-600');
    }, 1500);
  };

  return (
    <Link
      to={`/products/${product.slug}`}
      className="group bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden"
    >
      {/* Imagen */}
      <div className="relative aspect-square overflow-hidden bg-gray-100">
        <img
          src={product.image_url || 'https://via.placeholder.com/400'}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
        />

        {/* Badge de stock */}
        {product.stock > 0 ? (
          product.stock < 10 && (
            <div className="absolute top-3 right-3 bg-orange-500 text-white text-xs font-semibold px-2 py-1 rounded-full">
              ¡Solo {product.stock}!
            </div>
          )
        ) : (
          <div className="absolute top-3 right-3 bg-red-500 text-white text-xs font-semibold px-3 py-1 rounded-full">
            Agotado
          </div>
        )}
      </div>

      {/* Información */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
          {product.name}
        </h3>

        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {product.description}
        </p>

        <div className="flex items-center justify-between">
          <div>
            <span className="text-2xl font-bold text-blue-600">
              ${product.price.toFixed(2)}
            </span>
          </div>

          <button
            onClick={handleAddToCart}
            disabled={product.stock === 0}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            <ShoppingCart size={18} />
            <span className="text-sm font-medium">Agregar</span>
          </button>
        </div>
      </div>
    </Link>
  );
};

export default ProductCard;