import os
import unittest
from pathlib import Path

import state


class TestStatePaths(unittest.TestCase):
  def test_project_path_is_repo_root(self):
    expected_path = f"{Path(__file__).resolve().parent}{os.sep}"
    self.assertEqual(state.PROJECT_PATH, expected_path)

  def test_data_path_points_to_config(self):
    expected_data_path = Path(__file__).resolve().parent / "config.json"
    self.assertEqual(Path(state.DATA_PATH), expected_data_path)


if __name__ == "__main__":
  unittest.main()
