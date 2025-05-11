import os
from pyairtable import Base
from dotenv import load_dotenv

# ✅ Step 1: Load environment variables from .env
load_dotenv()

# ✅ Step 2: Read variables
token = os.getenv("AIRTABLE_PAT")
base_id = os.getenv("AIRTABLE_BASE_ID")
table_name = os.getenv("AIRTABLE_TABLE_NAME")

# ✅ Step 3: Debug print
print("AIRTABLE_PAT:", token[:8] + "..." if token else "None")
print("AIRTABLE_BASE_ID:", base_id)
print("AIRTABLE_TABLE_NAME:", table_name)


# ✅ Step 4: Try connection
def test_airtable_connection():
    try:
        base = Base(token, base_id)
        records = base.table(table_name).all(max_records=1)
        print(
            f"✅ Airtable connection successful. Found {len(records)} record(s) in '{table_name}'."
        )
    except Exception as e:
        print(f"❌ Airtable connection failed: {e}")


if __name__ == "__main__":
    test_airtable_connection()
