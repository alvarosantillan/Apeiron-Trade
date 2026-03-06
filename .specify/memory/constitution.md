<!--
Sync Impact Report:
- Version: 0.0.0 → 1.0.0
- Initial constitution creation for TRDIA (Trading IA) project
- Modified principles: N/A (initial creation)
- Added sections: All core principles, technology stack, security, development workflow, governance
- Templates requiring updates: ✅ All templates will be aligned with these principles
- Follow-up TODOs: None
-->

# TRDIA Constitution
<!-- Trading con IA - Aplicación Móvil de Trading Automatizado -->

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**Especificaciones antes que código. Siempre.**

- Toda feature DEBE tener una especificación completa en `.specify/` antes de iniciar implementación
- Las especificaciones DEBEN incluir:
  - Descripción funcional clara y no ambigua
  - Contratos de API (OpenAPI/Swagger)
  - Modelos de datos (schemas de DB y Pydantic)
  - Casos de prueba esperados
  - Consideraciones de seguridad
  - Dependencias internas y externas
- Las especificaciones son la fuente de verdad; el código las implementa
- GitHub Copilot y herramientas IA DEBEN usar las specs como contexto primario
- Cambios arquitectónicos DEBEN detectarse en fase de spec, no en fase de código

**Rationale**: Con dinero real en juego (Binance, MercadoPago) y decisiones autónomas del agente IA, no podemos permitirnos descubrir problemas arquitectónicos durante la implementación. El diseño cuidadoso previo es obligatorio.

### II. Test-Driven Development (NON-NEGOTIABLE)

**Tests primero, código después. Sin excepciones.**

- Ciclo TDD estricto: RED (test falla) → GREEN (implementación mínima) → REFACTOR
- Coverage mínimo obligatorio: 80% global, 90% en componentes críticos
- Componentes críticos (requieren 90%+ coverage):
  - Trading engine (ejecución de órdenes)
  - Payment webhooks (MercadoPago)
  - Subscription validation (límites de planes)
  - AI agent core (decisiones de trading)
  - Security modules (encriptación de API keys)
- Tests DEBEN ejecutarse en CI/CD; PRs sin tests passing no se fusionan
- Mocks obligatorios para APIs externas (Binance Testnet, MercadoPago Sandbox)
- Integration tests DEBEN validar contratos entre servicios

**Rationale**: En producción, un bug puede significar pérdidas de dinero real o fallos de cobro. Los tests nos dan la confianza necesaria para refactorizar y escalar sin miedo.

### III. Security-First (NON-NEGOTIABLE)

**La seguridad no es opcional; es el fundamento.**

- Credenciales sensibles DEBEN:
  - Cifrarse en backend con AES-256 (Fernet)
  - Nunca exponerse en frontend, logs, o respuestas API
  - Incluir rate limiting por usuario (10 req/min)
- Validación estricta de entrada en TODOS los endpoints:
  - Sanitización contra SQL injection
  - Validación de tipos con Pydantic
  - Límites de tamaño de payload
- Auditoría completa:
  - Logs de TODAS las operaciones de trading (éxito/fallo)
  - Logs de intentos de autenticación
  - Logs de cambios de plan/suscripción
  - Logs de acceso a credenciales Binance
- Gestión de secretos:
  - Variables de entorno para credenciales (`.env`)
  - Nunca commits de secretos en Git
  - Rotación periódica de JWT secrets
- Autenticación:
  - JWT + refresh tokens obligatorio
  - OAuth con Google/Facebook mediante proveedores oficiales
  - Expiración de tokens: 15 min (access), 7 días (refresh)

**Rationale**: Manejamos dinero real en exchanges, datos de tarjetas de crédito (MercadoPago), y API keys de usuarios. Una brecha de seguridad destruiría la confianza y el negocio.

### IV. Modularidad y Escalabilidad

**Arquitectura preparada para crecer desde día 1.**

