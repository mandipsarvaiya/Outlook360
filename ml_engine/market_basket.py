"""
OmniPulse AI - Market Basket Analysis & Association Rule Mining Engine
Extracts co-purchase patterns, affinity bundles, and cross-sell rules
using the Apriori algorithm from mlxtend.
"""
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.queries import AnalyticsQueries


class MarketBasketEngine:
    """Association rule mining and cross-sell recommendation engine."""

    def __init__(self):
        self.queries = AnalyticsQueries()

    def generate_association_rules(
        self,
        min_support: float = 0.015,
        min_confidence: float = 0.15,
        min_lift: float = 1.05
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Builds transaction matrix, finds frequent itemsets using Apriori,
        and generates association rules filtered by minimum thresholds.
        """
        df = self.queries.get_basket_transactions()
        if df.empty:
            return pd.DataFrame(), {"status": "No transaction data found"}

        # Fast pivot to binary one-hot transaction matrix using pd.crosstab
        basket_bool = pd.crosstab(df["order_id"], df["product_name"]).astype(bool)
        total_transactions = len(basket_bool)

        try:
            # Frequent itemsets
            frequent_itemsets = apriori(
                basket_bool,
                min_support=min_support,
                use_colnames=True,
                max_len=3
            )

            if frequent_itemsets.empty:
                # Retry with slightly lower support if sparse
                frequent_itemsets = apriori(
                    basket_bool,
                    min_support=max(0.005, min_support / 2),
                    use_colnames=True,
                    max_len=3
                )

            if frequent_itemsets.empty:
                return pd.DataFrame(), {"total_transactions": total_transactions, "total_rules": 0}

            # Generate association rules
            rules = association_rules(
                frequent_itemsets,
                metric="confidence",
                min_threshold=min_confidence
            )

            if rules.empty:
                return pd.DataFrame(), {"total_transactions": total_transactions, "total_rules": 0}

            # Filter by lift
            rules = rules[rules["lift"] >= min_lift].copy()

            # Clean and format rules for readability
            rules["antecedents_str"] = rules["antecedents"].apply(lambda s: ", ".join(list(s)))
            rules["consequents_str"] = rules["consequents"].apply(lambda s: ", ".join(list(s)))
            rules["rule_display"] = rules["antecedents_str"] + "  ➔  " + rules["consequents_str"]

            # Round metrics
            rules["support"] = rules["support"].round(4)
            rules["confidence"] = rules["confidence"].round(4)
            rules["lift"] = rules["lift"].round(3)
            rules["leverage"] = rules["leverage"].round(4)
            rules["conviction"] = rules["conviction"].round(3)

            rules = rules.sort_values(by=["lift", "confidence"], ascending=[False, False]).reset_index(drop=True)

            summary = {
                "total_transactions": total_transactions,
                "unique_products": basket_bool.shape[1],
                "frequent_itemsets_count": len(frequent_itemsets),
                "total_rules": len(rules),
                "highest_lift": float(rules["lift"].max()) if not rules.empty else 0.0,
                "highest_confidence": float(rules["confidence"].max()) if not rules.empty else 0.0
            }

            return rules, summary

        except Exception as e:
            print(f"[MarketBasketEngine Error] {e}")
            return pd.DataFrame(), {"error": str(e)}

    def get_recommendations_for_product(
        self,
        product_name: str,
        rules_df: Optional[pd.DataFrame] = None,
        top_n: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Given a product name in a cart, finds the highest-lift cross-sell recommendations.
        """
        if rules_df is None or rules_df.empty:
            rules_df, _ = self.generate_association_rules()

        if rules_df.empty:
            return []

        # Find rules where product_name is in antecedents
        matching_rules = rules_df[
            rules_df["antecedents"].apply(lambda a: product_name in a)
        ].sort_values(by=["lift", "confidence"], ascending=[False, False])

        recommendations = []
        seen_items = set()

        for _, row in matching_rules.iterrows():
            consequents = list(row["consequents"])
            for item in consequents:
                if item != product_name and item not in seen_items:
                    seen_items.add(item)
                    recommendations.append({
                        "recommended_product": item,
                        "confidence_pct": round(row["confidence"] * 100, 1),
                        "lift_score": row["lift"],
                        "support_pct": round(row["support"] * 100, 2),
                        "rule_basis": f"Purchased with {row['antecedents_str']}"
                    })
                    if len(recommendations) >= top_n:
                        break
            if len(recommendations) >= top_n:
                break

        return recommendations
