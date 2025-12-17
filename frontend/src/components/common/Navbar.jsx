import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Home, Package, User, LogOut } from 'lucide-react';
import { useCart } from '../../store/CartContext';

const Navbar = () => {
  const navigate = useNavigate();
  const { getItemsCount } = useCart();
  const itemsCount = getItemsCount();

  // Verificar si el usuario está logueado
  const isLoggedIn = localStorage.getItem('token');
  const user = isLoggedIn ? JSON.parse(localStorage.getItem('user') || '{}') : null;

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Package className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900">Mi Tienda</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className="flex items-center space-x-1 text-gray-700 hover:text-blue-600 transition-colors"
            >
              <Home size={20} />
              <span>Inicio</span>
            </Link>

            <Link
              to="/products"
              className="flex items-center space-x-1 text-gray-700 hover:text-blue-600 transition-colors"
            >
              <Package size={20} />
              <span>Productos</span>
            </Link>
          </div>

          {/* Right side icons */}
          <div className="flex items-center space-x-4">
            {/* Cart */}
            <Link
              to="/cart"
              className="relative p-2 text-gray-700 hover:text-blue-600 transition-colors"
            >
              <ShoppingCart size={24} />
              {itemsCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center animate-pulse">
                  {itemsCount}
                </span>
              )}
            </Link>

            {/* User */}
            {isLoggedIn ? (
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-700 hidden md:block">
                  {user?.email}
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 text-gray-700 hover:text-red-600 transition-colors"
                >
                  <LogOut size={20} />
                  <span className="hidden md:block">Salir</span>
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="flex items-center space-x-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                <User size={20} />
                <span>Iniciar Sesión</span>
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className="md:hidden border-t border-gray-200">
        <div className="flex justify-around py-2">
          <Link
            to="/"
            className="flex flex-col items-center text-gray-700 hover:text-blue-600 transition-colors"
          >
            <Home size={20} />
            <span className="text-xs mt-1">Inicio</span>
          </Link>

          <Link
            to="/products"
            className="flex flex-col items-center text-gray-700 hover:text-blue-600 transition-colors"
          >
            <Package size={20} />
            <span className="text-xs mt-1">Productos</span>
          </Link>

          <Link
            to="/cart"
            className="flex flex-col items-center text-gray-700 hover:text-blue-600 transition-colors relative"
          >
            <ShoppingCart size={20} />
            <span className="text-xs mt-1">Carrito</span>
            {itemsCount > 0 && (
              <span className="absolute -top-1 right-2 bg-red-500 text-white text-xs font-bold rounded-full h-4 w-4 flex items-center justify-center">
                {itemsCount}
              </span>
            )}
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;