- Backend organizado en módulos independientes:
  - `api/` - Endpoints FastAPI
  - `trading/` - Integración Binance + ejecución de órdenes
  - `agents/` - Core del agente IA multi-provider
  - `strategies/` - Motor de estrategias de trading
  - `analytics/` - Análisis técnico (TA-Lib, pandas-ta)
  - `workers/` - Tareas asíncronas (Celery)
- Cada módulo DEBE ser:
  - Independientemente testeable
  - Con interfaces claras (duck typing / protocols)
  - Documentado (docstrings + README)
- Preparación para microservicios:
  - `agents/` diseñado para extraerse como servicio separado si escala
  - Comunicación via APIs REST (posible migración a gRPC)
- Base de datos externa (PostgreSQL no dockerizada) para facilitar backups y escalado independiente

**Rationale**: El agente IA puede generar alta carga computacional. La arquitectura modular permite escalar componentes específicos sin rediseñar todo el sistema.

### V. Validation-Strict (Planes y Operaciones)

**Los límites de planes se validan SIEMPRE en backend. Sin confianza en frontend.**

- Validación de operaciones DEBE ocurrir en backend antes de ejecutar en Binance:
  - Plan activo y vigente (no vencido)
  - Límite semanal no excedido (Free: 1, Plus: 10, Premium: ilimitado)
  - Balance suficiente en cuenta Binance
  - Credenciales API configuradas y válidas
  - Activos permitidos según plan
  - Capital máximo por operación respetado (Free: 10%, Plus: 20%, Premium: 50%)
  - Stop-loss obligatorio para Free/Plus
- Cada transacción cuenta como operación:
  - 1 BUY = 1 operación
  - 1 SELL = 1 operación
  - Stop-loss ejecutado NO cuenta (protección)
- Paper trading (simulación) NO consume límite de operaciones (ilimitado para todos los planes)
- Reset semanal automático (cronjob todos los lunes 00:00 UTC)
- Frontend solo muestra estado; NUNCA decide si permitir operación

**Rationale**: La lógica de negocio del freemium reside en los límites. Si el frontend pudiera bypassearlos, perdemos el modelo de monetización. La validación estricta asegura que solo usuarios pagados accedan a features premium.

### VI. Observability y Auditoría

**Debugging eficiente y trazabilidad completa de operaciones.**

- Logging estructurado (JSON) en todos los componentes:
  - Nivel DEBUG en desarrollo
  - Nivel INFO en producción
  - Nivel ERROR siempre capturado con contexto completo
- Métricas clave (Prometheus/OpenTelemetry):
  - `trades.executed.count` - Contador de trades exitosos
  - `trades.failed.count` - Contador de trades fallidos
  - `trades.execution_time` - Latencia de ejecución
  - `binance.api.latency` - Latencia de Binance API
  - `ai_agent.decision_time` - Tiempo de decisión del agente
  - `subscriptions.active` - Suscripciones activas por plan
- Alertas críticas:
  - Tasa de error de Binance API > 5% (ventana 5 min)
  - Tiempo de ejecución de trade > 5s (P95)
  - Fallos de webhook MercadoPago
  - Suscripción expirada con operaciones intentadas
- Logs NUNCA deben contener:
  - API keys completas (solo últimos 4 caracteres)
  - Secretos de MercadoPago
  - Contraseñas o tokens

**Rationale**: Con un agente IA tomando decisiones autónomas, necesitamos visibilidad total para debugging, análisis post-mortem de trades, y cumplimiento regulatorio (auditoría de transacciones).

### VII. Progressive Enhancement (Features Incrementales)

**Empezar simple, iterar rápido, agregar complejidad solo cuando se necesita.**

- V1.0 (MVP):
  - Solo Spot trading (sin Futures)
  - Estrategias predefinidas (no custom scripts)
  - Solo MercadoPago (no Stripe/PayPal inicialmente)
  - Análisis técnico básico (10-15 indicadores)
