import "./styles.css";
import React from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import { isAuthenticated } from "./lib/auth";

const router = createBrowserRouter([
  { path: "/login", element: <Login /> },
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "users", element: <Users /> }
    ]
  }
]);

function GuardedRouter() {
  const authed = isAuthenticated();
  // Redirection simple cote pages elles-memes
  return <RouterProvider router={router} />;
}

const root = createRoot(document.getElementById("root")!);
root.render(<GuardedRouter />);
