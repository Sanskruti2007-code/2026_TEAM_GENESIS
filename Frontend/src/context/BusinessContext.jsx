import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { api } from "../services/api";
import { todayISO } from "../utils/date";

const BusinessContext = createContext(null);

export const productStatus = (product) => {
  if (Number(product.quantity) <= 0) return "Out of Stock";
  if (Number(product.quantity) <= Number(product.reorderLevel || 0)) {
    return "Low Stock";
  }
  return "In Stock";
};

export function BusinessProvider({ children }) {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connectionError, setConnectionError] = useState("");

  const refreshData = useCallback(async () => {
    try {
      const [productResponse, transactionResponse] = await Promise.all([
        api.products(),
        api.transactions(),
      ]);
      setProducts(productResponse.products || []);
      setOrders(transactionResponse.transactions || []);
      setConnectionError("");
    } catch (error) {
      setConnectionError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshData().catch(() => {});
  }, [refreshData]);

  const addProduct = async (data) => {
    const response = await api.createProduct({
      ...data,
      purchasePrice: Number(data.purchasePrice),
      sellingPrice: Number(data.sellingPrice),
      quantity: Number(data.quantity),
      reorderLevel: Number(data.reorderLevel),
    });
    await refreshData();
    return response.product;
  };

  const updateProduct = async (data) => {
    const response = await api.updateProduct(data.id, {
      ...data,
      purchasePrice: Number(data.purchasePrice),
      sellingPrice: Number(data.sellingPrice),
      quantity: Number(data.quantity),
      reorderLevel: Number(data.reorderLevel),
    });
    await refreshData();
    return response.product;
  };

  const deleteProduct = async (id) => {
    await api.deleteProduct(id);
    await refreshData();
  };

  const createOrder = async ({ customerName, items, status = "Completed" }) => {
    if (!customerName.trim()) throw new Error("Customer name is required.");
    if (!items.length) throw new Error("Add at least one product.");

    const response = await api.createOrder({ customerName, items, status });
    await refreshData();
    return response.transaction;
  };

  const executeCommand = async (text) => {
    const response = await api.processText(text);
    if (!response.success) throw new Error(response.message);
    await refreshData();
    return response;
  };

  const runVoiceDemo = async (intent) => {
    const commands = {
      ADD_STOCK:
        "Add 20 Dettol Soap, buying price 18, selling price 22",
      RECORD_SALE: "Sell 3 Dettol Soap",
      TODAY_REPORT: "आजची विक्री आणि नफा सांगा",
    };
    return executeCommand(commands[intent] || commands.TODAY_REPORT);
  };

  const summary = useMemo(() => {
    const completed = orders.filter((order) => order.status === "Completed");
    const today = completed.filter((order) => order.date === todayISO());
    return {
      totalProducts: products.length,
      currentStock: products.reduce(
        (sum, product) => sum + Number(product.quantity || 0),
        0
      ),
      todaySales: today.reduce(
        (sum, order) => sum + Number(order.totalAmount || 0),
        0
      ),
      pendingOrders: orders.filter((order) => order.status === "Pending")
        .length,
      completedOrders: completed.length,
      lowStockItems: products.filter(
        (product) => productStatus(product) !== "In Stock"
      ).length,
      totalRevenue: completed.reduce(
        (sum, order) => sum + Number(order.totalAmount || 0),
        0
      ),
      totalProfit: completed.reduce(
        (sum, order) => sum + Number(order.profit || 0),
        0
      ),
    };
  }, [orders, products]);

  const value = {
    products,
    orders,
    summary,
    loading,
    connectionError,
    refreshData,
    addProduct,
    updateProduct,
    deleteProduct,
    createOrder,
    executeCommand,
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
    throw new Error("useBusiness must be used inside BusinessProvider");
  }
  return context;
};
