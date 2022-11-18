from dn3.misc.colors import *
from dn3.misc.encoding import bytes2str
from dn3.misc.utils import find_arch
from dn3.misc.utils import *
from dn3.config import config
from logging import getLogger
from os import getcwd,urandom
from binascii import hexlify
import requests
import wget
import unix_ar
import tarfile


logger = getLogger(__name__)


class TemplateGenerator():

	def __init__(self, binary, libc=None, remote=None):
		self.binary = binary
		self.libc = libc
		self.remote = remote
		self.url = config.template
		self.path = dn3_prompt("Name of file (exp.py): ")
		self.template = ""

		if self.path in ["y", "Y", ""]:
			self.path = "exp.py"

		self.get_template()
		self.parse_template()
		self.write_template()


	def get_template(self):
		if self.url.startswith("file://"):
			self.url = self.template[7:]
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
		self.template.replace("BINARY", self.binary)
		
		if not self.libc:
			while True:
				idx = (self.template.find("l{"),self.template.find("}l"))
				if idx[0] < 0 or idx[1] < 0:
					break
				if idx[0] > idx[1]:
					logger.error("Invalid libc tags in template!")
				self.template = self.template[:idx[0]] + self.template[idx[1]+2:]
		else:
			self.template.replace("l{", "")
			self.template.replace("}l", "")
			self.template.replace("LIBC", self.libc)

		if not self.remote:
			while True:
				idx = (self.template.find("r{"),self.template.find("}r"))
				if idx[0] < 0 or idx[1] < 0:
					break
				if idx[0] > idx[1]:
					logger.error("Invalid remote tags in template!")
				self.template = self.template[:idx[0]] + self.template[idx[1]+2:]
		else:
			self.template.replace("r{", "")
			self.template.replace("}r", "")
			try:
				host, port = self.remote.split(":")
				self.template.replace("HOST", host)
				self.template.replace("PORT", port)
			except:
				logger.error("Invalid remote argument!")
				

	def write_template(self):
		f = open(self.path, "w+")
		f.write(self.template.rstrip("\n")+"\n")
		f.close()
		logger.info("Template generated!")


class LinkerPatcher():

	def __init__(self,binary,libc):

		try:
			self.binary = binary
			self.libc = libc
			self.dbg_libc = None
			self.ld = None
			self.arch = None
			self.type = None
			self.cwd = f"/tmp/dn3-{bytes2str(hexlify(urandom(4)))}/"
			sh(f"mkdir {self.cwd}")
			self.compatibility()
			self.version = self.get_libc_version()
			self.get_linker()
			self.unstrip()
			self.patch_binary()
			sh(f"rm -r {self.cwd}")
		except Exception as e:
			if sh(f"ls {self.cwd}"):
				sh(f"rm -r {self.cwd}")
			logger.error(e)


	def compatibility(self):

		if not check_ELF(self.libc):
			logger.error("Libc provided isn't an ELF")

		self.arch = find_arch(self.libc)
		if not self.arch:
			logger.error("Unsupported architecture!")

		if not sh('strings -h'):
			logger.error("strings not found in path!")

		if not sh('patchelf --version'):
			logger.error("patchelf not found in path!")

		if not sh('eu-unstrip --help'):
			logger.error("eu-unstrip not found in path!")


	def get_libc_version(self):

		libc_strs = open(self.libc, "r", encoding="latin-1").read()

		if libc_strs:
			if "GNU C Library" not in libc_strs:
				logger.error("Invaild libc ELF provided!")

			else:
				l = libc_strs.split("GNU C Library")[1].split("\n")[0]
				try:
					if "debian" in l or "ubuntu" in l:
						if "debian" in l:
							self.type = "debian"
						else:
							self.type = "ubuntu"
						version = l.split("GLIBC ")[1].split(")")[0]
						logger.info(f"Libc version: {version}_{self.arch}")
						return version
					else:
						self.type = "vanilla"
						self.arch = "x86_64"
						version = l.split()[-1][:-1]
						logger.info(f"Libc version: {version}-{self.arch}")
						return version
				except:
					logger.error("Libc not supported!")


	def download(self,url):
		try:
			file = wget.download(url, out=self.cwd)
			print()
			logger.info(f"Dowloaded pkg: {url.split('/')[-1]}")
			return file
		except:
			logger.error("Failed to download pkg")


	def get_file(self,file,target):

		if self.type == "ubuntu" or self.type == "debian":
			pkg_f = unix_ar.open(file)
			tars = pkg_f.infolist()
			tarball = None

			for file in tars:
				if b"data.tar.gz" == file.name:
					tarball = pkg_f.open("data.tar.gz")
					break

				if b"data.tar.xz" == file.name:
					tarball = pkg_f.open("data.tar.xz")
					break

				if b"data.tar.zst" == file.name:
					zstd = pkg_f.open("data.tar.zst")
					tarball = extract_zst(zstd,self.cwd,"work.tar")
					break

		else:
			pkg_f = open(file,"rb")
			if file.endswith(".tar.zst"):
				tarball = extract_zst(pkg_f,self.cwd,"work.tar")

		if tarball is None:
			logger.error("Coludn't extract pkg")

		untar = tarfile.open(fileobj=tarball)
		filepath = None
		for member in untar.getmembers():
			if f"{target}-" in member.name:
				filepath = member.name
				untar.extract(member, self.cwd)
				break

		if filepath is None:
			logger.error("Couldn't extract required file")

		dest = filepath.split("/")[-1]
		copy(self.cwd+filepath,getcwd())
		tarball.close()
		pkg_f.close()
		return dest


	def get_linker(self):

		if self.type == "ubuntu":
			vanilla_pkg = f"https://launchpad.net/ubuntu/+archive/primary/+files/libc6_{self.version}_{self.arch}.deb"
		elif self.type == "debian":
			vanilla_pkg = f"http://ftp.us.debian.org/debian/pool/main/g/glibc/libc6_{self.version}_{self.arch}.deb"
		else:
			if self.version > "2.30":
				suffix = "zst"
			else:
				suffix = "xz"
			for i in range(6,0,-1):
				vanilla_pkg = f"https://archive.archlinux.org/packages/g/glibc/glibc-{self.version}-{i}-{self.arch}.pkg.tar.{suffix}"
				r = requests.head(vanilla_pkg)
				if r.status_code == 200:
					break
				else:
					vanilla_pkg = ""

			if vanilla_pkg == "":
				logger.error("Unable to find requested linker")

		file = self.download(vanilla_pkg)
		self.ld = self.get_file(file,"ld")
		logger.info(f"Found file in pkg: {self.ld}")


	def unstrip(self):
		# todo
		return


	def patch_binary(self):
		if not sh(f"patchelf --set-interpreter ./{self.ld} {self.binary}"):
			logger.error("Unable to patch binary")
		if not sh(f"patchelf --replace-needed libc.so.6 ./{self.libc} {self.binary}"):
			logger.error("Unable to patch binary")
		logger.log(50,"Patched binary!")	