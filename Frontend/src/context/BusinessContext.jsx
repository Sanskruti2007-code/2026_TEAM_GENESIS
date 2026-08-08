import { createContext, useContext, useMemo, useState } from "react";
import { initialOrders, initialProducts } from "../data/sampleData";
import { currency } from "../utils/currency";
import { todayISO } from "../utils/date";

const BusinessContext = createContext(null);

const readSaved = (key, fallback) => {
  try {
    return JSON.parse(localStorage.getItem(key)) || fallback;
  } catch {
    return fallback;
  }
};

export const productStatus = (product) => {
  if (product.quantity <= 0) return "Out of Stock";
  if (product.quantity <= product.reorderLevel) return "Low Stock";
  return "In Stock";
};

export function BusinessProvider({ children }) {
  const [products, setProductsState] = useState(() =>
    readSaved("vs_products", initialProducts)
  );

  const [orders, setOrdersState] = useState(() =>
    readSaved("vs_orders", initialOrders)
  );

  const saveProducts = (updater) => {
    setProductsState((current) => {
      const next =
        typeof updater === "function" ? updater(current) : updater;

      localStorage.setItem("vs_products", JSON.stringify(next));
      return next;
    });
  };

  const saveOrders = (updater) => {
    setOrdersState((current) => {
      const next =
        typeof updater === "function" ? updater(current) : updater;

      localStorage.setItem("vs_orders", JSON.stringify(next));
      return next;
    });
  };

  const addProduct = (data) => {
    const product = {
      ...data,
      id: data.id || `SKU-${Date.now().toString().slice(-6)}`,
      purchasePrice: Number(data.purchasePrice),
      sellingPrice: Number(data.sellingPrice),
      quantity: Number(data.quantity),
      reorderLevel: Number(data.reorderLevel),
      openingStock: Number(data.quantity),
      stockIn: 0,
      stockOut: 0,
      updatedAt: todayISO(),
    };

    saveProducts((current) => [product, ...current]);
  };

  const updateProduct = (data) => {
    saveProducts((current) =>
      current.map((product) =>
        product.id === data.id
          ? {
              ...product,
              ...data,
              purchasePrice: Number(data.purchasePrice),
              sellingPrice: Number(data.sellingPrice),
              quantity: Number(data.quantity),
              reorderLevel: Number(data.reorderLevel),
              updatedAt: todayISO(),
            }
          : product
      )
    );
  };

  const deleteProduct = (id) => {
    saveProducts((current) =>
      current.filter((product) => product.id !== id)
    );
  };

  const createOrder = ({
    customerName,
    items,
    status = "Completed",
  }) => {
    if (!customerName.trim()) {
      throw new Error("Customer name is required.");
    }

    if (!items.length) {
      throw new Error("Add at least one product.");
    }

    const orderItems = items.map((item) => {
      const product = products.find(
        (entry) => entry.id === item.productId
      );

      const quantity = Number(item.quantity);

      if (!product) {
        throw new Error("Selected product was not found.");
      }

      if (quantity <= 0) {
        throw new Error(
          `Enter a valid quantity for ${product.name}.`
        );
      }

      if (quantity > product.quantity) {
        throw new Error(
          `Only ${product.quantity} units of ${product.name} are available.`
        );
      }

      return {
        productId: product.id,
        name: product.name,
        quantity,
        sellingPrice: product.sellingPrice,
        purchasePrice: product.purchasePrice,
        amount: product.sellingPrice * quantity,
        profit:
          (product.sellingPrice - product.purchasePrice) * quantity,
      };
    });

    const order = {
      id: `ORD-${Date.now().toString().slice(-6)}`,
      customerName: customerName.trim(),
      date: todayISO(),
      itemCount: orderItems.reduce(
        (sum, item) => sum + item.quantity,
        0
      ),
      totalAmount: orderItems.reduce(
        (sum, item) => sum + item.amount,
        0
      ),
      profit: orderItems.reduce(
        (sum, item) => sum + item.profit,
        0
      ),
      status,
      items: orderItems,
    };

    saveProducts((current) =>
      current.map((product) => {
        const sold = orderItems.find(
          (item) => item.productId === product.id
        );

        if (!sold) return product;

        return {
          ...product,
          quantity: product.quantity - sold.quantity,
          stockOut: product.stockOut + sold.quantity,
          updatedAt: todayISO(),
        };
      })
    );

    saveOrders((current) => [order, ...current]);

    return order;
  };

  const summary = useMemo(() => {
    const completed = orders.filter(
      (order) => order.status === "Completed"
    );

    const today = completed.filter(
      (order) => order.date === todayISO()
    );

    return {
      totalProducts: products.length,
      currentStock: products.reduce(
        (sum, product) => sum + product.quantity,
        0
      ),
      todaySales: today.reduce(
        (sum, order) => sum + order.totalAmount,
        0
      ),
      pendingOrders: orders.filter(
        (order) => order.status === "Pending"
      ).length,
      completedOrders: completed.length,
      lowStockItems: products.filter(
        (product) => productStatus(product) !== "In Stock"
      ).length,
      totalRevenue: completed.reduce(
        (sum, order) => sum + order.totalAmount,
        0
      ),
      totalProfit: completed.reduce(
        (sum, order) => sum + order.profit,
        0
      ),
    };
  }, [orders, products]);

  const runVoiceDemo = (intent) => {
    if (intent === "ADD_STOCK") {
      saveProducts((current) =>
        current.map((product) =>
          product.name === "Dettol Soap"
            ? {
                ...product,
                quantity: product.quantity + 20,
                stockIn: product.stockIn + 20,
                updatedAt: todayISO(),
              }
            : product
        )
      );

      return {
        transcript:
          "डेटॉल साबणाचे वीस नग स्टॉकमध्ये जोडा.",
        message:
          "डेटॉल साबणाचे 20 नग यशस्वीरित्या जोडले.",
      };
    }

    if (intent === "RECORD_SALE") {
      const dettol = products.find(
        (product) => product.name === "Dettol Soap"
      );

      if (!dettol) {
        throw new Error("Dettol Soap was not found.");
      }

      const order = createOrder({
        customerName: "Walk-in Customer",
        items: [
          {
            productId: dettol.id,
            quantity: 3,
          },
        ],
      });

      return {
        transcript: "तीन डेटॉल साबण विकले.",
        message: `विक्री ${currency(
          order.totalAmount
        )} आणि नफा ${currency(order.profit)} नोंदवला.`,
      };
    }

    return {
      transcript: "आजची विक्री आणि नफा सांगा.",
      message: `आजची विक्री ${currency(
        summary.todaySales
      )} आणि एकूण नफा ${currency(
        summary.totalProfit
      )} आहे.`,
    };
  };

  const value = {
    products,
    orders,
    summary,
    addProduct,
    updateProduct,
    deleteProduct,
    createOrder,
    runVoiceDemo,
  };

  return (
    <BusinessContext.Provider value={value}>
      {children}
    </BusinessContext.Provider>
  );
}

export const useBusiness = () => {
  const context = useContext(BusinessContext);

  if (!context) {
    throw new Error(
      "useBusiness must be used inside BusinessProvider"
    );
  }

  return context;
};