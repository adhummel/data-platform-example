#!/usr/bin/env python3
"""
Test script to verify dashboard prerequisites
Run this before launching the dashboard to ensure everything is configured correctly
"""

import sys
import os
from dotenv import load_dotenv

def test_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def test_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'plotly': 'Plotly',
        'psycopg2': 'psycopg2',
        'dotenv': 'python-dotenv',
        'numpy': 'NumPy',
        'sklearn': 'scikit-learn',
        'networkx': 'NetworkX'
    }

    all_installed = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} (missing)")
            all_installed = False

    if not all_installed:
        print("\n   Run: pip install -r requirements_dashboard.txt")

    return all_installed

def test_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔍 Checking environment configuration...")

    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        print("   Create .env file with database credentials")
        return False

    load_dotenv()

    required_vars = [
        'DATABASE_HOST',
        'DATABASE_PORT',
        'DATABASE_NAME',
        'DATABASE_USER',
        'DATABASE_PASSWORD'
    ]

    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask password
            display_value = '***' if 'PASSWORD' in var else value
            print(f"   ✅ {var} = {display_value}")
        else:
            print(f"   ❌ {var} (not set)")
            all_set = False

    return all_set

def test_database_connection():
    """Test connection to PostgreSQL database"""
    print("\n🔍 Testing database connection...")

    try:
        import psycopg2
        load_dotenv()

        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', 5432),
            database=os.getenv('DATABASE_NAME', 'geopolitical_platform'),
            user=os.getenv('DATABASE_USER', 'postgres'),
            password=os.getenv('DATABASE_PASSWORD', 'postgres')
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"   ✅ Connected to PostgreSQL")
        print(f"   ℹ️  {version[:50]}...")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"   ❌ Database connection failed: {str(e)}")
        print("   Ensure PostgreSQL is running and credentials are correct")
        return False

def test_mart_tables():
    """Check if required mart tables exist"""
    print("\n🔍 Checking dbt mart tables...")

    try:
        import psycopg2
        load_dotenv()

        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', 5432),
            database=os.getenv('DATABASE_NAME', 'geopolitical_platform'),
            user=os.getenv('DATABASE_USER', 'postgres'),
            password=os.getenv('DATABASE_PASSWORD', 'postgres')
        )

        cursor = conn.cursor()

        required_tables = [
            'dbt_marts.emerging_hotspots',
            'dbt_marts.group_expansion',
            'dbt_marts.cross_border_risk',
            'dbt_marts.forecasting_dataset',
            'dbt_marts.group_clustering_features'
        ]

        all_exist = True
        for table in required_tables:
            schema, table_name = table.split('.')
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = %s
                    AND table_name = %s
                );
            """, (schema, table_name))

            exists = cursor.fetchone()[0]
            if exists:
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} ({count:,} rows)")
            else:
                print(f"   ❌ {table} (not found)")
                all_exist = False

        cursor.close()
        conn.close()

        if not all_exist:
            print("\n   Run: cd dbt_project && dbt run --select marts")

        return all_exist

    except Exception as e:
        print(f"   ❌ Error checking tables: {str(e)}")
        return False

def test_dashboard_file():
    """Check if dashboard.py exists"""
    print("\n🔍 Checking dashboard file...")

    if os.path.exists('dashboard.py'):
        size = os.path.getsize('dashboard.py')
        print(f"   ✅ dashboard.py ({size:,} bytes)")
        return True
    else:
        print("   ❌ dashboard.py not found")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🔒 DASHBOARD PREREQUISITES TEST 🔒")
    print("=" * 70)

    results = {
        'Python Version': test_python_version(),
        'Dependencies': test_dependencies(),
        'Environment Config': test_env_file(),
        'Database Connection': test_database_connection(),
        'Mart Tables': test_mart_tables(),
        'Dashboard File': test_dashboard_file()
    }

    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    all_passed = True
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:>10} | {test}")
        if not passed:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("\n🎉 All tests passed! Ready to launch dashboard.")
        print("\nRun: ./run_dashboard.sh")
        print("Or:  streamlit run dashboard.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues above before launching.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
