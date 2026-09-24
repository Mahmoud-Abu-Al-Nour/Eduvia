"""
Eduvia — Development Test Data Reset Script

Convenience script to clear existing test data and re-seed all 20 test students
and cohorts deterministically.
"""
import asyncio
import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.clear_test_data import clear_test_data
from scripts.seed_test_data import seed_test_data


async def reset_test_data() -> None:
    print("Executing Eduvia Test Data Reset (Clear -> Seed)...")
    await clear_test_data()
    await seed_test_data()
    print("Eduvia Test Data Reset Complete.")


if __name__ == "__main__":
    asyncio.run(reset_test_data())
