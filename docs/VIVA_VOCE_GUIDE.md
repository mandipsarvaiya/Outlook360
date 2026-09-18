# Outlook360: Comprehensive Viva-Voce Examination Guide
### 50+ In-Depth Questions & Model Answers for MCA 3rd Semester & Technical Interviews

---

## Category 1: Python & System Architecture (Q1 – Q10)

### Q1: What is the architectural design pattern used in Outlook360?
**Answer:** The project follows a **Layered Clean Architecture (Separation of Concerns)** divided into 5 distinct tiers:
1. **Configuration Layer (`config/`)**: Manages environment variables, connection strings, and hyperparameters.
2. **Database & Data Tier (`database/`)**: Manages relational DDL schemas, connection pooling via SQLAlchemy, and parameterized analytical SQL queries.
3. **Synthetic Generator Tier (`data_generators/`)**: Provides domain presets and statistical transaction generation.
4. **Machine Learning & Analytics Tier (`ml_engine/`)**: Implements mathematical and ML pipelines independently of any UI framework.
5. **Presentation Tier (`app/` & `reports/`)**: Renders interactive Plotly visual components via Streamlit and generates automated executive HTML/PDF reports.

### Q2: Why did you choose SQLAlchemy alongside raw SQL queries?
**Answer:** SQLAlchemy provides robust connection pooling, transaction context managers (`with engine.begin()`), dialect abstraction between MySQL and SQLite, and SQL injection prevention via parameterized queries. We used raw SQL queries via SQLAlchemy for complex analytical aggregations (`GROUP BY`, window functions) to maintain full control over performance indexing and query optimization.

### Q3: What is the Singleton pattern used in `DatabaseManager`?
**Answer:** The `DatabaseManager` implements the **Singleton Pattern** using Python's `__new__` method to ensure that only a single database engine and connection pool instance is created across multiple web requests or Streamlit re-runs, preventing connection leaks and socket exhaustion.

### Q4: Why is `sys.path` dynamically configured at the top of each module?
**Answer:** It ensures that whether the project is executed via `streamlit run app/main.py`, `python test_runner.py`, or imported as a library, Python can locate all internal root modules (`config`, `database`, `ml_engine`) without raising `ModuleNotFoundError` across different operating systems.

### Q5: What is the purpose of `test_runner.py` and unit testing in this project?
**Answer:** `test_runner.py` executes automated integration and unit tests using Python's built-in `unittest` framework, validating database connectivity, schema integrity, and the numerical convergence of all 6 machine learning pipelines with execution time profiling.

---

## Category 2: Database Management & SQL / MySQL (Q11 – Q20)

### Q6: Explain the normalization level of your database schema.
**Answer:** The schema is normalized up to **Third Normal Form (3NF)**:
- **1NF**: All columns contain atomic values, and each record has a unique primary key.
- **2NF**: No partial dependency exists; all non-key attributes in `order_items` depend fully on the primary composite keys.
- **3NF**: No transitive dependencies exist. For example, `category_id` resides in `products`, while category descriptions reside in `categories`, avoiding redundant denormalization.

### Q7: How does your database support both MySQL and SQLite?
**Answer:** The schema uses ANSI SQL DDL compatible with SQLite and standard SQL. The connection manager inspects `DB_ENGINE` from `.env`. When configured for MySQL, it connects via `mysql-connector-python`, creates the database if absent, and translates SQLite autoincrement keywords to `AUTO_INCREMENT`. If MySQL is unavailable, it gracefully falls back to local SQLite to ensure uninterrupted offline demonstration during college viva exams.

### Q8: What indexing strategy did you apply to optimize query speed?
**Answer:** We created non-clustered B-Tree indexes:
1. `idx_orders_date` on `orders(order_date)` for fast time-series aggregation.
2. `idx_order_items_order` and `idx_order_items_product` on foreign keys in `order_items` for instant table joins.
3. `idx_products_category` on `products(category_id)` for category-level rollups.

### Q9: How are database transactions handled during POS billing?
**Answer:** Atomic ACID transactions are enforced using `with db_manager.engine.begin() as conn:`. Inserting the order header, inserting line items, decrementing product stock, and logging the inventory ledger happen inside a single transaction block. If any step fails, the entire transaction is rolled back automatically.

