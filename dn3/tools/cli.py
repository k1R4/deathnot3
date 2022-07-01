from dn3.tools.tools import *
from logging import getLogger
import argparse

logger = getLogger(__name__)


class CLIHandler():

	def argparse_handler(self):
		parser = argparse.ArgumentParser(description='DeathNot3 CLI',formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument("mode", help="""template/linker
		template  ---> Automatic template generation
		linker    ---> Patch challenge binary with linker
		\n""")
		parser.add_argument("binary", help="Path to challenge binary")
		parser.add_argument("-l","--libc", help="Path to libc binary",metavar="")
		parser.add_argument("-r","--remote", help="<remote_ip>:<port>",metavar="")
		parser.add_argument("-V","--verbose", action="store_true", help="Detailed logging")
		return parser.parse_args()


	def __init__(self):

		args = self.argparse_handler()
		
		if args.mode == "template":
			gen_template(args.binary,args.libc,args.remote)

		elif args.mode == "linker":
			linkpatcher(args.binary,args.libc)

