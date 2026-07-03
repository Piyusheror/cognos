import os
import asyncio
import argparse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import cognee

async def ingest_folder(folder_path: str):
    if not os.path.exists(folder_path):
        print(f"ERROR: Folder not found: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    if not files:
        print(f"No .txt files found in {folder_path}")
        return

    print(f"Found {len(files)} files. Starting ingestion...\n")

    success = 0
    failed = 0

    for filename in files:
        filepath = os.path.join(folder_path, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                print(f"  SKIP  {filename} - file is empty")
                continue

            tagged_content = f"[SOURCE: {filename}]\n[DATE_INGESTED: {datetime.now().strftime('%Y-%m-%d')}]\n\n{content}"

            print(f"  Ingesting: {filename} ({len(content)} chars)...")
            await cognee.remember(tagged_content, dataset_name="cognos")

            print(f"  Done: {filename}")
            success += 1

        except Exception as e:
            print(f"  Failed: {filename} - {e}")
            failed += 1

    print(f"\nIngestion complete.")
    print(f"  Success: {success} files")
    print(f"  Failed:  {failed} files")
    print(f"\nYou can now start the server and ask questions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CognOS data ingestion")
    parser.add_argument(
        "--folder",
        type=str,
        default="data",
        help="Path to folder containing .txt files (default: ./data)"
    )
    args = parser.parse_args()
    asyncio.run(ingest_folder(args.folder))