import argparse
import csv
import json
import pandas as pd
from jupiterone import JupiterOneClient
import sys


def execute_query(account_id, token, api_url, query, output_format, include_deleted):
    # Initialize the JupiterOne client
    client = JupiterOneClient(account=account_id, token=token, url=api_url)

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    # Execute the query
    response = client.query_v1(query, include_deleted=include_deleted)

    # Step 2: Process each item in the JSON response incrementally
    if "data" in response:
        for item in response["data"]:
            # Merge 'entity' and 'properties' and ignore 'id' if a plain return
            if "entity" in item and "properties" in item:
                merged_item = {**item["entity"], **item["properties"]}
            # If we have aliased items being returned
            elif first_item_contains_id_key(item):
                merged_item = flatten_with_prefix(item)
            # Specific fields selected
            else:
                merged_item = item

            # Create a DataFrame from the merged item
            temp_df = pd.DataFrame([merged_item])

            # Concatenate the new DataFrame with the existing one
            df = pd.concat([df, temp_df], ignore_index=True)

    else:
        sys.stderr.write("TREE queries are not currently supported by this CLI\n")
        sys.exit(1)

    # Output the results
    if output_format.lower() == "json":
        df.to_json(sys.stdout, orient="records", lines=True)
    else:  # Default to CSV
        df.to_csv(sys.stdout, index=False)


def first_item_contains_id_key(d):
    for value in d.values():
        if isinstance(value, dict) and "id" in value:
            return True
        break  # Only check the first item
    return False


def flatten_dict(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_with_prefix(d):
    flattened_dict = {}
    for key in d:
        # Only process 'entity' and 'properties' parts
        for sub_key in ["entity", "properties", "relationship"]:
            if sub_key in d[key]:
                # Flatten without including 'entity' or 'properties' in the key
                flattened_sub_dict = flatten_dict(d[key][sub_key], parent_key=key)
                flattened_dict.update(flattened_sub_dict)
    return flattened_dict


def main():
    parser = argparse.ArgumentParser(description="JupiterOne CLI Client")

    # Required arguments
    parser.add_argument("query", type=str, help="JupiterOne query to execute")

    # Optional arguments
    parser.add_argument(
        "--account-id", required=True, type=str, help="Customer's Account ID"
    )
    parser.add_argument("--token", required=True, type=str, help="API token")
    parser.add_argument(
        "--api-url",
        default="https://graphql.us.jupiterone.io",
        type=str,
        help="JupiterOne API URL (Default: https://graphql.us.jupiterone.io)",
    )
    parser.add_argument(
        "--output",
        default="csv",
        choices=["csv", "json"],
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--include-deleted",
        action="store_true",
        help="Include deleted entities in the query results",
    )

    args = parser.parse_args()

    # Execute the query with the provided arguments
    execute_query(
        account_id=args.account_id,
        token=args.token,
        api_url=args.api_url,
        query=args.query,
        output_format=args.output,
        include_deleted=args.include_deleted,
    )


if __name__ == "__main__":
    main()
