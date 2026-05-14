import unittest
from pathlib import Path

import state


class TestStatePaths(unittest.TestCase):
  def test_project_path_is_repo_root(self):
    project_path = Path(state.PROJECT_PATH).resolve()
    expected_project_path = Path(__file__).resolve().parent
    self.assertEqual(project_path, expected_project_path)

  def test_data_path_points_to_config(self):
    data_path = Path(state.DATA_PATH).resolve()
    self.assertEqual(data_path, Path(state.PROJECT_PATH).resolve() / "config.json")
    self.assertEqual(data_path.name, "config.json")


if __name__ == "__main__":
  unittest.main()
