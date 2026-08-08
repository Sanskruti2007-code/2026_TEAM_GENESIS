import { useState } from "react";
import Layout from "./components/Layout";
import { BusinessProvider } from "./context/BusinessContext";
import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import Login from "./pages/Login";
import Reports from "./pages/Reports";
import Sales from "./pages/Sales";
import Stock from "./pages/Stock";
import Workplace from "./pages/Workplace";

const pages = {
  Dashboard,
  Inventory,
  Sales,
  Stock,
  Workplace,
  Reports,
};

export default function App() {
  const [loggedIn, setLoggedIn] = useState(
    () =>
      localStorage.getItem("vs_logged_in") === "true" ||
      sessionStorage.getItem("vs_logged_in") === "true"
  );

  const [page, setPage] = useState("Dashboard");

  const login = (remember) => {
    const storage = remember ? localStorage : sessionStorage;
    storage.setItem("vs_logged_in", "true");
    setLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("vs_logged_in");
    sessionStorage.removeItem("vs_logged_in");
    setLoggedIn(false);
  };

  if (!loggedIn) {
    return <Login onLogin={login} />;
  }

  const CurrentPage = pages[page] || Dashboard;

  return (
    <BusinessProvider>
      <Layout page={page} setPage={setPage} onLogout={logout}>
        <CurrentPage goTo={setPage} />
      </Layout>
    </BusinessProvider>
  );
}