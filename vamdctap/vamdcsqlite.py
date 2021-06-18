# -*- coding: utf-8 -*-

import uuid
import os

import logging
log=logging.getLogger('vamdc.tap')

import sqlite3


        
def generateSqlite(filePath, tap, HeaderInfo=None, Sources=None, Methods=None, Functions=None,
          Environments=None, Atoms=None, Molecules=None, Solids=None, Particles=None,
          CollTrans=None, RadTrans=None, RadCross=None, NonRadTrans=None):
          
    try:
        log.debug('Connecting SQLite to %s...'%filePath)
        conn = sqlite3.connect(filePath)
        log.debug('...connected')
        ATOMS_FIELDS = [
            'AtomSpeciesId',
            'AtomSymbol',
            'AtomNuclearCharge',
            'AtomIonCharge',
            'AtomInchi',
            'AtomInchiKey',
        ]
        ATOMS_CREATE = 'CREATE TABLE Atoms(AtomSpeciesId INTEGER PRIMARY KEY, AtomSymbol CHAR(2), AtomNuclearCharge INTEGER, AtomIonCharge INTEGER, AtomInchi VARCHAR(64), AtomInchiKey VARCHAR(32))'
        if Atoms:
            c = conn.cursor()
            c.execute(ATOMS_CREATE)
            ATOMS_INSERT = ''' INSERT INTO Atoms(
                'AtomSpeciesId',
                'AtomSymbol',
                'AtomNuclearCharge',
                'AtomIonCharge',
                'AtomInchi',
                'AtomInchiKey')
                VALUES(?,?,?,?,?,?) '''
            for a in Atoms:
                c.execute(ATOMS_INSERT, (a.id, a.atomsymbol, a.atomnuclearcharge, a.atomioncharge, a.inchi, a.inchikey))
            conn.commit()
            
        ATOMSTATE_FIELDS = [
            'AtomStateId',
            'AtomRef',
            'AtomStateTotalAngMom',
            'AtomStateParity',
            'AtomStateStatisticalWeight',
            'AtomStateEnergy',
            'AtomStateDescription'
        ]    
        ATOMSTATE_CREATE = '''CREATE TABLE AtomicStates(
            AtomStateId INTEGER PRIMARY KEY, 
            AtomRef INTEGER REFERENCES Atoms(AtomSpeciesId),
            AtomStateTotalAngMom FLOAT, 
            AtomStateParity INTEGER, 
            AtomStateStatisticalWeight FLOAT,
            AtomStateEnergy DOUBLE PRECISION, 
            AtomStateDescription VARCHAR(128))'''
        c.execute(ATOMSTATE_CREATE)
        if Atoms:
            ATOMSTATE_INSERT = ''' INSERT INTO AtomicStates(
                'AtomStateId',
                'AtomRef',
                'AtomStateTotalAngMom',
                'AtomStateParity',
                'AtomStateStatisticalWeight',
                'AtomStateEnergy',
                'AtomStateDescription')
                VALUES(?,?,?,?,?,?,?) '''
            for a in Atoms:
                if not hasattr(a,'States'):
                    a.States = []
                for s in a.States:
                    c.execute(ATOMSTATE_INSERT,
                        (s.id, a.id, s.atomstatetotalangmom, s.parity, s.statisticalweight, s.energy, s.atomstateconfigurationlabel)
                    )
                conn.commit()
        RADTRANS_FIELDS = [
            'RadTransID',
            'RadTransWavelength',
            'RadTransWavelengthMethod',
            'RadTransProbabilityWeightedOscillatorStrength',
            'RadTransProbabilityA',
            'RadTransLowerStateRef',
            'RadTransUpperStateRef'
        ]
        RADTRANS_CREATE = '''CREATE TABLE RadTrans(
            RadTransId INTEGER PRIMARY KEY, 
            RadTransWavelength FLOAT,
            RadTransWavelengthMethod TEXT,
            RadTransProbabilityWeightedOscillatorStrength FLOAT,
            RadTransProbabilityA FLOAT,
            RadTRansLowerStateRef INTEGER REFERENCES AtomicStates(AtomStateId),
            RadTRansUpperStateRef INTEGER REFERENCES AtomicStates(AtomStateId)
        )'''
        c.execute(RADTRANS_CREATE)
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
            for t in RadTrans:
                c.execute(RADTRANS_INSERT,
                    (t.id, t.bestWavelength(), t.bestWavelengthMethod(), t.weightedoscillatorstrength, t.probabilitya, t.lowerStateRef(), t.upperStateRef())
                )
            conn.commit()
            
    finally:
        if conn:
            conn.close()

