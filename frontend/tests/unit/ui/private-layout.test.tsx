import { render, screen } from "@testing-library/react";
import { RouterProvider, createMemoryRouter } from "react-router-dom";

import { routes } from "../../../src/app/routes";
import { SessionProvider } from "../../../src/features/auth/session-store";

describe("Private layout UI Kit", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("shows authenticated shell with private navigation", async () => {
    localStorage.setItem("trdia.accessToken", "token-123");

    const router = createMemoryRouter(routes, {
      initialEntries: ["/dashboard"]
    });

    render(
      <SessionProvider>
        <RouterProvider router={router} />
      </SessionProvider>
    );

    expect(await screen.findByRole("heading", { name: "Dashboard" })).toBeInTheDocument();
    expect(screen.getByRole("navigation", { name: "Navegacion privada" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Trading" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Logout" })).toBeInTheDocument();
  });
});
