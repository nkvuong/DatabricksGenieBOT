import logging

from unittest.mock import create_autospec

from databricks.sdk import WorkspaceClient


logging.getLogger("tests").setLevel("DEBUG")
logger = logging.getLogger(__name__)


def mock_workspace_client():
    """
    Mock function to create a workspace client for testing purposes.
    """
    ws = create_autospec(WorkspaceClient)
    return ws
