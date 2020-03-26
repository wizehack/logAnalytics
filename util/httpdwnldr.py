from urllib.request import urlopen
import progressbar


class HttpDwnldr:
	def __init__(self, url, filename):
		self._url = url
		self._filename = filename

	def download(self):
		u = urlopen(self._url)
		f = open(self._filename, 'wb')
		print ("Downloading: ", self._filename)
		block_sz = 8192
		bar = progressbar.ProgressBar().start()
		index=0
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			f.write(buffer)
			try:
				if bar.percentage() < 98:
					bar.update(index)
					index = index+1
				else:
					pass
			except ValueError as err:
				print ("Error Occured: ",  err)
				return False
		f.close()
		bar.finish()
		print ("Compeleted")
		return True

#url = 'https://api.github.com/repos/DrkLO/Telegram/tarball'
#filename = url.split('/')[-1]
