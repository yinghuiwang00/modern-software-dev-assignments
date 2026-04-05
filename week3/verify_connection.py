#!/usr/bin/env python3
"""Verify connection to week2 API."""

import httpx
import asyncio


async def test_connection():
    """Test connection to week2 API."""
    api_url = "http://localhost:8000"

    print(f"Testing connection to {api_url}...")

    try:
        async with httpx.AsyncClient() as client:
            # Test root endpoint
            response = await client.get(f"{api_url}/")
            print(f"Root endpoint status: {response.status_code}")

            # Test notes endpoint
            response = await client.get(f"{api_url}/notes")
            print(f"Notes endpoint status: {response.status_code}")

            # Test action-items endpoint
            response = await client.get(f"{api_url}/action-items")
            print(f"Action items endpoint status: {response.status_code}")

            print("\nConnection successful! Week2 API is accessible.")

    except httpx.ConnectError as e:
        print(f"\nConnection failed: {e}")
        print("Please ensure week2 API is running on localhost:8000")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())