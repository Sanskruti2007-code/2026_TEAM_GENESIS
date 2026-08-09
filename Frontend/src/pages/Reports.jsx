import DashboardCards from "../components/DashboardCards";
import LowStockAlert from "../components/LowStockAlert";
import { useBusiness } from "../context/BusinessContext";
import { currency } from "../utils/currency";

export default function Reports() {
  const { products, summary } = useBusiness();

  const margin = summary.totalRevenue
    ? (
        (summary.totalProfit /
          summary.totalRevenue) *
        100
      ).toFixed(1)
    : 0;

  const cards = [
    {
      label: "Total Revenue",
      value: currency(summary.totalRevenue),
      icon: "revenue",
    },
    {
      label: "Total Profit",
      value: currency(summary.totalProfit),
      icon: "profit",
    },
    {
      label: "Gross Margin",
      value: `${margin}%`,
      icon: "sales",
    },
    {
      label: "Units in Stock",
      value: summary.currentStock,
      icon: "stock",
    },
  ];

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            Business intelligence
          </span>

          <h2>Reports</h2>

          <p>
            A clear summary of revenue, profit and
            inventory health.
          </p>
        </div>
      </div>

      <DashboardCards cards={cards} />

      <LowStockAlert products={products} />
    </div>
  );
}