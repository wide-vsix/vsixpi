#!/usr/bin/python3
from re import TEMPLATE
from jinja2 import Environment
from jinja2 import FileSystemLoader
import yaml
import os
import glob

BASE_PATH = os.path.dirname(__file__)
TEMPLATES_BASE_PATH = os.path.join(BASE_PATH, "templates")
CONFIGS_BASE_PATH = os.path.join(BASE_PATH, "system-boot")
PARAMETERS_PATH = os.path.join(BASE_PATH, "params.yml")


def boolstr(boolean):
  return ["false", "true"][boolean]


def main():
  env = Environment(loader=FileSystemLoader(TEMPLATES_BASE_PATH, encoding="utf_8"))
  env.filters["boolstr"] = boolstr

  params = None
  with open(PARAMETERS_PATH) as fd:
    params = yaml.safe_load(fd)
  
  for tpl_path in glob.glob(f"{TEMPLATES_BASE_PATH}/*.j2"):
    tpl_name = os.path.basename(tpl_path)
    tpl = env.get_template(tpl_name)
    cfg_path = os.path.join(CONFIGS_BASE_PATH, tpl_name.split(".")[0])
    with open(cfg_path, "w") as fd:
      out = tpl.render(params)
      fd.write(out)


if __name__ == "__main__":
  main()
