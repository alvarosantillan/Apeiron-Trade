Prompt refinado para generación de aplicación móvil

Objetivo general
Desarrollar una aplicación móvil moderna de trading automatizado con inteligencia artificial, orientada a criptomonedas, con arquitectura escalable, seguridad de nivel productivo y experiencia de usuario profesional.

1. Frontend (Aplicación móvil)

Crear una aplicación móvil multiplataforma (Android e iOS) con diseño moderno basado en Cryptocurrency App UI Kit (estilo fintech, dark/light mode).

Framework recomendado: React Native (Expo o CLI) o Flutter.

Navegación por menú principal (bottom tabs + stack navigation).

Secciones mínimas:

Dashboard (resumen de cuenta, operaciones, estado del bot)

Autenticación / Perfil

Configuración del Bot IA

Estrategias de Trading

Binance / Exchanges

Suscripción y Pagos

Historial de Operaciones

Ajustes / Seguridad

2. Autenticación y usuarios

Implementar autenticación segura mediante:

Google OAuth

Facebook OAuth

Registro tradicional (email + password)

Uso de JWT + refresh tokens.

Gestión de roles:

Usuario Free

Usuario Plus

Usuario Premium

3. Integración con Binance (Trading)

Permitir configurar credenciales API de Binance:

API Key

Secret Key

Las credenciales deben:

Guardarse cifradas en backend

Nunca exponerse en el frontend

Integración vía Binance API oficial

El sistema debe permitir:

Operaciones spot

Ejecución automática de órdenes

Modo simulación (paper trading)

4. Agente de Inteligencia Artificial (Core del sistema)

Implementar un agente de IA para trading automatizado.

El usuario debe poder:

Configurar estrategias de trading personalizadas

Estas estrategias se incorporan dinámicamente al system prompt del agente

El agente debe poder usar múltiples proveedores de IA:

OpenAI (GPT)

Groq

DeepSeek

Gemini

Arquitectura extensible para nuevos proveedores

Selección del proveedor de IA desde la UI.

Parámetros configurables:

Risk management

Timeframe

Activos permitidos

Stop-loss / Take-profit

Límite de operaciones

5. Planes de suscripción

Implementar control estricto por plan:

Plan	Operaciones	Precio
Free	1 operación semanal	$0
Plus	10 operaciones semanales	USD 20 / mes
Premium	Operaciones ilimitadas	USD 200 / mes

Validar límites en backend.

Reset automático semanal.

Bloqueo de operaciones al exceder el límite.

6. Pagos y suscripciones

Integrar la plataforma de pago más popular y ampliamente adoptada (ejemplo:

Stripe

MercadoPago

PayPal

Soporte para:

Suscripciones recurrentes

Webhooks de confirmación de pago

Upgrade / downgrade de plan

Estado de suscripción siempre validado en backend.

7. Backend

Backend RESTful o GraphQL.

Lenguajes recomendados:

Python (Django / FastAPI)

Node.js (NestJS)

Responsabilidades:

Autenticación

Gestión de usuarios

Control de planes

Ejecución del agente IA

Integración Binance

Gestión de pagos

Seguridad:

Rate limiting

Logs de auditoría

Manejo de errores centralizado

8. Base de datos

Base de datos NO dockerizada.

Configuración abierta para conectar a una DB externa:

PostgreSQL (recomendado)

Entidades principales:

Users

Subscriptions

TradingStrategies

AIProviders

Trades

Payments

Logs

9. Dockerización

Dockerizar todo el backend:

API

Servicios de IA

Workers de trading

Usar:

Dockerfile

docker-compose.yml

Variables sensibles por ENV.

Excluir la base de datos del stack Docker.

10. Build móvil (APK / IPA)

El frontend debe:

Usar una imagen Docker para build

Permitir generar:

APK (Android)

IPA (iOS)

Preparado para testing en dispositivos físicos.

Compatible con CI/CD.

11. Requisitos no funcionales

Arquitectura modular y escalable.

Código limpio y documentado.

Preparado para producción.

UX orientada a fintech/trading profesional.