import { Navigate, RouteObject } from "react-router-dom";

import PrivateLayout from "./layouts/PrivateLayout";
import AIAgentPage from "../pages/AIAgentPage";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";
import NotificationsPage from "../pages/NotificationsPage";
import TradingPage from "../pages/TradingPage";

export const routes: RouteObject[] = [
  {
    path: "/login",
    element: <LoginPage />
  },
  {
    path: "/",
    element: <PrivateLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "trading", element: <TradingPage /> },
      { path: "notifications", element: <NotificationsPage /> },
      { path: "ai-agent", element: <AIAgentPage /> }
    ]
  },
  {
    path: "*",
    element: <Navigate to="/login" replace />
  }
];
