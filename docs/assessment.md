# R.A.V.I.D. Assessment & Evaluation for Back End Candidates

_This Markdown rewrites the PDF into a cleaner format. Where the source PDF contains obvious typos or inconsistent examples, that is called out explicitly instead of being changed silently._

## Source Information

- Organization: American Tiger LLC
- Address: 5900 Balcones Drive Suite 100, Austin, TX 78731
- Website: www.americantiger.biz
- Assessment title: Assessment & Evaluation for Remote Candidates - Apr 2026

## Project Overview

**Project:** CSV File Uploader, Operations API, Logs Monitoring, and Dockerization

### Primary Objective

To consider your candidature for the Python Backend developer position.

### Evaluation Objective

This Mini Project will give your potential Team Member and other senior stakeholders an opportunity to assess and evaluate your technical skills and decide potential next steps, if any.

### Technical Objective

Build an API-based system that allows users to upload CSV files, perform operations like deduplication, extract unique values, and manage background task execution using Celery and Redis. Also build a logging dashboard to show logs for the API system and Celery worker.

## Timeline

- Project start date: Friday, April 17th, 2026
- Last submission date: Sunday, April 19th, 2026
- Status: Take Home / Remote
- Note: Submitting early will improve your evaluation. Do not hesitate to reach out if you have any questions.

## Project Requirements

## Part 1

### APIs to Be Created

### 1. CSV Upload API

- Endpoint: `/api/upload-csv/`
- Method: `POST`
- Request:
  - `multipart/form-data`
  - Includes a file field containing the CSV file

Example request:

```json
{
  "file": "sample.csv"
}
```

Responses:

- Success:

```json
{
  "message": "File uploaded successfully",
  "file_id": "<file_id>"
}
```

- Failure for invalid file type or empty request:

```json
{
  "error": "Invalid file format. Only CSV files are allowed."
}
```

### 2. CSV Operation API

- Endpoint: `/api/perform-operation/`
- Method: `POST`
- Request:
  - JSON body containing `file_id` and operation type

Example request:

```jsonc
{
  "file_id": "<file_id>",
  "operation": "dedup", // or "unique", "filter", etc.
}
```

Supported operations mentioned in the source:

- `dedup`: Remove duplicate rows from the CSV file
- `unique`: Extract unique values from a specific column
  - Requires an additional `column` input
- `filter`: Apply filters based on specific criteria
  - Requires additional filter parameters

Responses:

- Success when a background task is created:

```json
{
  "message": "Operation started",
  "task_id": "<task_id>"
}
```

- Failure for invalid operation or missing file:

```json
{
  "error": "Invalid operation or file not found."
}
```

### 3. Task Status API

- Endpoint: `/api/task-status/`
- Method: `GET`
- Request parameters:
  - `task_id`: ID of the task to check
  - `n` (optional): Number of records to return from the processed CSV file
    - Default: `100`

Example request:

```text
/api/task-status/?task_id=<task_id>&n=50
```

Responses:

#### Task Running

```json
{
  "task_id": "<task_id>",
  "status": "PENDING"
}
```

#### Task Success

- Return the first `n` records from the processed CSV file as JSON
- Default to `100` records when `n` is not provided
- Include a link to the processed file

```json
{
  "task_id": "<task_id>",
  "status": "SUCCESS",
  "result": {
    "data": [
      {
        "column1": "value1",
        "column2": "value2",
        "...": "..."
      },
      {
        "column1": "value1",
        "column2": "value2",
        "...": "..."
      }
    ],
    "file_link": "<processed_file_link>"
  }
}
```

Note: The source PDF indicates the `data` array continues `// ... up to n records`.

#### Task Failed

```json
{
  "task_id": "<task_id>",
  "status": "FAILURE",
  "error": "Description of the error"
}
```

## Operations Available

### 1. Deduplication

- Purpose: Remove duplicate rows from the CSV file
- Input: CSV file referenced by `file_id`
- Output: A new CSV file without duplicate rows

### 2. Unique

- Purpose: Extract unique values from a specific column
- Input:
  - CSV file referenced by `file_id`
  - `column`: the column to inspect for unique values
- Output:
  - A list of unique values, or
  - A CSV file with unique rows based on the selected column

### 3. Filter

- Purpose: Apply filters based on user-specified criteria (optional)
- Input:
  - CSV file referenced by `file_id`
  - Filtering conditions such as column names and values
- Output: A filtered CSV file based on the given conditions

