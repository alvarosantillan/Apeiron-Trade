import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { SessionProvider, useSession } from "../../../src/features/auth/session-store";

function SessionProbe() {
  const { session, login, logout } = useSession();
  return (
    <div>
      <span data-testid="auth-state">{session.isAuthenticated ? "yes" : "no"}</span>
      <button type="button" onClick={() => login("token-1")}>login</button>
      <button type="button" onClick={logout}>logout</button>
    </div>
  );
}

describe("Session store", () => {
  it("toggles authenticated state on login/logout", async () => {
    const user = userEvent.setup();
    render(
      <SessionProvider>
        <SessionProbe />
      </SessionProvider>
    );

    expect(screen.getByTestId("auth-state")).toHaveTextContent("no");

    await user.click(screen.getByRole("button", { name: "login" }));
    expect(screen.getByTestId("auth-state")).toHaveTextContent("yes");

    await user.click(screen.getByRole("button", { name: "logout" }));
    expect(screen.getByTestId("auth-state")).toHaveTextContent("no");
  });
});
