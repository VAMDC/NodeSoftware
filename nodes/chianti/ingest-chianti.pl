#!/usr/bin/perl

print "CREATE TABLE states (\n";
print "         id INTEGER, \n";
print "		ChiantiIonType CHAR(1), \n";
print "         species INTEGER, \n";
print "		AtomSymbol CHAR(8), \n";
print "		AtomNuclearCharge INTEGER, \n";
print "		AtomIonCharge INTEGER, \n";
print "		ChiantiAtomStateIndex INTEGER NOT NULL, \n";
print "		AtomStateConfigurationLabel VARCHAR(32), \n";
print "		AtomStateS FLOAT, \n";
print "		AtomStateL FLOAT, \n";
print "		AtomStateTotalAngMom FLOAT, \n";
print "		AtomStateEnergyExperimental DOUBLE, \n";
print "		AtomStateEnergyTheoretical DOUBLE, \n";
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
        print '0, '; # species reference - filled in later
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
print "		RadTransWavelength DOUBLE, \n";
print "         RadTransWavelengthMethod Char(4), \n";
print "		RadTransProbabilityWeightedOscillatorStrength DOUBLE, \n";
print "		RadTransProbabilityTransitionProbabilityA DOUBLE, \n";
print "         PRIMARY KEY (id) \n";
print ");\n";

open TRANSITIONS, "/home/guy/chianti/raw-data/chianti_data_v6_l-1.txt" or die;

# Throw away the first line, which is a comment.
$discard = <TRANSITIONS>;

$index = 0;
while(<TRANSITIONS>) {
	#print $_;
	my $line = $_;
	chomp $line;
	my @fields = split(/\s*\|\s*/, $line);
        my $transTypeCode = shift @fields;
        my $atomSymbol = firstWord(shift @fields);
        shift @fields; # AtomNuclearCharge - unwanted
        shift @fields; # AtomIonCharge - unwanted
        my $finalStateIndex = shift @fields;
        my $initialStateIndex = shift @fields;
        my $experimentalWavelength = shift @fields;
        my $theoreticalWavelength = shift @fields;
        my $weightedOscilatorStrength = shift @fields;
        my $probabilityAValue = shift @fields;

        if ($experimentalWavelength > 0) {
          $index = $index + 1;
	  print 'INSERT INTO transitions VALUES(';
          print $index, ', '; # index - the primary key
	  print '"', $transTypeCode, '", '; 
	  print '"', $atomSymbol, '", '; # AtomSymbol
  	  print $finalStateIndex, ', '; # ChiantiRadTransFinalStateIndex
	  print $initialStateIndex, ', '; # ChiantiRadTransInitialStateIndex
	  print $experimentalWavelength, ', '; # RadTransWavelengthExperimentalValue
          print '"EXP", ';
	  print $weightedOscilatorStrength, ', '; # RadTransProbabilityWeightedOscillatorStrengthValue
	  print $probabilityAValue; # RadTransProbabilityTransitionProbabilityAValue
          print ");\n";
	}

	if ($theoreticalWavelength > 0) {
          $index = $index + 1;
	  print 'INSERT INTO transitions VALUES(';
          print $index, ', '; # index - the primary key
	  print '"', $transTypeCode, '", '; 
	  print '"', $atomSymbol, '", ';
  	  print $finalStateIndex, ', ';
	  print $initialStateIndex, ', ';
	  print $theoreticalWavelength, ', ';
          print '"THEO", ';
	  print $weightedOscilatorStrength, ', ';
	  print $probabilityAValue;
          print ");\n";
	}
}

# Set the foreign key pointing from the states table into the species table.
print "UPDATE states SET species=(1000*AtomIonCharge) + AtomNuclearCharge;\n";

print "\n";
print "CREATE table species (\n";
print "id INTEGER NOT NULL,\n";
print "AtomSymbol CHAR(2),\n";
print "AtomNuclearCharge INTEGER,\n";
print "AtomIonCharge INTEGER,\n";
print "PRIMARY KEY(id)\n";
print ");\n";


print "INSERT INTO species(id,AtomSymbol,AtomNuclearCharge,AtomIonCharge) SELECT DISTINCT ((1000*AtomIonCharge) + AtomNuclearCharge),AtomSymbol,AtomNuclearCharge,AtomIonCharge FROM states;\n";


# Returns the first word of a given sentence in which words are 
# separated by one or more characters of white space.
sub firstWord {
	my $sentence = shift;
	my @words = split /\s+/, $sentence;
        return shift @words;
}


