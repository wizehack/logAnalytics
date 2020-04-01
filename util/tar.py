import tarfile

class Tar:
	def __init__(self, srcfile, destdir):
		self._srcfile = srcfile
		self._destdir = destdir

	def zxvf(self):
		print("extract: ", self._srcfile)
		ap = tarfile.open(self._srcfile)
		ap.extractall(self._destdir)
		ap.close()
		return True

#src = './testdata/tarball'
#dest = './testdata'


