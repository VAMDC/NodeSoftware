#!/usr/bin/perl

use Chemistry::OpenBabel;

print "DROP TABLE IF EXISTS sources;\n";
print "DROP TABLE IF EXISTS species;\n";
print "DROP TABLE IF EXISTS states;\n";
print "DROP TABLE IF EXISTS components;\n";
print "DROP TABLE IF EXISTS subshells;\n";
print "DROP TABLE IF EXISTS transitions;\n";
print "\n";



print "CREATE table sources (\n";
print "id INTEGER NOT NULL,\n";
print "species_id INTEGER,\n";
print "bibtex VARCHAR(2056),\n";
print "PRIMARY KEY(id)\n";
print ");\n";


open REFS, "/Users/guy/desktop/chianti-7/chianti_data_v7_l_ref-sample.txt" or die;


# Throw away the first line, which is a comment.
$discard = <REFS>;

$index = 0;
while(<REFS>) {
	$index++;
	
	$line = $_;
	chomp $line;
	@fields = split(/\s*\|\s*/, $line);
	
	my ($nuclearCharge, $ionCharge, $bibtex) = @fields;
	
	$bibtex =~ s/\'/\\\'/g;
	
	# Set the foreign key pointing into the species table.
	my $species = (1000 * $ionCharge) + $nuclearCharge;
	
	print "INSERT INTO sources VALUES($index, $species, '$bibtex');\n";
}


print "CREATE TABLE states (\n";
print "		ChiantiIonType CHAR(1), \n";
print "         species INTEGER, \n";
print "		AtomSymbol CHAR(8) NOT NULL, \n";
print "		AtomNuclearCharge INTEGER NOT NULL, \n";
print "		AtomIonCharge INTEGER NOT NULL, \n";
print "         inchi VARCHAR(32) NOT NULL, \n";
print "         inchikey CHAR(27) NOT NULL, \n";
print "		ChiantiAtomStateIndex INTEGER NOT NULL, \n";
print "		AtomStateConfigurationLabel VARCHAR(32), \n";
print "         atomcore CHAR(8) NOT NULL, \n";
print "		AtomStateS FLOAT NOT NULL, \n";
print "		AtomStateL INTEGER NOT NULL, \n";
print "		AtomStateTotalAngMom FLOAT NOT NULL, \n";
print "         parity CHAR(4) NOT NULL, \n";
print "		AtomStateEnergy DOUBLE, \n";
print "		AtomStateEnergyMethod CHAR(4), \n";
print "         id INTEGER, \n";
print "		PRIMARY KEY (id) \n";
print ");\n";


# A table of atomic components. Each row of the states table has exactly one component.
print "CREATE TABLE components (\n";
print "         id INTEGER, \n"; # Same values as id in states table - 1-to-1 match of rows
print "         label VARCHAR(32), \n";
print "         core CHAR(2), \n";
print "         lsl INTEGER, \n";
print "         lss FLOAT, \n";
print "	        PRIMARY KEY (id) \n";
print ");\n";

# A table of electronic sub-shells. Each row in the state table has one or more rows in sub-shells.
# The state column is a foreign key to the states table. 
print "CREATE TABLE subshells (\n";
print "        id INTEGER NOT NULL AUTO_INCREMENT, \n";
print "        state INTEGER, \n";
print "        n INTEGER, \n";
print "        l INTEGER, \n";
print "        pop INTEGER, \n";
print "        PRIMARY KEY (id) \n";
print ");\n";

open STATES, "/users/guy/desktop/chianti-7/chianti_data_v7_e.txt" or die;

my $inchiConverter = new Chemistry::OpenBabel::OBConversion();
$inchiConverter->SetInAndOutFormats('smi', 'inchi');
$inchiConverter->AddOption("X", $Chemistry::OpenBabel::OBConversion::OUTOPTIONS, "DoNotAddH");
my $inchiKeyConverter = new Chemistry::OpenBabel::OBConversion();
$inchiKeyConverter->SetInAndOutFormats('smi', 'inchi');
$inchiKeyConverter->AddOption("K");
$inchiKeyConverter->AddOption("X", $Chemistry::OpenBabel::OBConversion::OUTOPTIONS, "DoNotAddH");

# Throw away the first line, which is a comment.
$discard = <STATES>;

