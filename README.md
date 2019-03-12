# CHISE_char_decomposer
decompose Chinese characters according to CHISE

## Comparing CHISE and GlyphWiki

GlyphWiki is for generating the printable font for arbitrary Chinese characters.  
CHISE is the database collecting the information of the composition.  

For their different motivation, there will be some differences.

For example, for u63a8 (推).  It should be decomposed into 扌隹.

In GlyphWiki we see:

    u63a8  | u3013   | 99:0:0:0:0:200:200:u63a8-j

Glyphwiki describe the chracters just by u63a8-j . The shape is just represented by the japanese version of the same character. On the web version, http://glyphwiki.org/wiki/u63a8 there is also nothing about 扌隹.
 
While in CHISE, we can see:  

    推 aj1-02602
    Ideographic Radical : ⼿部 (R064)
    Ideographic Strokes : 8
    Ideographic Structure : ⿰扌隹
    
 Thus, decomposition according to CHISE is proper in my opinion.
 
 ## How to get CHISE
 
 http://www.chise.org/dataset.ja.html
 
 ## Structure of CHISE data
 
 You can find a detialed description here: http://git.chise.org/gitweb/?p=chise/ids.git;a=blob_plain;f=README.en;hb=HEAD

 ## What does this project do
 
 Replacing any Chinese characters in the input file with [radicals]
 
 ## Usage
 1 download the chise data by
    
    % git clone http://git.chise.org/git/chise/ids.git

 2 move the IDS-UCS-*.txt files to the root folder of THIS project.
 
 3 Start decomposition by
 
    python main.py -i [input_file] -o [output_file]
