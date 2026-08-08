import { useState } from "react";
import {
  Boxes,
  ChartNoAxesCombined,
  LayoutDashboard,
  LogOut,
  Menu,
  PackageSearch,
  ShoppingCart,
  Users,
  X,
} from "lucide-react";

const navItems = [
  ["Dashboard", LayoutDashboard],
  ["Inventory", PackageSearch],
  ["Sales", ShoppingCart],
  ["Stock", Boxes],
  ["Workplace", Users],
  ["Reports", ChartNoAxesCombined],
];

export default function Layout({
  page,
  setPage,
  onLogout,
  children,
}) {
  const [open, setOpen] = useState(false);

  const navigate = (nextPage) => {
    setPage(nextPage);
    setOpen(false);
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${open ? "open" : ""}`}>
        <div className="brand">
          <img
            src="/vyaparsaathi-logo.jpeg"
            alt="VyaparSaathi logo"
          />

          <div>
            <strong>VyaparSaathi</strong>
            <small>Business Management</small>
          </div>

          <button
            className="sidebar-close"
            onClick={() => setOpen(false)}
          >
            <X />
          </button>
        </div>

        <nav>
          {navItems.map(([label, Icon]) => (
            <button
              key={label}
              className={page === label ? "active" : ""}
              onClick={() => navigate(label)}
            >
              <Icon size={19} />
              {label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-mini">
            <span>AU</span>

            <div>
              <strong>Akhilesh</strong>
              <small>Business Owner</small>
            </div>
          </div>

          <button
            className="logout-button"
            onClick={onLogout}
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <button
            className="menu-button"
            onClick={() => setOpen(true)}
          >
            <Menu />
          </button>

          <div>
            <span className="eyebrow">
              VyaparSaathi Workspace
            </span>
            <h1>{page}</h1>
          </div>

          <div className="topbar-actions">
            <span className="live-dot" />
            Business online
          </div>
        </header>

        <main>{children}</main>
      </div>

      {open && (
        <button
          className="sidebar-overlay"
          onClick={() => setOpen(false)}
          aria-label="Close menu"
        />
      )}
    </div>
  );
}