## Expected Responses Summary

### CSV Upload API

- Success:

```json
{
  "message": "File uploaded successfully",
  "file_id": "<file_id>"
}
```

- Failure:

```json
{
  "error": "Invalid file format"
}
```

### CSV Operation API

- Success:

```json
{
  "message": "Operation started",
  "task_id": "<task_id>"
}
```

- Failure:

```json
{
  "error": "Invalid operation or file not found"
}
```

### Task Status API

#### Task Running

```json
{
  "task_id": "<task_id>",
  "status": "PENDING"
}
```

#### Task Success

- Return the first `n` records from the processed CSV file in JSON format
- Default to `100` records when `n` is not specified
- Include a processed file download link

```json
{
  "task_id": "<task_id>",
  "status": "SUCCESS",
  "result": {
    "data": [
      {
        "column1": "value1",
        "column2": "value2",
        "...": "..."
      },
      {
        "column1": "value1",
        "column2": "value2",
        "...": "..."
      }
    ],
    "file_link": "<processed_file_link>"
  }
}
```

Note: The source PDF indicates the `data` array continues `// ... up to n records`.

#### Task Failed

```json
{
  "task_id": "<task_id>",
  "status": "FAILURE",
  "error": "Description of the error"
}
```

## Part 2: Authentication and File Upload API Requirements

### 1. User Registration

- Endpoint: `/api/register/`
- Method: `POST`
- Request:
  - Form data containing email and password

Example request:

```json
{
  "email": "example@gmail.com",
  "password": "12345678"
}
```

Source note: The PDF example contains typographical and quotation issues (`exapmle@gmail.com` and malformed quotes). The example above is normalized only for readability; the required fields are still `email` and `password`.

Responses:

- On success:

```json
{
  "message": "Registration successful",
  "user_id": "<user_id>"
}
```

- On failure:

```json
{
  "error": "Password and confirm password do not match"
}
```

Source note: The failure response mentions `confirm password`, but the request example in the PDF only lists `email` and `password`.

### 2. User Login

- Endpoint: `/api/login/`
- Method: `POST`
- Request:
  - Form data containing email and password

Example request:

```json
{
  "email": "example@gmail.com",
  "password": "12345678"
}
```

Source note: The PDF example contains typographical and quotation issues (`exapmle@gmail.com` and malformed quotes). The example above is normalized only for readability; the required fields are still `email` and `password`.

Responses:

- On success:

```json
{
  "message": "Login successful"
}
```

- On failure:

```json
{
  "error": "Invalid email or password"
}
```

### 3. JWT Token Middleware

Ensure all protected routes require a valid JWT token in the `Authorization` header.

## Part 3: Structured Observability

Implement a centralized, structured logging system for the full application stack using Grafana and Loki.

### Requirements

#### 1. Structured Logging

- Configure Django to output logs in JSON format instead of plain text
- Configure Celery workers to include task-specific metadata in their JSON logs
  - Example metadata: `task_id`, `task_name`

#### 2. Log Aggregation

Add a log collection service to `docker-compose.yml` using one of the following:

- Promtail
- Grafana Alloy
- Any other log collecting tool

That service must:

- Scrape logs from the Django and Celery containers
- Ship the logs to a Loki service

#### 3. Visualization

Provision a Grafana dashboard that displays:

- A live stream of logs filtered by service (`Django` vs `Celery`)
- Bonus: A count of error-level logs over the last 30 minutes
- Bonus: A panel showing the "Top 5 slowest CSV operations" based on log data

## Part 4: Dockerizing and Finalization

### Dockerization

Use Docker and Docker Compose to package the following services:

- Web application
- Database
- Redis
- Celery
- Dashboard services

### Documentation and Delivery Requirements

- Include the necessary Docker commands to run the system in a `README`
- Document the API using one of the following:
  - Postman
  - Bruno
  - OpenAPI
  - Another widely used API documentation tool
- Ensure the `README` includes clear instructions for setting up and running the entire application

## Submission

Please submit the final submission / paper to:

- Mr. Phuong Tung Tran — `phuongtung.tran@ravid.cloud`
- Mr. Truong Vinh Phuoc “Matthew” — `phuoc.truong@ravid.cloud`

## Closing Notes

Should you have any technical questions at any time, please contact:

- Mr. Phuong Tung Tran, Back-End Developer & Full Stack Development Team
- Mr. Truong Vinh Phuoc “Matthew”, Back-End Developer & Full Stack Development Team
