import { useEffect, useState } from "react";
import { X } from "lucide-react";

const emptyProduct = {
  name: "",
  category: "Grocery",
  purchasePrice: "",
  sellingPrice: "",
  quantity: "",
  supplier: "",
  reorderLevel: "",
};

export default function ProductModal({
  product,
  onClose,
  onSave,
}) {
  const [form, setForm] = useState(emptyProduct);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm(product || emptyProduct);
  }, [product]);

  const change = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const submit = async (event) => {
    event.preventDefault();

    if (!form.name.trim() || !form.supplier.trim()) {
      setError(
        "Product name and supplier are required."
      );
      return;
    }

    const numberFields = [
      form.purchasePrice,
      form.sellingPrice,
      form.quantity,
      form.reorderLevel,
    ];

    if (
      numberFields.some(
        (value) => value === "" || Number(value) < 0
      )
    ) {
      setError("Enter valid price and stock values.");
      return;
    }

    try {
      setSaving(true);
      setError("");
      await onSave(form);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <section className="modal product-modal">
        <div className="modal-header">
          <div>
            <span className="eyebrow">
              Product master
            </span>

            <h2>
              {product ? "Edit Product" : "Add Product"}
            </h2>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
          >
            <X />
          </button>
        </div>

        <form onSubmit={submit} className="form-grid">
          <label className="span-2">
            Product Name

            <input
              name="name"
              value={form.name}
              onChange={change}
              placeholder="e.g. Parle-G Biscuits"
            />
          </label>

          <label>
            Category

            <input
              name="category"
              value={form.category}
              onChange={change}
            />
          </label>

          <label>
            Supplier

            <input
              name="supplier"
              value={form.supplier}
              onChange={change}
            />
          </label>

          <label>
            Purchase Price

            <input
              name="purchasePrice"
              type="number"
              value={form.purchasePrice}
              onChange={change}
            />
          </label>

          <label>
            Selling Price

            <input
              name="sellingPrice"
              type="number"
              value={form.sellingPrice}
              onChange={change}
            />
          </label>

          <label>
            Current Quantity

            <input
              name="quantity"
              type="number"
              value={form.quantity}
              onChange={change}
            />
          </label>

          <label>
            Reorder Level

            <input
              name="reorderLevel"
              type="number"
              value={form.reorderLevel}
              onChange={change}
            />
          </label>

          {error && (
            <p className="form-error span-2">
              {error}
            </p>
          )}

          <div className="modal-actions span-2">
            <button
              type="button"
              className="button secondary"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>

            <button className="button primary" disabled={saving}>
              {saving
                ? "Saving..."
                : product
                  ? "Save Changes"
                  : "Add Product"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
