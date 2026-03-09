# Research - 003-binance-integration

## Decision 1: Exchange Adapter Strategy

- Decision: Usar un adapter de exchange desacoplado con implementación inicial Binance Spot.
- Rationale: Permite mantener arquitectura extensible sin introducir complejidad de multi-exchange en v1.
- Alternatives considered:
  - Acoplar directamente endpoints a SDK Binance: rechazado por testabilidad y menor mantenibilidad.

## Decision 2: Idempotency for Trade Requests

- Decision: Requerir `request_id` único por operación y persistirlo antes de invocar exchange.
- Rationale: Evita doble ejecución por retries de red o reenvío de app.
- Alternatives considered:
  - Dedupe por payload exacto: rechazado por falsos positivos.

## Decision 3: Retry Policy

- Decision: Reintentos controlados solo para errores transitorios (timeout, 5xx del provider), máximo 3 intentos con backoff.
- Rationale: Minimiza fallos espurios sin duplicar órdenes.
- Alternatives considered:
  - Sin reintentos: rechazado por baja resiliencia.
  - Reintentos ilimitados: rechazado por riesgo operativo.

## Decision 4: Simulation Consistency

- Decision: Paper trading sigue el mismo pipeline de validación de negocio excepto envío a exchange y consumo de límite.
- Rationale: Garantiza que simulación sea representativa de ejecución real.
- Alternatives considered:
  - Simulación simplificada aislada: rechazada por diferencias de comportamiento.

## Decision 5: Credential Handling

- Decision: API Key/Secret Key cifradas en backend y desencriptado solo en runtime de ejecución.
- Rationale: Cumple constitution Security-First y reduce superficie de exposición.
