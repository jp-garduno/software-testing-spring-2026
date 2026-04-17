# -*- coding: utf-8 -*-

"""
Mock up testing examples.
"""
import unittest
from unittest.mock import patch, mock_open, MagicMock

from white_box.mockup_exercises import (
    fetch_data_from_api,
    perform_action_based_on_time,
    read_data_from_file,
    execute_command,
)


class TestFetchDataFromApi(unittest.TestCase):
    """
    Fetch data from API unittest class.
    """

    @patch("white_box.mockup_exercises.requests.get")
    def test_fetch_data_from_api_success(self, mock_get):
        """
        Success case.
        """
        # Set up the mock response
        mock_get.return_value.json.return_value = {"key": "value"}

        # Call the function under test
        result = fetch_data_from_api("https://api.example.com/data")

        # Assert that the function returns the expected result
        self.assertEqual(result, {"key": "value"})

        # Assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://api.example.com/data", timeout=10)

    @patch("white_box.mockup_exercises.requests.get")
    def test_fetch_data_from_api_returns_list(self, mock_get):
        """
        Success case returning a list.
        """
        mock_get.return_value.json.return_value = [1, 2, 3]

        result = fetch_data_from_api("https://api.example.com/list")

        self.assertEqual(result, [1, 2, 3])
        mock_get.assert_called_once_with("https://api.example.com/list", timeout=10)


class TestReadDataFromFile(unittest.TestCase):
    """
    Read data from file unittest class.
    """

    @patch("builtins.open", new_callable=mock_open, read_data="hello world")
    def test_read_data_from_file_success(self, mock_file):
        """
        Success case: file exists and returns content.
        """
        result = read_data_from_file("fake_file.txt")

        self.assertEqual(result, "hello world")
        mock_file.assert_called_once_with("fake_file.txt", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_data_from_file_not_found(self, mock_file):
        """
        Error case: file does not exist, raises FileNotFoundError.
        """
        with self.assertRaises(FileNotFoundError):
            read_data_from_file("nonexistent_file.txt")


class TestExecuteCommand(unittest.TestCase):
    """
    Execute command unittest class.
    """

    @patch("white_box.mockup_exercises.subprocess.run")
    def test_execute_command_success(self, mock_run):
        """
        Success case: command runs and returns stdout.
        """
        mock_result = MagicMock()
        mock_result.stdout = "command output"
        mock_run.return_value = mock_result

        result = execute_command(["echo", "hello"])

        self.assertEqual(result, "command output")
        mock_run.assert_called_once_with(
            ["echo", "hello"], capture_output=True, check=False, text=True
        )

    @patch("white_box.mockup_exercises.subprocess.run")
    def test_execute_command_empty_output(self, mock_run):
        """
        Case: command runs but returns empty stdout.
        """
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        result = execute_command(["ls", "/empty"])

        self.assertEqual(result, "")


class TestPerformActionBasedOnTime(unittest.TestCase):
    """
    Perform Action Based On Time unittest class.
    """

    @patch("white_box.mockup_exercises.time.time")
    def test_perform_action_based_on_time_action_a(self, mock_time):
        """
        Action A: time < 10.
        """
        mock_time.return_value = 5

        result = perform_action_based_on_time()

        self.assertEqual(result, "Action A")

    @patch("white_box.mockup_exercises.time.time")
    def test_perform_action_based_on_time_action_b(self, mock_time):
        """
        Action B: time >= 10.
        """
        mock_time.return_value = 15

        result = perform_action_based_on_time()

        self.assertEqual(result, "Action B")

    @patch("white_box.mockup_exercises.time.time")
    def test_perform_action_based_on_time_boundary(self, mock_time):
        """
        Boundary case: time == 10 should return Action B.
        """
        mock_time.return_value = 10

        result = perform_action_based_on_time()

        self.assertEqual(result, "Action B")