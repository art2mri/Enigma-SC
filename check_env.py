#!/usr/bin/env python3
"""Preflight checks for Enigma-SC runtime environment."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

DOCKER_IMAGE = "art2mri/vertebral_labeling:3.0"
DOCKER_CONTAINER = "vertebral_labeling"
SINGULARITY_SANDBOX = "vertebral_labeling.simg"
MIN_DISK_GB = 40
REQUIRED_FOLDER = "Enigma-SC"
MIN_PYTHON = (3, 11)

GUI_MODULES = (
    ("tkinter", "python3-tk (apt)"),
    ("PIL", "Pillow (pip)"),
    ("tkfilebrowser", "tkfilebrowser (pip)"),
)


@dataclass
class CheckResult:
    name: str
    status: str  # ok, warn, fail, info
    message: str


@dataclass
class EnvReport:
    results: list[CheckResult] = field(default_factory=list)
    docker_ok: bool = False
    singularity_ok: bool = False
    has_fail: bool = False

    def add(self, name: str, status: str, message: str) -> None:
        self.results.append(CheckResult(name, status, message))
        if status == "fail":
            self.has_fail = True

    def runtime_ok(self) -> bool:
        return self.docker_ok or self.singularity_ok


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=False,
    )


def check_working_directory(report: EnvReport, root: Path) -> None:
    if root.name != REQUIRED_FOLDER:
        report.add(
            "working_directory",
            "warn",
            f"Current folder is '{root.name}'; run from a folder named '{REQUIRED_FOLDER}' "
            "(Singularity uses relative paths).",
        )
    else:
        report.add("working_directory", "ok", f"Running from '{REQUIRED_FOLDER}' folder.")


def check_python(report: EnvReport) -> None:
    version = sys.version_info[:3]
    if version[:2] < MIN_PYTHON:
        report.add(
            "python",
            "fail",
            f"Python {version[0]}.{version[1]} found; Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required.",
        )
    else:
        report.add(
            "python",
            "ok",
            f"Python {version[0]}.{version[1]}.{version[2]}",
        )


def check_disk(report: EnvReport, root: Path) -> None:
    free_gb = shutil.disk_usage(root).free / (1024**3)
    if free_gb < MIN_DISK_GB:
        report.add(
            "disk_space",
            "warn",
            f"{free_gb:.1f} GB free; at least {MIN_DISK_GB} GB recommended.",
        )
    else:
        report.add(
            "disk_space",
            "ok",
            f"{free_gb:.1f} GB free (>= {MIN_DISK_GB} GB).",
        )


def check_gui_deps(report: EnvReport) -> None:
    for module_name, install_hint in GUI_MODULES:
        if importlib.util.find_spec(module_name) is None:
            report.add(
                f"gui_{module_name}",
                "warn",
                f"Missing {module_name}. Install: {install_hint}",
            )
        else:
            report.add(f"gui_{module_name}", "ok", f"{module_name} available.")


def check_docker(report: EnvReport) -> None:
    docker_bin = shutil.which("docker")
    if not docker_bin:
        report.add("docker", "info", "Docker CLI not found.")
        return

    version = run_cmd([docker_bin, "--version"])
    if version.returncode != 0:
        report.add("docker", "info", "Docker CLI found but `docker --version` failed.")
        return

    report.add("docker", "ok", version.stdout.strip() or "Docker CLI available.")

    image = run_cmd([docker_bin, "image", "inspect", DOCKER_IMAGE])
    if image.returncode != 0:
        report.add(
            "docker_image",
            "warn",
            f"Image {DOCKER_IMAGE} not found. Run: docker pull {DOCKER_IMAGE}",
        )
        return

    report.add("docker_image", "ok", f"Image {DOCKER_IMAGE} present.")
    report.docker_ok = True

    container = run_cmd(
        [docker_bin, "ps", "-q", "-f", f"name=^{DOCKER_CONTAINER}$"]
    )
    if container.returncode == 0 and container.stdout.strip():
        report.add(
            "docker_container",
            "info",
            f"Container '{DOCKER_CONTAINER}' is running.",
        )
    else:
        report.add(
            "docker_container",
            "info",
            f"Container '{DOCKER_CONTAINER}' is not running (will be created by the pipeline).",
        )


def check_singularity(report: EnvReport, root: Path) -> None:
    singularity_bin = shutil.which("singularity")
    apptainer_bin = shutil.which("apptainer")

    if not singularity_bin and not apptainer_bin:
        report.add("singularity", "info", "Singularity/Apptainer CLI not found.")
        return

    if singularity_bin:
        version = run_cmd([singularity_bin, "--version"])
        if version.returncode == 0:
            report.add("singularity", "ok", version.stdout.strip() or "Singularity available.")
        else:
            report.add("singularity", "info", "Singularity found but version check failed.")

    if apptainer_bin:
        version = run_cmd([apptainer_bin, "--version"])
        if version.returncode == 0:
            report.add("apptainer", "ok", version.stdout.strip() or "Apptainer available.")
        else:
            report.add("apptainer", "info", "Apptainer found but version check failed.")

    sandbox = root / SINGULARITY_SANDBOX
    if sandbox.is_dir():
        report.add("singularity_sandbox", "ok", f"{SINGULARITY_SANDBOX}/ present.")
        report.singularity_ok = True
    else:
        report.add(
            "singularity_sandbox",
            "warn",
            f"{SINGULARITY_SANDBOX}/ not found. Build it from the Enigma-SC folder "
            f"(see Installation Instructions).",
        )


def check_runtime(report: EnvReport) -> None:
    if report.runtime_ok():
        backends = []
        if report.docker_ok:
            backends.append("Docker")
        if report.singularity_ok:
            backends.append("Singularity/Apptainer")
        report.add("runtime", "ok", f"Usable runtime: {', '.join(backends)}.")
    else:
        report.add(
            "runtime",
            "fail",
            "No usable container runtime. Install Docker (with image pull) or "
            "Singularity/Apptainer (with sandbox build).",
        )


def build_report(root: Path, include_gui: bool) -> EnvReport:
    report = EnvReport()
    check_working_directory(report, root)
    check_python(report)
    check_disk(report, root)
    if include_gui:
        check_gui_deps(report)
    check_docker(report)
    check_singularity(report, root)
    check_runtime(report)
    return report


def print_report(report: EnvReport, quiet: bool) -> None:
    for item in report.results:
        if quiet and item.status not in ("warn", "fail"):
            continue
        prefix = {
            "ok": "[OK]",
            "warn": "[WARN]",
            "fail": "[FAIL]",
            "info": "[INFO]",
        }[item.status]
        print(f"{prefix} {item.name}: {item.message}")


def print_json(report: EnvReport) -> None:
    payload = {
        "ok": not report.has_fail and report.runtime_ok(),
        "docker_ok": report.docker_ok,
        "singularity_ok": report.singularity_ok,
        "checks": [
            {"name": r.name, "status": r.status, "message": r.message}
            for r in report.results
        ],
    }
    print(json.dumps(payload, indent=2))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify Enigma-SC runtime environment before running the pipeline.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--gui",
        action="store_true",
        help="Include GUI dependency checks (default).",
    )
    mode.add_argument(
        "--cli",
        action="store_true",
        help="Skip GUI dependency checks.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON report.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print warnings and failures.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    include_gui = not args.cli
    root = Path.cwd()
    report = build_report(root, include_gui=include_gui)

    if args.json:
        print_json(report)
    else:
        print_report(report, quiet=args.quiet)

    if report.has_fail or not report.runtime_ok():
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
