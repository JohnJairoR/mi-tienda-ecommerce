import { useNavigate, useSearchParams } from 'react-router-dom';
import { XCircle, ShoppingCart, CreditCard } from 'lucide-react';

const PaymentFailure = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const paymentId = searchParams.get('payment_id');
  const status = searchParams.get('status');

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-2xl mx-auto">
          {/* Card principal */}
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            {/* Ícono de error */}
            <div className="mb-6">
              <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto">
                <XCircle className="w-12 h-12 text-red-600" />
              </div>
            </div>

            {/* Título */}
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Pago Rechazado
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              No pudimos procesar tu pago
            </p>

            {/* Información del error */}
            <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8 text-left">
              <h3 className="font-semibold text-red-900 mb-2">
                ¿Qué pudo haber pasado?
              </h3>
              <ul className="space-y-2 text-sm text-red-800">
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>Fondos insuficientes en tu tarjeta</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>Datos de la tarjeta incorrectos</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>La tarjeta fue rechazada por el banco emisor</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>Límite de compra excedido</span>
                </li>
              </ul>
            </div>

            {/* Detalles técnicos */}
            {paymentId && (
              <div className="bg-gray-50 rounded-xl p-4 mb-8 text-sm text-gray-600">
                <p>ID de intento de pago: <span className="font-mono">{paymentId}</span></p>
                <p>Estado: <span className="font-semibold text-red-600">{status || 'Rechazado'}</span></p>
              </div>
            )}

            {/* Recomendaciones */}
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8 text-left">
              <h3 className="font-semibold text-blue-900 mb-3">
                💡 Recomendaciones
              </h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Verifica los datos de tu tarjeta e intenta nuevamente</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Contacta a tu banco para autorizar la compra</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Intenta con otro método de pago</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Usa otra tarjeta de crédito o débito</span>
                </li>
              </ul>
            </div>

            {/* Botones de acción */}
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={() => navigate('/checkout')}
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
              >
                <CreditCard size={20} />
                Intentar nuevamente
              </button>
              <button
                onClick={() => navigate('/cart')}
                className="flex-1 bg-white border-2 border-gray-300 text-gray-700 py-3 px-6 rounded-xl font-semibold hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
              >
                <ShoppingCart size={20} />
                Ver carrito
              </button>
            </div>
          </div>

          {/* Soporte */}
          <div className="text-center mt-8 text-sm text-gray-600">
            <p>
              ¿Necesitas ayuda?{' '}
              <a href="mailto:soporte@mitienda.com" className="text-blue-600 hover:underline">
                Contáctanos
              </a>
              {' '}o llámanos al{' '}
              <a href="tel:+51999999999" className="text-blue-600 hover:underline">
                +51 999 999 999
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentFailure;