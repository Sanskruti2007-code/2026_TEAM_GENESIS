import AISettings from "../components/AISettings";
import DashboardCards from "../components/DashboardCards";
import LowStockAlert from "../components/LowStockAlert";
import TransactionTable from "../components/TransactionTable";
import VoiceRecorder from "../components/VoiceRecorder";
import { useBusiness } from "../context/BusinessContext";
import { currency } from "../utils/currency";

export default function Dashboard({ goTo }) {
  const {
    products,
    orders,
    summary,
    runVoiceDemo,
    executeCommand,
    refreshData,
    loading,
    connectionError,
  } = useBusiness();

  const cards = [
    {
      label: "Total Products",
      value: summary.totalProducts,
      icon: "products",
      note: "Active inventory items",
    },
    {
      label: "Current Stock",
      value: summary.currentStock,
      icon: "stock",
      note: "Units available",
    },
    {
      label: "Today's Sales",
      value: currency(summary.todaySales),
      icon: "sales",
      note: "Completed orders",
    },
    {
      label: "Pending Orders",
      value: summary.pendingOrders,
      icon: "orders",
      note: "Need attention",
    },
    {
      label: "Low Stock Items",
      value: summary.lowStockItems,
      icon: "low",
      note: "At or below reorder",
    },
    {
      label: "Total Revenue",
      value: currency(summary.totalRevenue),
      icon: "revenue",
      note: "All completed sales",
    },
    {
      label: "Total Profit",
      value: currency(summary.totalProfit),
      icon: "profit",
      note: "Estimated gross profit",
    },
  ];

  return (
    <div className="page-stack">
      {connectionError && (
        <div className="backend-alert">
          <strong>Backend offline:</strong> {connectionError}
        </div>
      )}

      {loading && <p className="muted-copy">Business data load ho raha hai…</p>}

      <div className="welcome-row">
        <div>
          <span className="eyebrow">
            Good evening
          </span>

          <h2>Your business at a glance</h2>

          <p>
            Track today’s performance and take
            quick action.
          </p>
        </div>

        <button
          className="button primary"
          onClick={() => goTo("Sales")}
        >
          Create New Order
        </button>
      </div>

      <DashboardCards cards={cards} />

      <div className="dashboard-grid">
        <VoiceRecorder
          onDemoCommand={runVoiceDemo}
          onTextCommand={executeCommand}
          onCommandComplete={refreshData}
        />

        <LowStockAlert products={products} />
      </div>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <span className="eyebrow">
              Latest activity
            </span>

            <h2>Recent Orders</h2>
          </div>

          <button
            className="text-button"
            onClick={() => goTo("Sales")}
          >
            View all sales
          </button>
        </div>

        <TransactionTable
          orders={orders.slice(0, 5)}
        />
      </section>
      <AISettings />
    </div>
  );
}
