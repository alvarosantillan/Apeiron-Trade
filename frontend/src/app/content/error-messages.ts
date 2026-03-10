export const errorMessages: Record<string, string> = {
  NETWORK_ERROR: "Problema de red. Verifica tu conexion e intenta nuevamente.",
  UNAUTHORIZED: "Tu sesion expiro. Vuelve a iniciar sesion.",
  FORBIDDEN: "No tienes permisos para realizar esta accion.",
  VALIDATION_ERROR: "Revisa simbolo, cantidad y credenciales antes de reintentar.",
  SERVER_ERROR: "El servicio no esta disponible temporalmente.",
  UNKNOWN_ERROR: "Ocurrio un error inesperado.",
  DASHBOARD_EMPTY: "Aun no hay operaciones en el historial. Realiza una orden para ver resultados.",
  DASHBOARD_LOAD_ERROR: "No pudimos actualizar el dashboard. Intenta nuevamente.",
  TRADING_SUCCESS: "Orden enviada correctamente. Revisa el resultado en historial.",
  TRADING_ERROR: "No se pudo ejecutar la orden. Ajusta los datos y vuelve a intentar."
};

export function getErrorMessage(code?: string): string {
  if (!code) {
    return errorMessages.UNKNOWN_ERROR;
  }
  return errorMessages[code] ?? errorMessages.UNKNOWN_ERROR;
}
