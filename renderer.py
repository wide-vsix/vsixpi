#!/usr/bin/python3
from jinja2 import Template
import os

network_config_tpl = os.path.join(os.path.dirname(__file__), "./system-boot/network-config.j2")
user_data_tpl = os.path.join(os.path.dirname(__file__), "./system-boot/user-data.j2")


def main():
  pass


if __name__ == "__main__":
  main()
