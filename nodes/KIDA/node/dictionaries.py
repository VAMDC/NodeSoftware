# -*- coding: utf-8 -*-
"""
KidaNode dictionary definitions.
"""
RESTRICTABLES = {\
'AtomSymbol':'species__common_name',
'Inchi':'species__inchi',
'InchiKey':'species__inchi_key',
'IonCharge':'species__charge',
'MoleculeChemicalName': 'species__common_name',
'MoleculeStoichiometricFormula': 'species__formula',
'ParticleName': 'species__common_name',
                 
'FunctionID': 'function',

'MethodCategory': 'method__category',
                 
'SourceDOI': 'source__doi',
                 

'reactant0.InchiKey':'reactant__inchi_key',
'reactant0.Inchi':'reactant__inchi',
'reactant0.MoleculeChemicalName':'reactant__common_name',
'reactant0.MoleculeStoichiometricFormula':'reactant__formula',
'reactant0.AtomSymbol':'reactant__common_name',
'reactant0.ParticleName':'reactant__common_name',
'reactant0.IonCharge':'reactant__charge',

'reactant1.InchiKey':'reactant__inchi_key',
'reactant1.Inchi':'reactant__inchi',
'reactant1.MoleculeChemicalName':'reactant__common_name',
'reactant1.MoleculeStoichiometricFormula':'reactant__formula',
'reactant1.AtomSymbol':'reactant__common_name',
'reactant1.ParticleName':'reactant__common_name',
'reactant1.IonCharge':'reactant__charge',
                 

'product0.InchiKey':'product__inchi_key',
'product0.Inchi':'product__inchi',
'product0.MoleculeChemicalName':'product__common_name',
'product0.MoleculeStoichiometricFormula':'product__formula',
'product0.AtomSymbol':'product__common_name',
'product0.ParticleName':'product__common_name',
'product0.IonCharge':'reactant__charge',

'product1.InchiKey':'product__inchi_key',
'product1.Inchi':'product__inchi',
'product1.MoleculeChemicalName':'product__common_name',
'product1.MoleculeStoichiometricFormula':'product__formula',
'product1.AtomSymbol':'product__common_name',
'product1.ParticleName':'product__common_name',
'product1.IonCharge':'reactant__charge',

'product2.InchiKey':'product__inchi_key',
'product2.Inchi':'product__inchi',
'product2.MoleculeChemicalName':'product__common_name',
'product2.MoleculeStoichiometricFormula':'product__formula',
'product2.AtomSymbol':'product__common_name',
'product2.ParticleName':'product__common_name',
'product2.IonCharge':'reactant__charge',

'product3.InchiKey':'product__inchi_key',
'product3.Inchi':'product__inchi',
'product3.MoleculeChemicalName':'product__common_name',
'product3.MoleculeStoichiometricFormula':'product__formula',
'product3.AtomSymbol':'product__common_name',
'product3.ParticleName':'product__common_name',
'product3.IonCharge':'reactant__charge',
                 
}


RETURNABLES={\
'NodeID':'KIDA',
'AtomInchi':'Atom.Inchi',
'AtomInchiKey':'Atom.InchiKey',
'AtomSymbol':'Atom.Name',
'AtomSpeciesID':'Atom.SpeciesID',
'AtomIonCharge': 'Atom.Charge',
'AtomNuclearCharge':'Atom.atomic',
             
'MoleculeSpeciesID':'Molecule.id',
'MoleculeInChI':'Molecule.inchi',
'MoleculeInChIKey':'Molecule.inchi_key',
'MoleculeOrdinaryStructuralFormula':'Molecule.common_name',
'MoleculeStoichiometricFormula':'Molecule.formula',
'MoleculeCASRegistryNumber':'Molecule.cas',
'MoleculeChemicalName':'Molecule.description',
'MoleculeIonCharge':'Molecule.charge',

'ParticleCharge':'Particle.charge',
'ParticleName':'Particle.commonNameText()',
'ParticleSpeciesID':'Particle.id', 
             
 
'MethodCategory':'Method.category',
'MethodDescription':'Method.description',
'MethodID':'Method.id',
             

'FunctionID':'Function.id',
'FunctionName':'Function.Name',
'FunctionArgumentDescription':'FunctionArgument.description',
'FunctionArgumentName':'FunctionArgument.name',
'FunctionArgumentUnits':'FunctionArgument.units',
'FunctionParameterDescription':'FunctionParameter.description',
'FunctionParameterName':'FunctionParameter.name',
'FunctionParameterUnits':'FunctionParameter.units',
'FunctionComputerLanguage':'Function.computer_language',
'FunctionExpression':'Function.expression',
'FunctionYName':'Function.Y.name',
'FunctionYUnits':'Function.Y.units',

             
'SourceID':'Source.id',
'SourceAuthorName':'Source.main_author',
'SourcePageBegin':'Source.pagebegin',
'SourcePageEnd':'Source.pageend',
'SourceName':'Source.sourcename',
'SourceTitle':'Source.titleXML',
'SourceVolume':'Source.volume',
'SourceYear':'Source.year',
'SourceDOI':'Source.doi',
'SourceCategory':'Source.category',
             
         
'CollisionID' : 'CollTran.id',
'CollisionUserDefinition':'CollTran.reaction.type_channel.name',          
'CollisionReactantSpecies':'Reactant.id',
'CollisionProductSpecies':'Product.id',   
'CollisionDataSetDescription':'DataSet.description',   
             
'CollisionFitDataMethod':'FitData.method',
'CollisionFitDataAccuracy':'FitData.uncert',
'CollisionFitDataProductionDate':'FitData.date',
'CollisionFitDataFunction' : 'FitData.functionref',
'CollisionFitDataRef' : 'FitData.biblio',
'CollisionFitDataArgumentName' : 'Argument.name',
'CollisionFitDataArgumentUnits' : 'Argument.units',
'CollisionFitDataArgumentDescription' : 'Argument.description',
'CollisionFitDataArgumentLowerLimit' : 'Argument.tmin',
'CollisionFitDataArgumentUpperLimit' : 'Argument.tmax',
'CollisionFitDataParameter' : 'Parameter.parameter',
'CollisionFitDataParameterName' : 'Parameter.names',
'CollisionFitDataParameterUnit' : 'Parameter.units',
             

# ne fonctionne pas (pas dans les returnables de XSAMS)
'CollisionFitDataEval':'FitData.uncert',
'CollisionFitDataEvalRecommended':'FitData.uncert',
'CollisionFitDataEvalComment':'FitData.uncert',
             
}
