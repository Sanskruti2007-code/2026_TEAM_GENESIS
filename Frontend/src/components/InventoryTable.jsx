import { Pencil, Trash2 } from "lucide-react";
import {
  productStatus,
} from "../context/BusinessContext";
import { currency } from "../utils/currency";

export default function InventoryTable({
  products,
  onEdit,
  onDelete,
}) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Purchase</th>
            <th>Selling</th>
            <th>Quantity</th>
            <th>Supplier</th>
            <th>Reorder</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {products.map((product) => {
            const status = productStatus(product);

            return (
              <tr key={product.id}>
                <td>
                  <strong>{product.name}</strong>
                  <small className="table-subtext">
                    {product.id}
                  </small>
                </td>

                <td>{product.category}</td>
                <td>{currency(product.purchasePrice)}</td>
                <td>{currency(product.sellingPrice)}</td>
                <td>{product.quantity}</td>
                <td>{product.supplier}</td>
                <td>{product.reorderLevel}</td>

                <td>
                  <span
                    className={`status ${status
                      .toLowerCase()
                      .replaceAll(" ", "-")}`}
                  >
                    {status}
                  </span>
                </td>

                <td>
                  <div className="action-group">
                    <button
                      className="icon-button"
                      onClick={() => onEdit(product)}
                      aria-label="Edit product"
                    >
                      <Pencil size={16} />
                    </button>

                    <button
                      className="icon-button danger"
                      onClick={() => onDelete(product)}
                      aria-label="Delete product"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}