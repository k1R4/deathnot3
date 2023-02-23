from dn3.tools.config import cfg
from dn3.misc import dn3_prompt
from logging import getLogger
import requests

logger = getLogger(__name__)


class TemplateGenerator():

	def __init__(self, binary, libc=None, remote=None):
		self.binary = binary
		self.libc = libc
		self.remote = remote
		self.url = cfg.template
		self.path = dn3_prompt("Name of file (exp.py): ")
		self.template = ""

		if self.path in ["y", "Y", ""]:
			self.path = "exp.py"

		self.get_template()
		self.parse_template()
		self.write_template()


	def get_template(self):
		if self.url.startswith("file://"):
			self.url = self.url[7:]
			try:
				f = open(self.url, "r")
				self.template = f.read()
				f.close()
				return
			except:
				logger.error("Error retrieving local template")

		else:
			r = requests.get(self.url)
			if r.status_code not in range(200,300):
				logger.error("Error retrieving template!")
			self.template = r.text
			return


	def parse_template(self):
		self.template = self.template.replace("BINARY", self.binary)
		
		if not self.libc:
			while True:
				idx = (self.template.find("l{"),self.template.find("}l"))
				if idx[0] < 0 or idx[1] < 0:
					break
				if idx[0] > idx[1]:
					logger.error("Invalid libc tags in template!")
				self.template = self.template[:idx[0]] + self.template[idx[1]+2:]
		else:
			self.template = self.template.replace("l{", "")
			self.template = self.template.replace("}l", "")
			self.template = self.template.replace("LIBC", self.libc)

		if not self.remote:
			while True:
				idx = (self.template.find("r{"),self.template.find("}r"))
				if idx[0] < 0 or idx[1] < 0:
					break
				if idx[0] > idx[1]:
					logger.error("Invalid remote tags in template!")
				self.template = self.template[:idx[0]] + self.template[idx[1]+2:]
		else:
			self.template = self.template.replace("r{", "")
			self.template = self.template.replace("}r", "")
			try:
				host, port = self.remote.split(":")
				self.template = self.template.replace("HOST", host)
				self.template = self.template.replace("PORT", port)
			except:
				logger.error("Invalid remote argument!")
				

	def write_template(self):
		f = open(self.path, "w+")
		f.write(self.template.rstrip("\n")+"\n")
		f.close()
		logger.info("Template generated!")
