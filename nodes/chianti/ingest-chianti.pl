#!/usr/bin/perl

print "CREATE TABLE states (\n";
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
print "         id INTEGER, \n";
print "		PRIMARY KEY (id) \n";
print ");\n";


open STATES, "/users/guy/desktop/chianti/chianti_data_v6_e.txt" or die;

# Throw away the first line, which is a comment.
$discard = <STATES>;

$index = 0;
while(<STATES>) {
	#print $_;
	$line = $_;
	chomp $line;
	@fields = split(/\s*\|\s*/, $line);
	#print join ":", @fields, "\n";
	print 'INSERT INTO states VALUES(';
	print '"', shift @fields, '", '; # ChiantiIonType
        print '0, '; # species reference - filled in later
	print '"', firstWord(shift @fields), '", '; # AtomSymbol
	$nuclearCharge = shift @fields; print $nuclearCharge, ', '; # AtomNuclearCharge
	$ionCharge     = shift @fields; print $ionCharge, ', '; # AtomIonCharge
	$stateIndex    = shift @fields; print $stateIndex, ', '; # ChiantiAtomStateIndex
	print '"', shift @fields, '", '; # AtomStateConfigurationLabel
	print shift @fields, ', '; # AtomStateS
	print shift @fields, ', '; # AtomStateL
	print shift @fields, ', '; # AtomStateTotalAngMom
	print shift @fields, ', '; # AtomStateEnergyExperimentalValue
	print shift @fields, ', '; # AtomStateEnergyTheoreticalValue
	$index = (1000000 * $stateIndex) + (1000 * $ionCharge) + $nuclearCharge;
	print $index; # id - primary key
        print ");\n";
}

close STATES;

# Unknown energies are represented in the input by negative values; convert them to nulls.
print "UPDATE states SET AtomStateEnergyExperimental = NULL WHERE AtomStateEnergyExperimental < 0.0;\n";
print "UPDATE states SET AtomStateEnergyTheoretical = NULL WHERE AtomStateEnergyTheoretical < 0.0;\n";



print "CREATE TABLE transitions (\n";
print "         id INTEGER NOT NULL, \n"; # Primary key: just an index number.
print "		ChiantiRadTransType CHAR(1), \n";
print "		AtomSymbol CHAR(8), \n";
print "		ChiantiRadTransFinalStateIndex INTEGER, \n";
print "		ChiantiRadTransInitialStateIndex INTEGER, \n";
print "         wavelength DOUBLE, \n";
print "		wavelengthexperimental DOUBLE, \n";
print "		wavelengththeoretical DOUBLE, \n";
print "		RadTransProbabilityWeightedOscillatorStrength DOUBLE, \n";
print "		RadTransProbabilityTransitionProbabilityA DOUBLE, \n";
print "         PRIMARY KEY (id) \n";
print ");\n";

open TRANSITIONS, "/users/guy/desktop/chianti/chianti_data_v6_l-1.txt" or die;

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
    my $nuclearCharge = shift @fields; # AtomNuclearCharge - unwanted
    my $ionCharge     = shift @fields; # AtomIonCharge - unwanted
    my $finalStateIndex   = (1000000 * (shift @fields)) + (1000 * $ionCharge) + $nuclearCharge;
    my $initialStateIndex = (1000000 * (shift @fields)) + (1000 * $ionCharge) + $nuclearCharge;;
    my $experimentalWavelength = shift @fields; # RadTransWavelength
    my $theoreticalWavelength = shift @fields; # RadTransWavelength
    my $weightedOscilatorStrength = shift @fields; # RadTransProbabilityWeightedOscillatorStrength
    my $probabilityAValue = shift @fields; # RadTransProbabilityTransitionProbabilityAValue

    $index = $index + 1;
	print 'INSERT INTO transitions VALUES(';
	print $index, ', '; # the primary key
	print '"', $transTypeCode, '", '; 
	print '"', $atomSymbol, '", ';
  	print $finalStateIndex, ', ';
	print $initialStateIndex, ', ';
	print bestWavelength($experimentalWavelength, $theoreticalWavelength), ', ';
	print $experimentalWavelength, ', ';
	print $theoreticalWavelength, ', ';
	print $weightedOscilatorStrength, ', ';
	print $probabilityAValue; 
    print ");\n";
}

# In the input, unknowns are denoted by -1. Change these to proper nulls.
print "UPDATE transitions SET RadTransProbabilityWeightedOscillatorStrength = NULL WHERE RadTransProbabilityWeightedOscillatorStrength < 0.0;\n";
print "UPDATE transitions SET RadTransProbabilityTransitionProbabilityA = NULL WHERE RadTransProbabilityTransitionProbabilityA < 0.0;\n";
print "UPDATE transitions SET wavelength = NULL WHERE wavelength <= 0.0;\n";
print "UPDATE transitions SET wavelengthexperimental = NULL WHERE wavelengthexperimental <= 0.0;\n";
print "UPDATE transitions SET wavelengththeoretical = NULL WHERE wavelengththeoretical <= 0.0;\n";


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


sub bestWavelength {
	my $experimental = shift @_;
	my $theoretical = shift @_;
        return $experimental if $experimental > 0.0;
	return $theoretical if $theoretical > 0.0;
	return -1.0;
}
