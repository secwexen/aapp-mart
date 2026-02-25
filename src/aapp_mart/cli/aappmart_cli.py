import argparse
import logging
from aapp_mart.core.graph_service import GraphService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        prog="aapp-mart",
        description="AAPP-MART CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser("build", help="Build and export attack graph")
    build_parser.add_argument("--input", required=True, help="Input file path")
    build_parser.add_argument("--export", required=True, help="Export file path")

    args = parser.parse_args()

    if args.command == "build":
        try:
            service = GraphService()
            service.build_graph(args.input, args.export)
        except FileNotFoundError:
            logger.error(f"Input file not found: {args.input}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
