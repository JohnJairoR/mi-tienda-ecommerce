import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { CheckCircle, Package, Home, Receipt } from 'lucide-react';
import useCartStore from '../store/cartStore';

const PaymentSuccess = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { clearCart } = useCartStore();
  const [orderData, setOrderData] = useState(null);

  useEffect(() => {
    // Limpiar el carrito
    clearCart();

    // Obtener datos de la orden guardada
    const savedOrder = localStorage.getItem('pending_order');
    if (savedOrder) {
      setOrderData(JSON.parse(savedOrder));
      localStorage.removeItem('pending_order');
    }

    // Obtener parámetros de Mercado Pago
    const paymentId = searchParams.get('payment_id');
    const status = searchParams.get('status');
    const externalReference = searchParams.get('external_reference');
    const preferenceId = searchParams.get('preference_id');

    console.log('✅ Pago exitoso:', {
      paymentId,
      status,
      externalReference,
      preferenceId
    });

    // Aquí podrías hacer una llamada a tu backend para confirmar el pago
    // y actualizar el estado de la orden
  }, [searchParams, clearCart]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-2xl mx-auto">
          {/* Card principal */}
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            {/* Ícono de éxito */}
            <div className="mb-6">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto animate-bounce">
                <CheckCircle className="w-12 h-12 text-green-600" />
              </div>
            </div>

            {/* Título */}
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              ¡Pago Exitoso!
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Tu pedido ha sido procesado correctamente
            </p>

            {/* Información del pago */}
            <div className="bg-gray-50 rounded-xl p-6 mb-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                <div>
                  <p className="text-sm text-gray-500 mb-1">ID de Pago</p>
                  <p className="font-semibold text-gray-900">
                    {searchParams.get('payment_id') || 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Estado</p>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                    Aprobado
                  </span>
                </div>
                {orderData && (
                  <>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">Total Pagado</p>
                      <p className="font-semibold text-gray-900">
                        ${orderData.total.toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">Productos</p>
                      <p className="font-semibold text-gray-900">
                        {orderData.items.length} artículo(s)
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Detalles de la orden */}
            {orderData && (
              <div className="bg-blue-50 rounded-xl p-6 mb-8 text-left">
                <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <Package size={20} />
                  Resumen de tu pedido
                </h3>
                <div className="space-y-2">
                  {orderData.items.map((item, index) => (
                    <div key={index} className="flex justify-between text-sm">
                      <span className="text-gray-600">
                        {item.name} x{item.quantity}
                      </span>
                      <span className="font-medium">
                        ${(item.price * item.quantity).toFixed(2)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Información de envío */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-8">
              <p className="text-sm text-yellow-800">
                📧 Te hemos enviado un email de confirmación a{' '}
                <span className="font-semibold">
                  {orderData?.customer?.email || 'tu correo'}
                </span>
              </p>
            </div>

            {/* Próximos pasos */}
            <div className="text-left mb-8">
              <h3 className="font-semibold text-gray-900 mb-3">
                ¿Qué sigue?
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-0.5">✓</span>
                  <span>Recibirás un email con los detalles de tu pedido</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-0.5">✓</span>
                  <span>Procesaremos tu pedido en las próximas 24 horas</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-0.5">✓</span>
                  <span>Te notificaremos cuando tu pedido sea enviado</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-0.5">✓</span>
                  <span>El envío llegará en 3-5 días hábiles</span>
                </li>
              </ul>
            </div>

            {/* Botones de acción */}
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                onClick={() => navigate('/')}
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
              >
                <Home size={20} />
                Volver al inicio
              </button>
              <button
                onClick={() => navigate('/products')}
                className="flex-1 bg-white border-2 border-blue-600 text-blue-600 py-3 px-6 rounded-xl font-semibold hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
              >
                <Package size={20} />
                Seguir comprando
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
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaymentSuccess;