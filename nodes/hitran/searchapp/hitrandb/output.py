# output.py
# v0.2, 18/01/10
# v0.1, 22/06/10
# Dr Christian Hill,
# Department of Physics and Astronomy, University College London
# christian.hill@ucl.ac.uk
#
# Defines the base Output class for outputing results of a HITRAN query
# - this class is derived by OutputXML and OutputTXT to provide XSAMS and
# ASCII text table (including par) formatted output respectively.
import tarfile

class Output:
    def __init__(self, filestem, compression=None):
        self.filestem = filestem
        if compression=='None':
            compression=None
        self.compression = compression
        self.filenames = []

    def compress(self, tar_name, filenames):
        """
        Compress the files filenames into a tarball, using the requested
        compression algorithm.

        """

        if not self.compression:
            return

        tar = tarfile.open(tar_name,'w:%s' % self.compression)
        for pathname in self.filenames:
            # tarfile.addfile chokes on unicode strings, so:
            pathname = str(pathname)
            filename = pathname.split('/')[-1]
            # a little bit of stackoverflow magic to write the files without
            # the directory hierarchy:
            tarinfo = tar.gettarinfo(pathname,filename)
            tar.addfile(tarinfo, file(pathname))
        tar.close()
