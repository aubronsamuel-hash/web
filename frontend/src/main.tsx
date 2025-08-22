import "./styles.css";
import React from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Intermittents from "./pages/Intermittents";
import Missions from "./pages/Missions";
import MissionForm from "./pages/MissionForm";

const router = createBrowserRouter([
  { path: "/login", element: <Login /> },
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "users", element: <Users /> },
      { path: "intermittents", element: <Intermittents /> },
      { path: "missions", element: <Missions /> },
      { path: "missions/new", element: <MissionForm /> },
      { path: "missions/:id", element: <MissionForm /> }
    ]
  }
]);

const root = createRoot(document.getElementById("root")!);
root.render(<RouterProvider router={router} />);
