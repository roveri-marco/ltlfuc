#!/usr/bin/perl
#
# by: Kristin Yvonne Rozier
# begun: Sept/1/2017

# Generate a random conjunction of $f LTLf formulas over $v variables.

#Declare the LTLf formulas
@LTLfFormulas = qw(
Absence2
AlternativePrecedence
AlternativeResponse
AlternativeSuccession
ChainPrecedence
ChainResponse
ChainSuccession
Choice
Coexistence
End
ExclusiveChoice
Existence
NegativeChainSuccession
NegativeSuccession
NotCoexistence
Precedence
RespondedExistence
Response
Succession
);
#NOTE: all of these use a and b as the variables

$debug = 0;


#################### Argument Setup ####################

#Check for correct number and type of command line arguments

if (($ARGV[0] =~ /--help/) || (@ARGV != 2)) {
    die "Usage: LTLfRandomConjunction.pl NumVariables NumConjuncts\nRandomly generate an LTLf formula containing NumConjuncts ANDed together. The variables in each formula will be chosen randomly from NumVars variables.\n";
} #end if

$v = $ARGV[0]; #NumVariables
$c = $ARGV[1]; #NumConjuncts

#Check for errors
if ( (! ($v =~ /^\d+$/)) || (! ($c =~ /^\d+$/)) ) {
    print STDERR "ERROR: NumVariables and NumConjuncts must both be positive integers.\n";
    die "Usage: LTLfRandomConjunction.pl NumVariables NumConjuncts\nRandomly generate an LTLf formula containing NumConjuncts ANDed together. The variables in each formula will be chosen randomly from NumVars variables.\n";
} #end if
else { #debug
    if ($debug) {
	print STDERR "Generating $c conjuncts over $v variables\n";
    } #end if
} #end else


##################################################################
#
# Main Program: 
# 
#    Generate $c conjuncts; for each one, choose an LTLf formula
#       from the list and assign its variables to one of $v in
#       the set.
#
##################################################################

for ($i = 0; $i < $c; $i++) {
    
    #Pick an LTLf formula to add to the conjunction
    $NumFormulas = @LTLfFormulas; 
    $f_num = int(rand($NumFormulas)); 
    if ($debug) {
	print STDERR "Choosing formula number $f_num from the set of $NumFormulas formulas, which is formula $LTLfFormulas[$f_num]\n";
    } #end if    

    $conjunct = $LTLfFormulas[$f_num];
    
    $f = `cat $conjunct`;  #get formula
    chomp $f;              #remove trailing \n
    $v_num = int(rand($v)); #get the number of the first variable
    $a = "p$v_num";
    $v_num = int(rand($v)); #get the number of the second variable
    $b = "p$v_num";
    
    $f =~ s/a/$a/g;
    $f =~ s/b/$b/g;

    if ($i > 0) {
	$formula = "$formula & ($f)";
    } #end if    
    else {
	$formula = "($f)";
    } #end else

} #end for

print "$formula";

