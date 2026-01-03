import argparse
from pathlib import Path
from rich import print

from app.log_parser import summarize_failure


def main():
    parser = argparse.ArgumentParser(description="AI Copilot for CI/CD Failures (Phase 0)")
    parser.add_argument("--log", required=True, help="Path to CI log file")
    args = parser.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        raise SystemExit(f"Log file not found: {log_path}")

    summary = summarize_failure(log_path.read_text(encoding="utf-8", errors="ignore"))

    print("\n[bold cyan]=== Failure Summary ===[/bold cyan]")
    print(f"[bold]Probable root cause:[/bold] {summary.probable_root_cause or 'Unknown (we will improve this)'}\n")

    if not summary.error_lines:
        print("[yellow]No error-like lines detected. Try a different log sample.[/yellow]")
        return

    print("[bold]Key error lines:[/bold]")
    for line in summary.error_lines:
        print(f" - {line}")


if __name__ == "__main__":
    main()
