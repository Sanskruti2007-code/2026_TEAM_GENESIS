import {
  productStatus,
  useBusiness,
} from "../context/BusinessContext";
import { formatDate } from "../utils/date";

export default function Stock() {
  const { products } = useBusiness();

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            Availability & movement
          </span>

          <h2>Stock</h2>

          <p>
            Monitor opening stock, inward stock,
            sales movement and current availability.
          </p>
        </div>
      </div>

      <section className="panel">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Opening</th>
                <th>Stock In</th>
                <th>Stock Out</th>
                <th>Current</th>
                <th>Reorder</th>
                <th>Status</th>
                <th>Last Updated</th>
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

                    <td>{product.openingStock}</td>

                    <td className="profit">
                      +{product.stockIn}
                    </td>

                    <td className="stock-out">
                      -{product.stockOut}
                    </td>

                    <td>
                      <strong>{product.quantity}</strong>
                    </td>

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
                      {formatDate(product.updatedAt)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}