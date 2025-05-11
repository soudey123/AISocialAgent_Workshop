from pyairtable import Base
import os
from datetime import datetime
import logging
import unicodedata
import html

logger = logging.getLogger("airtable_logger")
logger.setLevel(logging.INFO)


def log_to_airtable(prompt, platform, content):
    try:
        token = os.getenv("AIRTABLE_PAT")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_TABLE_NAME")

        if not all([token, base_id, table_name]):
            raise ValueError("Airtable token, base ID, or table name not set.")

        # Convert CrewOutput to string if needed
        if not isinstance(content, str):
            content = str(content.result) if hasattr(
                content, "result") else str(content)

        # Decode HTML and Unicode escape sequences
        content = html.unescape(content)
        content = content.encode('latin1',
                                 errors='ignore').decode('utf-8',
                                                         errors='ignore')
        content = ''.join(c for c in content
                          if 32 <= ord(c) <= 126 or c in '\n\r\t')

        # Safe truncation before Airtable API breaks
        if len(content) > 7500:
            content = content[:7490] + "... [truncated]"

        base = Base(token, base_id)
        base.table(table_name).create({
            "Prompt": prompt,
            "Platform": platform,
            "Generated Content": content
        })

        logger.info(f"Airtable log successful for {platform}")
        return True

    except Exception as e:
        logger.error(f"Error logging to Airtable: {e}")
        return False
