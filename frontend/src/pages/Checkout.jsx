import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CreditCard, Smartphone, Building2, CheckCircle, AlertCircle } from 'lucide-react';
import useCartStore from '../store/cartStore';
import api from '../services/api';

const Checkout = () => {
  const navigate = useNavigate();
  const { items, getTotal, clearCart } = useCartStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    documento: '',
    direccion: '',
    ciudad: '',
    codigoPostal: '',
    metodoPago: 'mercadopago',
    notas: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (items.length === 0) {
      alert('Tu carrito está vacío');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Preparar los items para Mercado Pago
      const mercadoPagoItems = items.map(item => ({
        id: item.id.toString(),
        title: item.name,
        description: item.description || item.name,
        picture_url: item.image_url || 'https://via.placeholder.com/500',
        category_id: 'electronics', // Puedes categorizar según tu producto
        quantity: item.quantity,
        unit_price: parseFloat(item.price),
        currency_id: 'PEN' // o 'USD', 'ARS', 'MXN', etc.
      }));

      // Crear la preferencia de pago
      const preferenceData = {
        items: mercadoPagoItems,
        payer: {
          name: formData.nombre,
          surname: formData.apellido,
          email: formData.email,
          phone: {
            area_code: '51', // Código de país Perú
            number: formData.telefono
          },
          identification: {
            type: 'DNI',
            number: formData.documento
          },
          address: {
            street_name: formData.direccion,
            street_number: '',
            zip_code: formData.codigoPostal
          }
        },
        back_urls: {
          success: `${window.location.origin}/payment-success`,
          failure: `${window.location.origin}/payment-failure`,
          pending: `${window.location.origin}/payment-pending`
        },
        auto_return: 'approved',
        payment_methods: {
          excluded_payment_methods: [],
          excluded_payment_types: [],
          installments: 12 // Número máximo de cuotas
        },
        notification_url: `${import.meta.env.VITE_API_URL}/webhooks/mercadopago`,
        statement_descriptor: 'MI TIENDA',
        external_reference: `ORDER-${Date.now()}`, // ID único de tu orden
        metadata: {
          customer_email: formData.email,
          customer_name: `${formData.nombre} ${formData.apellido}`,
          notas: formData.notas
        }
      };

      console.log('📦 Enviando preferencia a Mercado Pago:', preferenceData);

      // Enviar al backend para crear la preferencia
      const response = await api.post('/payments/create-preference', preferenceData);

      console.log('✅ Respuesta de Mercado Pago:', response.data);

      // Redirigir a Mercado Pago
      if (response.data.init_point) {
        // Guardar información de la orden antes de redirigir
        localStorage.setItem('pending_order', JSON.stringify({
          items,
          total: getTotal(),
          customer: formData,
          preference_id: response.data.id,
          date: new Date().toISOString()
        }));

        // Redirigir al checkout de Mercado Pago
        window.location.href = response.data.init_point;
      } else {
        throw new Error('No se recibió el link de pago de Mercado Pago');
      }

    } catch (err) {
      console.error('❌ Error al procesar el pago:', err);
      setError(err.response?.data?.detail || err.message || 'Error al procesar el pago');
      setLoading(false);
    }
  };

  // Manejo de otros métodos de pago
  const handleAlternativePayment = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError(null);

    try {
      const orderData = {
        cliente: {
          nombre: `${formData.nombre} ${formData.apellido}`,
          email: formData.email,
          telefono: formData.telefono,
          direccion: formData.direccion,
          ciudad: formData.ciudad,
          codigoPostal: formData.codigoPostal
        },
        items: items.map(item => ({
          product_id: item.id,
          nombre: item.name,
          cantidad: item.quantity,
          precio: item.price,
          subtotal: item.price * item.quantity
        })),
        total: getTotal(),
        metodoPago: formData.metodoPago,
        notas: formData.notas,
        estado: 'pendiente',
        fecha: new Date().toISOString()
      };

      // Guardar orden en tu backend
      await api.post('/orders/', orderData);

      // Mostrar instrucciones según el método
      let mensaje = '';
      if (formData.metodoPago === 'yape') {
        mensaje = '📱 Instrucciones de pago por Yape:\n\n' +
                 '1. Abre tu app Yape\n' +
                 '2. Escanea el código QR o envía a: 999-999-999\n' +
                 '3. Monto: S/. ' + getTotal().toFixed(2) + '\n' +
                 '4. Envía tu comprobante a: pagos@mitienda.com\n\n' +
                 'Procesaremos tu pedido al confirmar el pago.';
      } else if (formData.metodoPago === 'transferencia') {
        mensaje = '🏦 Instrucciones de transferencia bancaria:\n\n' +
                 'Banco: BCP\n' +
                 'Cuenta: 123-456-789-0\n' +
                 'CCI: 00212345678900123456\n' +
                 'Monto: S/. ' + getTotal().toFixed(2) + '\n\n' +
                 'Envía tu voucher a: pagos@mitienda.com';
      }

      alert('¡Orden creada exitosamente! 🎉\n\n' + mensaje);
      clearCart();
      navigate('/');

    } catch (err) {
      console.error('Error:', err);
      setError('Error al crear la orden. Por favor intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-md mx-auto">
          <div className="text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Tu carrito está vacío
          </h2>
          <button
            onClick={() => navigate('/products')}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Ir a comprar
          </button>
        </div>
      </div>
    );
  }

  const handleFormSubmit = formData.metodoPago === 'mercadopago'
    ? handleSubmit
    : handleAlternativePayment;

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Finalizar Compra</h1>
        <p className="text-gray-600 mb-8">Complete los datos para procesar su pedido</p>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <h3 className="font-semibold text-red-800 mb-1">Error al procesar el pago</h3>
              <p className="text-sm text-red-600">{error}</p>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Formulario */}
          <div className="lg:col-span-2">
            <form onSubmit={handleFormSubmit} className="space-y-6">
              {/* Información personal */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="bg-blue-100 text-blue-600 w-8 h-8 rounded-full flex items-center justify-center font-bold">1</span>
                  Información Personal
                </h2>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nombre *
                    </label>
                    <input
                      type="text"
                      name="nombre"
                      required
                      value={formData.nombre}
                      onChange={handleInputChange}
                      placeholder="Juan"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Apellido *
                    </label>
                    <input
                      type="text"
                      name="apellido"
                      required
                      value={formData.apellido}
                      onChange={handleInputChange}
                      placeholder="Pérez"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      name="email"
                      required
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="ejemplo@correo.com"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Teléfono *
                    </label>
                    <input
                      type="tel"
                      name="telefono"
                      required
                      value={formData.telefono}
                      onChange={handleInputChange}
                      placeholder="999999999"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    DNI / Documento *
                  </label>
                  <input
                    type="text"
                    name="documento"
                    required
                    value={formData.documento}
                    onChange={handleInputChange}
                    placeholder="12345678"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Dirección */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="bg-blue-100 text-blue-600 w-8 h-8 rounded-full flex items-center justify-center font-bold">2</span>
                  Dirección de Envío
                </h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Dirección completa *
                    </label>
                    <input
                      type="text"
                      name="direccion"
                      required
                      value={formData.direccion}
                      onChange={handleInputChange}
                      placeholder="Av. Ejemplo 123, Dpto 456"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Ciudad *
                      </label>
                      <input
                        type="text"
                        name="ciudad"
                        required
                        value={formData.ciudad}
                        onChange={handleInputChange}
                        placeholder="Lima"
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Código Postal
                      </label>
                      <input
                        type="text"
                        name="codigoPostal"
                        value={formData.codigoPostal}
                        onChange={handleInputChange}
                        placeholder="15001"
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Método de pago */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="bg-blue-100 text-blue-600 w-8 h-8 rounded-full flex items-center justify-center font-bold">3</span>
                  Método de Pago
                </h2>
                <div className="space-y-3">
                  <label className="flex items-center p-4 border-2 border-gray-300 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50">
                    <input
                      type="radio"
                      name="metodoPago"
                      value="mercadopago"
                      checked={formData.metodoPago === 'mercadopago'}
                      onChange={handleInputChange}
                      className="mr-4"
                    />
                    <CreditCard className="mr-3 text-blue-600" size={24} />
                    <div className="flex-1">
                      <span className="font-medium block">Mercado Pago</span>
                      <p className="text-sm text-gray-500">Tarjetas, Yape, Plin y más</p>
                    </div>
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">Recomendado</span>
                  </label>

                  <label className="flex items-center p-4 border-2 border-gray-300 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50">
                    <input
                      type="radio"
                      name="metodoPago"
                      value="yape"
                      checked={formData.metodoPago === 'yape'}
                      onChange={handleInputChange}
                      className="mr-4"
                    />
                    <Smartphone className="mr-3 text-purple-600" size={24} />
                    <div className="flex-1">
                      <span className="font-medium block">Yape / Plin</span>
                      <p className="text-sm text-gray-500">Pago manual - Recibirás instrucciones</p>
                    </div>
                  </label>

                  <label className="flex items-center p-4 border-2 border-gray-300 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50">
                    <input
                      type="radio"
                      name="metodoPago"
                      value="transferencia"
                      checked={formData.metodoPago === 'transferencia'}
                      onChange={handleInputChange}
                      className="mr-4"
                    />
                    <Building2 className="mr-3 text-green-600" size={24} />
                    <div className="flex-1">
                      <span className="font-medium block">Transferencia Bancaria</span>
                      <p className="text-sm text-gray-500">Depósito - Recibirás datos bancarios</p>
                    </div>
                  </label>
                </div>
              </div>

              {/* Botón */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Procesando...
                  </>
                ) : (
                  <>
                    <CheckCircle size={20} />
                    {formData.metodoPago === 'mercadopago'
                      ? `Pagar con Mercado Pago - $${getTotal().toFixed(2)}`
                      : `Confirmar Pedido - $${getTotal().toFixed(2)}`
                    }
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Resumen */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-md p-6 sticky top-4">
              <h2 className="text-xl font-semibold mb-4">Resumen del Pedido</h2>

              <div className="space-y-3 mb-4 max-h-64 overflow-y-auto">
                {items.map(item => (
                  <div key={item.id} className="flex gap-3 pb-3 border-b border-gray-100">
                    <img
                      src={item.image_url || 'https://via.placeholder.com/80'}
                      alt={item.name}
                      className="w-16 h-16 object-cover rounded-lg"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {item.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {item.quantity} x ${item.price.toFixed(2)}
                      </p>
                      <p className="text-sm font-semibold text-blue-600">
                        ${(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="border-t border-gray-200 pt-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Subtotal</span>
                  <span className="font-medium">${getTotal().toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Envío</span>
                  <span className="font-medium text-green-600">Gratis</span>
                </div>
                <div className="border-t border-gray-200 pt-2 flex justify-between">
                  <span className="text-lg font-semibold">Total</span>
                  <span className="text-2xl font-bold text-blue-600">
                    ${getTotal().toFixed(2)}
                  </span>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="space-y-2 text-xs text-gray-500">
                  <div className="flex items-center gap-2">
                    <span>🔒</span>
                    <span>Pago 100% seguro con Mercado Pago</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>🚚</span>
                    <span>Envío en 3-5 días hábiles</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>↩️</span>
                    <span>Devoluciones gratis hasta 30 días</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span>💳</span>
                    <span>Hasta 12 cuotas sin interés</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
