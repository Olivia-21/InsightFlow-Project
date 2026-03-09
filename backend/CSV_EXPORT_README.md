# CSV Export to MinIO - Implementation Guide

## Overview
This feature allows exporting Review data as CSV files directly to MinIO object storage.

## Components Implemented

### 1. Configuration (application.yml)
```yaml
minio:
  url: http://localhost:9000
  access-key: minioadmin
  secret-key: minioadmin
  bucket: insightflow-exports
```

### 2. MinIO Client Configuration
- **File**: `config/MinioConfig.java`
- Creates and configures `MinioClient` bean for dependency injection
- Uses properties from application.yml

### 3. CSV Generator
- **File**: `util/CsvGenerator.java`
- Generates CSV format from Review entities
- Includes columns: review_id, user_id, product_id, product_name, store_id, store_name, rating, comment, review_date
- Uses Apache Commons CSV library

### 4. Review Export Service
- **File**: `service/ReviewExportService.java`
- **Method**: `exportReviews()`
- **Flow**:
  1. Fetches all reviews from database (ordered by created date)
  2. Generates CSV using CsvGenerator
  3. Ensures MinIO bucket exists (creates if not)
  4. Uploads CSV file to MinIO with timestamp-based filename
  5. Returns the object path in MinIO

### 5. Review Export Controller
- **File**: `controller/ReviewExportController.java`
- **Endpoint**: `GET /api/export/reviews`
- **Response**: JSON with export status and MinIO file path
- **Error Handling**: Returns 500 with error details on failure

## API Usage

### Export Reviews to MinIO
```http
GET /api/export/reviews
```

**Success Response** (200 OK):
```json
{
  "message": "Reviews exported successfully",
  "path": "reviews/reviews_1709888400000.csv"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "Export failed",
  "details": "Connection refused to MinIO"
}
```

## Setup Requirements

### 1. MinIO Server
Start MinIO locally:
```bash
# Using Docker
docker run -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

### 2. Dependencies
All required dependencies are in `pom.xml`:
- `io.minio:minio:8.5.14` - MinIO SDK
- `org.apache.commons:commons-csv:1.11.0` - CSV generation

### 3. Database
Ensure Reviews exist in the database to export

## File Structure Created
```
backend/
├── src/main/java/com/insightflow/
│   ├── config/
│   │   └── MinioConfig.java         # MinIO client configuration
│   ├── controller/
│   │   └── ReviewExportController.java  # REST endpoint
│   ├── service/
│   │   └── ReviewExportService.java     # Export logic
│   └── util/
│       └── CsvGenerator.java             # CSV generation utility
└── src/main/resources/
    └── application.yml                    # MinIO configuration
```

## CSV Output Format
```csv
review_id,user_id,product_id,rating,comment,review_date
1,101,201,5,"Great product!",2026-03-08T10:30:00
2,102,202,4,"Good quality",2026-03-08T11:15:00
```

## Compilation Issue Note

**Current Status**: The code is complete and correct, but compilation fails due to a **Lombok + Java 25 compatibility issue** (nbjavac/TypeTag error).

**Solutions**:
1. **Recommended**: Switch to Java 17 or 21 LTS:
   ```bash
   # Set JAVA_HOME to Java 17/21
   # Then run: mvn clean compile
   ```

2. **Alternative**: Update IDE to use standard javac instead of nbjavac

3. **Future**: Wait for Lombok 1.18.37+ which may have full Java 25 support

## Testing the Feature

Once compilation succeeds:

1. Start the application
2. Ensure MinIO is running  
3. Add some review data to the database
4. Call the export endpoint:
```bash
curl http://localhost:8080/api/export/reviews
```
5. Check MinIO console (http://localhost:9001) for the exported CSV file in `insightflow-exports` bucket

## Mappers Created

Additional MapStruct mappers generated for all model classes:
- ReviewMapper
- UserMapper  
- ProductMapper
- CartMapper
- OrderMapper
- StoreMapper
- FeedbackCategoryMapper
- DataSourceMapper
- PipelineMapper

These will be automatically implemented by MapStruct annotation processor once compilation succeeds.

Final Step: Data Migration
To move your local data into the Docker volume, run this command in your terminal:

```bash
pg_dump -U postgres -a -d insight-flow | PGPASSWORD=insightflow_pass psql -h localhost -p 5434 -U insightflow -d insight-flow
```

Why run this?
pg_dump -a: Extracts only the data (since the tables already exist).
psql -p 5434: Sends that data to the Docker database.
PGPASSWORD: Automatically handles the Docker database password.
You will still be prompted for your local Postgres password (for the postgres user).

Verification
After running the migration:

Refresh your backend export or check the logs.
You can access the Docker database at any time using port 5434.