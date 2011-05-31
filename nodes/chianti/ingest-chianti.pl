#!/usr/bin/perl

print "CREATE TABLE states (\n";
print "         id INTEGER, \n";
print "		ChiantiIonType CHAR(1), \n";
print "		AtomSymbol CHAR(8), \n";
print "		AtomNuclearCharge INTEGER, \n";
print "		AtomIonCharge INTEGER, \n";
print "		ChiantiAtomStateIndex INTEGER NOT NULL, \n";
print "		AtomStateConfigurationLabel VARCHAR(32), \n";
print "		AtomStateS FLOAT, \n";
print "		AtomStateL FLOAT, \n";
print "		AtomStateTotalAngMom FLOAT, \n";
print "		AtomStateEnergyExperimentalValue DOUBLE, \n";
print "		AtomStateEnergyTheoreticalValue DOUBLE, \n";
print "		PRIMARY KEY (id) \n";
print ");\n";


open STATES, "/home/guy/chianti/raw-data/chianti_data_v6_e.txt" or die;

# Throw away the first line, which is a comment.
$discard = <STATES>;

$index = 0;
while(<STATES>) {
	$index++;
	#print $_;
	$line = $_;
	chomp $line;
	@fields = split(/\s*\|\s*/, $line);
	#print join ":", @fields, "\n";
	print 'INSERT INTO states VALUES(';
	print $index, ', '; # Primary key
	print '"', shift @fields, '", '; # ChiantiIonType
	print '"', firstWord(shift @fields), '", '; # AtomSymbol
	print shift @fields, ', '; # AtomNuclearCharge
	print shift @fields, ', '; # AtomIonCharge
	print shift @fields, ', '; # ChiantiAtomStateIndex
	print '"', shift @fields, '", '; # AtomStateConfigurationLabel
	print shift @fields, ', '; # AtomStateS
	print shift @fields, ', '; # AtomStateL
	print shift @fields, ', '; # AtomStateTotalAngMom
	print shift @fields, ', '; # AtomStateEnergyExperimentalValue
	print shift @fields; # AtomStateEnergyTheoreticalValue
        print ");\n";
}

close STATES;


print "CREATE TABLE transitions (\n";
print "         id INTEGER NOT NULL, \n"; # Primary key: just an index number.
print "		ChiantiRadTransType CHAR(1), \n";
print "		AtomSymbol CHAR(8), \n";
print "		ChiantiRadTransFinalStateIndex INTEGER, \n";
print "		ChiantiRadTransInitialStateIndex INTEGER, \n";
print "		RadTransWavelengthExperimentalValue DOUBLE, \n";
print "		RadTransWavelengthTheoreticalValue DOUBLE, \n";
print "		RadTransProbabilityWeightedOscillatorStrengthValue DOUBLE, \n";
print "		RadTransProbabilityTransitionProbabilityAValue DOUBLE, \n";
print "         PRIMARY KEY (id) \n";
print ");\n";

open TRANSITIONS, "/home/guy/chianti/raw-data/chianti_data_v6_l-1.txt" or die;

# Throw away the first line, which is a comment.
$discard = <TRANSITIONS>;

$index = 0;
while(<TRANSITIONS>) {
	#print $_;
	$line = $_;
	chomp $line;
	@fields = split(/\s*\|\s*/, $line);
        $index = $index + 1;
	#print join ":", @fields, "\n";
	print 'INSERT INTO transitions VALUES(';
        print $index, ', '; # index - the primary key
	print '"', shift @fields, '", '; # ChiantiRadTransType
	print '"', firstWord(shift @fields), '", '; # AtomSymbol
	shift @fields; # AtomNuclearCharge - unwanted
	shift @fields; # AtomIonCharge - unwanted
	print shift @fields, ', '; # ChiantiRadTransFinalStateIndex
	print shift @fields, ', '; # ChiantiRadTransInitialStateIndex
	print shift @fields, ', '; # RadTransWavelengthExperimentalValue
	print shift @fields, ', '; # RadTransWavelengthTheoreticalValue
	print shift @fields, ', '; # RadTransProbabilityWeightedOscillatorStrengthValue
	print shift @fields; # RadTransProbabilityTransitionProbabilityAValue
        print ");\n";
}

# Returns the first word of a given sentence in which words are 
# separated by one or more characters of white space.
sub firstWord {
	my $sentence = shift;
	my @words = split /\s+/, $sentence;
        return shift @words;
}
