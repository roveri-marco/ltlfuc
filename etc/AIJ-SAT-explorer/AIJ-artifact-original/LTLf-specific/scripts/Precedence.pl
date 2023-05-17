#!/usr/bin/perl
# Author: Kristin Yvonne Rozier
# 2017
# 
# Precedence.pl
#
# Input: n = the number of variables arranged in the output formula
# 
# Output: an LTLf formula of the form 
#           Precedence(n) = ((~x) V (OR _{i=1} ^{n} (yi)))
#
# Usage: Precedence.pl n
#

# System Description
#
# - n variables: y1 .. yn

# Purpose: to create a scaleable formula generator inspired by the Target-Branched Declare Templates from Table 2 in "Efficient Discovery of Target-Branched Declare Constraints" by Claudio Di Ciccio, Fabrizio Maria Maggi, and Jan Mendling



#################### Argument Setup ####################

#Check for correct number and type of command line arguments
if ($ARGV[0] =~ /^-v?/) {
    $verbose = 1;
    shift(@ARGV);
} #end if
else {
    $verbose = 0;
} #end else

if (@ARGV != 1) {
    die "Usage: Precedence.pl n\n\tproduces an n-part formula of the form Precedence(n) = (~x) V (OR _{i=1} ^{n} (yi))\n\tUse flag -v for verbose, human-readable output.\n";
} #end if

$n = $ARGV[0];

#Check that we have an integer
if (($n !~ /^\d+?/) || ($n < 2)) {
    die "Error: Expecting a positive integer (at least 2) as input; Got $n\n";
} #end if


#################### Generation of the Formula ####################
$pattern = "(~x) V (y1"; #initialize the pattern

for ($i = 2; $i <= $n; $i++) {
    $iplus1 = $i + 1;
    $pattern = "$pattern | y$i";
} #end for
$pattern = "$pattern)";

if ($verbose == 1) {
    print "\nComputer readable: ";
} #end if
print "$pattern\n";

