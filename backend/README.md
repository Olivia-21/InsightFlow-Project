# InsightFlow Backend

This is the core Spring Boot application for the InsightFlow project, designed to handle data ingestion, processing, and exports for retail analytics.

## 🚀 Quick Start (Docker)

The easiest way to run the entire stack (Backend, Postgres, MinIO) is using Docker Compose from the project root.

```bash
# Start all services
docker compose up -d

# View backend logs
docker logs -f insightflow-backend
```

- **Backend API**: `http://localhost:8080`
- **Postgres (App DB)**: `localhost:5434`
- **Postgres (Warehouse)**: `localhost:5433`
- **MinIO Console**: `http://localhost:9001` (User/Pass: `minioadmin` / `minioadmin`)

---

## 🏗️ Data Architecture

### Core Entities
The backend follows a refined retail schema. Key entities include:
- **Users**: Admin and customer accounts.
- **Product**: Catalog items with `unit_price`, `reorder_level`, and `supplier` tracking.
- **Store**: Physical locations categorized by `region`.
- **StoreInventory**: Real-time stock tracking (`opening_stock`, `closing_stock`, `unit_sold`).
- **Order / OrderItem**: Sales transaction records with `tax_amount` and `discount_applied`.
- **Review**: Customer feedback and ratings.

### Database Seeding
On every clean startup, the application automatically seeds the database with realistic test data from `src/main/resources/scripts/seed-data.sql`. This ensures a ready-to-use environment for development and data engineering.

---

## 📊 For Data Engineers

### CSV Export to MinIO
The application provides an automated pipeline to export database records to MinIO object storage for downstream processing.

**Trigger Export:**
To generate the latest CSV snapshots and upload them to MinIO, call the following endpoint:
```bash
curl http://localhost:8080/api/export/reviews
```

**Accessing Data:**
1. Log in to the **MinIO Console** (`http://localhost:9001`).
2. Navigate to the `insightflow-exports` bucket.
3. Your CSV files will be stored under the `reviews/` prefix with a timestamp.

---

## 🛠️ Local Development

### Prerequisites
- **Java**: 17 or 21 (LTS recommended).
- **Maven**: 3.8+.
- **Docker**: For running supporting services.

### Manual Build
```bash
mvn clean install -DskipTests
java -jar target/insightflow-0.0.1-SNAPSHOT.jar
```

> [!IMPORTANT]
> **Lombok Compatibility Note**: If you encounter compilation errors like `nbjavac/TypeTag`, ensure you are using Java 17 or 21. Java 25 is currently not fully supported by older Lombok versions used in this project.

### Environment Variables
The following variables can be used to override default settings:
| Variable | Description | Default |
|----------|-------------|---------|
| `SPRING_DATASOURCE_URL` | JDBC URL | `jdbc:postgresql://localhost:5432/insight-flow` |
| `MINIO_URL` | MinIO Server URL | `http://localhost:9000` |
| `MINIO_BUCKET` | Export Bucket Name | `insightflow-exports` |

---

## 📜 API Documentation
Once the app is running, you can access the interactive Swagger UI at:
`http://localhost:8080/swagger-ui.html`
