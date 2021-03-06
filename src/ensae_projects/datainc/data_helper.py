"""
@file
@brief Simple functions to process text files.
"""
import datetime
from pyquickhelper.loghelper import noLOG
from .data_exception import FileFormatException


def convert_dates(sd, option=None, exc=False):
    """
    Converts a string into a date.

    @param      sd          string
    @param      option      see below
    @param      exc         raise an exception
    @return                 string

    * ``'F'``: dates must contain ``/`` and format is ``DD/MM/YY``
    """
    if option == "F":
        if "/" in sd:
            try:
                v2 = datetime.datetime.strptime(sd, "%d/%m/%y")
                return v2.strftime("%Y-%m-%d")
            except ValueError:
                pass
    return sd


def clean_column_name_sql_dump(i, line, hist, sep=";"):
    """
    Removes quotes in a line which looks like:

    ::

        0; "a"; 'j"'; "r;"

    @param      i       line number (unused)
    @param      line    line to process
    @param      hist    distribution of the number of columns
    @param      sep     line separator
    @return             text line, number of columns
    """
    vals = []
    beg = -1
    ending = ""
    for ii, c in enumerate(line):
        if beg == -1:
            beg = ii
            if c in ('"', "'"):
                nxt = c
            else:
                nxt = sep
        elif c == nxt:
            if c == sep:
                vals.append(line[beg:ii].strip())
                beg = -1
            else:
                nxt = sep
        elif c == "\n":
            ending = c
    if beg != -1:
        vals.append(line[beg:].strip())
    if ending:
        return sep.join(vals) + ending, len(vals)
    else:
        return sep.join(vals), len(vals)


def change_encoding(infile, outfile, enc1, enc2="utf-8",
                    process=None, fLOG=noLOG):
    """
    Changes the encoding of a text file and removes quotes.
    By default *process* is @see fn process_line.

    @param      infile      input file
    @param      outfile     output file
    @param      enc1        encoding of the input file
    @param      enc2        encoding of the output file
    @param      process     function which processes a line, see below
    @param      fLOG        logging function
    @return                 number of processed lines

    function ``process`` ::

        def process(line_number, line):
            # ...
            return line

    See @see fn clean_column_name_sql_dump for an example.
    """
    if process is None:
        def process_line(i, s):
            return s
        process = process_line
    with open(infile, "r", encoding=enc1) as f:
        with open(outfile, "w", encoding=enc2) as g:
            lasti = 0
            for i, line in enumerate(f):
                lasti = i
                if (i + 1) % 10000 == 0:
                    fLOG(infile, "-", i + 1, "lines")
                g.write(process(i, line))
            return lasti


def change_encoding_improve(infile, outfile, enc1, enc2="utf-8",
                            process=None, fLOG=noLOG):
    """
    Changes the encoding of a text file, removes quotes.
    By default *process* is @see fn process_line
    but the function has access to the distribution of the number of columns
    in the previous lines.

    @param      infile      input file
    @param      outfile     output file
    @param      enc1        encoding of the input file
    @param      enc2        encoding of the output file
    @param      process     function which processes a line, see below
    @param      fLOG        logging function
    @return                 number of processed lines

    function ``process`` ::

        def process(line_number, line, histo_nb_columns):
            # ...
            return line, number_of_columns
    """
    if process is None:
        def process_line(i, s, hist):
            return s, 0
        process = process_line
    hist = {}
    with open(infile, "r", encoding=enc1) as f:
        with open(outfile, "w", encoding=enc2) as g:
            lasti = 0
            for i, line in enumerate(f):
                lasti = i
                if (i + 1) % 10000 == 0:
                    fLOG(infile, "-", i + 1, "lines")
                line, nb_col = process(i, line, hist)
                hist[nb_col] = hist.get(nb_col, 0) + 1
                g.write(line)
            return lasti


def enumerate_text_lines(filename, sep="\t", encoding="utf-8", quotes_as_str=False, header=True,
                         clean_column_name=None, convert_float=False, option=None, skip=0, take=-1,
                         fLOG=noLOG):
    """
    Enumerates all lines from a text file and does some cleaning (see the list of parameters).

    @param          filename            filename
    @param          sep                 column separator
    @param          header              first row is header
    @param          encoding            encoding
    @param          quotes_as_str       surrounded by quotes
    @param          clean_column_name   function to clean column name
    @param          convert_float       convert number into float wherever possible
    @param          option              several option to clean dates, see below
    @param          skip                number of rows to skip
    @param          take                number of rows to consider (-1 for all)
    @param          fLOG                logging function
    @return                             iterator on dictionary

    Options to cleaning dates:

    * ``'F'``: dates must contain ``/`` and format is ``DD/MM/YY``
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
            if s and len(s) > 1 and s[0] == s[-1] and s[0] in ('"', "'"):
                return s[1:-1]
        return s

    def clean_dates(fields, option):
        if option:
            if option == "F":
                update = {}
                for k, v in fields.items():
                    if "/" in v:
                        try:
                            v2 = datetime.datetime.strptime(v, "%d/%m/%y")
                            update[k] = v2.strftime("%Y-%m-%d")
                        except ValueError:
                            continue
                if update:
                    fields.update(update)
        return fields

    with open(filename, "r", encoding=encoding) as f:
        d = 0
        nb = 0
        for i, line in enumerate(f):
            if nb >= take >= 0:
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
                    # probably the last line
                    continue
                raise FileFormatException("different number of columns: schema {0} != {1} for line {2}".format(
                    len(schema), len(spl), i + 1))
            val = {k: convert(clean_quotes(v, quotes_as_str), convert_float)
                   for k, v in zip(schema, spl)}
            val = clean_dates(val, option)
            yield val
            nb += 1
            if nb % 100000 == 0:
                fLOG(filename, "-", nb, "lines")
