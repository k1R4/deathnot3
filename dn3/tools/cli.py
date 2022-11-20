from dn3.tools.linkerpatcher import *
from dn3.tools.templategen import *
from dn3.config import *
from logging import getLogger
from sys import argv
import argparse

logger = getLogger(__name__)


class CLIHandler():

	def argparse_handler(self):
		parser = argparse.ArgumentParser(description='DeathNot3 CLI',formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument("mode", help="""template/linker/interactive
		template                ---> Automatic template generation
		linker                  ---> Patch challenge binary with linker
		interactive (or) i      ---> Open python interactive shell with dn3 imported
		\n""")
		parser.add_argument("binary", help="Path to challenge binary")
		parser.add_argument("-l","--libc", help="Path to libc binary",metavar="")
		parser.add_argument("-r","--remote", help="<remote_ip>:<port>",metavar="")
		parser.add_argument("-V","--verbose", action="store_true", help="Detailed logging")
		return parser.parse_args()


	def __init__(self):

		if argv and len(argv) > 1:
			if argv[1] == "config":
				return config.write(argv)
			
		args = self.argparse_handler()
		
		if args.mode == "template":
			TemplateGenerator(args.binary,args.libc,args.remote)

		elif args.mode == "linker":
			LinkerPatcher(args.binary,args.libc)