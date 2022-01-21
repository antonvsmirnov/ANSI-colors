class Parser():


    def __init__(self):
        from argparse import ArgumentParser as argparse_Parser
        from argparse import FileType as argparse_FileType
        from argparse import RawDescriptionHelpFormatter as Formatter

        self.INDENT = '\n  '
        INDENT = self.INDENT
        PREFIX = '@'
        DESCRIPTION = f"description:{INDENT}Python <SCRIPT> for indexation, ANSI color highlighting and redacting of text streams."
        EPILOG = f'''use cases:\
                 {INDENT}<NAME> an absolute/relative path to the corresponding file NAME\
                 {INDENT}{PREFIX}<NAME> an '{PREFIX}'-prefixed call of configuraton file NAME with a newline-separated list of parse arguments\
                 {INDENT}<python.exe> <SCRIPT> [options]\
                 {INDENT}<python.exe> <SCRIPT> {PREFIX}<NAME>\
                 {INDENT}<python.exe> <SCRIPT> {PREFIX}<NAME> --no-ansi\
                 {INDENT}<python.exe> <SCRIPT> {PREFIX}<NAME> --no-ansi -h\
                 {INDENT}<python.exe> <SCRIPT> --mode create-index    --original <ORIGINAL> --terms <TERMS> --index <INDEX>\
                 {INDENT}<python.exe> <SCRIPT> --mode view-index      --i <INDEX>\
                 {INDENT}<python.exe> <SCRIPT> --mode view-revision   --o <ORIGINAL> --i <INDEX>\
                 {INDENT}<python.exe> <SCRIPT> --mode export-revision --o <ORIGINAL> --i <INDEX> --revision <REVISION> --no-ansi\
                 '''
        parser = argparse_Parser( description           = DESCRIPTION,
                                  epilog                = EPILOG,
                                  fromfile_prefix_chars = PREFIX,
                                  formatter_class       = Formatter )

        parser.add_argument("--mode"     ,help="processing mode of redactor: create-index, view-index, view-revision, export-revision")
        parser.add_argument("--original" ,help="ORIGINAL source file for redacting")
        parser.add_argument("--terms"    ,help="file with TERMS for indexation of original")
        parser.add_argument("--index"    ,help=".CSV file with INDEX data corresponding to original")
        parser.add_argument("--revision" ,help="export path for REVISION of original content according to index data")
        parser.add_argument("--ansi"     ,help="enable ANSI color markup of rendered content", dest='ansi', action='store_true')
        parser.add_argument("--no-ansi"  ,help="disable ANSI coloring of content for tasks with plain text", dest='ansi', action='store_false')
        parser.add_argument("--verbose"  ,help="verbosity of output: 0 (silent), 1 (verbose)", type=int)
        parser.set_defaults( mode      = None,
                             original  = None,
                             terms     = None,
                             index     = None,
                             revision  = None,
                             ansi      = True,
                             verbose   = 1 )
        self.parser = parser
# ....... End of __init__() .......




    def parse(self):
        args,other = self.parser.parse_known_args()
        if args.verbose>=1:
            print(f"\nParsed Arguments:{self.INDENT}{args}{self.INDENT}{other}")
        return vars(args)
# ....... End of parse() .......




    def help(self):
        self.parser.print_help()
# ....... End of help() .......
# ....... End of Parser .......




if __name__=='__main__':
    from sys import argv
    if len(argv)>1: Parser().parse()
    else:           Parser().help()


