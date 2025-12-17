import { Link, useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus, ShoppingBag } from 'lucide-react';
import { useCart } from '../store/CartContext';

const Cart = () => {
  const navigate = useNavigate();
  const { cart, removeFromCart, updateQuantity, getTotal, clearCart } = useCart();

  const handleQuantityChange = (productId, currentQuantity, change) => {
    const newQuantity = currentQuantity + change;
    if (newQuantity > 0) {
      updateQuantity(productId, newQuantity);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-md mx-auto text-center">
          <ShoppingBag className="mx-auto h-24 w-24 text-gray-400 mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Tu carrito está vacío
          </h2>
          <p className="text-gray-600 mb-6">
            Agrega productos para comenzar a comprar
          </p>
          <Link
            to="/products"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Explorar Productos
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Carrito de Compras
      </h1>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Lista de productos */}
        <div className="lg:col-span-2 space-y-4">
          {cart.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-lg shadow-md p-4 flex items-center gap-4"
            >
              {/* Imagen */}
              <Link
                to={`/products/${item.slug}`}
                className="flex-shrink-0 w-24 h-24 bg-gray-100 rounded-lg overflow-hidden"
              >
                <img
                  src={item.image_url || 'https://via.placeholder.com/200'}
                  alt={item.name}
                  className="w-full h-full object-cover hover:scale-110 transition-transform"
                />
              </Link>

              {/* Información */}
              <div className="flex-1">
                <Link
                  to={`/products/${item.slug}`}
                  className="font-semibold text-gray-800 hover:text-blue-600 transition-colors"
                >
                  {item.name}
                </Link>
                <p className="text-sm text-gray-600 mt-1">
                  ${item.price.toFixed(2)} c/u
                </p>

                {/* Controles de cantidad */}
                <div className="flex items-center gap-3 mt-3">
                  <button
                    onClick={() => handleQuantityChange(item.id, item.quantity, -1)}
                    className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <Minus size={16} />
                  </button>

                  <span className="w-12 text-center font-medium">
                    {item.quantity}
                  </span>

                  <button
                    onClick={() => handleQuantityChange(item.id, item.quantity, 1)}
                    disabled={item.quantity >= (item.stock || 100)}
                    className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Plus size={16} />
                  </button>
                </div>
              </div>

              {/* Precio y eliminar */}
              <div className="flex flex-col items-end gap-2">
                <p className="text-lg font-bold text-blue-600">
                  ${(item.price * item.quantity).toFixed(2)}
                </p>
                <button
                  onClick={() => removeFromCart(item.id)}
                  className="text-red-500 hover:text-red-700 transition-colors p-2"
                  title="Eliminar del carrito"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            </div>
          ))}

          {/* Botón limpiar carrito */}
          <button
            onClick={() => {
              if (window.confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
                clearCart();
              }
            }}
            className="text-red-600 hover:text-red-700 text-sm font-medium"
          >
            Vaciar carrito
          </button>
        </div>

        {/* Resumen */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-20">
            <h2 className="text-xl font-semibold mb-4">Resumen del Pedido</h2>

            <div className="space-y-3 mb-6">
              <div className="flex justify-between text-gray-600">
                <span>Subtotal ({cart.length} productos)</span>
                <span className="font-medium">${getTotal().toFixed(2)}</span>
              </div>

              <div className="flex justify-between text-gray-600">
                <span>Envío</span>
                <span className="font-medium text-green-600">Gratis</span>
              </div>

              <div className="border-t border-gray-200 pt-3 flex justify-between">
                <span className="text-lg font-semibold">Total</span>
                <span className="text-2xl font-bold text-blue-600">
                  ${getTotal().toFixed(2)}
                </span>
              </div>
            </div>

            <button
              onClick={() => navigate('/checkout')}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors mb-3"
            >
              Proceder al Pago
            </button>

            <Link
              to="/products"
              className="block w-full text-center text-blue-600 hover:text-blue-700 font-medium"
            >
              Continuar Comprando
            </Link>

            {/* Beneficios */}
            <div className="mt-6 pt-6 border-t border-gray-200 space-y-3 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <span>✓</span>
                <span>Envío gratis en compras mayores a $100</span>
              </div>
              <div className="flex items-center gap-2">
                <span>✓</span>
                <span>Devoluciones gratis dentro de 30 días</span>
              </div>
              <div className="flex items-center gap-2">
                <span>✓</span>
                <span>Pago 100% seguro</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
