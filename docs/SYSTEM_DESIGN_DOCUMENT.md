# System Design Document (SDD)

# Outlook360: Enterprise Architecture, ER Diagrams, DFD & UML Specifications

---

## 1. Entity-Relationship Diagram (ERD)

The database follows a **Normalized 3NF Relational Structure** that simultaneously functions as an analytical **Star Schema** with `orders` and `order_items` as Fact tables and `products`, `categories`, `customers`, and `inventory_logs` as Dimension tables.

```mermaid
erDiagram
    USERS {
        int user_id PK
        string emp_id UK
        string email UK
        string password_hash
        string full_name
        string role
        int is_active
        datetime created_at
    }

    BUSINESS_PROFILES {
        int id PK
        string domain_key
        string business_name
        string currency
        decimal tax_rate
        string tagline
        datetime created_at
    }

    CATEGORIES {
        int category_id PK
        string name
        string department
        string description
        decimal tax_slab_percent
    }

    PRODUCTS {
        int product_id PK
        string sku UK
        string name
        int category_id FK
        decimal cost_price
        decimal unit_price
        int current_stock
        int reorder_level
        int lead_time_days
        int shelf_life_days
        int is_active
        datetime created_at
    }

    CUSTOMERS {
        int customer_id PK
        string customer_code UK
        string name
        string email
        string phone
        string gender
        string age_group
        string city
        string tier
        date registered_at
    }

    ORDERS {
        int order_id PK
        string invoice_no UK
        datetime order_date
        int customer_id FK
        string payment_method
        string channel
        decimal subtotal
        decimal discount_amount
        decimal tax_amount
        decimal total_amount
        string status
        datetime created_at
    }

    ORDER_ITEMS {
        int item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_cost
        decimal unit_price
        decimal total_price
        decimal profit_margin
    }

    INVENTORY_LOGS {
        int log_id PK
        int product_id FK
        string change_type
        int quantity
        datetime timestamp
        string reason
        decimal cost_impact
    }

    CATEGORIES ||--o{ PRODUCTS : "contains"
    CUSTOMERS ||--o{ ORDERS : "places"
    ORDERS ||--|{ ORDER_ITEMS : "has_lines"
    PRODUCTS ||--o{ ORDER_ITEMS : "referenced_in"
    PRODUCTS ||--o{ INVENTORY_LOGS : "tracks_stock"
```

---

## 2. Data Flow Diagrams (DFD)

### 2.1 DFD Level 0 (Context Level Diagram)
```mermaid
graph LR
    User[Store Manager / Business Executive / Recruiter] -->|Selects Domain / Enters Transactions / Adjusts Hyperparameters| OmniPulse[Outlook360 Platform]
    OmniPulse -->|Executive KPIs, Demand Forecasts, Customer Clusters, Basket Rules, Stock Alerts| User
    OmniPulse <-->|Atomic Transactions, DDL, SQL Queries| DB[(MySQL 8.0 / SQLite Relational DB)]
```

### 2.2 DFD Level 1 (System Decomposition)
```mermaid
graph TD
    User[Executive / Operator] -->|POS Billing Entry| POS[1.0 POS Transaction Simulator]
    POS -->|Insert Order & Line Items| DB[(MySQL / SQLite DB)]
    POS -->|Deduct Stock| DB

    User -->|Domain Switch Request| DS[2.0 Domain Manager & Seeder]
    DS -->|Re-seed Schema & Catalogs| DB

    DB -->|Raw Transaction Tables| ETL[3.0 Data Extraction & Aggregation Layer]
    
    ETL -->|Aggregated Series| ML1[4.0 Demand Forecaster - Holt-Winters]
    ETL -->|RFM Vectors| ML2[5.0 Customer Clustering - K-Means & PCA]
    ETL -->|Transaction Baskets| ML3[6.0 Market Basket Engine - Apriori]
    ETL -->|Product Sales & Variance| ML4[7.0 Inventory ABC-XYZ Optimizer]
    ETL -->|Order Feature Vectors| ML5[8.0 Anomaly Detection - Isolation Forest]

    ML1 --> UI[9.0 Streamlit Glassmorphic Dashboard]
    ML2 --> UI
    ML3 --> UI
    ML4 --> UI
    ML5 --> UI
    UI -->|Render Visualizations & Interactive Reports| User
```

