import { useState } from "react";
import { Plus } from "lucide-react";
import DashboardCards from "../components/DashboardCards";
import OrderModal from "../components/OrderModal";
import TransactionTable from "../components/TransactionTable";
import { useBusiness } from "../context/BusinessContext";
import { currency } from "../utils/currency";

export default function Sales() {
  const {
    products,
    orders,
    summary,
    createOrder,
  } = useBusiness();

  const [creating, setCreating] = useState(false);
  const [viewOrder, setViewOrder] = useState(null);

  const cards = [
    {
      label: "Today's Sales",
      value: currency(summary.todaySales),
      icon: "sales",
    },
    {
      label: "Total Sales",
      value: currency(summary.totalRevenue),
      icon: "revenue",
    },
    {
      label: "Total Profit",
      value: currency(summary.totalProfit),
      icon: "profit",
    },
    {
      label: "Pending Orders",
      value: summary.pendingOrders,
      icon: "orders",
    },
    {
      label: "Completed Orders",
      value: summary.completedOrders,
      icon: "products",
    },
  ];

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            Orders & earnings
          </span>

          <h2>Sales</h2>

          <p>
            Track order value, status and estimated
            profit.
          </p>
        </div>

        <button
          className="button primary"
          onClick={() => setCreating(true)}
        >
          <Plus size={18} />
          Create Order
        </button>
      </div>

      <DashboardCards cards={cards} />

      <section className="panel">
        <div className="panel-heading">
          <div>
            <span className="eyebrow">
              Order register
            </span>

            <h2>All Sales Orders</h2>
          </div>
        </div>

        <TransactionTable
          orders={orders}
          onView={setViewOrder}
        />
      </section>

      {creating && (
        <OrderModal
          products={products}
          onClose={() => setCreating(false)}
          onCreate={createOrder}
        />
      )}

      {viewOrder && (
        <div className="modal-backdrop">
          <section className="modal small-modal">
            <div className="modal-header">
              <div>
                <span className="eyebrow">
                  {viewOrder.id}
                </span>

                <h2>{viewOrder.customerName}</h2>
              </div>
            </div>

            <div className="order-totals">
              <div>
                <span>Order Amount</span>
                <strong>
                  {currency(viewOrder.totalAmount)}
                </strong>
              </div>

              <div>
                <span>Estimated Profit</span>
                <strong className="profit">
                  {currency(viewOrder.profit)}
                </strong>
              </div>
            </div>

            <p>
              {viewOrder.itemCount} items ·{" "}
              {viewOrder.status}
            </p>

            <button
              className="button primary full"
              onClick={() => setViewOrder(null)}
            >
              Close
            </button>
          </section>
        </div>
      )}
    </div>
  );
}