import { useMemo, useState } from "react";
import { Plus, Search } from "lucide-react";
import InventoryTable from "../components/InventoryTable";
import ProductModal from "../components/ProductModal";
import {
  productStatus,
  useBusiness,
} from "../context/BusinessContext";

export default function Inventory() {
  const {
    products,
    addProduct,
    updateProduct,
    deleteProduct,
  } = useBusiness();

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");
  const [modal, setModal] = useState(false);
  const [editing, setEditing] = useState(null);

  const filtered = useMemo(
    () =>
      products.filter((product) => {
        const searchableText = `
          ${product.name}
          ${product.id}
          ${product.category}
          ${product.supplier}
        `.toLowerCase();

        const matchesSearch =
          searchableText.includes(search.toLowerCase());

        const matchesFilter =
          filter === "All" ||
          productStatus(product) === filter;

        return matchesSearch && matchesFilter;
      }),
    [products, search, filter]
  );

  const closeModal = () => {
    setModal(false);
    setEditing(null);
  };

  const removeProduct = (product) => {
    const confirmed = window.confirm(
      `Delete ${product.name}?`
    );

    if (confirmed) {
      deleteProduct(product.id);
    }
  };

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">
            Product master
          </span>

          <h2>Inventory</h2>

          <p>
            Manage products, pricing, suppliers and
            reorder levels.
          </p>
        </div>

        <button
          className="button primary"
          onClick={() => setModal(true)}
        >
          <Plus size={18} />
          Add Product
        </button>
      </div>

      <section className="panel">
        <div className="toolbar">
          <div className="search-box">
            <Search size={18} />

            <input
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
              placeholder="Search product, SKU, category or supplier"
            />
          </div>

          <select
            value={filter}
            onChange={(event) =>
              setFilter(event.target.value)
            }
          >
            <option>All</option>
            <option>In Stock</option>
            <option>Low Stock</option>
            <option>Out of Stock</option>
          </select>
        </div>

        <InventoryTable
          products={filtered}
          onEdit={(product) => {
            setEditing(product);
            setModal(true);
          }}
          onDelete={removeProduct}
        />
      </section>

      {modal && (
        <ProductModal
          product={editing}
          onClose={closeModal}
          onSave={
            editing ? updateProduct : addProduct
          }
        />
      )}
    </div>
  );
}