#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program implements a database importer that reads from
ascii-input files to the django database. It's generic and is
controlled from a mapping file.

"""

import sys
import gzip
import collections
import six
from time import time

TOTAL_LINES = 0
TOTAL_ERRS = 0
is_iter = lambda iterable: isinstance(iterable, collections.Iterable) and not isinstance(iterable, six.string_types)

DELIM = ';'
QUOTE = '"'
NULL = '\\N'


def ftime(t0, t1):
    "formats time to nice format."
    ds = t1 - t0
    dm, ds = int(ds) / 60, ds % 60
    return "%s min, %s s." % (dm, ds)

def log_trace(e, info=""):
    """
    Intended to be called from inside a traceback exception with
    the exception object as first argument.
    Captures the latest traceback.
    """
    sys.stderr.write("%s%s\n" % (info, str(e)))

def read_mapping(fname):
    """
    Read the config dictionary from a file.
    Note: very unsafe, since the content gets executed.
    Have a look at createcfg() to see how it should look like.
    """
    try:
        f=open(fname)
    except IOError:
        print("Error: File name '%s' not found." % fname)
        return None
    exec(f.read()) # this should define a variable "mapping"
    try:
        return mapping
    except NameError:
        print("Error: mapping_file must contain a global variable called 'mapping'.")
        return None

def validate_mapping(mapping):
    """
    Check the mapping definition to make sure it contains
    a structure suitable for the parser.
    """
    required_fdict_keys = ("infiles", "linemap", "outfile")
    required_col_keys = ("cname", "cbyte")
    if not mapping:
        raise Exception("Empty/malformed mapping.")
    if not type(mapping) == list or \
           any([True for fdict in mapping if type(fdict) != dict]):
        raise Exception("Mapping must be a list of dictionaries, one for each file to convert.")
    for fdict in mapping:
        if len([True for key in fdict.keys() if key in required_fdict_keys]) < len(required_fdict_keys):
            string = "Mapping error: One of the keys %s is missing from the mapping %s."
            raise Exception(string % (required_fdict_keys, fdict.keys()))
        if not fdict['linemap'] or type(fdict['linemap']) != list:
            raise Exception("Mapping error: 'linemap' must be a list of dicts.")
        for col in fdict['linemap']:
            if not type(col) == dict or \
                len([True for key in col.keys()
                     if key in required_col_keys]) < len(required_col_keys):
                string = "Mapping error: Linemaps must have at least keys %s"
                raise Exception(string % required_col_keys)
    return True


# working functions for the importer
def get_value(linedata, column_dict):
    """
    Process one line/block of data. Linedata is a tuple that always starts with
    the raw string for the line. The function with its arguments is read from
    the column_dict and applied to the linedata. The result is returned, after
    checking for the NULL value.
    """
    global TOTAL_ERRS
    cbyte = column_dict['cbyte']
    colfunc = cbyte[0]
    filenum = column_dict.get('filenum', 0)
    if is_iter(filenum):
        linedata = [linedata[num] for num in filenum] # this will raise error if out of bounds, as it should.
    else:
        linedata = linedata[filenum]
    args = ()
    if len(cbyte) > 1:
        args = cbyte[1:]
    kwargs = column_dict.get('kwargs', {})
    try:
        dat = colfunc(linedata,  *args, **kwargs)
    except RuntimeError:
        # this is let through, it should be a controlled raise to skip this line
        raise
    except Exception as e:
        # a general error
        log_trace(e, "error processing line/block '%s' - in %s%s: " % (linedata, colfunc, args))
        TOTAL_ERRS += 1
        raise
    if not dat or ('cnull' in column_dict and dat == column_dict['cnull']):
        return None

    return QUOTE+str(dat)+QUOTE


class MappingFile(object):
    r"""
    This class implements an object that represents
    an open file from which one can read blocks. The object
    keeps track of its own block-step speed and will return lines
    as defined by this speed. E.g. for a line-step speed of 0.5,
    it will return the same line twice in a row whereas for a
    step speed of 2, will return every second block etc.

    If endblock is \\n (default), the block will infact represent a line.
    """

    def block_generator(self, fileobj, startblock=None, endblock='\n'):
        "generator, stepping through blocks"

        if not startblock and endblock == '\n':
            # fast line-generator
            for line in self.file:#.xreadlines():
                yield line
            return

        # we also accept multiple start/end conditions
        if not is_iter(startblock):
            startblock = [startblock]
        if not is_iter(endblock):
            endblock = [endblock]

        # block generator
        block = ""
        for line in self.file:  # Previously used .xreadlines():
            if startblock[0] != None:
                if block:
                    # we are already in a block, so ignore startblock
                    pass
                else:
                    # find any matching startblock entries in the line, and index the matches
                    smatches = [inum for inum, start in enumerate(startblock) if start in line]
                    if smatches:
                        # start a new block
                        start = startblock[smatches[0]]
                        scrap, block = line.split(start, 1)
                        block = start + block
                        continue
                    else:
                        # we are outside a block; ignore
                        continue

            ematches = [inum for inum, end in enumerate(endblock) if end in line]
            if ematches:
                # ending the block
                end = endblock[ematches[0]]
                nline, buf = line.split(end, 1)
                block += nline
                yield block
                if startblock[0] != None:
                    if end in startblock:
                        # we have to re-insert the startblock(=endblock) in this case
                        block = end + buf
                    else:
                        # we ignore data outside startblock...endblock
                        block = ""
                else:
                    block = buf
                buf = ""
            else:
                block += line
        if block:
            # if we still have data when the file ends (without having hit an endblock),
            # return this too.
            yield block

    def __init__(self, filepath, headblocks, commentchar,
                 blockoffset, blockstep, errblock, startblock=None, endblock='\n'):
        "Initialize the file"

        self.commentchar = commentchar

        if filepath.endswith('.gz'):
            # a gzipped file. Try to open with gzip library
            self.file = gzip.open(filepath, 'r')
        else:
            self.file = open(filepath, 'r')
        self.blocks = self.block_generator(self.file, startblock, endblock) # a generator
        for i in range(headblocks + blockoffset):
            next(self.blocks)
        while True:
            self.block = next(self.blocks)
            if not self.block.startswith(self.commentchar):
                break
        self.counter = -blockstep
        self.blockstep = blockstep
        self.errblock = str(errblock)

    def readblock(self):
        """
        Return a block from the file.

        This method understand both slower
        block stepping (0 < blockstep < 1) and faster (> 1)
        """
        self.counter += self.blockstep
        if self.counter == 0:
            # always return the first block
            return self.block
        elif self.counter % 1 == 0:
            # only step if counter equals an even block
            for i in range(max(1, self.blockstep)):
                while True:
                    self.block = next(self.blocks)
                    if not self.block.startswith(self.commentchar):
                        break
        if self.block.startswith(self.errblock):
            self.block = ""
        # print(self.block)
        return self.block

def make_outfile(file_dict, global_debug=False):
    """
    Process one file definition from a config dictionary by
    processing the file name stored in it and parse it according
    to the mapping.

    file_dict - config dictionary representing one input file structure
    (for an example see e.g. mapping_vald3.py)

    a function raising a RuntimeError exception will skip the current
    line being parsed.

    """

    outf = open(file_dict['outfile'],'a')

    linemap = file_dict['linemap']

    filepaths = file_dict['infiles']
    if not is_iter(filepaths):
        filepaths = [filepaths]
    nfiles = len(filepaths)
    filenames = [path.split('/')[-1] for path in filepaths]

    # optional keys, set default values
    headlines = file_dict.get('headlines', [0])
    if not is_iter(headlines):
        headlines = [headlines]
    commentchars = file_dict.get('commentchar', ['#'])
    if not is_iter(commentchars):
        commentchars = [commentchars]
    linesteps = file_dict.get('linestep', [1 for i in range(nfiles)])
    if not is_iter(linesteps):
        linesteps = [linesteps]
    lineoffsets = file_dict.get('lineoffset', [0 for i in range(nfiles)])
    if not is_iter(lineoffsets):
        lineoffsets = [lineoffsets]
    # lines that are identified as bad
    errlines = file_dict.get('errlines', ["Unknown" for i in range(nfiles)])
    if not is_iter(errlines):
        errlines = [errlines]
    # treat start/endblock characters
    startblock = file_dict.get("startblock", None)
    endblock = file_dict.get('endblock', '\n')

    # -----

    if len(filenames) == 1:
        print('Working on %s ...' % filenames[0])
    else:
        print("Working on " + " + ".join(filenames) + " ...")

    # open file handles
    mapfiles = []
    for fnum, filepath in enumerate(filepaths):
        # print(filepath)
        mapfiles.append(MappingFile(filepath, headlines[fnum], commentchars[fnum],
                                    lineoffsets[fnum], linesteps[fnum], errlines[fnum],
                                    startblock=startblock, endblock=endblock))

    total = 0
    errors = 0
    while True:
        # step and read one line from all files
        lines = []
        data = []

        try:
            for mapfile in mapfiles:
                # this automatically syncs all files' lines
                lines.append(mapfile.readblock())
        except StopIteration:
            # we are done.
            break

        total += 1

        try:
            for linedef in linemap:

                # check if debug flag is set for this line

                debug = global_debug or 'debug' in linedef and linedef['debug']

                # do not stop or log on errors (this does not hide debug messages if debug is active)
                #skiperrors = linedef.has_key("skiperrors") and linedef["skip_errors"]

                # parse the mapping for this line(s)
                dat = get_value(lines, linedef)
                if debug:
                    print("DEBUG: get_value on %s returns '%s'" % (linedef['cname'],dat))

                data.append(dat or NULL)
            outf.write(';'.join(data) +'\n')
        except RuntimeError:
            # a parse method indicates we should skip creating this line
            total -= 1
            continue

    outf.close()

    print('  %s -> %s: %s lines processed. %s collisions/errors/nomatches.' % (" + ".join(filenames), file_dict['outfile'], total, errors))

    global TOTAL_LINES, TOTAL_ERRS
    TOTAL_LINES += total
    TOTAL_ERRS += errors

def parse_mapping(mapping, debug=False):
    """
    Step through a list of mappings describing
    the relation between (usually ascii-)files and
    django database fields. This should ideally
    not have to be changed for different database types.
    """

    if not validate_mapping(mapping):  return
    t0 = time()

    for file_dict in mapping:
        t1 = time()
        make_outfile(file_dict, global_debug=debug)
        print("Time used: %s" % ftime(t1, time()))
        #pdb.set_trace()
        #print gc.garbage
        #print gc.get_count()

    print("Total time used: %s" % ftime(t0, time()))
    print("Total number of errors/fails/skips: %s/%s (%g%%)" % (TOTAL_ERRS,
                                                                TOTAL_LINES,
                                                                100*float(TOTAL_ERRS)/TOTAL_LINES))

