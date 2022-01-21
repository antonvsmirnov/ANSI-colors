class Redactor:

    def __init__( self,
                  original = None,
                  terms    = None,
                  index    = None,
                  revision = None,
                  **kwargs ):
        self.name     = self.import_path( original )
        self.terms    = self.import_path( terms )
        self.revision = self.export_path( revision )
        self.index    = self.export_path( index )
        self.records  = {}
        self.lines    = {}
        self.places   = {}
        self.tokens   = {}
# ....... End of __init__() .......




    def import_path( self,import_name ):
        from os.path import abspath as os_abspath
        from os.path import exists  as os_exists
        return os_abspath( import_name ) if import_name and os_exists( import_name ) else None
# ....... End of import_path




    def export_path( self,export_name ):
        from os.path import abspath as os_abspath
        return os_abspath( export_name ) if export_name else None
# ....... End of export_path




    def set_original( self,original_file ):
        self.name = self.import_path( original_file )
# ....... End of set_original() .......




    def set_terms( self,terms_file ):
        self.terms = self.import_path( terms_file )
# ....... End of set_terms() .......




    def set_index( self,index_file ):
        self.index = self.export_path( index_file )
# ....... End of set_index() .......




    def set_revision( self,revision_file ):
        self.revision = self.export_path( revision_file )
# ....... End of set_index() .......



    def promote_ANSI( self ):
        from os import system as os_system
        os_system('')
# ....... End of promote_ANSI() .......




    def ANSI( self,
              VALUE,
              Theme='255;155;55,;;',
              TAG="\x1b["):

        """ ------- ANSI Color Syntax -------
        TAG        :  hex=\x1b[  unicode=\u001b[  octal=\033[
        STYLE      :  monochrome=0  bold=1  light=2  underlined=4  reverse=7
        Theme[0]   :  Foreground
        Theme[1]   :  Background
        true color :  38;2; Foreground (RED;GREEN;BLUE) (0-255);(0-255);(0-255)
        true color :  48;2; Background (RED;GREEN;BLUE) (0-255);(0-255);(0-255)
        """
        if Theme != None:
            Theme = Theme.split(',')
            VALUE = f"{TAG}38;2;{Theme[0]}m{TAG}48;2;{Theme[1]}m{VALUE}{TAG}0;0;0m"
        return VALUE
# ....... End of ANSI() .......




    def render_filestream( self,ansi=True ):
        if self.name:
            with open( self.name, 'r', encoding='utf-8' ) as file_stream:
                render_Ln      = self.render_Ln
                ANSI           = self.ANSI
                index_iterator = sorted( self.lines ).__iter__()
                indexed_Ln     = next( index_iterator,-1 )
                for Ln,line in enumerate(file_stream, start=1):
                    Ln_mark = f"{Ln:^7}"
                    if Ln==indexed_Ln:
                        indexed_Ln = next( index_iterator,-1 )
                        if ansi:
                            Ln_mark = ANSI( VALUE=Ln_mark )
                        line = render_Ln( Ln=Ln,ansi=ansi )
                    print( Ln_mark, line,end='' )
        return self.name
# ....... End of render_filestream() .......




    def export_filestream( self,ansi=False ):
        if self.name and self.revision:
            with open( self.name, 'r', encoding='utf-8' ) as name_stream:
                with open( self.revision, 'w', encoding='utf-8') as revision_stream:
                    render_Ln      = self.render_Ln
                    index_iterator = sorted( self.lines ).__iter__()
                    indexed_Ln     = next( index_iterator,-1 )
                    for Ln, line in enumerate( name_stream,start=1 ):
                        if Ln==indexed_Ln:
                            indexed_Ln = next( index_iterator,-1 )
                            line = render_Ln( Ln=Ln,ansi=ansi )
                        revision_stream.write( line )
        return self.name, self.revision
