import { useMemo, useState } from "react";
import { Plus, Trash2, X } from "lucide-react";
import { currency } from "../utils/currency";

export default function OrderModal({
  products,
  onClose,
  onCreate,
}) {
  const available = products.filter(
    (product) => product.quantity > 0
  );

  const [customerName, setCustomerName] =
    useState("");

  const [selectedId, setSelectedId] = useState(
    available[0]?.id || ""
  );

  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  const addItem = () => {
    if (!selectedId) return;

    if (
      items.some(
        (item) => item.productId === selectedId
      )
    ) {
      return;
    }

    setItems([
      ...items,
      {
        productId: selectedId,
        quantity: 1,
      },
    ]);
  };

  const updateQuantity = (productId, quantity) => {
    setItems(
      items.map((item) =>
        item.productId === productId
          ? {
              ...item,
              quantity: Math.max(1, Number(quantity)),
            }
          : item
      )
    );
  };

  const removeItem = (productId) => {
    setItems(
      items.filter(
        (item) => item.productId !== productId
      )
    );
  };

  const totals = useMemo(
    () =>
      items.reduce(
        (total, item) => {
          const product = products.find(
            (entry) => entry.id === item.productId
          );

          if (!product) return total;

          return {
            amount:
              total.amount +
              product.sellingPrice * item.quantity,

            profit:
              total.profit +
              (product.sellingPrice -
                product.purchasePrice) *
                item.quantity,
          };
        },
        {
          amount: 0,
          profit: 0,
        }
      ),
    [items, products]
  );

  const submit = (event) => {
    event.preventDefault();

    try {
      onCreate({
        customerName,
        items,
      });

      onClose();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="modal-backdrop">
      <section className="modal order-modal">
        <div className="modal-header">
          <div>
            <span className="eyebrow">New sale</span>
            <h2>Create Order</h2>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
          >
            <X />
          </button>
        </div>

        <form onSubmit={submit}>
          <label>
            Customer Name

            <input
              value={customerName}
              onChange={(event) =>
                setCustomerName(event.target.value)
              }
              placeholder="e.g. Rahul Traders"
            />
          </label>

          <div className="product-picker">
            <label>
              Choose Product

              <select
                value={selectedId}
                onChange={(event) =>
                  setSelectedId(event.target.value)
                }
              >
                {available.map((product) => (
                  <option
                    value={product.id}
                    key={product.id}
                  >
                    {product.name} · {product.quantity} available
                  </option>
                ))}
              </select>
            </label>

            <button
              type="button"
              className="button dark"
              onClick={addItem}
            >
              <Plus size={17} />
              Add
            </button>
          </div>

          <div className="order-lines">
            {items.length === 0 && (
              <div className="empty-state">
                Select a product and click Add.
              </div>
            )}

            {items.map((item) => {
              const product = products.find(
                (entry) =>
                  entry.id === item.productId
              );

              const amount =
                product.sellingPrice * item.quantity;

              const profit =
                (product.sellingPrice -
                  product.purchasePrice) *
                item.quantity;

              return (
                <div
                  className="order-line"
                  key={item.productId}
                >
                  <div>
                    <strong>{product.name}</strong>

                    <small>
                      {currency(product.sellingPrice)} each ·{" "}
                      {product.quantity} in stock
                    </small>
                  </div>

                  <label>
                    Qty

                    <input
                      type="number"
                      min="1"
                      max={product.quantity}
                      value={item.quantity}
                      onChange={(event) =>
                        updateQuantity(
                          item.productId,
                          event.target.value
                        )
                      }
                    />
                  </label>

                  <div className="line-total">
                    <strong>{currency(amount)}</strong>
                    <small>
                      {currency(profit)} profit
                    </small>
                  </div>

                  <button
                    type="button"
                    className="icon-button danger"
                    onClick={() =>
                      removeItem(item.productId)
                    }
                  >
                    <Trash2 size={17} />
                  </button>
                </div>
              );
            })}
          </div>

          <div className="order-totals">
            <div>
              <span>Total Order Amount</span>
              <strong>{currency(totals.amount)}</strong>
            </div>

            <div>
              <span>Estimated Profit</span>
              <strong className="profit">
                {currency(totals.profit)}
              </strong>
            </div>
          </div>

          {error && (
            <p className="form-error">{error}</p>
          )}

          <div className="modal-actions">
            <button
              type="button"
              className="button secondary"
              onClick={onClose}
            >
              Cancel
            </button>

            <button className="button primary">
              Create Order
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}