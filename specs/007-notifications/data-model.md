# Data Model: TRDIA - Notifications and Alerts

**Feature**: `007-notifications`  
**Date**: 2026-03-06

## Entity: PushDeviceToken

- Purpose: Representar tokens de dispositivos para entrega push.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `device_id` (string)
  - `platform` (enum: IOS, ANDROID)
  - `push_token` (text, protected)
  - `is_active` (bool)
  - `last_seen_at` (timestamp)
  - `created_at` (timestamp)
  - `updated_at` (timestamp)
- Validation Rules:
  - `device_id` único por usuario/plataforma.
  - Tokens inválidos se marcan `is_active=false`.

## Entity: NotificationPreference

- Purpose: Guardar preferencias por categoría de notificación del usuario.
- Fields:
  - `id` (UUID)
  - `user_id` (UUID, FK)
  - `category` (enum: TRADING, SUBSCRIPTION, SECURITY, SYSTEM, MARKETING)
  - `enabled` (bool)
  - `updated_at` (timestamp)
- Validation Rules:
  - Un registro por `user_id + category`.
  - Categoría `SECURITY` puede forzarse por política crítica.

## Entity: NotificationEvent

- Purpose: Evento lógico que origina una o múltiples entregas.
- Fields:
  - `id` (UUID)
  - `event_id` (string, unique)
  - `user_id` (UUID, FK)
  - `category` (enum)
  - `priority` (enum: CRITICAL, HIGH, NORMAL, LOW)
  - `title` (string)
  - `message` (string)
  - `reference_id` (string, nullable)
  - `payload` (jsonb, sanitized)
  - `created_at` (timestamp)
- Validation Rules:
  - `event_id` idempotente.
  - Payload sin datos sensibles.

## Entity: NotificationDelivery

- Purpose: Resultado de envío por evento y dispositivo.
- Fields:
  - `id` (UUID)
  - `event_id` (UUID, FK -> NotificationEvent)
  - `device_token_id` (UUID, FK -> PushDeviceToken)
  - `status` (enum: QUEUED, SENT, DELIVERED, FAILED, DROPPED)
  - `attempt_count` (integer)
  - `last_error` (text, nullable)
  - `sent_at` (timestamp, nullable)
  - `delivered_at` (timestamp, nullable)
  - `updated_at` (timestamp)
- Validation Rules:
  - Constraint única `event_id + device_token_id`.
  - `attempt_count >= 0`.

## Relationships

- `User` 1..N `PushDeviceToken`
- `User` 1..N `NotificationPreference`
- `User` 1..N `NotificationEvent`
- `NotificationEvent` 1..N `NotificationDelivery`
- `PushDeviceToken` 1..N `NotificationDelivery`

## State Transitions

## NotificationDelivery Lifecycle

- `QUEUED` -> `SENT` -> `DELIVERED`
- `SENT` -> `FAILED` (error transitorio)
- `FAILED` -> `QUEUED` (reintento)
- `SENT|FAILED` -> `DROPPED` (token inválido/permanente)

## Preference Enforcement

- Si `enabled=false` para categoría no crítica, no crear `NotificationDelivery`.
- Para eventos críticos (`SECURITY` o `CRITICAL`), crear entrega aunque categoría opcional esté desactivada según política.
