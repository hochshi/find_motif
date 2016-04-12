#!/usr/bin/perl

# This is a script to render a plain text file into SVG, line by line.

use strict;
use SVG;
use vars qw($VERSION);
$VERSION = '1.00';

my $svg = new SVG;

$svg->comment('Generated by txt2svg');

my $i=0;
while (<>) {
    chomp($_);
    s/\t/    /g;        # Convert tabs into spaces, otherwise we get errors about invalid char

    my $text = $svg->text(id    => "text_line_$i",
			  x     => 10,
			  y     => 12*(1+$i),
			  'xml:space' => 'preserve',
			  style => { 'font' => 'Courier', 
				     'font-family' => 'Courier 10 pitch', 
				     'font-size' => 10,
				 }
			  )
	->cdata($_);
    $i++;
}

print $svg->xmlify();
