export const errorMessages: Record<string, string> = {
  NETWORK_ERROR: "Problema de red. Verifica tu conexion e intenta nuevamente.",
  UNAUTHORIZED: "Tu sesion expiro. Vuelve a iniciar sesion.",
  FORBIDDEN: "No tienes permisos para realizar esta accion.",
  VALIDATION_ERROR: "Revisa los datos ingresados.",
  SERVER_ERROR: "El servicio no esta disponible temporalmente.",
  UNKNOWN_ERROR: "Ocurrio un error inesperado."
};

export function getErrorMessage(code?: string): string {
  if (!code) {
    return errorMessages.UNKNOWN_ERROR;
  }
  return errorMessages[code] ?? errorMessages.UNKNOWN_ERROR;
}
