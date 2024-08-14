import unittest
import subprocess
import json
import os
import csv


class TestJupiterOneCLI(unittest.TestCase):
    def setUp(self):
        self.account_id = "ACCOUNT ID HERE"
        self.token = "API TOKEN HERE"
        self.api_url = "https://api.us.jupiterone.io"
        self.output_file = "output.csv"

    def parse_ndjson(self, ndjson_str):
        return [json.loads(line) for line in ndjson_str.strip().splitlines()]

    def run_query(self, query, output_format="json"):
        result = subprocess.run(
            [
                "python3",
                "-m",
                "jupiterone_cli.cli",
                query,
                "--account-id",
                self.account_id,
                "--token",
                self.token,
                "--output",
                output_format,
            ],
            capture_output=True,
            text=True,
        )
        return result

    # Test cases based on the provided queries

    def test_query_s_t_ids_json(self):
        query = "FIND * AS s THAT RELATES TO * AS t RETURN s._id, t._id LIMIT 10"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 10)
        for item in data:
            self.assertIn("s._id", item)
            self.assertIn("t._id", item)

    def test_query_tree_json(self):
        query = "FIND * AS s THAT RELATES TO * AS t RETURN TREE LIMIT 10"
        result = self.run_query(query, "json")

        # Check that the CLI exits with code 1, indicating an error
        self.assertEqual(result.returncode, 1)

        # Depending on your CLI implementation, you might want to check if any specific error message was returned
        # For example, checking that the error output contains certain text:
        self.assertIn(
            "TREE queries are not currently supported by this CLI", result.stderr
        )

    def test_query_s_t_json(self):
        query = "FIND * AS s THAT RELATES TO * AS t LIMIT 10"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 10)

    def test_query_s_t_full_json(self):
        query = "FIND * AS s THAT RELATES TO * AS t RETURN s, t LIMIT 10"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 10)
        for item in data:
            self.assertIn("s._deleted", item)
            self.assertIn("t._deleted", item)

    def test_query_s_t_limit_1_json(self):
        query = "FIND * AS s THAT RELATES TO * AS t RETURN s, t LIMIT 1"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 1)
        self.assertIn("s.displayName", data[0])
        self.assertIn("t.displayName", data[0])

    def test_query_s_t_limit_1_csv(self):
        query = "FIND * AS s THAT RELATES TO * AS t RETURN s, t LIMIT 1"
        with open(self.output_file, "w") as f:
            result = subprocess.run(
                [
                    "python3",
                    "-m",
                    "jupiterone_cli.cli",
                    query,
                    "--account-id",
                    self.account_id,
                    "--token",
                    self.token,
                    "--output",
                    "csv",
                ],
                stdout=f,
                text=True,
            )
        self.assertEqual(result.returncode, 0)
        with open(self.output_file) as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertIn("s.displayName", rows[0])
            self.assertIn("t.displayName", rows[0])
        os.remove(self.output_file)

    def test_query_s_t_limit_1_json_no_return(self):
        query = "FIND * AS s THAT RELATES TO * AS t LIMIT 1"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 1)

    def test_query_s_r_t_limit_1_json(self):
        query = "FIND * AS s THAT RELATES TO AS r * AS t RETURN s, r, t LIMIT 1"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 1)
        self.assertIn("s._id", data[0])
        self.assertIn("r._id", data[0])
        self.assertIn("t._id", data[0])

    def test_query_s_r_t_displayName_limit_1_json(self):
        query = "FIND * AS s THAT RELATES TO AS r * AS t RETURN s.displayName, t.displayName LIMIT 1"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        self.assertEqual(len(data), 1)
        self.assertIn("s.displayName", data[0])
        self.assertIn("t.displayName", data[0])

    # Additional variations of the last query if needed
    def test_query_s_r_t_displayName_with_typo_json(self):
        query = "FIND * AS s THAT RELATES TO AS r * AS t RETURN s.displayName, t.displayNamet LIMIT 1"
        result = self.run_query(query, "json")
        self.assertEqual(result.returncode, 0)
        data = self.parse_ndjson(result.stdout)
        # This might return an error or a different structure; adjust based on expected behavior
        # For example, check if the correct fields were included or a proper error message is returned


if __name__ == "__main__":
    unittest.main()