$index = 0;
while(<STATES>) {
	$line = $_;
	chomp $line;
	@fields = split(/\s*\|\s*/, $line);
	my ($chiantiIonType, $ionName, $nuclearCharge, $ionCharge, $stateIndex, $configurationLabel, 
           $atomStateS, $atomStateL, $totalAngMom, $energyExperimental, $energyTheoretical) = @fields;

        my $atomSymbol = firstWord($ionName);
	my $index = (1000000 * $stateIndex) + (1000 * $ionCharge) + $nuclearCharge;
        my ($energy, $energyMethod)  = bestEnergy($energyExperimental, $energyTheoretical);

        my $smiles = "[".$atomSymbol;
        for (1..$ionCharge) {
          $smiles .= '+';
        }
	$smiles .= ']';

        my $molecule = new Chemistry::OpenBabel::OBMol();
        $inchiConverter->ReadString($molecule, $smiles);
	my $inchi = $inchiConverter->WriteString($molecule);
	chomp $inchi;
	print ERR $inchi, "\n";
        $inchiKeyConverter->ReadString($molecule, $smiles);
	my $inchiKey = $inchiKeyConverter->WriteString($molecule);
	chomp $inchiKey;

        # The valence shell is described in the subshells tables.
        # The remaining, closed shells form an isoelectronic core to the atom.
        # Chianti has a few cases where the "core" includes part of the valence shell.
        my ($label, $outerElectronCount, $parity) = configuration($index, $configurationLabel);
        my $isoElectronicCount = $nuclearCharge - $outerElectronCount - $ionCharge;
        my $atomCore = "";
        $atomCore = "H"  if $isoElectronicCount ==  1;
        $atomCore = "He" if $isoElectronicCount ==  2;
        $atomCore = "Be" if $isoElectronicCount ==  4;
        $atomCore = "C"  if $isoElectronicCount ==  6;
        $atomCore = "O"  if $isoElectronicCount ==  8;
        $atomCore = "F"  if $isoElectronicCount ==  9;
        $atomCore = "Ne" if $isoElectronicCount == 10;
        $atomCore = "Mg" if $isoElectronicCount == 12;
        $atomCore = "S"  if $isoElectronicCount == 16;
        $atomCore = "Cl" if $isoElectronicCount == 17;
        $atomCore = "Ar" if $isoElectronicCount == 18;
        $atomCore = "Kr" if $isoElectronicCount == 36;
        $atomCore = "Xe" if $isoElectronicCount == 54;
        die "No core, $isoElectronicCount" if $isoElectronicCount > 0 && !$atomCore;

	print 'INSERT INTO states VALUES(';
	print '"', $chiantiIonType, '", ';
	print '0, '; # species reference - filled in later
	print '"', $atomSymbol, '", ';
	print $nuclearCharge, ', ';
	print $ionCharge, ', ';
        print '"', $inchi, '", ';
	print '"', $inchiKey, '", ';
	print $stateIndex, ', ';
	print '"', $label, '", ';
        print '"', $atomCore, '", ';
	print $atomStateS, ', '; 
	print $atomStateL, ', ';
	print $totalAngMom, ', ';
        print '"', $parity, '", ';
	print $energy, ', ';
	print '"', $energyMethod, '", ';
	print $index; # id - primary key
	print ");\n";

	print 'INSERT INTO components VALUES(';
	print $index, ', '; # foreign key to states table
	print '"', $label, '", ';
        print '"', $atomCore, '", ' if $atomCore;
        print 'NULL, ' if !$atomCore;
	print $atomStateL, ', '; 
	print $atomStateS;
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

open TRANSITIONS, "/users/guy/desktop/chianti-7/chianti_data_v7_l.txt" or die;

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
print "inchi VARCHAR(32), \n";
print "inchikey CHAR(27), \n";
print "PRIMARY KEY(id)\n";
print ");\n";


print "INSERT INTO species(id,AtomSymbol,AtomNuclearCharge,AtomIonCharge,inchi,inchikey) SELECT DISTINCT ((1000*AtomIonCharge) + AtomNuclearCharge),AtomSymbol,AtomNuclearCharge,AtomIonCharge,inchi,inchikey FROM states;\n";


print "CREATE INDEX energy ON states(AtomStateEnergy);\n";
print "CREATE INDEX wavelength ON transitions(wavelength);\n";

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

sub bestEnergy {
	my $experimental = shift @_;
	my $theoretical = shift @_;
        return ($experimental, 'EXP') if $experimental >= 0.0;
	return ($theoretical, 'THEO') if $theoretical >= 0.0;
	return -1.0;
}


# Parses a configuration label and writes one row into the subshells table for each sub-shell.
sub configuration {
  my ($state, $label) = @_;

  # The scalar sum of the orbital angular momenta determines the parity of the state.
  my $sigmaL = 0;

  # Some of the sub-shells have a coupling-term notation, written in parantheses, which we discard.
  $label =~ s/\(\d*[A-Z]\d*\)/ /;

  # All the sub-shell notations should be separated by spaces, but some are elided.
  $label =~ s/(\d)([a-z])(\d)([a-z])/$1$2 $3$4/;

  # Sadly, some of the angular-momentum characters appear in the wrong case.
  $label = lc $label;

  # Keep track of the total number of electrons in the sub-shells.
  my $totalPop = 0;

  # This matches the nominal notiation for sub-shells, after the correction above.
  while ($label =~ m/(\d+)([a-z])(\d*)/g) {
    my $n = $1;
    my $l = lQn($2);
    my $pop;
    if (!$3) {
      $pop = 1;
    }
    else {
      $pop = $3;
    }

    $totalPop += $pop;

    $id += 1;
    print "INSERT INTO subshells VALUES(NULL, $state, $n, $l, $pop);\n";
    $sigmaL += $pop * $l;
  }
  my $parity = ($sigmaL % 2 == 0)? "even" : "odd";
 
  return ($label, $totalPop, $parity);
}


# Decodes the angular-momnentum quantum number from the 
# s(harp)-p(principal)-d(iffuse)-f(aint)-etc notation of letters.
sub lQn {
  my ($l) = @_;

  return 0 if $l eq "s";
  return 1 if $l eq "p";
  return 2 if $l eq "d";
  return 3 if $l eq "f";
  return 4 if $l eq "g";
  return 5 if $l eq "i";
  return 6 if $l eq "k";
  return 7 if $l eq "l";
  return 8 if $l eq "m";
  return 9 if $l eq "n";
} 
