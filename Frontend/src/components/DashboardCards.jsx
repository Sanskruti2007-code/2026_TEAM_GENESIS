
import {
  AlertTriangle,
  Boxes,
  IndianRupee,
  PackageCheck,
  ShoppingBag,
  TrendingUp,
  WalletCards,
} from "lucide-react";

const icons = {
  products: PackageCheck,
  stock: Boxes,
  sales: ShoppingBag,
  orders: WalletCards,
  low: AlertTriangle,
  revenue: IndianRupee,
  profit: TrendingUp,
};

export default function DashboardCards({ cards }) {
  return (
    <div className="summary-grid">
      {cards.map((card) => {
        const Icon = icons[card.icon] || PackageCheck;

        return (
          <article
            className="summary-card"
            key={card.label}
          >
            <span className="summary-icon">
              <Icon size={20} />
            </span>

            <div>
              <p>{card.label}</p>
              <h3>{card.value}</h3>

              {card.note && <small>{card.note}</small>}
            </div>
          </article>
        );
      })}
    </div>
  );
}