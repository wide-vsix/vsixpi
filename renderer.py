#!/usr/bin/python3
"""
Building cloud-config templates for vSIX Pi
See: https://github.com/wide-vsix/cloud-init-vsixpi
"""
from jinja2 import Environment
from jinja2 import FileSystemLoader
from pprint import pprint
import jinja2
import yaml
import os
import sys
import glob
import argparse

BASE_PATH = os.path.dirname(__file__)
TEMPLATES_BASE_PATH = os.path.join(BASE_PATH, "templates")
CONFIGS_BASE_PATH = os.path.join(BASE_PATH, "system-boot")
PARAMETERS_PATH = os.path.join(BASE_PATH, "vsixpi.yml")


def boolstr(boolean):
  return ["false", "true"][boolean]


def validate_yaml(data, on_error=None):
  try:
    d = yaml.safe_load(data)
  except yaml.YAMLError as e:
    if on_error:
      print(f"{on_error}:\n{e}", file=sys.stderr)
    return False, e
  else:
    return True, d


def provisioning(cloud_config):
  if "write_files" not in cloud_config:
    return

  configs = cloud_config["write_files"]
  for config in configs:
    path, content = config["path"], config["content"]
    with open(path, "w") as fd:
      fd.write(content)


def render(reconf=False):
  env = Environment(loader=FileSystemLoader(TEMPLATES_BASE_PATH))
  env.filters["boolstr"] = boolstr

  params = None
  with open(PARAMETERS_PATH) as fd:
    ok, params = validate_yaml(fd, on_error="Failed to parse vsixpi.yml")
    if not ok:
      sys.exit(1)

  for tpl_path in glob.glob(f"{TEMPLATES_BASE_PATH}/*.j2"):
    tpl_name = os.path.basename(tpl_path)
    tpl = env.get_template(tpl_name)
    tpl_name_bare = ".".join(tpl_name.split(".")[:-1])
    cfg_path = os.path.join(CONFIGS_BASE_PATH, tpl_name_bare)

    try:
      with open(cfg_path, "w") as fd:
        out = tpl.render(params)
        ok, parsed = validate_yaml(out, on_error=f"Failed to validate rendered config {cfg_path}")
        if not ok:
          sys.exit(254)
        if reconf:
          #pprint(parsed)
          provisioning(parsed)
        fd.write(out)

    except FileNotFoundError as e:
      print(f"Template not found:\n{e}", file=sys.stderr)
      sys.exit(2)

    except jinja2.exceptions.UndefinedError as e:
      print(f"Broken vsixpi.yml:\n{e}", file=sys.stderr)
      sys.exit(3)


def main():
  parser = argparse.ArgumentParser(description="A helper utility to setup vSIX Pi - see wide-vsix/vsixpi at GitHub for details.")
  parser.add_argument("--reconfigure", action="store_true", help="Reconfigure running vSIX Pi, need to run with sudo (default: False)")
  args = parser.parse_args()
  render(reconf=args.reconfigure)


if __name__ == "__main__":
  main()
