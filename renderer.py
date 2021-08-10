#!/usr/bin/python3
"""
Building cloud-config templates for vSIX Pi
See: https://github.com/wide-vsix/cloud-config-vsixpi
"""
from jinja2 import Environment
from jinja2 import FileSystemLoader
import jinja2
import yaml
import os
import sys
import glob

BASE_PATH = os.path.dirname(__file__)
TEMPLATES_BASE_PATH = os.path.join(BASE_PATH, "templates")
CONFIGS_BASE_PATH = os.path.join(BASE_PATH, "system-boot")
PARAMETERS_PATH = os.path.join(BASE_PATH, "vsixpi.yml")


def boolstr(boolean):
  return ["false", "true"][boolean]


def yaml_validate(data):
  try:
    yaml.safe_load(data)
  except yaml.YAMLError as e:
    return False, e
  return True, None


def main():
  env = Environment(loader=FileSystemLoader(TEMPLATES_BASE_PATH, encoding="utf_8"))
  env.filters["boolstr"] = boolstr

  params = None
  with open(PARAMETERS_PATH) as fd:
    try:
      params = yaml.safe_load(fd)
    except yaml.YAMLError as e:
      print("Failed to parse vsixpi.yml:", e, file=sys.stderr)
      sys.exit(1)
  
  for tpl_path in glob.glob(f"{TEMPLATES_BASE_PATH}/*.j2"):
    tpl_name = os.path.basename(tpl_path)
    tpl = env.get_template(tpl_name)
    cfg_path = os.path.join(CONFIGS_BASE_PATH, ".".join(tpl_name.split(".")[:-1]))
    
    try:
      with open(cfg_path, "w") as fd:
        out = tpl.render(params)
        ok, e = yaml_validate(out)
        if not ok:
          print(f"Failed to validate rendered config {cfg_path}:", e, file=sys.stderr)
          sys.exit(254)
        fd.write(out)
    except FileNotFoundError as e:
      print("Template not found:", e, file=sys.stderr)
      sys.exit(2)
    except jinja2.exceptions.UndefinedError as e:
      print("Broken vsixpi.yml:", e, file=sys.stderr)
      sys.exit(3)


if __name__ == "__main__":
  main()