### Q10: What is the difference between OLTP and OLAP, and how does your project handle both?
**Answer:**
- **OLTP (Online Transaction Processing)**: High-frequency, single-record writes (e.g., POS checkout inserting rows into `orders` and `order_items`).
- **OLAP (Online Analytical Processing)**: Complex aggregate queries spanning thousands of rows for business intelligence (e.g., monthly growth trends, Pareto distributions). Outlook360 manages OLTP through transactional writes and OLAP through analytical SQL queries and in-memory Pandas transformations.

---

## Category 3: Exploratory Data Analysis & Statistics (Q21 – Q28)

### Q11: What is the Pareto Principle (80/20 Rule), and how is it calculated in your project?
**Answer:** The Pareto Principle states that roughly 80% of revenue comes from 20% of products. In `ml_engine/eda_engine.py`, products are sorted by revenue descending. Cumulative revenue percentage is calculated ($C_k = \frac{\sum R_i}{R_{total}} \times 100\%$). SKUs where $C_k \le 80\%$ are tagged as *Vital Few*, while the remainder are tagged as *Useful Many*.

### Q12: How is Average Order Value (AOV) calculated?
**Answer:** $\text{AOV} = \frac{\text{Total Gross Revenue}}{\text{Total Completed Orders}}$. It measures the average monetary spend per transaction basket.

### Q13: Explain the Hourly Footfall Heatmap calculation.
**Answer:** SQL extracts `DAYOFWEEK(order_date)` and `HOUR(order_date)`, aggregating total order count. Pandas pivots this into a $7 \times 24$ matrix, visualized via Plotly Heatmaps to identify peak lunch and evening rush hours for staff scheduling.

---

## Category 4: Customer Segmentation & Machine Learning (Q29 – Q36)

### Q14: What is RFM Analysis?
**Answer:** RFM is a behavioral customer segmentation framework:
- **Recency ($R$)**: Days elapsed since customer's last order (lower is better).
- **Frequency ($F$)**: Total number of orders placed by customer (higher is better).
- **Monetary ($M$)**: Total financial value of purchases made (higher is better).

### Q15: Why did you apply Log-Transformation before K-Means clustering?
**Answer:** Customer spend and order frequency follow a right-skewed Pareto distribution with extreme outliers. Applying $X_{\text{log}} = \ln(1 + X)$ normalizes the variance and compresses long-tail distributions, preventing high-spending outliers from skewing Euclidean distance calculations in K-Means.

### Q16: Why is `StandardScaler` mandatory for K-Means?
**Answer:** K-Means relies on Euclidean distance: $d(p, q) = \sqrt{\sum (p_i - q_i)^2}$. If Monetary is in hundreds of dollars and Recency is in days, Monetary would dominate the distance metric. `StandardScaler` standardizes each feature to $\mu=0$ and $\sigma=1$, ensuring equal weight.

### Q17: How did you determine the optimal number of clusters ($K$)?
**Answer:** We evaluated two diagnostic metrics:
1. **The Elbow Method**: Plots Within-Cluster Sum of Squares (Inertia) against $K$. The "elbow" point where diminishing returns set in indicates optimal $K$.
2. **Silhouette Score**: Evaluates cluster cohesion versus separation ($s \in [-1, 1]$). A score $> 0.35$ confirms solid cluster separation.

### Q18: What is Principal Component Analysis (PCA) used for in your project?
**Answer:** Customer feature space contains 3 scaled dimensions (Recency, Frequency, Monetary). PCA performs orthogonal linear transformation to project this 3D feature space into 2D and 3D principal components ($PCA_1, PCA_2, PCA_3$) that capture the maximum variance, allowing interactive visualization of customer clusters.

---

## Category 5: Time Series Forecasting (Q37 – Q42)

### Q19: Why Holt-Winters Triple Exponential Smoothing over simple ARIMA?
**Answer:** Daily retail sales exhibit both a linear growth trend and strong 7-day cyclical weekly seasonality (weekend sales peaks). Holt-Winters explicitly decomposes the series into Level ($\alpha$), Trend ($\beta$), and Seasonality ($\gamma$) with minimal computational latency compared to high-order SARIMA search.

### Q20: Explain the error metrics MAE, RMSE, and MAPE.
**Answer:**
- **MAE (Mean Absolute Error)**: Average absolute magnitude of errors $\frac{1}{n}\sum |y - \hat{y}|$ (in currency units).
- **RMSE (Root Mean Squared Error)**: Penalizes large outlier errors more heavily $\sqrt{\frac{1}{n}\sum (y - \hat{y})^2}$.
- **MAPE (Mean Absolute Percentage Error)**: Expresses error as a percentage of actual sales $\frac{100\%}{n}\sum |\frac{y - \hat{y}}{y}|$, making accuracy intuitive for business managers.

