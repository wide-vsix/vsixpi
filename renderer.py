#!/usr/bin/env python3
"""
Copyright 2021 vSIX Working Group, WIDE Project
A helper script building cloud-config templates for vSIX Pi
See: https://github.com/wide-vsix/vsixpi
"""

from jinja2 import Environment
from jinja2 import FileSystemLoader
from pprint import pprint
import argparse
import glob
import jinja2
import os
import sys
import yaml

BASE_PATH = os.path.dirname(__file__)
TEMPLATES_BASE_PATH = os.path.join(BASE_PATH, "templates")
CONFIGS_BASE_PATH = os.path.join(BASE_PATH, "cloud-config")
PARAMETERS_PATH = os.path.join(BASE_PATH, "vsixpi.yml")

CODE_MISSING_TEMPLATES = 10
CODE_RENDERING_ISSUE = 11
CODE_PROVISIONING_ISSUE = 12
CODE_UNKNOWN_ISSUE = 255


def parse_yaml(data, on_error=None):
    try:
        parsed = yaml.safe_load(data)
    except yaml.YAMLError as e:
        if on_error:
            print(f"{on_error}:\n{e}", file=sys.stderr)
        return False, e
    else:
        return True, parsed


def provisioning(cloud_config):
    if "write_files" not in cloud_config:
        return

    # Imitate cloud-init and write out files. Permission and owner specifications are ignored.
    configs = cloud_config["write_files"]
    for config in configs:
        path, content = config["path"], config["content"]
        try:
            with open(path, "w") as fd:
                fd.write(content)
        except OSError as e:
            print(f"Failed to provisioning {path}:\n{e}", file=sys.stderr)
            sys.exit(CODE_PROVISIONING_ISSUE)


def rendering(reconf=False):
    env = Environment(loader=FileSystemLoader(TEMPLATES_BASE_PATH))
    env.filters["boolstr"] = lambda b: ["false", "true"][b]

    vsixpi_yml, params = None, None
    with open(PARAMETERS_PATH) as fd:
        vsixpi_yml = fd.read()
        ok, params = parse_yaml(vsixpi_yml, on_error="Failed to parse vsixpi.yml")
        if not ok:
            sys.exit(CODE_RENDERING_ISSUE)
    params["vsixpi_yml"] = vsixpi_yml

    # All rendering targets have to be located under TEMPLATES_BASE_PATH having a .j2 extension.
    for tpl_path in glob.glob(f"{TEMPLATES_BASE_PATH}/*.j2"):
        tpl_name = os.path.basename(tpl_path)  # e.g., example.txt.j2
        tpl = env.get_template(tpl_name)
        tpl_name_bare = ".".join(tpl_name.split(".")[:-1])  # e.g., example.txt
        cfg_path = os.path.join(CONFIGS_BASE_PATH, tpl_name_bare)

        try:
            with open(cfg_path, "w") as fd:
                out = tpl.render(params)
                ok, parsed = parse_yaml(out, on_error=f"Failed to validate rendered config {cfg_path}")
                if not ok:
                    sys.exit(CODE_UNKNOWN_ISSUE)
                if reconf:
                    #pprint(parsed)  # debug
                    provisioning(parsed)
                fd.write(out)

        except FileNotFoundError as e:
            print(f"Failed to find template {tpl_path}:\n{e}", file=sys.stderr)
            sys.exit(CODE_MISSING_TEMPLATES)

        except jinja2.exceptions.UndefinedError as e:
            print(f"Broken templates or vsixpi.yml:\n{e}", file=sys.stderr)
            sys.exit(CODE_RENDERING_ISSUE)


def main():
    parser = argparse.ArgumentParser(description="A helper utility to setup vSIX Pi - see wide-vsix/vsixpi at GitHub for details.")
    parser.add_argument("--reconfigure", action="store_true", help="Reconfigure current vSIX Pi, need to run with sudo (default: false)")
    args = parser.parse_args()
    rendering(reconf=args.reconfigure)


if __name__ == "__main__":
    main()
