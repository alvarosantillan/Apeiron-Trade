import { render, screen } from "@testing-library/react";

import TradingFormPanel from "../../../src/features/trading/TradingFormPanel";

describe("Trading form state", () => {
  it("disables submit buttons in submitting state", () => {
    render(
      <TradingFormPanel
        status="submitting"
        apiKey="api"
        secretKey="secret"
        symbol="BTCUSDT"
        quantity={1}
        onApiKeyChange={() => undefined}
        onSecretKeyChange={() => undefined}
        onSymbolChange={() => undefined}
        onQuantityChange={() => undefined}
        onSave={async () => undefined}
        onTrade={async () => undefined}
      />
    );

    expect(screen.getByRole("button", { name: "Guardando..." })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Enviando orden..." })).toBeDisabled();
  });
});
