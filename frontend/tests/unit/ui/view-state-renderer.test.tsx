import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import StatePanel from "../../../src/app/components/StatePanel";

describe("StatePanel", () => {
  it("renders loading and empty states", () => {
    const { rerender } = render(<StatePanel kind="loading" message="Loading dashboard" />);
    expect(screen.getByText("Loading...")).toBeInTheDocument();

    rerender(<StatePanel kind="empty" message="No data" />);
    expect(screen.getByText("No data")).toBeInTheDocument();

    rerender(<StatePanel kind="success" message="Dashboard listo" />);
    expect(screen.getByText("Dashboard listo")).toBeInTheDocument();
  });

  it("renders error state with retry", async () => {
    const user = userEvent.setup();
    const onRetry = vi.fn();

    render(<StatePanel kind="error" message="Failed" onRetry={onRetry} />);
    await user.click(screen.getByRole("button", { name: "Retry" }));

    expect(onRetry).toHaveBeenCalledTimes(1);
  });
});
