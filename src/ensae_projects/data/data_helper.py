"""
@file
@brief Exception raised when data is not available
"""
from pyquickhelper import noLOG
from .data_exception import FileFormatException


def change_encoding(infile, outfile, enc1, enc2="utf-8", process=None, fLOG=noLOG):
    """
    change the encoding of a text file

    @param      infile      input file
    @param      outfile     output file
    @param      enc1        encoding of the input file
    @param      enc2        encoding of the output file
    @param      process     function which processes a line
    @param      fLOG        logging function
    @return                 number of processed lines
    """
    if process is None:
        def process_line(s):
            return s
        process = process_line
    with open(infile, "r", encoding=enc1) as f:
        with open(outfile, "w", encoding=enc2) as g:
            for i, line in enumerate(f):
                if (i + 1) % 1000000 == 0:
                    fLOG(infile, "-", i, "lines")
                g.write(process(line))
            return i


def enumerate_text_lines(filename, sep="\t",
                         encoding="utf-8",
                         quotes_as_str=False,
                         header=True,
                         clean_column_name=None,
                         convert_float=False,
                         skip=0,
                         take=-1,
                         fLOG=noLOG):
    """
    enumerate all lines from a text file,
    considers it as column

    @param          filename            filename
    @param          sep                 column separator
    @param          header              first row is header
    @param          encoding            encoding
    @param          clean_column_name   function to clean column name
    @param          convert_float       convert number into float wherever possible
    @param          skip                number of rows to skip
    @param          take                number of rows to consider (-1 for all)
    @param          fLOG                logging function
    @return                             iterator on dictionary
    """
    def get_schema(row, header, clean_column_name):
        if header:
            sch = [_.strip('"') for _ in row]
            if clean_column_name:
                sch = [clean_column_name(_) for _ in sch]
            return sch
        else:
            return ["c%00d" % i for i in range(len(row))]

    def convert(s, convert_float):
        if convert_float:
            try:
                return float(s)
            except ValueError:
                return s
        else:
            return s

    def clean_quotes(s, quotes_as_str):
        if quotes_as_str:
            if s and len(s) > 1 and s[0] == s[-1] == '"':
                return s[1:-1]
        return s

    with open(filename, "r", encoding=encoding) as f:
        d = 0
        nb = 0
        for i, line in enumerate(f):
            if take >= 0 and nb >= take:
                break
            spl = line.strip("\r\n").split(sep)
            if i == 0:
                schema = get_schema(spl, header, clean_column_name)
                if header:
                    d = 1
                    continue
            if i + d < skip:
                continue
            if len(spl) != len(schema):
                if len(spl) == 1:
                    # probably the last file
                    continue
                else:
                    raise FileFormatException("different number of columns: schema {0} != {1} for line {2}".format(
                        len(schema), len(spl), i + 1))
            val = {k: convert(clean_quotes(v, quotes_as_str), convert_float)
                   for k, v in zip(schema, spl)}
            yield val
            nb += 1
            if nb % 100000 == 0:
                fLOG(filename, "-", nb, "lines")
