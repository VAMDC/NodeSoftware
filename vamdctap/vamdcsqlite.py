# -*- coding: utf-8 -*-

import uuid
import os

import logging
log=logging.getLogger('vamdc.tap')

import sqlite3


        
def generateSqlite(filePath, tap, HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None,
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
          
    conn = None
          
    try:
        log.debug('Connecting SQLite to %s...'%filePath)
        conn = sqlite3.connect(filePath)
        log.debug('...connected')
        c = conn.cursor()
        
        ATOMS_CREATE = '''CREATE TABLE Atoms(
            AtomSpeciesId INTEGER PRIMARY KEY,
            AtomSymbol CHAR(2),
            AtomNuclearCharge INTEGER,
            AtomIonCharge INTEGER,
            AtomInchi VARCHAR(64),
            AtomInchiKey VARCHAR(32))'''
        ATOMSTATE_CREATE = '''CREATE TABLE AtomicStates(
            AtomStateId INTEGER PRIMARY KEY, 
            AtomRef INTEGER REFERENCES Atoms(AtomSpeciesId),
            AtomStateTotalAngMom FLOAT, 
            AtomStateParity INTEGER, 
            AtomStateStatisticalWeight FLOAT,
            AtomStateEnergy DOUBLE PRECISION, 
            AtomStateDescription VARCHAR(128))'''
        RADTRANS_CREATE = '''CREATE TABLE RadTrans(
            RadTransId INTEGER PRIMARY KEY, 
            RadTransWavelength FLOAT,
            RadTransWavelengthMethod TEXT,
            RadTransProbabilityWeightedOscillatorStrength FLOAT,
            RadTransProbabilityA FLOAT,
            RadTRansLowerStateRef INTEGER REFERENCES AtomicStates(AtomStateId),
            RadTRansUpperStateRef INTEGER REFERENCES AtomicStates(AtomStateId))'''
        c.execute(ATOMS_CREATE)
        c.execute(ATOMSTATE_CREATE)
        c.execute(RADTRANS_CREATE)
        
        if Atoms:
            ATOMS_INSERT = ''' INSERT INTO Atoms(
                'AtomSpeciesId',
                'AtomSymbol',
                'AtomNuclearCharge',
                'AtomIonCharge',
                'AtomInchi',
                'AtomInchiKey')
                VALUES(?,?,?,?,?,?) '''
            for a in Atoms:
                #log.debug('Inserting atom %s'%str(a.id))
                c.execute(ATOMS_INSERT, (a.id, a.atomsymbol, a.atomnuclearcharge, a.atomioncharge, a.inchi, a.inchikey))
                ATOMSTATE_INSERT = ''' INSERT INTO AtomicStates(
                    'AtomStateId',
                    'AtomRef',
                    'AtomStateTotalAngMom',
                    'AtomStateParity',
                    'AtomStateStatisticalWeight',
                    'AtomStateEnergy',
                    'AtomStateDescription')
                    VALUES(?,?,?,?,?,?,?) '''
                if hasattr(a, 'States'):
                    for s in a.States.all().iterator():
                        #log.debug('Inserting state %s'%str(s.id))
                        c.execute(ATOMSTATE_INSERT,
                            (s.id, a.id, s.atomstatetotalangmom, s.parity, s.statisticalweight, s.energy, s.atomstateconfigurationlabel)
                        )
                conn.commit()
                #log.debug('Finished atoms and states')
       
        if RadTrans:
            RADTRANS_INSERT = '''INSERT INTO RadTrans(
                'RadTransId',
                'RadTransWavelength',
                'RadTransWavelengthMethod',
                'RadTransProbabilityWeightedOscillatorStrength',
                'RadTransProbabilityA',
                'RadTransLowerStateRef',
                'RadTransUpperStateRef')
                VALUES(?,?,?,?,?,?,?)'''
            for t in RadTrans.all().iterator():
                #log.debug('Inserting transition %s'%str(t.id))
                c.execute(RADTRANS_INSERT,
                    (t.id, t.bestWavelength(), t.bestWavelengthMethod(), t.weightedoscillatorstrength, t.probabilitya, t.lowerStateRef(), t.upperStateRef())
                )
            conn.commit()
            
    finally:
        if conn:
            conn.close()

