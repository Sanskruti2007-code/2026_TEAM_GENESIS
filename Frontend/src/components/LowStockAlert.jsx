import { AlertTriangle } from "lucide-react";
import {
  productStatus,
} from "../context/BusinessContext";

export default function LowStockAlert({ products }) {
  const lowProducts = products.filter(
    (product) => productStatus(product) !== "In Stock"
  );

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">
            Attention needed
          </span>
          <h2>Low Stock Alerts</h2>
        </div>

        <AlertTriangle className="gold" />
      </div>

      <div className="alert-list">
        {lowProducts.length === 0 && (
          <p className="muted">
            All products have sufficient stock.
          </p>
        )}

        {lowProducts.map((product) => (
          <div className="alert-row" key={product.id}>
            <div>
              <strong>{product.name}</strong>
              <small>
                {product.id} · Reorder at{" "}
                {product.reorderLevel}
              </small>
            </div>

            <span
              className={`status ${
                product.quantity === 0 ? "out" : "low"
              }`}
            >
              {product.quantity} left
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}