- Futures para V2.0 (solo plan Premium, con modo experto)
- Principio YAGNI (You Aren't Gonna Need It):
  - No optimizaciones prematuras
  - No features especulativos
  - Validar con usuarios antes de agregar complejidad
- Cada nueva feature DEBE tener spec + tests antes de merge

**Rationale**: El trading con IA es complejo. Agregar Futures, múltiples exchanges, o estrategias altamente customizables sin validar el core sería desarrollar features que nadie usa. Iteramos basándonos en feedback real.

## Technology Stack (IMMUTABLE in V1.0)

**Stack tecnológico definido para evitar parálisis de decisión.**

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Validación**: Pydantic V2
- **Workers**: Celery + Redis
- **Testing**: pytest + pytest-asyncio + pytest-cov
- **Seguridad**: python-jose (JWT), cryptography (Fernet)

### Frontend
- **Framework**: React Native (Expo)
- **UI Kit**: Cryptocurrency App UI Kit (o similar fintech)
- **Estado**: Redux Toolkit
- **Navegación**: React Navigation (bottom tabs + stack)
- **Testing**: Jest + React Native Testing Library

### Integrations
- **Exchange**: Binance Spot API (ccxt library)
- **Payments**: MercadoPago SDK
- **AI Providers**: OpenAI, Groq, DeepSeek, Gemini (vía SDKs oficiales)
- **Análisis Técnico**: pandas-ta, TA-Lib

### Infrastructure
- **Database**: PostgreSQL 15+ (externa, no dockerizada)
- **Cache**: Redis 7+
- **Containerización**: Docker + docker-compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana (futuro)

**Cambios de stack requieren aprobación explícita y migración documentada.**

## Security Requirements

### Encryption
- API keys de Binance: AES-256 con Fernet (key derivada de `USER_ID` + secret global)
- Contraseñas: bcrypt con salt automático
- JWT: RS256 (asimétrico) para producción

### Rate Limiting
- Endpoints públicos: 100 req/min por IP
- Endpoints autenticados: 10 req/min por usuario (trading), 50 req/min (lectura)
- Webhooks: IP whitelist de MercadoPago

### Compliance
- GDPR: Derecho al olvido implementado (borrado de datos)
- CCPA: Exportación de datos de usuario disponible
- Logs de auditoría retenidos 2 años mínimo

## Development Workflow

### Branching Strategy
- `main` - Producción (protegido)
- `develop` - Integración de features
- `feature/*` - Nuevas features (desde develop)
- `hotfix/*` - Fixes urgentes (desde main)

### PR Requirements
- ✅ Tests passing (CI)
- ✅ Coverage ≥ 80% (componentes críticos ≥ 90%)
- ✅ Spec documentation actualizada
- ✅ Code review aprobado (1 reviewer mínimo)
- ✅ No secrets en código
- ✅ Changelog actualizado

### CI/CD Pipeline
1. Lint (flake8, black, isort en Python; ESLint en React Native)
2. Tests unitarios + integration
3. Security scan (dependencias vulnerables)
4. Build Docker images
5. Deploy a staging (automático desde develop)
6. Deploy a producción (manual desde main)

## Governance

**Esta constitución es la ley suprema del proyecto.**

- Todos los PRs, code reviews, y decisiones arquitectónicas DEBEN cumplir estos principios
- Violaciones a principios NON-NEGOTIABLE requieren justificación explícita y aprobación del maintainer
- Amendments (cambios a la constitución):
  - Propuesta documentada en issue
  - Discusión con stakeholders
  - Plan de migración (si afecta código existente)
  - Actualización de version (MAJOR/MINOR/PATCH según impacto)
  - Sincronización con templates en `.specify/templates/`
- Complejidad técnica DEBE justificarse con métricas o necesidad de negocio clara
- Para guía operacional en runtime: consultar `.specify/templates/*.md`

**Esta constitución aplica a todo código, documentación, y decisiones del proyecto TRDIA.**

**Version**: 1.0.0 | **Ratified**: 2026-03-05 | **Last Amended**: 2026-03-05
