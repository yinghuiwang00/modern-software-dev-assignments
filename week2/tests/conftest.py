"""Configuration for pytest to set up the test environment."""

import os
import pytest

# Set environment variables for testing to avoid errors during import
os.environ['ZHIPU_API_KEY'] = 'test_api_key_for_unit_tests_only'
os.environ['LOG_LEVEL'] = 'WARNING'  # Reduce logging noise during tests