### Q21: How are the 95% Confidence Intervals calculated in your forecast?
**Answer:** Using the standard deviation of residuals ($\sigma_{\text{res}}$) from historical test splits:
$$\text{Upper} = \hat{y}_t + 1.96 \cdot \sigma_{\text{res}}, \quad \text{Lower} = \max(0, \hat{y}_t - 1.96 \cdot \sigma_{\text{res}})$$

---

## Category 6: Market Basket Analysis & Association Rules (Q43 – Q47)

### Q22: What is the Apriori principle?
**Answer:** The Apriori principle states that *all non-empty subsets of a frequent itemset must also be frequent*. If $\{A, B\}$ is infrequent, then $\{A, B, C\}$ cannot be frequent. This allows pruning the search space efficiently.

### Q23: Define Support, Confidence, and Lift.
**Answer:**
- **Support**: Proportion of total transactions containing both $A$ and $B$: $P(A \cap B)$.
- **Confidence**: Conditional probability of buying $B$ given $A$: $P(B \mid A) = \frac{\text{Support}(A \cap B)}{\text{Support}(A)}$.
- **Lift**: Ratio of observed co-occurrence to expected co-occurrence if independent: $\frac{\text{Confidence}(A \Rightarrow B)}{\text{Support}(B)}$.
  - $\text{Lift} = 1$: Independent events.
  - $\text{Lift} > 1$: Strong affinity (buying $A$ increases likelihood of buying $B$).

---

## Category 7: Inventory Optimization & Supply Chain Science (Q48 – Q52)

### Q24: What is the ABC-XYZ Inventory Matrix?
**Answer:**
- **ABC Analysis (Value)**: Classifies items by cumulative revenue contribution (A: 70%, B: 20%, C: 10%).
- **XYZ Analysis (Predictability)**: Classifies items by Coefficient of Variation ($CV = \frac{\sigma}{\mu}$) of daily demand:
  - **X**: $CV \le 0.45$ (Constant, stable demand).
  - **Y**: $0.45 < CV \le 0.85$ (Fluctuating/seasonal).
  - **Z**: $CV > 0.85$ (Erratic, sporadic demand).
- The 9 combinations (AX through CZ) dictate stocking strategy (e.g., AX is automated Just-In-Time; AZ requires tight managerial oversight).

### Q25: Explain the statistical Safety Stock ($SS$) and Reorder Point ($ROP$) formulas.
**Answer:**
- **Safety Stock**: $SS = Z \times \sqrt{L \times \sigma_d^2}$, where $Z$ is the standard normal factor for target service level (e.g., $Z=1.65$ for 95%), $L$ is supplier lead time in days, and $\sigma_d$ is daily demand standard deviation.
- **Reorder Point**: $ROP = (\bar{d} \times L) + SS$. When stock dips to $ROP$, a purchase order must be issued to prevent stockouts before the supplier delivers.

---

## Category 9: Role-Based Access Control (RBAC) & Authentication (Q28 – Q30)

### Q28: How does Outlook360 implement Role-Based Access Control (RBAC)?
**Answer:** The system implements a three-tier RBAC architecture stored in the `users` table:
1. **Store Owner (Executive / Admin)**: Logs in using **Gmail/Email & Password**. Possesses full access across all 11 modules including Executive BI, Sales Analytics, ML Models, Staff Account Management, and Domain Switching.
2. **Cashier (Counter Operations)**: Logs in using **Employee ID (`EMP-CSH-01`) & Password**. Has access restricted to the Point-of-Sale (POS) Billing Terminal, Customer Onboarding (Add Customer), and AI Cross-Sell Recommendations.
3. **Inventory Staff (Supply Chain)**: Logs in using **Employee ID (`EMP-INV-01`) & Password**. Has access restricted to Product Master Catalog CRUD, Stock In/Out Ledger Adjustments, and **🚨 Low Stock & Stockout Early-Warning Alerts**.

### Q29: How are user passwords secured?
**Answer:** Passwords are never stored in plaintext. They are hashed using **SHA-256 with a cryptographic application salt** (`hashlib.sha256((password + salt).encode('utf-8')).hexdigest()`). Database queries validate credentials against this one-way cryptographic hash.

### Q30: How are financial transactions localized to Indian Rupee (`₹` / INR)?
**Answer:** The `business_profiles` metadata and database schema store currency formatters (`₹`), and all product prices, discount rules, margins, and Plotly charts are dynamically rendered in INR (`₹`) with Indian numbering conventions.

