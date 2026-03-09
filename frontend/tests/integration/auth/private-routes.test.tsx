import { render, screen } from "@testing-library/react";
import { RouterProvider, createMemoryRouter } from "react-router-dom";

import { SessionProvider } from "../../../src/features/auth/session-store";
import { routes } from "../../../src/app/routes";

describe("Private routes", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("redirects unauthenticated users to login", async () => {
    const router = createMemoryRouter(routes, {
      initialEntries: ["/dashboard"]
    });

    render(
      <SessionProvider>
        <RouterProvider router={router} />
      </SessionProvider>
    );

    expect(await screen.findByRole("heading", { name: "TRDIA Login" })).toBeInTheDocument();
  });

  it("allows authenticated users to access dashboard", async () => {
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
  });
});
