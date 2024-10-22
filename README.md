# EzyMetrics Backend

## Description

EzyMetrics Backend is a backend service for EzyMetrics that focuses on data integrations and reporting. It integrates with dummy CRM and marketing platforms to simulate fetching lead and campaign data. The backend is built using Flask and connects to a database for data storage and processing.

## Features

- API service development for fetching lead and campaign data.
- Data storage in a relational database.
- ETL process to transform raw data into meaningful metrics.
- API endpoints for generating reports in PDF and CSV formats.
- Email notifications for alerts based on specified conditions.

## Technologies Used

- **Flask**: Web framework for building the API.
- **SQLAlchemy**: ORM for database interactions.
- **Pandas**: Data manipulation and analysis.
- **ReportLab**: PDF generation.
- **SMTP**: Email notifications.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rajkumarpasupuleti710/EzyMetrics_Backend.git
   cd EzyMetrics_Backend
