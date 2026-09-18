import argparse
import json
import logging
import sys

from config import load_config
from diagnostics import analyze_transaction
from db_client import check_database_health, get_transaction_data
from health import check_api_health


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


def build_parser():
    parser = argparse.ArgumentParser(
        description="MiniPay transaction support diagnostic tool"
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--transaction",
        help="Transaction reference, for example TXN00000001",
    )

    mode.add_argument(
        "--health",
        action="store_true",
        help="Check database and API health",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Return machine-readable JSON output",
    )

    return parser

def print_transaction(result):
    print("=" * 60)

    print(f"Transaction ID:       {result['transaction_id']}")
    print(f"Transaction Ref:      {result['transaction_ref']}")
    print(f"Customer ID:          {result['customer_id']}")
    print(f"Customer Ref:         {result['customer_ref']}")
    print(f"Customer Name:        {result['customer_name']}")
    print(f"Amount:               {result['amount']}")
    print(f"Status:               {result['status']}")
    print(f"Created At:           {result['created_at']}")
    print(f"Completed At:         {result['completed_at']}")
    print(f"Failure Code:         {result['failure_code']}")

    print(f"Callback Attempts:    {result['callback_attempts']}")
    print(f"Successful Callbacks: {result['successful_callbacks']}")
    print(f"Failed Callbacks:     {result['failed_callbacks']}")
    print(f"Last Callback:        {result['last_callback_at']}")

    print("\nCallback / Retry Details:")

    if result["callback_details"]:
        for callback in result["callback_details"]:
            print(
                f"- Attempt {callback['attempt_no']}: "
                f"HTTP {callback['http_status']} | "
                f"{callback['callback_status']} | "
                f"{callback['attempted_at']}"
            )
    else:
        print("- No callback attempts recorded")

    print("\nAnomalies:")

    if result["anomalies"]:
        for anomaly in result["anomalies"]:
            print(f"- {anomaly}")
    else:
        print("- None detected")

    print("\nRecommended Next Action:")
    print(result["recommended_next_action"])


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config()
        if args.health:
            logger.info("Running API and database health checks")

            database_healthy = False

            try:
                database_healthy = check_database_health(
                    config.database_url,
                    config.db_timeout,
                )
            except Exception as exc:
                database_error = str(exc)
            else:
                database_error = None

            api_result = check_api_health(
                config.api_url,
                config.api_timeout,
            )

            result = {
                "database": {
                    "status": "healthy" if database_healthy else "unhealthy",
                    "error": database_error,
                },
                "api": api_result,
            }

            healthy = (
                database_healthy
                and api_result["status"] == "healthy"
            )

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print("Database:")
                print(f"  Status: {result['database']['status']}")

                if database_error:
                    print(f"  Error: {database_error}")

                print("\nAPI:")
                print(f"  Status: {api_result['status']}")

                if api_result.get("http_status"):
                    print(f"  HTTP Status: {api_result['http_status']}")

                if api_result.get("error"):
                    print(f"  Error: {api_result['error']}")

            return 0 if healthy else 1

        logger.info(
            "Investigating transaction reference %s",
            args.transaction,
        )

        records = get_transaction_data(
            config.database_url,
            args.transaction,
            config.db_timeout,
        )

        if not records:
            message = (
                f"No transaction found for reference: "
                f"{args.transaction}"
            )

            if args.json:
                print(json.dumps({"error": message}))
            else:
                print(message)

            return 2

        duplicate_count = len(records)

        results = [
            analyze_transaction(
                record,
                duplicate_count=duplicate_count,
            )
            for record in records
        ]

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for result in results:
                print_transaction(result)

        return 0

    except Exception as exc:
        logger.exception("Support tool failed")

        if args.json:
            print(json.dumps({"error": str(exc)}))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)

        return 1


if __name__ == "__main__":
    sys.exit(main())