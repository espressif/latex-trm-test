# latexmkrc

# Unix-based systems (Overleaf, Linux, macOS)
if ($^O =~ /^(darwin|linux)$/) {
    $pdflatex = 'xelatex --shell-escape --synctex=1 %O %S';
    $ENV{'TEXINPUTS'}='../00-shared//:./00-chip-spec-content//:' . $ENV{'TEXINPUTS'};
}

# Windows
elsif ($^O eq 'MSWin32') {
    $pdflatex = 'xelatex --shell-escape --synctex=1 %O %S';
    $ENV{'TEXINPUTS'}='../00-shared//;./00-chip-spec-content//;' . $ENV{'TEXINPUTS'};
}

add_cus_dep( 'tex', 'aux', 0, 'makeexternaldocument' );

sub makeexternaldocument {
    # if the dependency isn't one of the files that this latexmk run will consider, process it
    # without this test, we would get an infinite loop!
    if (!($root_filename eq $_[0]))
    {   # PLEASE ENABLE ONLY ONE OF THE FOLLOWING
        # DEPENDING ON THE ENGINE YOU'RE USING

        # FOR PDFLATEX
        # system( "latexmk -cd -pdf \"$_[0]\"" );

        # FOR LATEX+DVIPDF
        # system( "latexmk -cd \"$_[0]\"" );

        # FOR XELATEX
        system( "latexmk -cd -xelatex \"$_[0]\"" );

        # FOR LUALATEX
        # system( "latexmk -cd -lualatex \"$_[0]\"" );
   }
}
