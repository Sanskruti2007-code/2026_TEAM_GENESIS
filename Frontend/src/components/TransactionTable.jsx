import { Eye } from "lucide-react";
import { currency } from "../utils/currency";
import { formatDate } from "../utils/date";

export default function TransactionTable({
  orders,
  onView,
}) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Customer</th>
            <th>Date</th>
            <th>Items</th>
            <th>Amount</th>
            <th>Profit</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td>
                <strong>{order.id}</strong>
              </td>

              <td>{order.customerName}</td>
              <td>{formatDate(order.date)}</td>
              <td>{order.itemCount}</td>
              <td>{currency(order.totalAmount)}</td>

              <td className="profit">
                {currency(order.profit)}
              </td>

              <td>
                <span
                  className={`status ${order.status.toLowerCase()}`}
                >
                  {order.status}
                </span>
              </td>

              <td>
                <button
                  className="icon-button"
                  onClick={() => onView?.(order)}
                  aria-label={`View ${order.id}`}
                >
                  <Eye size={17} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}