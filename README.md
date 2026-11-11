
# E-commerce Data Analysis Using MongoDB and PyMongo

An exploratory data analysis project built using **MongoDB, PyMongo, Python, Pandas, NumPy, Plotly, and Streamlit**. The project analyses an e-commerce sample database containing 31 collections and demonstrates MongoDB document queries, aggregation pipelines, data analysis, and indexing performance.

It also includes an interactive Streamlit dashboard to explore product information, inventory, orders, customers, payments, and product reviews.

## Project Structure

```text
E-commerce-Data-Analysis-Using-MongoDB-and-PyMongo/
│
├── Data/
│   └── ecommerce-sample-database-1k-en_GB-v2.json
│
├── Notebooks/
│   ├── 01_LoadingDataset.ipynb
│   ├── 02_product_exploration.ipynb
│   ├── 03_product_price_analysis.ipynb
│   ├── 04_category_analysis.ipynb
│   └── 05_indexing_performance.ipynb
│
├── Dashboard/
│   └── app.py
│
├── findings.ipynb
├── imp_findings.txt
├── README.md
├── requirements.txt
└── .gitignore
```

## Project Contents

- **Dataset:** A sample e-commerce database containing 31 collections, including products, users, orders, payments, inventory, and other related records.
- **01 - Loading Dataset:** Connects to MongoDB Atlas, loads the JSON dataset, imports records into their respective collections, and verifies document counts.
- **02 - Product Data Exploration and Filtering:** Demonstrates document retrieval, projection, filtering, sorting, limiting, comparison operators, and regular expression searches using PyMongo.
- **03 - Product Price Analysis:** Calculates product price summaries using MongoDB aggregation operators such as `$group`, `$avg`, `$min`, `$max`, and `$sum`. It also explores product-category relationships.
- **04 - Product Distribution by Category:** Uses `$lookup`, `$unwind`, `$group`, and `$sort` to analyse product distribution across categories.
- **05 - Indexing and Query Performance:** Compares MongoDB query execution statistics before and after creating an index on the product price field.
- **Findings:** Contains additional analysis and documented relationships between the database collections.
- **Interactive Dashboard:** A Streamlit application presenting different e-commerce analytics through interactive charts, metrics, and data tables.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| MongoDB Atlas | NoSQL database |
| PyMongo | MongoDB connectivity and queries |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Plotly Express | Interactive visualizations |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Exploratory analysis |

## Requirements

- Python 3.9 or newer
- MongoDB Atlas account or an accessible MongoDB deployment
- Jupyter Notebook or JupyterLab

Install the project dependencies using the provided `requirements.txt` file.

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```bash
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure MongoDB

1. Create a MongoDB Atlas cluster.
2. Configure your database user and allow your IP address to connect.
3. Create a `.env` file in the project root.
4. Add your MongoDB connection string:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-host>/?retryWrites=true&w=majority
```

Replace the placeholders with your own MongoDB Atlas credentials and cluster details.

The notebooks and dashboard use the database:

```text
ecommerce_analysis
```

**Important:** Keep your `.env` file private. Never commit database credentials to GitHub.

## Load the Sample Dataset

1. Open a terminal in the project root.
2. Start Jupyter Notebook:

```bash
jupyter notebook
```

3. Open `Notebooks/01_LoadingDataset.ipynb`.
4. Execute the notebook cells in sequence.

The notebook reads the JSON dataset from the `Data/` directory and imports each collection into MongoDB Atlas.

After importing, it verifies the collection names and document counts.

**Note:** The data-loading notebook uses `insert_many()`. Running the import operation multiple times can create duplicate records. Use a fresh database or clear the existing imported collections before re-importing.

## Run the Analysis Notebooks

After successfully importing the dataset, execute the notebooks in the `Notebooks/` directory.

The analyses demonstrate:

- MongoDB document retrieval and projection.
- Filtering with comparison and logical operators.
- Sorting and limiting query results.
- Case-insensitive text searches using `$regex`.
- Aggregation using `$group`, `$avg`, `$min`, `$max`, and `$sum`.
- Joining collections using `$lookup` and `$unwind`.
- Index creation and query performance analysis.

The indexing analysis uses the `products.price` field. Execution statistics can vary depending on database size and cluster conditions.

## Interactive Streamlit Dashboard

The project includes an interactive dashboard built using Streamlit, PyMongo, Pandas, NumPy, and Plotly Express.

Run the dashboard from the project root:

```bash
python -m streamlit run Dashboard/app.py
```

The dashboard provides seven sections:

1. **Overview:** Displays key e-commerce metrics and product summaries.
2. **Product Analysis:** Explores product prices, product availability, and expensive products.
3. **Inventory Analysis:** Examines product stock, reserved stock, available stock, warehouse-wise inventory, and reorder levels.
4. **Order Analysis:** Analyses orders, order items, quantities, and popular products.
5. **Customer Analysis:** Explores customer information, order activity, and addresses.
6. **Payment Analysis:** Examines payment amounts and payment status.
7. **Review Analysis:** Analyses product reviews and rating distributions.

The dashboard uses the `ecommerce_analysis` database and requires the relevant collections to be imported before execution.

## Database Collections and Relationships

The original JSON dataset contains 31 collections. The dashboard focuses on the following nine collections:

| Collection | Description |
|---|---|
| `products` | Product details and pricing |
| `product_inventories` | Product stock and warehouse references |
| `warehouses` | Warehouse information |
| `users` | Customer information |
| `orders` | Customer order records |
| `order_items` | Products and quantities associated with orders |
| `payments` | Payment records and statuses |
| `addresses` | Customer address information |
| `product_reviews` | Customer product reviews |

### Important Collection Relationships

The project explores the following document references:

- `users.id` → `orders.user_id`
- `users.id` → `addresses.user_id`
- `users.id` → `product_reviews.user_id`
- `orders.id` → `order_items.order_id`
- `orders.id` → `payments.order_id`
- `products.id` → `order_items.product_id`
- `products.id` → `product_inventories.product_id`
- `products.id` → `product_reviews.product_id`
- `warehouses.id` → `product_inventories.warehouse_id`
- `payment_methods.id` → `payments.payment_method_id`
- `categories.id` → `products.category_id`

These relationships are maintained through document fields. MongoDB does not automatically enforce relational foreign-key constraints.

The project uses MongoDB queries, Pandas operations, and aggregation pipelines to retrieve and analyse related information.

## Security

- Store MongoDB credentials in the `.env` file.
- Do not hardcode credentials in Python scripts or notebooks.
- Do not commit `.env` to the GitHub repository.
- If database credentials are accidentally exposed, rotate the password through MongoDB Atlas.

## Dataset Source

[DatabaseSample – E-commerce Sample Database](https://databasesample.com/datasets/ecommerce-sample-database)

## References

- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [PyMongo Documentation](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/)
- [MongoDB Aggregation Pipeline](https://www.mongodb.com/docs/manual/aggregation/)
- [MongoDB Indexes](https://www.mongodb.com/docs/manual/indexes/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)

---

**Project:** E-commerce Data Analysis Using MongoDB and PyMongo

**Focus:** NoSQL Database Management, Data Analysis, Query Optimization, and Interactive Visualization
