#!/bin/bash

# Global Terrorism Database Dashboard Launcher
# FBI-Style Threat Intelligence Platform

echo "=================================================="
echo "🔒 THREAT INTELLIGENCE DASHBOARD 🔒"
echo "=================================================="
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found."
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "Installing dashboard dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Check database connection
echo "Checking database connection..."
if ! python3 -c "import psycopg2; from dotenv import load_dotenv; import os; load_dotenv(); psycopg2.connect(host=os.getenv('DATABASE_HOST'), port=os.getenv('DATABASE_PORT'), database=os.getenv('DATABASE_NAME'), user=os.getenv('DATABASE_USER'), password=os.getenv('DATABASE_PASSWORD'))" 2>/dev/null; then
    echo "⚠️  WARNING: Could not connect to database"
    echo "Please ensure:"
    echo "  1. PostgreSQL is running"
    echo "  2. .env file has correct credentials"
    echo "  3. dbt models are materialized (run 'dbt run' in dbt_project/)"
    echo ""
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Database connection successful"
fi

echo ""
echo "=================================================="
echo "🚀 LAUNCHING DASHBOARD..."
echo "=================================================="
echo ""
echo "📍 Dashboard will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
streamlit run dashboard/dashboard.py --server.address=localhost