### 2.3 DFD Level 2 (Data Science Pipeline Flow)
```mermaid
graph TD
    A[Raw Database Tables] --> B[Data Preprocessing & Cleansing]
    B --> C1[RFM Matrix Computation]
    B --> C2[Time-Series Continuous Aggregation]
    B --> C3[Binary Basket Crosstab Matrix]
    B --> C4[Daily SKU Demand Variance Calculation]

    C1 --> D1[Log Transform + Standard Scaler]
    D1 --> E1[K-Means Clustering & Silhouette Evaluation]
    E1 --> F1[PCA 2D/3D Dimensionality Reduction]

    C2 --> D2[Train/Test Historical Split]
    D2 --> E2[Holt-Winters Level + Trend + Seasonality Fit]
    E2 --> F2[Error Metrics MAE/RMSE/MAPE + 95% Confidence Band]

    C3 --> D3[Apriori Frequent Itemset Generation]
    D3 --> E3[Association Rule Pruning Lift > 1.0 & Confidence Filter]
    E3 --> F3[Cross-Sell Recommendation Ranking]

    C4 --> D4[Cumulative Revenue Share ABC Class]
    C4 --> E4[Coefficient of Variation XYZ Class]
    D4 & E4 --> F4[9-Box Matrix + Statistical Safety Stock SS & Dynamic ROP]
```

---

## 3. UML Class Diagram

```mermaid
classDiagram
    class DatabaseManager {
        -Engine _engine
        +execute_query(sql, params) DataFrame
        +execute_non_query(sql, params) int
        +ensure_schema() void
        +is_sqlite() bool
        +get_table_names() List
    }

    class EDAEngine {
        +get_kpi_summary() Dict
        +get_monthly_growth_trend() DataFrame
        +get_pareto_analysis() Tuple
        +get_hourly_heatmap_matrix() DataFrame
    }

    class RFMSegmentationEngine {
        +compute_rfm_metrics() DataFrame
        +find_optimal_clusters(df, max_k) Dict
        +run_kmeans_clustering(n_clusters) Tuple
    }

    class DemandForecaster {
        +prepare_daily_series() DataFrame
        +forecast_holt_winters(target_col, horizon, test_days) Tuple
    }

    class MarketBasketEngine {
        +generate_association_rules(min_support, min_conf, min_lift) Tuple
        +get_recommendations_for_product(product_name, rules_df, top_n) List
    }

    class InventoryOptimizer {
        +compute_abc_xyz_matrix(service_level) Tuple
    }

    class AnomalyDetector {
        +detect_order_anomalies(contamination, random_state) Tuple
    }

    class ExecutiveReportGenerator {
        +generate_html_report(output_path) str
    }

    EDAEngine --> DatabaseManager
    RFMSegmentationEngine --> DatabaseManager
    DemandForecaster --> DatabaseManager
    MarketBasketEngine --> DatabaseManager
    InventoryOptimizer --> DatabaseManager
    AnomalyDetector --> DatabaseManager
    ExecutiveReportGenerator --> EDAEngine
    ExecutiveReportGenerator --> RFMSegmentationEngine
    ExecutiveReportGenerator --> DemandForecaster
    ExecutiveReportGenerator --> InventoryOptimizer
```

---

## 4. UML Sequence Diagram (Real-Time POS Billing Flow)

```mermaid
sequenceDiagram
    autonumber
    actor Cashier as Store Cashier / User
    participant UI as POS Simulator UI (Streamlit)
    participant Engine as DatabaseManager / Transaction Engine
    participant DB as MySQL / SQLite Database
    participant MBA as MarketBasketEngine

    Cashier->>UI: Selects Product & Quantity
    UI->>MBA: get_recommendations_for_product(selected_item)
    MBA-->>UI: Returns Frequently Bought Together items (Lift score)
    UI-->>Cashier: Displays Cross-Sell AI Recommendation Card
    Cashier->>UI: Selects Customer & Clicks "Complete Transaction"
    UI->>Engine: begin_transaction()
    Engine->>DB: INSERT INTO orders (Header details, totals, tax)
    Engine->>DB: INSERT INTO order_items (Line items, costs, profit)
    Engine->>DB: UPDATE products SET current_stock = current_stock - qty
    Engine->>DB: INSERT INTO inventory_logs (Stock movement record)
    Engine->>DB: COMMIT
    DB-->>Engine: Transaction Success (ACID Guaranteed)
    Engine-->>UI: Return invoice_id and order summary
    UI-->>Cashier: Renders Printable Thermal Receipt Preview & Clears Cart
```

---

## 5. Performance Indexing & Query Optimization Strategy

To ensure zero latency across analytical aggregations and machine learning model training, the relational schema enforces non-clustered B-Tree indexing on all foreign keys and temporal filter columns:

1. `idx_orders_date`: Accelerates time-series slicing and daily revenue aggregation (`GROUP BY DATE(order_date)`).
2. `idx_order_items_order`: Optimizes inner joins between orders header and line items.
3. `idx_order_items_product`: Accelerates product-level velocity and Market Basket crosstab pivoting.
4. `idx_products_category`: Speeds up department and category hierarchy rollups.
5. `idx_inventory_logs_timestamp`: Enables fast chronological stock ledger audits.
