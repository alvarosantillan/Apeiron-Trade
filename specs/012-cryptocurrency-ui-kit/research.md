# Research: Cryptocurrency UI Kit Integration (Iteracion 1)

**Feature**: `012-cryptocurrency-ui-kit`  
**Date**: 2026-03-10  
**Spec**: `specs/012-cryptocurrency-ui-kit/spec.md`

## Decision 1: Integracion del UI Kit por composicion, no por reescritura de flujo

- Decision: aplicar el UI Kit sobre `PrivateLayout`, `DashboardPage` y `TradingPage` reutilizando viewmodels y servicios existentes.
- Rationale: reduce riesgo funcional y respeta FR-002, FR-008 y FR-010 (sin cambios de backend ni auth).
- Alternatives considered:
  - Reescribir arquitectura de rutas/layout desde cero: descartado por alto riesgo de regresion.
  - Integracion parcial solo cosmetica sin tokens/patrones del kit: descartado por baja consistencia visual.

## Decision 2: Mantener contratos backend como fuente de verdad

- Decision: no crear endpoints ni alterar payloads; dashboard/trading consumen APIs existentes.
- Rationale: el alcance de la feature es visual y la spec exige preservar contratos backend.
- Alternatives considered:
  - Introducir endpoint agregador para dashboard/trading: descartado por expansion de alcance.
  - Mockear estados UI fuera de respuestas reales: descartado por debilitar regresion funcional.

## Decision 3: Preservar guardas de sesion y navegacion privada

- Decision: mantener comportamiento de `PrivateLayout` y reglas de redireccion (login <-> area privada), cambiando solo presentacion.
- Rationale: evita regresiones de seguridad y cumple SC-001.
- Alternatives considered:
  - Mover validaciones de acceso al cliente por componente: descartado por violar Principle V.
  - Relajar redireccion para mejorar UX visual: descartado por riesgo de acceso no autorizado.

## Decision 4: Contrato transversal de estados UX para Dashboard y Trading

- Decision: estandarizar render de `loading`, `empty`, `error`, `success` con componentes/patrones del UI Kit.
- Rationale: asegura consistencia y cumple FR-005.
- Alternatives considered:
  - Estado visual ad hoc por pantalla: descartado por inconsistencia.
  - Priorizar solo estado `success`: descartado por mala resiliencia UX.

## Decision 5: Responsive y accesibilidad minima como gate de implementacion

- Decision: incluir como criterio obligatorio teclado/focus visible/contraste y validacion en viewport desktop + mobile.
- Rationale: cumple FR-006 y FR-007 sin ampliar alcance funcional.
- Alternatives considered:
  - Tratar accesibilidad y mobile en sprint posterior: descartado por riesgo de deuda inmediata.
  - Optimizar solo desktop: descartado por incumplimiento de spec.

## Decision 6: Riesgo de gobernanza por stack constitucional

- Decision: registrar en plan el riesgo vigente (constitucion sugiere React Native) y tratarlo como pendiente de governance para Sprint 012.
- Rationale: el guardrail de excepciones de Sprint 011 exige revalidacion antes de 012.
- Alternatives considered:
  - Ignorar conflicto y avanzar silenciosamente: descartado por incumplimiento de governance.
  - Frenar planificacion hasta amendment global: descartado porque bloquea el flujo de diseno de feature ya especificada.