# ....... End of export_filestream() .......




    def render_index( self,ansi=True ):
        render_Ln = self.render_Ln
        for Ln in self.lines:
            Ln_mark = f"-{Ln}-"
            print(f"{Ln_mark:^7}", render_Ln( Ln=Ln,ansi=ansi ), end='')
 #....... End of render_index() .......




    def view_index( self,ansi=True ):
        view_Ln = self.view_Ln
        for Ln in self.lines:
            view_Ln( Ln=Ln,ansi=ansi )
 #....... End of view_index() .......




    def view_Ln( self,Ln=None,ansi=True ):
        ANSI = self.ANSI
        Ln_iterator = self.lines[Ln].__iter__()
        RECORD = next(Ln_iterator)
        RIGHT, TOKEN = RECORD[2], RECORD[4]
        index_theme = '50;60;30,;;'
        Ln_mark = f"-{Ln}-"
        print(f"{Ln_mark:^7}{TOKEN}",end='')
        for index, record in enumerate( Ln_iterator,start=1 ):
            left, role, token = record[1], record[3], record[4]
            place = f'[{index}]'
            left_side   = '.'*left
            right_side  = '.'*(RIGHT-len(token)-left)
            token_place = token
            if ansi:
                left_side   = ANSI( left_side,   Theme=index_theme)
                right_side  = ANSI( right_side,  Theme=index_theme)
                token_place = ANSI( token_place, Theme=role)
            print(f"{place:^7}{left_side}{token_place}{right_side}")
#....... End of view_Ln() .......




    def render_Ln( self,Ln=None,ansi=True ):
        ANSI  = self.ANSI
        Index = self.lines[Ln]
        base = Index[0]
        base_rank, base_token = 0, base[4]
        mask = [0]*len( base_token )
        for Rank in range( 1,len(Index) ):
            record = Index[Rank]
            left, right = record[1], record[2]
            for Place in range(left, right):
                if Rank > mask[Place]:
                    mask[Place] = Rank
        view = []
        left = 0
        Rank = mask[left]
        for Place in range( len(mask) ):
            if mask[Place] != Rank:
                right  = Place - 1
                primer = Index[Rank][1]
                token  = Index[Rank][4]
                quote =  token[left-primer:len(token)+1] if mask[Place]<Rank else Index[Rank][4][left-primer:right-primer+1]
                if ansi:
                    role  = Index[Rank][3]
                    quote = ANSI( quote,role )
                view.append( quote )
                left = Place
                Rank = mask[Place]
        right = Place
        primer = Index[Rank][1]
        token  = Index[Rank][4]
        quote  = token[left-primer:len(token)+1]
        if ansi:
            role  = Index[Rank][3]
            quote = ANSI( quote,role )
        view.append( quote )
        return ''.join(view)
# ....... End of render_Ln() .......




    def create_record( self,
                       Ln=None,
                       left=None,
                       right=None,
                       role=None,
                       token=None ):
        records, lines, tokens, places = self.records, self.lines, self.tokens, self.places
        if not left in places:
            places[left] = left
        left = places[left]
        if not right in places:
            places[right] = right
        right = places[right]
        if not token in tokens:
            tokens[token] = token
        token = tokens[token]
        record = ( Ln, left, right, role, token )
        if not record in records:
            records[record] = record
            if not Ln in lines:
                lines[Ln]=[]
            lines[Ln].append( record )
        record = records[record]
        return record
# ....... End of create_record() .......




    def drop_Ln( self,Ln=None ):
        if Ln in self.lines:
            Line=self.lines[Ln]
            while len( Line )>0:
                record = Line[0]
                Line.remove( record )
                del self.records[record]
                del record
            del self.lines[Ln]
#....... drop_Ln() .......




    def drop_lines( self,Ln=None ):
        for Ln in sorted(self.lines):
            self.drop_Ln( Ln=Ln )
#....... drop_lines() .......




    def collect_lines( self,term=None,role=None ):
        if self.name:
            with open( self.name, 'r', encoding='utf-8' ) as source:
                create_record = self.create_record
                for Ln, line in enumerate( source, start=1 ):
                    index,offset = 0,0
                    while index != -1:
                        index = line.lower().find( term.lower(),offset )
                        if index != -1:
                            offset = index + len( term )
                            token = line[index:offset]
                            record = create_record( Ln=Ln,
                                                    left=index,
                                                    right=offset,
                                                    role=role,
                                                    token=token )
                    if (offset>0):
                        record = create_record( Ln=Ln,
                                                left=0,
                                                right=len(line),
                                                role=None,
                                                token=line )
