from dn3.misc.colors import *
from logging import getLogger
import os

logger = getLogger(__name__)

config_path = "%s/.dn3.conf" % os.getenv('HOME')

template_url = ""
gdbport = 0


def config_handler():

    global template_url
    global gdbport

    template_url = input(f"{BOLD}({PURPLE}dn3{END}{BOLD}){END} Template URL (default): ").rstrip("\n")
    gdbport = input(f"{BOLD}({PURPLE}dn3{END}{BOLD}){END} GDBserver Port (1337): ").rstrip("\n")

    if template_url == "y" or template_url == "Y" or not template_url:
        template_url = "https://raw.githubusercontent.com/k1R4/deathnot3/v1.0.0/template.py"

    if gdbport == "y" or gdbport == "Y" or not gdbport:
        gdbport = 1337

    f = open(config_path, "w+")
    f.write("template_url = %s\ngdbport = %s\n" % (template_url,gdbport))
    f.close()


def parse_config():

    global template_url
    global gdbport

    if not os.path.exists(config_path):
        logger.info("Config doesn't exist, creating one!")
        default_config = "template_url = https://raw.githubusercontent.com/k1R4/deathnot3/v1.0.0/template.py\ngdbport = 1337\n"
        try:
            open(config_path,"w+").write(default_config)
        except:
            logger.error("Unable to write config!")

    try:
        f = open(config_path, "r")

        for i in f.readlines():
            if i.startswith("template_url"):
                template_url = (i.split()[2]).rstrip("\n")
            elif i.startswith("gdbport"):
                gdbport = int((i.split()[2]).rstrip("\n"))
    except:
        logger.error("Error parsing config file!")

if not template_url or not gdbport:
    parse_config()