# ....... End of collect_lines() .......




    def create_index( self,ansi=True ):
        if self.terms:
            with open(self.terms, 'r') as terms_file:
                from random import randint as random_int
                ANSI, collect_lines = self.ANSI, self.collect_lines
                for priority, term in enumerate( terms_file.read().split() ):
                    Theme = None
                    if ansi:
                        R = random_int(0,255)
                        G = random_int(0,255)
                        B = random_int(0,255)
                        Theme = f"{R};{G};{B},{255-R};{255-G};{255-B}"
                    collect_lines( term=term, role=Theme )
                    print(priority, ANSI( VALUE=term,Theme=Theme ))
                self.sort_index()
        return self.terms
# ....... End of create_index() .......




    def sort_index( self ):
        for Ln in self.lines:
            self.lines[Ln].sort(key=lambda record:(record[1],-1*record[2]))
# ....... End of sort_index() .......




    def export_index( self ):
        if self.index:
            from csv import writer as Writer
            with open(self.index, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = Writer( csv_file )
                for Ln in sorted( self.lines ):
                    csv_writer.writerows(self.lines[Ln])
        return self.index
# ....... End of export_index() .......




    def import_index( self ):
        from os.path import exists as os_exists
        if self.index and os_exists( self.index ):
            self.drop_lines()
            from csv import reader as Reader
            with open(self.index, 'r', newline='', encoding='utf-8') as csv_file:
                csv_reader = Reader(csv_file)
                for csv_line in csv_reader:
                    Ln    = int( csv_line[0] )
                    left  = int( csv_line[1] )
                    right = int( csv_line[2] )
                    token  = csv_line[4]
                    if csv_line[3]=='':
                        role = None
                    else:
                        role = csv_line[3]
                    record = self.create_record( Ln=Ln,
                                                 left=left,
                                                 right=right,
                                                 role=role,
                                                 token=token )
        return self.index
# ....... End of import_index() .......
# ....... End of Redactor .......



def main( mode          = None,
          original      = None,
          terms         = None,
          index         = None,
          revision      = None,
          ansi          = True,
          verbose       = True,
          **kwargs ):

    draft = Redactor( original=original,terms=terms,index=index,revision=revision,**kwargs )
    SIDE = '='*7
    INDENT = '\n  '
    if verbose:
        print(f"""\n{SIDE} ANSI_Redactor configuration {SIDE}\
            {INDENT}<MODE>      {mode}\
            {INDENT}<ORIGINAL>  {draft.name}\
            {INDENT}<TERMS>     {draft.terms}\
            {INDENT}<INDEX>     {draft.index}\
            {INDENT}<REVISION>  {draft.revision}\
            """)
    if ansi:
        draft.promote_ANSI()

    if mode=='create-index':
        if verbose: print(f"\n{SIDE} Details of created INDEX {SIDE}{INDENT}{draft.name}{INDENT}{draft.terms}")
        draft.create_index( ansi=ansi )
        draft.export_index()
        if verbose: print(f"\n{SIDE} Export path of created INDEX {SIDE}{INDENT}{draft.index}")
                        
    if mode=='view-index':
        draft.import_index()
        if verbose: print(f"\n{SIDE} View of imported INDEX {SIDE}{INDENT}{draft.index}")
        draft.view_index( ansi=ansi )
        if verbose: print(f"\n{SIDE} Render of imported INDEX {SIDE}{INDENT}{draft.index}")
        draft.render_index( ansi=ansi )

    if mode=='view-revision':
        draft.import_index()
        if verbose: print(f"\n{SIDE} Details of rendered REVISION {SIDE}{INDENT}{draft.name}{INDENT}{draft.index}")
        draft.render_filestream( ansi=ansi )

    if mode=='export-revision':
        draft.import_index()
        if verbose: print(f"\n{SIDE} Import path of revision index {SIDE}{INDENT}{draft.index}")
        revision_file = draft.export_filestream( ansi=ansi )
        if verbose: print(f"\n{SIDE} Import path of ORIGINAL {SIDE}{INDENT}{draft.name}")
        if verbose: print(f"\n{SIDE} Export path of REVISION {SIDE}{INDENT}{draft.revision}")
# ....... End of main() .......




if __name__=="__main__":
    from ansi_parser import Parser
    configuration = Parser().parse() 
    main( **configuration )



