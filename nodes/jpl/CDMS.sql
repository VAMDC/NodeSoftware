-- phpMyAdmin SQL Dump
-- version 3.3.2deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 26. September 2011 um 19:17
-- Server Version: 5.1.41
-- PHP-Version: 5.3.2-1ubuntu4.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `CDMS`
--

-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_Energies`
--
DROP VIEW IF EXISTS `V_Energies`;
CREATE TABLE IF NOT EXISTS `V_Energies` (
`M_ID` int(11)
,`M_Name` varchar(200)
,`M_Symbol` varchar(250)
,`M_CAS` varchar(20)
,`M_StoichiometricFormula` varchar(200)
,`M_TrivialName` varchar(200)
,`M_Comment` longtext
,`E_ID` int(11)
,`E_M_ID` int(11)
,`E_TAG` int(11)
,`E_Name` varchar(200)
,`E_Isotopomer` varchar(100)
,`E_States` varchar(200)
,`E_Comment` longtext
,`EGY_ID` int(8)
,`EGY_E_ID` int(5)
,`EGY_E_Tag` int(10)
,`EGY_DAT_ID` int(11)
,`EGY_Energy` double
,`EGY_Uncertainty` double
,`EGY_PMIX` double
,`EGY_IBLK` int(5)
,`EGY_INDX` int(5)
,`EGY_IDGN` int(6)
,`EGY_QN1` int(4)
,`EGY_QN2` int(4)
,`EGY_QN3` int(4)
,`EGY_QN4` int(4)
,`EGY_QN5` int(4)
,`EGY_QN6` int(4)
,`EGY_User` varchar(40)
,`EGY_TIMESTAMP` date
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_ExpLinesPer100GHz`
--
DROP VIEW IF EXISTS `V_ExpLinesPer100GHz`;
CREATE TABLE IF NOT EXISTS `V_ExpLinesPer100GHz` (
`VEL_Origin_ID` int(5)
,`VEL_100GHz_Group` double(17,0)
,`VEL_Count` bigint(21)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_MolQN`
--
DROP VIEW IF EXISTS `V_MolQN`;
CREATE TABLE IF NOT EXISTS `V_MolQN` (
`Id` int(11)
,`StateID` int(8)
,`Case` varchar(20)
,`Label` varchar(100)
,`Value` varbinary(300)
,`SpinRef` varchar(10)
,`Attribute` varchar(20)
,`Order` int(11)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_MolstateQN`
--
DROP VIEW IF EXISTS `V_MolstateQN`;
CREATE TABLE IF NOT EXISTS `V_MolstateQN` (
`Id` int(11)
,`StateID` int(8)
,`Case` varchar(20)
,`Label` varchar(100)
,`Value` varbinary(300)
,`SpinRef` varchar(10)
,`Attribute` varchar(20)
,`Order` int(11)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_PredictionsWithEnergies`
--
DROP VIEW IF EXISTS `V_PredictionsWithEnergies`;
CREATE TABLE IF NOT EXISTS `V_PredictionsWithEnergies` (
`E_ID` int(11)
,`E_M_ID` int(11)
,`P_ID` bigint(8)
,`P_Frequency` double
,`P_Intensity` double
,`P_Energy_Lower` double
,`P_Uncertainty` double
,`P_Upper_State_Degeneracy` int(5)
,`P_QN_Up_1` int(4)
,`P_QN_Up_2` int(4)
,`P_QN_Up_3` int(4)
,`P_QN_Up_4` int(4)
,`P_QN_Up_5` int(4)
,`P_QN_Up_6` int(4)
,`P_QN_Low_1` int(4)
,`P_QN_Low_2` int(4)
,`P_QN_Low_3` int(4)
,`P_QN_Low_4` int(4)
,`P_QN_Low_5` int(4)
,`P_QN_Low_6` int(4)
,`EGY_Up_ID` int(8)
,`EGY_Up_Energy` double
,`EGY_Up_PMix` double
,`EGY_Up_Uncertainty` double
,`EGY_Up_IDGN` int(6)
,`EGY_Low_ID` int(8)
,`EGY_Low_Energy` double
,`EGY_Low_PMix` double
,`EGY_Low_Uncertainty` double
,`EGY_Low_IDGN` int(6)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_Predictions_XSAMS`
--
DROP VIEW IF EXISTS `V_Predictions_XSAMS`;
CREATE TABLE IF NOT EXISTS `V_Predictions_XSAMS` (
`M_ID` int(11)
,`E_ID` int(11)
,`E_Tag` int(11)
,`M_Name` varchar(200)
,`M_TrivialName` varchar(200)
,`E_Name` varchar(200)
,`E_Isotopomer` varchar(100)
,`E_States` varchar(200)
,`P_ID` bigint(8)
,`P_Frequency` double
,`P_Intensity` double
,`P_Energy_Lower` double
,`P_Uncertainty` double
,`P_Upper_State_Degeneracy` int(5)
,`P_QN_TAG` int(10)
,`P_QN_Up_1` int(4)
,`P_QN_Up_2` int(4)
,`P_QN_Up_3` int(4)
,`P_QN_Up_4` int(4)
,`P_QN_Up_5` int(4)
,`P_QN_Up_6` int(4)
,`P_QN_Low_1` int(4)
,`P_QN_Low_2` int(4)
,`P_QN_Low_3` int(4)
,`P_QN_Low_4` int(4)
,`P_QN_Low_5` int(4)
,`P_QN_Low_6` int(4)
,`EGY_UpId` int(11)
,`EGY_LowId` int(11)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_RadiativeTransitions`
--
DROP VIEW IF EXISTS `V_RadiativeTransitions`;
CREATE TABLE IF NOT EXISTS `V_RadiativeTransitions` (
`Resource` varchar(4)
,`RadiativeTransitionID` bigint(8)
,`MoleculeID` int(11)
,`ChemicalName` varchar(200)
,`MolecularChemicalSpecies` varchar(200)
,`Isotopomer` varchar(100)
,`EnergyWavelength` varchar(9)
,`WavelengthWavenumber` varchar(11)
,`FrequencyValue` double
,`FrequencyUnit` varchar(3)
,`EnergyWavelengthAccuracy` double
,`Multipole` varchar(2)
,`Log10WeightedOscillatorStrengthValue` double
,`Log10WeightedOscillatorStrengthUnit` varchar(8)
,`LowerStateEnergyValue` double
,`LowerStateEnergyUnit` varchar(4)
,`UpperStateNuclearStatisticalWeight` int(5)
,`InitialStateRef` int(11)
,`FinalStateRef` int(11)
,`CaseQN` int(10)
,`QN_Up_1` int(4)
,`QN_Up_2` int(4)
,`QN_Up_3` int(4)
,`QN_Up_4` int(4)
,`QN_Up_5` int(4)
,`QN_Up_6` int(4)
,`QN_Low_1` int(4)
,`QN_Low_2` int(4)
,`QN_Low_3` int(4)
,`QN_Low_4` int(4)
,`QN_Low_5` int(4)
,`QN_Low_6` int(4)
,`E_ID` int(11)
,`E_Tag` int(11)
,`E_States` varchar(200)
,`E_Name` varchar(200)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_RadiativeTransitions2`
--
DROP VIEW IF EXISTS `V_RadiativeTransitions2`;
CREATE TABLE IF NOT EXISTS `V_RadiativeTransitions2` (
`Resource` varchar(4)
,`RadTransComments` char(0)
,`RadTransMethodRef` char(0)
,`RadiativeTransitionID` bigint(8)
,`MoleculeID` int(11)
,`ChemicalName` varchar(200)
,`MolecularChemicalSpecies` varchar(200)
,`Isotopomer` varchar(100)
,`RadTransFrequencyTheoreticalComments` char(0)
,`RadTransFrequencyTheoreticalSourceRef` char(0)
,`RadTransFrequencyTheoreticalValue` double
,`RadTransFrequencyTheoreticalUnits` varchar(3)
,`RadTransFrequencyTheoreticalAccuracy` double
,`RadTransProbabilityProbabilityMultipoleValue` varchar(2)
,`RadTransProbabilityWeightedOscillatorStrengthComments` char(0)
,`RadTransProbabilityWeightedOscillatorStrengthSourceRef` char(0)
,`RadTransProbabilityWeightedOscillatorStrengthMethodRef` char(0)
,`RadTransProbabilityWeightedOscillatorStrengthValue` char(0)
,`RadTransProbabilityWeightedOscillatorStrengthUnits` char(0)
,`RadTransProbabilityWeightedOscillatorStrengthAccuracy` char(0)
,`RadTransProbabilityLog10WeightedOscillatorStrengthComments` char(0)
,`RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef` char(0)
,`RadTransProbabilityLog10WeightedOscillatorStrengthMethodRef` char(0)
,`RadTransProbabilityLog10WeightedOscillatorStrengthValue` double
,`RadTransProbabilityLog10WeightedOscillatorStrengthUnits` varchar(8)
,`RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy` char(0)
,`LowerStateEnergyValue` double
,`LowerStateEnergyUnit` varchar(4)
,`UpperStateNuclearStatisticalWeight` int(5)
,`RadTransInitialStateRef` int(11)
,`RadTransFinalStateRef` int(11)
,`CaseQN` int(10)
,`QN_Up_1` int(4)
,`QN_Up_2` int(4)
,`QN_Up_3` int(4)
,`QN_Up_4` int(4)
,`QN_Up_5` int(4)
,`QN_Up_6` int(4)
,`QN_Low_1` int(4)
,`QN_Low_2` int(4)
,`QN_Low_3` int(4)
,`QN_Low_4` int(4)
,`QN_Low_5` int(4)
,`QN_Low_6` int(4)
,`E_ID` int(11)
,`E_Tag` int(11)
,`E_States` varchar(200)
,`E_Name` varchar(200)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_StatesIVOA`
--
DROP VIEW IF EXISTS `V_StatesIVOA`;
CREATE TABLE IF NOT EXISTS `V_StatesIVOA` (
`EGY_ID` int(8)
,`EGY_E_ID` int(5)
,`EGY_E_Tag` int(10)
,`EGY_DAT_ID` int(11)
,`EGY_Energy` double
,`EGY_Uncertainty` double
,`EGY_PMIX` double
,`EGY_IBLK` int(5)
,`EGY_INDX` int(5)
,`EGY_IDGN` int(6)
,`EGY_QN1` int(4)
,`EGY_QN2` int(4)
,`EGY_QN3` int(4)
,`EGY_QN4` int(4)
,`EGY_QN5` int(4)
,`EGY_QN6` int(4)
,`EGY_User` varchar(40)
,`EGY_TIMESTAMP` date
,`QN_ID` int(11)
,`QN_E_ID` int(11)
,`QN_DAT_ID` int(11)
,`QN_P_ID` int(11)
,`QN_F_ID` int(11)
,`QN_EGY_ID` int(11)
,`QN_1` int(11)
,`QN_2` int(11)
,`QN_3` int(11)
,`QN_4` int(11)
,`QN_5` int(11)
,`QN_6` int(11)
,`QN_label` varchar(10)
,`QN_type` varchar(50)
,`QN_Path` varchar(500)
,`QN_NumeratorValue` int(11)
,`QN_DenominatorValue` double
,`QN_StringValue` varchar(100)
,`QN_Description` text
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_StatesMolecules`
--
DROP VIEW IF EXISTS `V_StatesMolecules`;
CREATE TABLE IF NOT EXISTS `V_StatesMolecules` (
`Resource` varchar(4)
,`StateID` int(8)
,`MoleculeID` int(11)
,`ChemicalName` varchar(200)
,`MolecularChemicalSpecies` varchar(200)
,`Isotopomer` varchar(100)
,`StateEnergyValue` double
,`StateEnergyUnit` varchar(4)
,`StateEnergyAccuracy` double
,`MixingCoefficient` double
,`StateNuclearStatisticalWeight` int(6)
,`QN_String` varchar(500)
,`EGY_QN_Tag` int(6)
,`EGY_QN1` int(4)
,`EGY_QN2` int(4)
,`EGY_QN3` int(4)
,`EGY_QN4` int(4)
,`EGY_QN5` int(4)
,`EGY_QN6` int(4)
,`E_ID` int(11)
,`EGY_DAT_ID` int(11)
,`E_Tag` int(11)
);
-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `V_States_XSAMS`
--
DROP VIEW IF EXISTS `V_States_XSAMS`;
CREATE TABLE IF NOT EXISTS `V_States_XSAMS` (
`M_ID` int(11)
,`E_ID` int(11)
,`EGY_ID` int(8)
,`EGY_DAT_ID` int(11)
,`E_Tag` int(11)
,`M_TrivialName` varchar(200)
,`E_Name` varchar(200)
,`E_Isotopomer` varchar(100)
,`E_States` varchar(200)
,`EGY_Energy` double
,`EGY_Uncertainty` double
,`EGY_PMIX` double
,`EGY_IDGN` int(6)
,`EGY_QN_Tag` int(6)
,`EGY_QN1` int(4)
,`EGY_QN2` int(4)
,`EGY_QN3` int(4)
,`EGY_QN4` int(4)
,`EGY_QN5` int(4)
,`EGY_QN6` int(4)
,`QN_String` varchar(500)
);
-- --------------------------------------------------------

--
-- Struktur des Views `V_Energies`
--
DROP TABLE IF EXISTS `V_Energies`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_Energies` AS select `Molecules`.`M_ID` AS `M_ID`,`Molecules`.`M_Name` AS `M_Name`,`Molecules`.`M_Symbol` AS `M_Symbol`,`Molecules`.`M_CAS` AS `M_CAS`,`Molecules`.`M_StoichiometricFormula` AS `M_StoichiometricFormula`,`Molecules`.`M_TrivialName` AS `M_TrivialName`,`Molecules`.`M_Comment` AS `M_Comment`,`Entries`.`E_ID` AS `E_ID`,`Entries`.`E_M_ID` AS `E_M_ID`,`Entries`.`E_TAG` AS `E_TAG`,`Entries`.`E_Name` AS `E_Name`,`Entries`.`E_Isotopomer` AS `E_Isotopomer`,`Entries`.`E_States` AS `E_States`,`Entries`.`E_Comment` AS `E_Comment`,`Energies`.`EGY_ID` AS `EGY_ID`,`Energies`.`EGY_E_ID` AS `EGY_E_ID`,`Energies`.`EGY_E_Tag` AS `EGY_E_Tag`,`Energies`.`EGY_DAT_ID` AS `EGY_DAT_ID`,`Energies`.`EGY_Energy` AS `EGY_Energy`,`Energies`.`EGY_Uncertainty` AS `EGY_Uncertainty`,`Energies`.`EGY_PMIX` AS `EGY_PMIX`,`Energies`.`EGY_IBLK` AS `EGY_IBLK`,`Energies`.`EGY_INDX` AS `EGY_INDX`,`Energies`.`EGY_IDGN` AS `EGY_IDGN`,`Energies`.`EGY_QN1` AS `EGY_QN1`,`Energies`.`EGY_QN2` AS `EGY_QN2`,`Energies`.`EGY_QN3` AS `EGY_QN3`,`Energies`.`EGY_QN4` AS `EGY_QN4`,`Energies`.`EGY_QN5` AS `EGY_QN5`,`Energies`.`EGY_QN6` AS `EGY_QN6`,`Energies`.`EGY_User` AS `EGY_User`,`Energies`.`EGY_TIMESTAMP` AS `EGY_TIMESTAMP` from ((`Molecules` join `Entries` on((`Molecules`.`M_ID` = `Entries`.`E_M_ID`))) left join `Energies` on((`Energies`.`EGY_E_ID` = `Entries`.`E_ID`)));

-- --------------------------------------------------------

--
-- Struktur des Views `V_ExpLinesPer100GHz`
--
DROP TABLE IF EXISTS `V_ExpLinesPer100GHz`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_ExpLinesPer100GHz` AS select distinct `Vorhersagen`.`V_Origin_Id` AS `VEL_Origin_ID`,ceiling((`Vorhersagen`.`V_Frequency_Exp` / 100000)) AS `VEL_100GHz_Group`,count(`Vorhersagen`.`V_ID`) AS `VEL_Count` from `Vorhersagen` where (`Vorhersagen`.`V_Frequency_Exp` is not null) group by ceiling((`Vorhersagen`.`V_Frequency_Exp` / 100000)),`Vorhersagen`.`V_Origin_Id`;

-- --------------------------------------------------------

--
-- Struktur des Views `V_MolQN`
--
DROP TABLE IF EXISTS `V_MolQN`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_MolQN` AS select `StateQNXsams`.`SQN_ID` AS `Id`,`EnergiesTMP`.`EGY_ID` AS `StateID`,`StateQNXsams`.`SQN_Case` AS `Case`,`StateQNXsams`.`SQN_Label` AS `Label`,ifnull(`StateQNXsams`.`SQN_ValueFloat`,ifnull(`StateQNXsams`.`SQN_ValueString`,ifnull(`F_ReturnQNColumnValue`(`EnergiesTMP`.`EGY_QN1`,`EnergiesTMP`.`EGY_QN2`,`EnergiesTMP`.`EGY_QN3`,`EnergiesTMP`.`EGY_QN4`,`EnergiesTMP`.`EGY_QN5`,`EnergiesTMP`.`EGY_QN6`,`StateQNXsams`.`SQN_ColumnValue`,`StateQNXsams`.`SQN_ColumnValueFunction`),NULL))) AS `Value`,`StateQNXsams`.`SQN_SpinRef` AS `SpinRef`,`StateQNXsams`.`SQN_Attribute` AS `Attribute`,`StateQNXsams`.`SQN_Order` AS `Order` from (`EnergiesTMP` join `StateQNXsams`) where ((`StateQNXsams`.`SQN_E_ID` = `EnergiesTMP`.`EGY_E_ID`) and (`StateQNXsams`.`SQN_QN_Tag` = `EnergiesTMP`.`EGY_QN_Tag`) and (`EnergiesTMP`.`EGY_QN1` <=> ifnull(`StateQNXsams`.`SQN_QN1`,`EnergiesTMP`.`EGY_QN1`)) and (`EnergiesTMP`.`EGY_QN2` <=> ifnull(`StateQNXsams`.`SQN_QN2`,`EnergiesTMP`.`EGY_QN2`)) and (`EnergiesTMP`.`EGY_QN3` <=> ifnull(`StateQNXsams`.`SQN_QN3`,`EnergiesTMP`.`EGY_QN3`)) and (`EnergiesTMP`.`EGY_QN4` <=> ifnull(`StateQNXsams`.`SQN_QN4`,`EnergiesTMP`.`EGY_QN4`)) and (`EnergiesTMP`.`EGY_QN5` <=> ifnull(`StateQNXsams`.`SQN_QN5`,`EnergiesTMP`.`EGY_QN5`)) and (`EnergiesTMP`.`EGY_QN6` <=> ifnull(`StateQNXsams`.`SQN_QN6`,`EnergiesTMP`.`EGY_QN6`))) order by `EnergiesTMP`.`EGY_ID`,`StateQNXsams`.`SQN_Order`,`StateQNXsams`.`SQN_Attribute`;

-- --------------------------------------------------------

--
-- Struktur des Views `V_MolstateQN`
--
DROP TABLE IF EXISTS `V_MolstateQN`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_MolstateQN` AS select `StateQNXsams`.`SQN_ID` AS `Id`,`Energies`.`EGY_ID` AS `StateID`,`StateQNXsams`.`SQN_Case` AS `Case`,`StateQNXsams`.`SQN_Label` AS `Label`,ifnull(`StateQNXsams`.`SQN_ValueFloat`,ifnull(`StateQNXsams`.`SQN_ValueString`,ifnull(`F_ReturnQNColumnValue`(`Energies`.`EGY_QN1`,`Energies`.`EGY_QN2`,`Energies`.`EGY_QN3`,`Energies`.`EGY_QN4`,`Energies`.`EGY_QN5`,`Energies`.`EGY_QN6`,`StateQNXsams`.`SQN_ColumnValue`,`StateQNXsams`.`SQN_ColumnValueFunction`),NULL))) AS `Value`,`StateQNXsams`.`SQN_SpinRef` AS `SpinRef`,`StateQNXsams`.`SQN_Attribute` AS `Attribute`,`StateQNXsams`.`SQN_Order` AS `Order` from (`Energies` join `StateQNXsams` on(((`StateQNXsams`.`SQN_E_ID` = `Energies`.`EGY_E_ID`) and (`StateQNXsams`.`SQN_QN_Tag` = `Energies`.`EGY_QN_Tag`) and (`Energies`.`EGY_QN1` <=> ifnull(`StateQNXsams`.`SQN_QN1`,`Energies`.`EGY_QN1`)) and (`Energies`.`EGY_QN2` <=> ifnull(`StateQNXsams`.`SQN_QN2`,`Energies`.`EGY_QN2`)) and (`Energies`.`EGY_QN3` <=> ifnull(`StateQNXsams`.`SQN_QN3`,`Energies`.`EGY_QN3`)) and (`Energies`.`EGY_QN4` <=> ifnull(`StateQNXsams`.`SQN_QN4`,`Energies`.`EGY_QN4`)) and (`Energies`.`EGY_QN5` <=> ifnull(`StateQNXsams`.`SQN_QN5`,`Energies`.`EGY_QN5`)) and (`Energies`.`EGY_QN6` <=> ifnull(`StateQNXsams`.`SQN_QN6`,`Energies`.`EGY_QN6`))))) order by `Energies`.`EGY_ID`,`StateQNXsams`.`SQN_Order`,`StateQNXsams`.`SQN_Attribute`;

-- --------------------------------------------------------

--
-- Struktur des Views `V_PredictionsWithEnergies`
--
DROP TABLE IF EXISTS `V_PredictionsWithEnergies`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_PredictionsWithEnergies` AS select `Entries`.`E_ID` AS `E_ID`,`Entries`.`E_M_ID` AS `E_M_ID`,`Predictions`.`P_ID` AS `P_ID`,`Predictions`.`P_Frequency` AS `P_Frequency`,`Predictions`.`P_Intensity` AS `P_Intensity`,`Predictions`.`P_Energy_Lower` AS `P_Energy_Lower`,`Predictions`.`P_Uncertainty` AS `P_Uncertainty`,`Predictions`.`P_Upper_State_Degeneracy` AS `P_Upper_State_Degeneracy`,`Predictions`.`P_QN_Up_1` AS `P_QN_Up_1`,`Predictions`.`P_QN_Up_2` AS `P_QN_Up_2`,`Predictions`.`P_QN_Up_3` AS `P_QN_Up_3`,`Predictions`.`P_QN_Up_4` AS `P_QN_Up_4`,`Predictions`.`P_QN_Up_5` AS `P_QN_Up_5`,`Predictions`.`P_QN_Up_6` AS `P_QN_Up_6`,`Predictions`.`P_QN_Low_1` AS `P_QN_Low_1`,`Predictions`.`P_QN_Low_2` AS `P_QN_Low_2`,`Predictions`.`P_QN_Low_3` AS `P_QN_Low_3`,`Predictions`.`P_QN_Low_4` AS `P_QN_Low_4`,`Predictions`.`P_QN_Low_5` AS `P_QN_Low_5`,`Predictions`.`P_QN_Low_6` AS `P_QN_Low_6`,`EGY_Up`.`EGY_ID` AS `EGY_Up_ID`,`EGY_Up`.`EGY_Energy` AS `EGY_Up_Energy`,`EGY_Up`.`EGY_PMIX` AS `EGY_Up_PMix`,`EGY_Up`.`EGY_Uncertainty` AS `EGY_Up_Uncertainty`,`EGY_Up`.`EGY_IDGN` AS `EGY_Up_IDGN`,`EGY_Low`.`EGY_ID` AS `EGY_Low_ID`,`EGY_Low`.`EGY_Energy` AS `EGY_Low_Energy`,`EGY_Low`.`EGY_PMIX` AS `EGY_Low_PMix`,`EGY_Low`.`EGY_Uncertainty` AS `EGY_Low_Uncertainty`,`EGY_Low`.`EGY_IDGN` AS `EGY_Low_IDGN` from (((`Entries` join `Predictions` on((`Predictions`.`P_E_ID` = `Entries`.`E_ID`))) left join `Energies` `EGY_Up` on(((`Predictions`.`P_E_ID` = `EGY_Up`.`EGY_E_ID`) and (`Predictions`.`P_QN_Up_1` <=> `EGY_Up`.`EGY_QN1`) and (`Predictions`.`P_QN_Up_2` <=> `EGY_Up`.`EGY_QN2`) and (`Predictions`.`P_QN_Up_3` <=> `EGY_Up`.`EGY_QN3`) and (`Predictions`.`P_QN_Up_4` <=> `EGY_Up`.`EGY_QN4`) and (`Predictions`.`P_QN_Up_5` <=> `EGY_Up`.`EGY_QN5`) and (`Predictions`.`P_QN_Up_6` <=> `EGY_Up`.`EGY_QN6`)))) left join `Energies` `EGY_Low` on(((`Predictions`.`P_E_ID` = `EGY_Low`.`EGY_E_ID`) and (`Predictions`.`P_QN_Low_1` <=> `EGY_Low`.`EGY_QN1`) and (`Predictions`.`P_QN_Low_2` <=> `EGY_Low`.`EGY_QN2`) and (`Predictions`.`P_QN_Low_3` <=> `EGY_Low`.`EGY_QN3`) and (`Predictions`.`P_QN_Low_4` <=> `EGY_Low`.`EGY_QN4`) and (`Predictions`.`P_QN_Low_5` <=> `EGY_Low`.`EGY_QN5`) and (`Predictions`.`P_QN_Low_6` <=> `EGY_Low`.`EGY_QN6`)))) where (ifnull(`Predictions`.`P_Origin_Id`,0) <> 1);

-- --------------------------------------------------------

--
-- Struktur des Views `V_Predictions_XSAMS`
--
DROP TABLE IF EXISTS `V_Predictions_XSAMS`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_Predictions_XSAMS` AS select `Molecules`.`M_ID` AS `M_ID`,`Entries`.`E_ID` AS `E_ID`,`Entries`.`E_TAG` AS `E_Tag`,`Molecules`.`M_Name` AS `M_Name`,`Molecules`.`M_TrivialName` AS `M_TrivialName`,`Entries`.`E_Name` AS `E_Name`,`Entries`.`E_Isotopomer` AS `E_Isotopomer`,`Entries`.`E_States` AS `E_States`,`Predictions`.`P_ID` AS `P_ID`,`Predictions`.`P_Frequency` AS `P_Frequency`,`Predictions`.`P_Intensity` AS `P_Intensity`,`Predictions`.`P_Energy_Lower` AS `P_Energy_Lower`,`Predictions`.`P_Uncertainty` AS `P_Uncertainty`,`Predictions`.`P_Upper_State_Degeneracy` AS `P_Upper_State_Degeneracy`,`Predictions`.`P_QN_TAG` AS `P_QN_TAG`,`Predictions`.`P_QN_Up_1` AS `P_QN_Up_1`,`Predictions`.`P_QN_Up_2` AS `P_QN_Up_2`,`Predictions`.`P_QN_Up_3` AS `P_QN_Up_3`,`Predictions`.`P_QN_Up_4` AS `P_QN_Up_4`,`Predictions`.`P_QN_Up_5` AS `P_QN_Up_5`,`Predictions`.`P_QN_Up_6` AS `P_QN_Up_6`,`Predictions`.`P_QN_Low_1` AS `P_QN_Low_1`,`Predictions`.`P_QN_Low_2` AS `P_QN_Low_2`,`Predictions`.`P_QN_Low_3` AS `P_QN_Low_3`,`Predictions`.`P_QN_Low_4` AS `P_QN_Low_4`,`Predictions`.`P_QN_Low_5` AS `P_QN_Low_5`,`Predictions`.`P_QN_Low_6` AS `P_QN_Low_6`,`F_GetEnergy`(`Predictions`.`P_E_ID`,`Predictions`.`P_QN_TAG`,`Predictions`.`P_QN_Up_1`,`Predictions`.`P_QN_Up_2`,`Predictions`.`P_QN_Up_3`,`Predictions`.`P_QN_Up_4`,`Predictions`.`P_QN_Up_5`,`Predictions`.`P_QN_Up_6`) AS `EGY_UpId`,`F_GetEnergy`(`Predictions`.`P_E_ID`,`Predictions`.`P_QN_TAG`,`Predictions`.`P_QN_Low_1`,`Predictions`.`P_QN_Low_2`,`Predictions`.`P_QN_Low_3`,`Predictions`.`P_QN_Low_4`,`Predictions`.`P_QN_Low_5`,`Predictions`.`P_QN_Low_6`) AS `EGY_LowId` from ((`Molecules` join `Entries` on((`Molecules`.`M_ID` = `Entries`.`E_M_ID`))) join `Predictions` on((`Predictions`.`P_E_ID` = `Entries`.`E_ID`))) where ((`Entries`.`E_Origin` = 5) and (ifnull(`Predictions`.`P_Origin_Id`,0) <> 1) and (`Predictions`.`P_Archive` = 0)) order by `Molecules`.`M_ID`,`Entries`.`E_ID`,`Predictions`.`P_ID`;

-- --------------------------------------------------------

--
-- Struktur des Views `V_RadiativeTransitions`
--
DROP TABLE IF EXISTS `V_RadiativeTransitions`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_RadiativeTransitions` AS select 'CDMS' AS `Resource`,`Predictions`.`P_ID` AS `RadiativeTransitionID`,`Molecules`.`M_ID` AS `MoleculeID`,`Molecules`.`M_TrivialName` AS `ChemicalName`,`Molecules`.`M_Name` AS `MolecularChemicalSpecies`,`Entries`.`E_Isotopomer` AS `Isotopomer`,'Frequency' AS `EnergyWavelength`,'Theoretical' AS `WavelengthWavenumber`,`Predictions`.`P_Frequency` AS `FrequencyValue`,'MHz' AS `FrequencyUnit`,`Predictions`.`P_Uncertainty` AS `EnergyWavelengthAccuracy`,'E2' AS `Multipole`,`Predictions`.`P_Intensity` AS `Log10WeightedOscillatorStrengthValue`,'nm^2 MHz' AS `Log10WeightedOscillatorStrengthUnit`,`Predictions`.`P_Energy_Lower` AS `LowerStateEnergyValue`,'cm-1' AS `LowerStateEnergyUnit`,`Predictions`.`P_Upper_State_Degeneracy` AS `UpperStateNuclearStatisticalWeight`,`F_GetEnergy2`(`Predictions`.`P_E_ID`,`Predictions`.`P_QN_TAG`,`Predictions`.`P_QN_Up_1`,`Predictions`.`P_QN_Up_2`,`Predictions`.`P_QN_Up_3`,`Predictions`.`P_QN_Up_4`,`Predictions`.`P_QN_Up_5`,`Predictions`.`P_QN_Up_6`) AS `InitialStateRef`,`F_GetEnergy2`(`Predictions`.`P_E_ID`,`Predictions`.`P_QN_TAG`,`Predictions`.`P_QN_Low_1`,`Predictions`.`P_QN_Low_2`,`Predictions`.`P_QN_Low_3`,`Predictions`.`P_QN_Low_4`,`Predictions`.`P_QN_Low_5`,`Predictions`.`P_QN_Low_6`) AS `FinalStateRef`,`Predictions`.`P_QN_TAG` AS `CaseQN`,`Predictions`.`P_QN_Up_1` AS `QN_Up_1`,`Predictions`.`P_QN_Up_2` AS `QN_Up_2`,`Predictions`.`P_QN_Up_3` AS `QN_Up_3`,`Predictions`.`P_QN_Up_4` AS `QN_Up_4`,`Predictions`.`P_QN_Up_5` AS `QN_Up_5`,`Predictions`.`P_QN_Up_6` AS `QN_Up_6`,`Predictions`.`P_QN_Low_1` AS `QN_Low_1`,`Predictions`.`P_QN_Low_2` AS `QN_Low_2`,`Predictions`.`P_QN_Low_3` AS `QN_Low_3`,`Predictions`.`P_QN_Low_4` AS `QN_Low_4`,`Predictions`.`P_QN_Low_5` AS `QN_Low_5`,`Predictions`.`P_QN_Low_6` AS `QN_Low_6`,`Entries`.`E_ID` AS `E_ID`,`Entries`.`E_TAG` AS `E_Tag`,`Entries`.`E_States` AS `E_States`,`Entries`.`E_Name` AS `E_Name` from ((`Molecules` join `Entries` on((`Molecules`.`M_ID` = `Entries`.`E_M_ID`))) join `Predictions` on((`Predictions`.`P_E_ID` = `Entries`.`E_ID`))) where ((`Entries`.`E_Origin` = 5) and (ifnull(`Predictions`.`P_Origin_Id`,0) <> 1) and (`Predictions`.`P_Archive` = 0)) order by `Molecules`.`M_ID`,`Entries`.`E_ID`,`Predictions`.`P_ID`;

-- --------------------------------------------------------

--
-- Struktur des Views `V_RadiativeTransitions2`
--
DROP TABLE IF EXISTS `V_RadiativeTransitions2`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_RadiativeTransitions2` AS select 'CDMS' AS `Resource`,'' AS `RadTransComments`,'' AS `RadTransMethodRef`,`Predictions`.`P_ID` AS `RadiativeTransitionID`,`Molecules`.`M_ID` AS `MoleculeID`,`Molecules`.`M_TrivialName` AS `ChemicalName`,`Molecules`.`M_Name` AS `MolecularChemicalSpecies`,`Entries`.`E_Isotopomer` AS `Isotopomer`,'' AS `RadTransFrequencyTheoreticalComments`,'' AS `RadTransFrequencyTheoreticalSourceRef`,`Predictions`.`P_Frequency` AS `RadTransFrequencyTheoreticalValue`,'MHz' AS `RadTransFrequencyTheoreticalUnits`,`Predictions`.`P_Uncertainty` AS `RadTransFrequencyTheoreticalAccuracy`,'E2' AS `RadTransProbabilityProbabilityMultipoleValue`,'' AS `RadTransProbabilityWeightedOscillatorStrengthComments`,'' AS `RadTransProbabilityWeightedOscillatorStrengthSourceRef`,'' AS `RadTransProbabilityWeightedOscillatorStrengthMethodRef`,'' AS `RadTransProbabilityWeightedOscillatorStrengthValue`,'' AS `RadTransProbabilityWeightedOscillatorStrengthUnits`,'' AS `RadTransProbabilityWeightedOscillatorStrengthAccuracy`,'' AS `RadTransProbabilityLog10WeightedOscillatorStrengthComments`,'' AS `RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef`,'' AS `RadTransProbabilityLog10WeightedOscillatorStrengthMethodRef`,`Predictions`.`P_Intensity` AS `RadTransProbabilityLog10WeightedOscillatorStrengthValue`,'nm^2 MHz' AS `RadTransProbabilityLog10WeightedOscillatorStrengthUnits`,'' AS `RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy`,`Predictions`.`P_Energy_Lower` AS `LowerStateEnergyValue`,'cm-1' AS `LowerStateEnergyUnit`,`Predictions`.`P_Upper_State_Degeneracy` AS `UpperStateNuclearStatisticalWeight`,`F_GetEnergy2`(`Predictions`.`P_E_ID`,`Predictions`.`P_QN_TAG`,`Predictions`.`P_QN_Up_1`,`Predictions`.`P_QN_Up_2`,`Predictions`.`P_QN_Up_3`,`Predictions`.`P_QN_Up_4`,`Predictions`.`P_QN_Up_5`,`Predictions`.`P_QN_Up_6`) AS `RadTransInitialStateRef`,`F_GetEnergy2`(`Predictions`.`P_E_ID`,`Predictions`.`P_QN_TAG`,`Predictions`.`P_QN_Low_1`,`Predictions`.`P_QN_Low_2`,`Predictions`.`P_QN_Low_3`,`Predictions`.`P_QN_Low_4`,`Predictions`.`P_QN_Low_5`,`Predictions`.`P_QN_Low_6`) AS `RadTransFinalStateRef`,`Predictions`.`P_QN_TAG` AS `CaseQN`,`Predictions`.`P_QN_Up_1` AS `QN_Up_1`,`Predictions`.`P_QN_Up_2` AS `QN_Up_2`,`Predictions`.`P_QN_Up_3` AS `QN_Up_3`,`Predictions`.`P_QN_Up_4` AS `QN_Up_4`,`Predictions`.`P_QN_Up_5` AS `QN_Up_5`,`Predictions`.`P_QN_Up_6` AS `QN_Up_6`,`Predictions`.`P_QN_Low_1` AS `QN_Low_1`,`Predictions`.`P_QN_Low_2` AS `QN_Low_2`,`Predictions`.`P_QN_Low_3` AS `QN_Low_3`,`Predictions`.`P_QN_Low_4` AS `QN_Low_4`,`Predictions`.`P_QN_Low_5` AS `QN_Low_5`,`Predictions`.`P_QN_Low_6` AS `QN_Low_6`,`Entries`.`E_ID` AS `E_ID`,`Entries`.`E_TAG` AS `E_Tag`,`Entries`.`E_States` AS `E_States`,`Entries`.`E_Name` AS `E_Name` from ((`Molecules` join `Entries` on((`Molecules`.`M_ID` = `Entries`.`E_M_ID`))) join `Predictions` on((`Predictions`.`P_E_ID` = `Entries`.`E_ID`))) where ((`Entries`.`E_Origin` = 5) and (ifnull(`Predictions`.`P_Origin_Id`,0) <> 1) and (`Predictions`.`P_Archive` = 0)) order by `Molecules`.`M_ID`,`Entries`.`E_ID`,`Predictions`.`P_ID`;

-- --------------------------------------------------------

--
-- Struktur des Views `V_StatesIVOA`
--
DROP TABLE IF EXISTS `V_StatesIVOA`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_StatesIVOA` AS select `Energies`.`EGY_ID` AS `EGY_ID`,`Energies`.`EGY_E_ID` AS `EGY_E_ID`,`Energies`.`EGY_E_Tag` AS `EGY_E_Tag`,`Energies`.`EGY_DAT_ID` AS `EGY_DAT_ID`,`Energies`.`EGY_Energy` AS `EGY_Energy`,`Energies`.`EGY_Uncertainty` AS `EGY_Uncertainty`,`Energies`.`EGY_PMIX` AS `EGY_PMIX`,`Energies`.`EGY_IBLK` AS `EGY_IBLK`,`Energies`.`EGY_INDX` AS `EGY_INDX`,`Energies`.`EGY_IDGN` AS `EGY_IDGN`,`Energies`.`EGY_QN1` AS `EGY_QN1`,`Energies`.`EGY_QN2` AS `EGY_QN2`,`Energies`.`EGY_QN3` AS `EGY_QN3`,`Energies`.`EGY_QN4` AS `EGY_QN4`,`Energies`.`EGY_QN5` AS `EGY_QN5`,`Energies`.`EGY_QN6` AS `EGY_QN6`,`Energies`.`EGY_User` AS `EGY_User`,`Energies`.`EGY_TIMESTAMP` AS `EGY_TIMESTAMP`,`QuantumNumbersIVOA`.`QN_ID` AS `QN_ID`,`QuantumNumbersIVOA`.`QN_E_ID` AS `QN_E_ID`,`QuantumNumbersIVOA`.`QN_DAT_ID` AS `QN_DAT_ID`,`QuantumNumbersIVOA`.`QN_P_ID` AS `QN_P_ID`,`QuantumNumbersIVOA`.`QN_F_ID` AS `QN_F_ID`,`QuantumNumbersIVOA`.`QN_EGY_ID` AS `QN_EGY_ID`,`QuantumNumbersIVOA`.`QN_1` AS `QN_1`,`QuantumNumbersIVOA`.`QN_2` AS `QN_2`,`QuantumNumbersIVOA`.`QN_3` AS `QN_3`,`QuantumNumbersIVOA`.`QN_4` AS `QN_4`,`QuantumNumbersIVOA`.`QN_5` AS `QN_5`,`QuantumNumbersIVOA`.`QN_6` AS `QN_6`,`QuantumNumbersIVOA`.`QN_label` AS `QN_label`,`QuantumNumbersIVOA`.`QN_type` AS `QN_type`,`QuantumNumbersIVOA`.`QN_Path` AS `QN_Path`,`QuantumNumbersIVOA`.`QN_NumeratorValue` AS `QN_NumeratorValue`,`QuantumNumbersIVOA`.`QN_DenominatorValue` AS `QN_DenominatorValue`,`QuantumNumbersIVOA`.`QN_StringValue` AS `QN_StringValue`,`QuantumNumbersIVOA`.`QN_Description` AS `QN_Description` from (`Energies` left join `QuantumNumbersIVOA` on((`Energies`.`EGY_ID` = `QuantumNumbersIVOA`.`QN_EGY_ID`)));

-- --------------------------------------------------------

--
-- Struktur des Views `V_StatesMolecules`
--
DROP TABLE IF EXISTS `V_StatesMolecules`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_StatesMolecules` AS select 'CDMS' AS `Resource`,`EnergiesTMP`.`EGY_ID` AS `StateID`,`Molecules`.`M_ID` AS `MoleculeID`,`Molecules`.`M_TrivialName` AS `ChemicalName`,`Molecules`.`M_Name` AS `MolecularChemicalSpecies`,`Entries`.`E_Isotopomer` AS `Isotopomer`,`EnergiesTMP`.`EGY_Energy` AS `StateEnergyValue`,'cm-1' AS `StateEnergyUnit`,`EnergiesTMP`.`EGY_Uncertainty` AS `StateEnergyAccuracy`,`EnergiesTMP`.`EGY_PMIX` AS `MixingCoefficient`,`EnergiesTMP`.`EGY_IDGN` AS `StateNuclearStatisticalWeight`,`F_GetStateQNS_String`(`Entries`.`E_ID`,`EnergiesTMP`.`EGY_QN_Tag`,`EnergiesTMP`.`EGY_QN1`,`EnergiesTMP`.`EGY_QN2`,`EnergiesTMP`.`EGY_QN3`,`EnergiesTMP`.`EGY_QN4`,`EnergiesTMP`.`EGY_QN5`,`EnergiesTMP`.`EGY_QN6`) AS `QN_String`,`EnergiesTMP`.`EGY_QN_Tag` AS `EGY_QN_Tag`,`EnergiesTMP`.`EGY_QN1` AS `EGY_QN1`,`EnergiesTMP`.`EGY_QN2` AS `EGY_QN2`,`EnergiesTMP`.`EGY_QN3` AS `EGY_QN3`,`EnergiesTMP`.`EGY_QN4` AS `EGY_QN4`,`EnergiesTMP`.`EGY_QN5` AS `EGY_QN5`,`EnergiesTMP`.`EGY_QN6` AS `EGY_QN6`,`Entries`.`E_ID` AS `E_ID`,`EnergiesTMP`.`EGY_DAT_ID` AS `EGY_DAT_ID`,`Entries`.`E_TAG` AS `E_Tag` from ((`Molecules` join `Entries` on(((`Molecules`.`M_ID` = `Entries`.`E_M_ID`) and (`Entries`.`E_Origin` = 5)))) join `EnergiesTMP` on((`Entries`.`E_ID` = `EnergiesTMP`.`EGY_E_ID`)));

-- --------------------------------------------------------

--
-- Struktur des Views `V_States_XSAMS`
--
DROP TABLE IF EXISTS `V_States_XSAMS`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `V_States_XSAMS` AS select `Molecules`.`M_ID` AS `M_ID`,`Entries`.`E_ID` AS `E_ID`,`EnergiesTMP`.`EGY_ID` AS `EGY_ID`,`EnergiesTMP`.`EGY_DAT_ID` AS `EGY_DAT_ID`,`Entries`.`E_TAG` AS `E_Tag`,`Molecules`.`M_TrivialName` AS `M_TrivialName`,`Entries`.`E_Name` AS `E_Name`,`Entries`.`E_Isotopomer` AS `E_Isotopomer`,`Entries`.`E_States` AS `E_States`,`EnergiesTMP`.`EGY_Energy` AS `EGY_Energy`,`EnergiesTMP`.`EGY_Uncertainty` AS `EGY_Uncertainty`,`EnergiesTMP`.`EGY_PMIX` AS `EGY_PMIX`,`EnergiesTMP`.`EGY_IDGN` AS `EGY_IDGN`,`EnergiesTMP`.`EGY_QN_Tag` AS `EGY_QN_Tag`,`EnergiesTMP`.`EGY_QN1` AS `EGY_QN1`,`EnergiesTMP`.`EGY_QN2` AS `EGY_QN2`,`EnergiesTMP`.`EGY_QN3` AS `EGY_QN3`,`EnergiesTMP`.`EGY_QN4` AS `EGY_QN4`,`EnergiesTMP`.`EGY_QN5` AS `EGY_QN5`,`EnergiesTMP`.`EGY_QN6` AS `EGY_QN6`,`F_GetStateQNS_String`(`Entries`.`E_ID`,`EnergiesTMP`.`EGY_QN_Tag`,`EnergiesTMP`.`EGY_QN1`,`EnergiesTMP`.`EGY_QN2`,`EnergiesTMP`.`EGY_QN3`,`EnergiesTMP`.`EGY_QN4`,`EnergiesTMP`.`EGY_QN5`,`EnergiesTMP`.`EGY_QN6`) AS `QN_String` from ((`Molecules` join `Entries` on(((`Molecules`.`M_ID` = `Entries`.`E_M_ID`) and (`Entries`.`E_Origin` = 5)))) join `EnergiesTMP` on((`Entries`.`E_ID` = `EnergiesTMP`.`EGY_E_ID`)));

DELIMITER $$
--
-- Prozeduren
--
DROP PROCEDURE IF EXISTS `P_AssignStates2Predictions`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_AssignStates2Predictions`(pDatID Integer, eDatID Integer)
BEGIN

DECLARE pID INTEGER;
DECLARE qnTag INTEGER;
DECLARE qnUp1 INTEGER;
DECLARE qnUp2 INTEGER;
DECLARE qnUp3 INTEGER;
DECLARE qnUp4 INTEGER;
DECLARE qnUp5 INTEGER;
DECLARE qnUp6 INTEGER;
DECLARE qnLow1 INTEGER;
DECLARE qnLow2 INTEGER;
DECLARE qnLow3 INTEGER;
DECLARE qnLow4 INTEGER;
DECLARE qnLow5 INTEGER;
DECLARE qnLow6 INTEGER;
DECLARE egyUpID INTEGER;
DECLARE egyLowID INTEGER;

DECLARE done INT DEFAULT 0;

DECLARE cur_predictions CURSOR FOR 
  SELECT P_ID,
         P_QN_TAG, 
         P_QN_Up_1, 
         P_QN_Up_2, 
         P_QN_Up_3,
         P_QN_Up_4, 
         P_QN_Up_5, 
         P_QN_Up_6, 
         P_QN_Low_1, 
         P_QN_Low_2, 
         P_QN_Low_3,
         P_QN_Low_4, 
         P_QN_Low_5, 
         P_QN_Low_6
   FROM Predictions 
   WHERE P_DAT_ID=pDatID;

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;

OPEN cur_predictions;
                
REPEAT
 FETCH cur_predictions INTO 
   pID, qnTag, qnUp1, qnUp2, qnUp3, qnUp4, qnUp5, qnUp6, 
      qnLow1, qnLow2, qnLow3, qnLow4, qnLow5, qnLow6;

 IF NOT done THEN

   SELECT F_Get_Egy_ID(eDatID,
        qnTag, 
        qnUp1,
        qnUp2,
        qnUp3,
        qnUp4,
        qnUp5,
        qnUp6) into egyUpID;

   SELECT F_Get_Egy_ID(eDatID,
        qnTag, 
        qnLow1,
        qnLow2,
        qnLow3,
        qnLow4,
        qnLow5,
        qnLow6) into egyLowID;


  UPDATE Predictions 
    SET P_Up_EGY_ID  = egyUpID,
        P_Low_EGY_ID = egyLowID
    WHERE P_ID=pID;

 END IF;
UNTIL done END REPEAT;
CLOSE cur_predictions;  

END$$

DROP PROCEDURE IF EXISTS `P_CreateEgyFromCat`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_CreateEgyFromCat`(
eID INTEGER,
pDatID INTEGER,
eDatID INTEGER
)
    READS SQL DATA
BEGIN
DECLARE egyID INTEGER;
DECLARE energy DOUBLE;
DECLARE eLow DOUBLE;
DECLARE freq DOUBLE;
DECLARE degeneracy INTEGER;
DECLARE dof INTEGER;
DECLARE unc DOUBLE;
DECLARE pmix DOUBLE;
DECLARE tag INTEGER;
DECLARE qnTag INTEGER;
DECLARE qn1 INTEGER;
DECLARE qn2 INTEGER;
DECLARE qn3 INTEGER;
DECLARE qn4 INTEGER;
DECLARE qn5 INTEGER;
DECLARE qn6 INTEGER;
DECLARE done INT DEFAULT 0;

DECLARE cur_lowerStates CURSOR FOR 
  SELECT DISTINCT P_Energy_Lower, 
         P_E_Tag,
         P_QN_TAG, 
         P_QN_Low_1, 
         P_QN_Low_2, 
         P_QN_Low_3,
         P_QN_Low_4, 
         P_QN_Low_5, 
         P_QN_Low_6, 
         P_Degree_Of_Freedom, 
         P_E_ID 
   FROM Predictions 
   WHERE P_E_ID=eID
   AND P_DAT_ID=pDatID;

DECLARE cur_upperStates CURSOR FOR 
  SELECT DISTINCT P_Energy_Lower + ROUND((P_Frequency/29979.2458),4), 
         P_E_Tag,
         P_QN_TAG, 
         P_QN_Up_1, 
         P_QN_Up_2, 
         P_QN_Up_3,
         P_QN_Up_4, 
         P_QN_Up_5, 
         P_QN_Up_6, 
         P_Degree_Of_Freedom, 
         P_E_ID,
         P_Upper_State_Degeneracy
   FROM Predictions 
   WHERE P_E_ID=eID
   AND P_DAT_ID=pDatID;


DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;



OPEN cur_lowerStates;
                
REPEAT
 FETCH cur_lowerStates INTO energy, tag, qnTag, qn1, qn2, qn3, qn4, qn5, qn6, dof, eID;
 IF NOT done THEN


   IF energy IS NOT NULL THEN
  
    INSERT INTO Energies 
    (EGY_E_ID, EGY_DAT_ID, EGY_E_Tag, EGY_Energy, EGY_QN_Tag, EGY_QN1, EGY_QN2, EGY_QN3, EGY_QN4, EGY_QN5, EGY_QN6, EGY_TIMESTAMP)
    VALUES
    (eID, eDatID, tag, energy, qnTag, qn1, qn2, qn3, qn4, qn5, qn6, now());
    SELECT LAST_INSERT_ID() INTO egyID;
  
   END IF;
 END IF;
UNTIL done END REPEAT;
CLOSE cur_lowerStates;  

SET done=0;
OPEN cur_upperStates;
                
REPEAT
 FETCH cur_upperStates INTO energy, tag, qnTag, qn1, qn2, qn3, qn4, qn5, qn6, dof, eID, degeneracy;
 IF NOT done THEN

   IF energy IS NOT NULL THEN
    SET egyID = NULL;

    SELECT F_Get_Egy_ID(eDatID, qnTag, qn1, qn2, qn3, qn4, qn5, qn6) into egyID;

    IF egyID is not null THEN 
      UPDATE Energies SET EGY_IDGN=degeneracy WHERE EGY_ID=egyID;
    ELSE
      INSERT INTO Energies 
      (EGY_E_ID, EGY_DAT_ID, EGY_E_Tag, EGY_Energy, EGY_IDGN, EGY_QN_Tag, EGY_QN1, EGY_QN2, EGY_QN3, EGY_QN4, EGY_QN5, EGY_QN6, EGY_TIMESTAMP)
      VALUES
      (eID, eDatID, tag, energy, degeneracy, qnTag, qn1, qn2, qn3, qn4, qn5, qn6, now());
      SELECT LAST_INSERT_ID() INTO egyID;


    END IF;
   END IF;
 END IF;
UNTIL done END REPEAT;
CLOSE cur_upperStates; 

END$$

DROP PROCEDURE IF EXISTS `P_CreateEnergiesForActualMRGLoop`$$
CREATE DEFINER=`root`@`%` PROCEDURE `P_CreateEnergiesForActualMRGLoop`()
BEGIN

DECLARE datId INTEGER;
DECLARE eDatId INTEGER;
DECLARE eId INTEGER;
DECLARE eTag INTEGER;
DECLARE name VarChar(100);
DECLARE type VarChar(10);
DECLARE public INTEGER;
DECLARE archive INTEGER;
DECLARE hfs INTEGER;

DECLARE done INT DEFAULT 0;

DECLARE cur_actualMrgDatasets CURSOR FOR
 SELECT DAT_ID, DAT_E_ID, DAT_E_Tag, DAT_Name, DAT_Type, DAT_Public, DAT_Archive, DAT_HFS 
  FROM  Datasets
  WHERE DAT_Type='cat'
    AND DAT_Name like '%.mrg - actual CDMS entry';

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;



OPEN cur_actualMrgDatasets;
                
REPEAT
 FETCH cur_actualMrgDatasets INTO datId, eId, eTag, name, type, public, archive, hfs;
 IF NOT done THEN
    SET eDatId = null;
    INSERT INTO Datasets 
    (DAT_E_ID, DAT_E_Tag, DAT_Name, DAT_Type, DAT_Public, DAT_Archive, DAT_HFS)
    VALUES 
    (eId, eTag, CONCAT('Energies created from Predictions: ',name), 'egy', public, archive, hfs);

    SELECT LAST_INSERT_ID() INTO eDatId;

    CALL P_CreateEgyFromCat(eId, datId, eDatId);
    CALL P_AssignStates2Predictions(datId, eDatId);

 END IF;

UNTIL done END REPEAT;
CLOSE cur_actualMrgDatasets;  

END$$

DROP PROCEDURE IF EXISTS `P_EnergyFromPredictions`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_EnergyFromPredictions`(
eID INTEGER,
qnTag INTEGER, 
qn1 INTEGER,
qn2 INTEGER,
qn3 INTEGER,
qn4 INTEGER,
qn5 INTEGER,
qn6 INTEGER,
out energy double,
out degeneracy integer
)
BEGIN
SELECT DISTINCT P_Energy_Lower INTO energy  
FROM Predictions 
WHERE P_E_ID=eID
AND P_QN_TAG = qnTag 
AND P_QN_Low_1 <=> qn1
AND P_QN_Low_2 <=> qn2
AND P_QN_Low_3 <=> qn3
AND P_QN_Low_4 <=> qn4
AND P_QN_Low_5 <=> qn5
AND P_QN_Low_6 <=> qn6
AND P_Archive=0;
SELECT DISTINCT P_Upper_State_Degeneracy INTO degeneracy  
FROM Predictions 
WHERE P_E_ID=eID
AND P_QN_TAG = qnTag 
AND P_QN_Up_1 <=> qn1
AND P_QN_Up_2 <=> qn2
AND P_QN_Up_3 <=> qn3
AND P_QN_Up_4 <=> qn4
AND P_QN_Up_5 <=> qn5
AND P_QN_Up_6 <=> qn6
AND P_Archive=0;
END$$

DROP PROCEDURE IF EXISTS `P_GetStateQNS`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_GetStateQNS`(eId Integer, qnTag Integer,
qn1 Integer,
qn2 Integer,
qn3 Integer,
qn4 Integer,
qn5 Integer,
qn6 Integer)
BEGIN
select SQN_ID as Id, SQN_Case as 'Case', SQN_Label as Label, IFNULL(SQN_ValueFloat, IFNULL(SQN_ValueString,IFNULL(F_ReturnQNColumnValue(qn1,qn2,qn3,qn4,qn5,qn6,SQN_ColumnValue,SQN_ColumnValueFunction),NULL))) AS Value, SQN_SpinRef as SpinRef, SQN_Attribute as Attribute
from StateQNXsams 
where SQN_E_ID=eId
and SQN_QN_Tag=qnTag 
and (qn1<=>IFNULL(SQN_QN1,qn1))
and (qn2<=>IFNULL(SQN_QN2,qn2))
and (qn3<=>IFNULL(SQN_QN3,qn3))
and (qn4<=>IFNULL(SQN_QN4,qn4))
and (qn5<=>IFNULL(SQN_QN5,qn5))
and (qn6<=>IFNULL(SQN_QN6,qn6));
END$$

DROP PROCEDURE IF EXISTS `P_ImportCatFromFile`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_ImportCatFromFile`(id INTEGER, datId INTEGER, eId INTEGER, hfs INTEGER, onlyCheck BOOLEAN  )
    MODIFIES SQL DATA
BEGIN

DECLARE Done boolean;
DECLARE counter INT;
DECLARE FILE LONGTEXT;
DECLARE line VARCHAR(255);

DECLARE error VARCHAR(255);

DECLARE freq VARCHAR(25);
DECLARE freqExp VARCHAR(25);
DECLARE unc, inten, elow VARCHAR(20);
DECLARE tag, qntag, usd, dof, unit VARCHAR(10);
DECLARE qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10,qn11,qn12 VARCHAR(5);
DECLARE archive, quality INTEGER;
DECLARE origin VARCHAR(2);

set Done = false;
set counter = 1;
set error = "";

SET unit = "MHz";
SET archive = -2;
SET quality = 10;

select FIL_ASCIIFILE into FILE from Files where FIL_ID=id;

IF FILE is NULL THEN
  SET Done = true;
END IF;

  WHILE not Done DO
   SET line = F_GetLine(FILE,counter);

   IF (length(line)=0) THEN
      set Done = true;
   ELSE 
   
     SET freq = SUBSTR(line,1,13);
     SET unc  = SUBSTR(line,14,8);
     SET inten = SUBSTR(line, 22, 8);
     SET dof  = F_ConvertSpfitHex2Int(SUBSTR(line, 30,2));
     SET elow = SUBSTR(line,32,10);
     SET usd  = F_ConvertSpfitHex2Int(SUBSTR(line,42,3));
     SET tag  = SUBSTR(line,45,7);
     SET qntag= SUBSTR(line,52,4);
     SET qn1  = F_ConvertSpfitHex2Int(SUBSTR(line,56,2));
     SET qn2  = F_ConvertSpfitHex2Int(SUBSTR(line,58,2));
     SET qn3  = F_ConvertSpfitHex2Int(SUBSTR(line,60,2));
     SET qn4  = F_ConvertSpfitHex2Int(SUBSTR(line,62,2));
     SET qn5  = F_ConvertSpfitHex2Int(SUBSTR(line,64,2));
     SET qn6  = F_ConvertSpfitHex2Int(SUBSTR(line,66,2));
     SET qn7  = F_ConvertSpfitHex2Int(SUBSTR(line,68,2));
     SET qn8  = F_ConvertSpfitHex2Int(SUBSTR(line,70,2));
     SET qn9  = F_ConvertSpfitHex2Int(SUBSTR(line,72,2));
     SET qn10 = F_ConvertSpfitHex2Int(SUBSTR(line,74,2));
     SET qn11 = F_ConvertSpfitHex2Int(SUBSTR(line,76,2));
     SET qn12 = F_ConvertSpfitHex2Int(SUBSTR(line,78,2));

     SET origin = SUBSTR(tag,-3,1);

     IF (tag<0) THEN
SET tag=-tag;
        SET freqExp = freq;
     END IF;

     IF (onlyCheck) THEN

SELECT eId AS P_E_ID,
tag     AS P_E_Tag, 
freq    AS P_Frequency,
freqExp AS P_Frequency_Exp,
inten   AS P_Intensity,
unc     AS P_Uncertainty,
elow    AS P_Energy_Lower,
qntagAS P_QN_TAG,
qn1AS P_QN_Up_1,
qn2AS P_QN_Up_2,
qn3AS P_QN_Up_3,
qn4AS P_QN_Up_4,
qn5AS P_QN_Up_5,
qn6AS P_QN_Up_6,
qn7AS P_QN_Low_1,
qn8AS P_QN_Low_2,
qn9AS P_QN_Low_3,
qn10AS P_QN_Low_4,
qn11AS P_QN_Low_5,
qn12AS P_QN_Low_6,
unitAS P_Unit,
dofAS P_Degree_Of_Freedom,
usdAS P_Upper_State_Degeneracy,
originAS P_Origin_Id,
hfsAS P_HFS,
datIdAS P_DAT_ID,
quality AS P_Quality,
archive AS P_Archive;
  
     ELSE


INSERT INTO Predictions 
(P_E_ID,
P_E_Tag, 
P_Frequency,
P_Frequency_Exp,
P_Intensity,
P_Uncertainty,
P_Energy_Lower,
P_QN_TAG,
P_QN_Up_1,
P_QN_Up_2,
P_QN_Up_3,
P_QN_Up_4,
P_QN_Up_5,
P_QN_Up_6,
P_QN_Low_1,
P_QN_Low_2,
P_QN_Low_3,
P_QN_Low_4,
P_QN_Low_5,
P_QN_Low_6,
P_Unit,
P_Degree_Of_Freedom,
P_Upper_State_Degeneracy,
P_Origin_Id,
P_HFS,
P_DAT_ID,
P_Quality,
P_Archive,
P_TIMESTAMP
          ) VALUES (
eId,
tag, 
freq,
freqExp,
inten,
unc,
elow,
qntag,
qn1,
qn2,
qn3,
qn4,
qn5,
qn6,
qn7,
qn8,
qn9,
qn10,
qn11,
qn12,
unit,
dof,
usd,
origin,
hfs,
datId,
quality,
archive,
now()
);
     END IF;

     set counter=counter+1;

   END IF;

  END WHILE;


END$$

DROP PROCEDURE IF EXISTS `P_ImportEgyFromFile`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_ImportEgyFromFile`(id INTEGER, datId INTEGER, eId INTEGER, tag INTEGER, qnTag INTEGER, onlyCheck BOOLEAN  )
    MODIFIES SQL DATA
BEGIN

DECLARE Done boolean;
DECLARE FILE LONGTEXT;
DECLARE counter INT;
DECLARE line VARCHAR(255);

DECLARE error VARCHAR(255);

DECLARE unc, pmix, egy VARCHAR(25);
DECLARE qn1,qn2,qn3,qn4,qn5,qn6 VARCHAR(3);
DECLARE iblk, indx, idgn VARCHAR(10);

set Done = false;
set counter = 1;
set error = "";

select FIL_ASCIIFILE into FILE from Files where FIL_ID=id;

IF FILE is NULL THEN
  SET Done = true;
END IF;

  WHILE not Done DO
   SET line = F_GetLine(FILE,counter);

   IF (length(line)=0) THEN
      set Done = true;
   ELSE 
   
     SET iblk = SUBSTR(line,1,6);
     SET indx = SUBSTR(line,7,5);
     SET egy  = SUBSTR(line,13,18);
     SET unc  = SUBSTR(line,31,18);
     SET pmix = SUBSTR(line,49,11);
     SET idgn = F_ConvertSpfitHex2Int(SUBSTR(line,60,5));

     

     SET qn1  = F_ConvertSpfitHex2Int(SUBSTR(line,66,3));
     SET qn2  = F_ConvertSpfitHex2Int(SUBSTR(line,69,3));
     SET qn3  = F_ConvertSpfitHex2Int(SUBSTR(line,72,3));
     SET qn4  = F_ConvertSpfitHex2Int(SUBSTR(line,75,3));
     SET qn5  = F_ConvertSpfitHex2Int(SUBSTR(line,78,3));
     SET qn6  = F_ConvertSpfitHex2Int(SUBSTR(line,81,3));
     

     IF (not (isNumeric(egy) AND isNumeric(unc))) THEN
       SET error = concat(error," Error parsing line: ", counter, "\n");
     END IF;

     

     IF (onlyCheck) THEN

SELECT
eId AS EGY_E_ID,
tag AS EGY_E_Tag,
datId AS EGY_DAT_ID,
egy AS EGY_Energy,
unc AS EGY_Uncertainty,
pmix AS EGY_PMIX,
iblk AS EGY_IBLK,
indx AS EGY_INDX,
idgn AS EGY_IDGN,
qnTag AS EGY_QN_Tag,
qn1 AS EGY_QN1,
qn2 AS EGY_QN2,
qn3 AS EGY_QN3,
qn4 AS EGY_QN4,
qn5 AS EGY_QN5,
qn6 AS EGY_QN6;
          
     ELSE 

INSERT INTO Energies
(
EGY_E_ID,
EGY_E_Tag,
EGY_DAT_ID,
EGY_Energy,
EGY_Uncertainty,
EGY_PMIX,
EGY_IBLK,
EGY_INDX,
EGY_IDGN,
EGY_QN_Tag,
EGY_QN1,
EGY_QN2,
EGY_QN3,
EGY_QN4,
EGY_QN5,
EGY_QN6,
EGY_TIMESTAMP
) VALUES (
eId,
tag,
datId,
egy,
unc,
pmix,
iblk,
indx,
idgn,
qnTag,
qn1,
qn2,
qn3,
qn4,
qn5,
qn6,
now()
);
     END IF;
     set counter=counter+1;

   END IF;

  END WHILE;


END$$

DROP PROCEDURE IF EXISTS `P_ImportLinFromFile`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_ImportLinFromFile`(id INTEGER, datId INTEGER, eId INTEGER, onlyCheck BOOLEAN  )
    MODIFIES SQL DATA
BEGIN

Declare Done boolean;
DECLARE endOfLine BOOLEAN;
DECLARE FILE LONGTEXT;
DECLARE counter INT;
DECLARE line VARCHAR(255);
DECLARE lineEnd INT;
DECLARE linelength INT;

DECLARE error VARCHAR(255);

DECLARE freq VARCHAR(255);
DECLARE unc, weight, comment VARCHAR(255);
DECLARE rest VARCHAR(255);
DECLARE qn VARCHAR(36);
DECLARE pos INT;
DECLARE qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10,qn11,qn12 VARCHAR(3);

set Done = false;
set counter = 1;
set lineEnd = 0;
set error = "";

select FIL_ASCIIFILE into FILE from Files where FIL_ID=id;

IF FILE is NULL THEN
  SET Done = true;
END IF;

  WHILE not Done DO
   SET line = F_GetLine(FILE,counter);

   IF (length(line)=0) THEN
      set Done = true;
   ELSE 
   
     SET qn   = SUBSTR(line,1,36);
     SET rest = SUBSTR(line,37);

     SET qn1  = F_ConvertSpfitHex2Int(SUBSTR(qn,1,3));
     SET qn2  = F_ConvertSpfitHex2Int(SUBSTR(qn,4,3));
     SET qn3  = F_ConvertSpfitHex2Int(SUBSTR(qn,7,3));
     SET qn4  = F_ConvertSpfitHex2Int(SUBSTR(qn,10,3));
     SET qn5  = F_ConvertSpfitHex2Int(SUBSTR(qn,13,3));
     SET qn6  = F_ConvertSpfitHex2Int(SUBSTR(qn,16,3));
     SET qn7  = F_ConvertSpfitHex2Int(SUBSTR(qn,19,3));
     SET qn8  = F_ConvertSpfitHex2Int(SUBSTR(qn,22,3));
     SET qn9  = F_ConvertSpfitHex2Int(SUBSTR(qn,25,3));
     SET qn10 = F_ConvertSpfitHex2Int(SUBSTR(qn,28,3));
     SET qn11 = F_ConvertSpfitHex2Int(SUBSTR(qn,31,3));
     SET qn12 = F_ConvertSpfitHex2Int(SUBSTR(qn,34,3));

     
     SET pos = 0;
     SET linelength = length(rest);
     SET freq = " ";
     SET unc = " ";
     SET weight = " ";

     WHILE (pos < linelength AND freq=" " ) DO
       SET freq=substring_index(rest,' ',pos);
       SET pos=pos+1;
     END WHILE;

     
     SET rest = SUBSTR(rest,length(freq)+1);
     SET linelength = length(rest);
     SET pos = 0;

     WHILE (pos < linelength AND unc=" " ) DO
       SET unc=substring_index(rest,' ',pos);
       SET pos=pos+1;
     END WHILE;

     
     SET rest = SUBSTR(rest,length(unc)+1);
     SET linelength = length(rest);
     SET pos = 0;

     WHILE (pos < linelength AND weight=" " ) DO
       SET weight=substring_index(rest,' ',pos);
       SET pos=pos+1;
     END WHILE;

     SET comment = NULL;
     
     IF (isNumeric(replace(weight," ",""))=1) THEN
       SET comment = SUBSTR(rest,length(weight)+1);
     ELSE 
       SET weight = NULL;
       SET comment = rest;
     END IF;


     
     SET freq=replace(freq," ","");
     SET unc=replace(unc," ","");
     SET weight=replace(weight," ","");
     SET comment = LTRIM(comment);

     IF (not (isNumeric(freq) AND isNumeric(unc))) THEN
       SET error = concat(error," Error parsing line: ", counter, "\n");
     END IF;

     
     IF (unc < 0) THEN
       SET freq=freq*29979.2458;
       SET unc=unc*29979.2458;
     END IF;

     IF (onlyCheck) THEN

       IF (qn3 is NULL) THEN
          SELECT eId as F_E_ID, datId as F_DAT_ID, qn1,NULL,NULL,NULL,NULL,NULL,qn2,NULL,NULL,NULL,NULL,NULL, freq AS F_Frequency, unc as F_Error, weight as F_WT, comment as F_Comment;
       ELSEIF (qn5 is NULL) THEN
          SELECT eId as F_E_ID, datId as F_DAT_ID, qn1,qn2,NULL,NULL,NULL,NULL,qn3,qn4,NULL,NULL,NULL,NULL, freq AS F_Frequency, unc as F_Error, weight as F_WT, comment as F_Comment;     
       ELSEIF (qn7 is NULL) THEN
          SELECT eId as F_E_ID, datId as F_DAT_ID, qn1,qn2,qn3,NULL,NULL,NULL,qn4,qn5,qn6,NULL,NULL,NULL, freq AS F_Frequency, unc as F_Error, weight as F_WT, comment as F_Comment;     
       ELSEIF (qn9 is NULL) THEN
          SELECT eId as F_E_ID, datId as F_DAT_ID, qn1,qn2,qn3,qn4,NULL,NULL,qn5,qn6,qn7,qn8,NULL,NULL, freq AS F_Frequency, unc as F_Error, weight as F_WT, comment as F_Comment;     
       ELSEIF (qn11 is NULL) THEN
          SELECT eId as F_E_ID, datId as F_DAT_ID, qn1,qn2,qn3,qn4,qn5,NULL,qn6,qn7,qn8,qn9,qn10,NULL, freq AS F_Frequency, unc as F_Error, weight as F_WT, comment as F_Comment;     
       ELSE
          SELECT eId as F_E_ID, datId as F_DAT_ID, qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10,qn11,qn12, freq AS F_Frequency, unc as F_Error, weight as F_WT, comment as F_Comment;     
       END IF;

     ELSE 

       IF (qn3 is NULL) THEN
  INSERT INTO Frequencies (F_E_ID, F_QN_Up_1,F_QN_Low_1, F_Frequency, F_Error, F_WT, F_Unit, F_Comment, F_DAT_ID, F_TIMESTAMP) 
          VALUES ( eId, qn1,qn2,freq, unc, weight, 'MHz', comment, datId, now() );
       ELSEIF (qn5 is NULL) THEN
  INSERT INTO Frequencies (F_E_ID, F_QN_Up_1, F_QN_Up_2, F_QN_Low_1, F_QN_Low_2, F_Frequency, F_Error, F_WT, F_Unit, F_Comment, F_DAT_ID, F_TIMESTAMP) 
          VALUES ( eId, qn1,qn2,qn3,qn4, freq, unc, weight, 'MHz', comment, datId, now() );
       ELSEIF (qn7 is NULL) THEN
  INSERT INTO Frequencies (F_E_ID, F_QN_Up_1,F_QN_Up_2,F_QN_Up_3,F_QN_Low_1, F_QN_Low_2, F_QN_Low_3, F_Frequency, F_Error, F_WT, F_Unit, F_Comment, F_DAT_ID, F_TIMESTAMP) 
          VALUES ( eId, qn1,qn2,qn3,qn4,qn5,qn6,freq, unc, weight, 'MHz', comment, datId, now() );
       ELSEIF (qn9 is NULL) THEN
  INSERT INTO Frequencies (F_E_ID, F_QN_Up_1,F_QN_Up_2,F_QN_Up_3,F_QN_Up_4,F_QN_Low_1, F_QN_Low_2, F_QN_Low_3, F_QN_Low_4, F_Frequency, F_Error, F_WT, F_Unit, F_Comment, F_DAT_ID, F_TIMESTAMP) 
          VALUES ( eId, qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,freq, unc, weight, 'MHz', comment, datId, now() );
       ELSEIF (qn11 is NULL) THEN
  INSERT INTO Frequencies (F_E_ID, F_QN_Up_1,F_QN_Up_2,F_QN_Up_3,F_QN_Up_4, F_QN_Up_5, F_QN_Low_1, F_QN_Low_2, F_QN_Low_3, F_QN_Low_4, F_QN_Low_5, F_Frequency, F_Error, F_WT, F_Unit, F_Comment, F_DAT_ID, F_TIMESTAMP) 
          VALUES ( eId, qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10,freq, unc, weight, 'MHz', comment, datId, now() );
       ELSE
  INSERT INTO Frequencies (F_E_ID, F_QN_Up_1,F_QN_Up_2,F_QN_Up_3,F_QN_Up_4, F_QN_Up_5, F_QN_Up_6, F_QN_Low_1, F_QN_Low_2, F_QN_Low_3, F_QN_Low_4, F_QN_Low_5, F_QN_Low_6, F_Frequency, F_Error, F_WT, F_Unit, F_Comment, F_DAT_ID, F_TIMESTAMP) 
          VALUES ( eId, qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10,qn11,qn12,freq, unc, weight, 'MHz', comment, datId, now() );
       END IF;

     END IF;
     set counter=counter+1;

   END IF;

  END WHILE;


END$$

DROP PROCEDURE IF EXISTS `P_UpdateAllEinsteinA`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_UpdateAllEinsteinA`()
BEGIN
  DECLARE datID INT;
  
  DECLARE done INT DEFAULT 0;
  
  DECLARE dat_cursor CURSOR FOR 
    SELECT DISTINCT P_DAT_ID 
    FROM Predictions JOIN Entries on P_E_ID = E_ID
    WHERE P_EinsteinA is NULL
    AND   P_Archive = 0
    AND   substr(E_Tag,-3,1)='5'
    AND   P_DAT_ID is NOT NULL;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done=1;            

OPEN dat_cursor;

REPEAT
 FETCH dat_cursor INTO datID;
  IF NOT done THEN
    Call P_UpdateEinsteinA(datID);
  End If;
 UNTIL done END REPEAT;

CLOSE dat_cursor;

END$$

DROP PROCEDURE IF EXISTS `P_UpdateEinsteinA`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_UpdateEinsteinA`(datID INT)
BEGIN
  DECLARE Q300 double;
  DECLARE eID INT;
  
            
# Get the Entry - ID
SELECT DAT_E_ID INTO eID FROM Datasets WHERE DAT_ID=datID;

IF eID IS NOT NULL THEN

  # Get the stored Partitionfunction for 300K
  SELECT distinct PF_Partitionfunction INTO Q300 
  FROM Partitionfunctions 
  WHERE PF_E_ID=eID
  AND PF_Temperature=300
  AND PF_M_ID Is NOT NULL;

  IF Q300 IS NOT NULL THEN
    UPDATE Predictions 
    SET P_EinsteinA = pow(10,F_GetEinsteinA(P_Frequency, P_Intensity, Q300, P_Energy_Lower, P_Upper_State_Degeneracy)) 
    WHERE P_DAT_ID=datID;
  END IF;


END IF;


END$$

DROP PROCEDURE IF EXISTS `P_UpdateQNTag`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `P_UpdateQNTag`(datID INT)
BEGIN
  DECLARE tag INT;
            
SELECT distinct P_QN_Tag into tag FROM Predictions WHERE P_DAT_ID=datID;
UPDATE Datasets SET DAT_QN_Tag = tag WHERE DAT_ID=datID;

END$$

--
-- Funktionen
--
DROP FUNCTION IF EXISTS `F_ConvertSpfitHex2Int`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_ConvertSpfitHex2Int`(str VARCHAR(50)) RETURNS varchar(50) CHARSET utf8
    NO SQL
BEGIN

DECLARE RetVal VARCHAR(50);

SET RetVal = Replace(str,"a","-10"); 
SET RetVal = Replace(RetVal,"b","-11"); 
SET RetVal = Replace(RetVal,"c","-12"); 
SET RetVal = Replace(RetVal,"d","-13"); 
SET RetVal = Replace(RetVal,"e","-14"); 
SET RetVal = Replace(RetVal,"f","-15"); 
SET RetVal = Replace(RetVal,"g","-16"); 
SET RetVal = Replace(RetVal,"h","-17"); 
SET RetVal = Replace(RetVal,"i","-18"); 
SET RetVal = Replace(RetVal,"j","-19"); 
SET RetVal = Replace(RetVal,"k","-20"); 
SET RetVal = Replace(RetVal,"l","-21"); 
SET RetVal = Replace(RetVal,"m","-22"); 
SET RetVal = Replace(RetVal,"n","-23"); 
SET RetVal = Replace(RetVal,"o","-24"); 
SET RetVal = Replace(RetVal,"p","-25"); 
SET RetVal = Replace(RetVal,"q","-26"); 
SET RetVal = Replace(RetVal,"r","-27"); 
SET RetVal = Replace(RetVal,"s","-28"); 
SET RetVal = Replace(RetVal,"t","-29"); 
SET RetVal = Replace(RetVal,"u","-30"); 
SET RetVal = Replace(RetVal,"v","-31"); 
SET RetVal = Replace(RetVal,"w","-32"); 
SET RetVal = Replace(RetVal,"x","-33"); 
SET RetVal = Replace(RetVal,"y","-34"); 
SET RetVal = Replace(RetVal,"z","-35"); 

SET RetVal = Replace(RetVal,"A","10"); 
SET RetVal = Replace(RetVal,"B","11"); 
SET RetVal = Replace(RetVal,"C","12"); 
SET RetVal = Replace(RetVal,"D","13"); 
SET RetVal = Replace(RetVal,"E","14"); 
SET RetVal = Replace(RetVal,"F","15"); 
SET RetVal = Replace(RetVal,"G","16"); 
SET RetVal = Replace(RetVal,"H","17"); 
SET RetVal = Replace(RetVal,"I","18"); 
SET RetVal = Replace(RetVal,"J","19"); 
SET RetVal = Replace(RetVal,"K","20"); 
SET RetVal = Replace(RetVal,"L","21"); 
SET RetVal = Replace(RetVal,"M","22"); 
SET RetVal = Replace(RetVal,"N","23"); 
SET RetVal = Replace(RetVal,"O","24"); 
SET RetVal = Replace(RetVal,"P","25"); 
SET RetVal = Replace(RetVal,"Q","26"); 
SET RetVal = Replace(RetVal,"R","27"); 
SET RetVal = Replace(RetVal,"S","28"); 
SET RetVal = Replace(RetVal,"T","29"); 
SET RetVal = Replace(RetVal,"U","30"); 
SET RetVal = Replace(RetVal,"V","31"); 
SET RetVal = Replace(RetVal,"W","32"); 
SET RetVal = Replace(RetVal,"X","33"); 
SET RetVal = Replace(RetVal,"Y","34"); 
SET RetVal = Replace(RetVal,"Z","35"); 
IF (RetVal = "") THEN
  SET RetVal = NULL;
END IF;

Return RetVal;

END$$

DROP FUNCTION IF EXISTS `F_GetCML`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetCML`(eID Integer) RETURNS text CHARSET utf8
    READS SQL DATA
BEGIN
DECLARE mID INT;

DECLARE mFormalCharge VARCHAR(5);

DECLARE atomId VARCHAR(10);
DECLARE elementType VARCHAR(10);
DECLARE isotopeNumber INT;
DECLARE formalCharge VARCHAR(5);
DECLARE molId INTEGER;

DECLARE atomId1 VARCHAR(10);
DECLARE atomId2 VARCHAR(10);
DECLARE bondOrder VARCHAR(10);

DECLARE done INT DEFAULT 0;

DECLARE xmlVersion VARCHAR(38) DEFAULT '';
DECLARE atomArray VARCHAR(1000);
DECLARE bondArray VARCHAR(1000);
DECLARE moleculeArray VARCHAR(1000);

DECLARE cur_atomArray CURSOR FOR 
  SELECT AA_AtomId, AA_ElementType, AA_IsotopeNumber, AA_FormalCharge 
  FROM AtomArray
  WHERE AA_E_ID=eID;

DECLARE cur_bondArray CURSOR FOR
  SELECT BA_AtomId1, BA_AtomId2, BA_Order
  FROM BondArray
  WHERE BA_E_ID=eID;

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;

SELECT E_M_ID INTO mID FROM Entries WHERE E_ID=eID;

SELECT M_ID, M_FormalCharge INTO molId, mFormalCharge FROM Molecules WHERE M_ID=mID;
SET moleculeArray='<molecule id="';
SET moleculeArray=CONCAT(moleculeArray,molId);
IF mFormalCharge is NOT NULL THEN
  SET moleculeArray=CONCAT(moleculeArray,'" formalCharge="');
  SET moleculeArray=CONCAT(moleculeArray,mFormalCharge);
END IF;
SET moleculeArray=CONCAT(moleculeArray,'">');

SET atomArray="<atomArray>";

OPEN cur_atomArray;
                
REPEAT
 FETCH cur_atomArray INTO atomId, elementType, isotopeNumber, formalCharge;
 IF NOT done THEN
   SET atomArray=CONCAT(atomArray, '\n  <atom id="');
   SET atomArray=CONCAT(atomArray, atomId);
   SET atomArray=CONCAT(atomArray, '" elementType="');
   SET atomArray=CONCAT(atomArray, elementType);
   IF isotopeNumber is not null THEN
     SET atomArray=CONCAT(atomArray, '" isotopeNumber="');
     SET atomArray=CONCAT(atomArray, isotopeNumber);
   END IF;
   IF formalCharge is not null THEN
     SET atomArray=CONCAT(atomArray, '" formalCharge="');
     SET atomArray=CONCAT(atomArray, formalCharge);
   END IF;
   SET atomArray=CONCAT(atomArray, '"/>');
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_atomArray;
SET atomArray=CONCAT(atomArray, '\n</atomArray>');

SET done=0;


#SET bondArray="\n<bondArray>";
SET bondArray="";

OPEN cur_bondArray;
                
REPEAT
 FETCH cur_bondArray INTO atomId1, atomId2, bondOrder;
 IF NOT done THEN
   SET bondArray=CONCAT(bondArray, '\n  <bond atomRefs2="');
   SET bondArray=CONCAT(bondArray, atomId1);
   SET bondArray=CONCAT(bondArray, ' ');
   SET bondArray=CONCAT(bondArray, atomId2);
   SET bondArray=CONCAT(bondArray, '" id="');
   SET bondArray=CONCAT(bondArray, atomId1);
   SET bondArray=CONCAT(bondArray, '_');
   SET bondArray=CONCAT(bondArray, atomId2);
   SET bondArray=CONCAT(bondArray, '" order="');
   SET bondArray=CONCAT(bondArray, bondOrder);
   SET bondArray=CONCAT(bondArray, '"/>');
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_bondArray;

IF (bondArray!="") THEN
  SET bondArray=CONCAT('\n<bondArray>', bondArray, '\n</bondArray>');
END IF;

RETURN CONCAT(xmlVersion, '<cml>\n',moleculeArray,'\n',atomArray,bondArray,'\n</molecule>\n</cml>');

END$$

DROP FUNCTION IF EXISTS `F_GetCML4XSAMS`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetCML4XSAMS`(eID Integer) RETURNS text CHARSET utf8
    READS SQL DATA
BEGIN
DECLARE mID INT;

DECLARE mFormalCharge VARCHAR(5);

DECLARE atomId VARCHAR(10);
DECLARE elementType VARCHAR(10);
DECLARE isotopeNumber INT;
DECLARE formalCharge VARCHAR(5);
DECLARE molId INTEGER;

DECLARE atomId1 VARCHAR(10);
DECLARE atomId2 VARCHAR(10);
DECLARE bondOrder VARCHAR(10);

DECLARE done INT DEFAULT 0;

DECLARE xmlVersion VARCHAR(38) DEFAULT '';
DECLARE atomArray VARCHAR(1000);
DECLARE bondArray VARCHAR(1000);
DECLARE moleculeArray VARCHAR(1000);

DECLARE cur_atomArray CURSOR FOR 
  SELECT AA_AtomId, AA_ElementType, AA_IsotopeNumber, AA_FormalCharge 
  FROM AtomArray
  WHERE AA_E_ID=eID;

DECLARE cur_bondArray CURSOR FOR
  SELECT BA_AtomId1, BA_AtomId2, BA_Order
  FROM BondArray
  WHERE BA_E_ID=eID;

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;


SET atomArray="<cml:atomArray>";

OPEN cur_atomArray;
                
REPEAT
 FETCH cur_atomArray INTO atomId, elementType, isotopeNumber, formalCharge;
 IF NOT done THEN
   SET atomArray=CONCAT(atomArray, '\n  <cml:atom id="');
   SET atomArray=CONCAT(atomArray, atomId);
   SET atomArray=CONCAT(atomArray, '" elementType="');
   SET atomArray=CONCAT(atomArray, elementType);
   IF isotopeNumber is not null THEN
     SET atomArray=CONCAT(atomArray, '" isotopeNumber="');
     SET atomArray=CONCAT(atomArray, isotopeNumber);
   END IF;
   IF formalCharge is not null THEN
     SET atomArray=CONCAT(atomArray, '" formalCharge="');
     SET atomArray=CONCAT(atomArray, formalCharge);
   END IF;
   SET atomArray=CONCAT(atomArray, '"/>');
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_atomArray;
SET atomArray=CONCAT(atomArray, '\n</cml:atomArray>');

SET done=0;


#SET bondArray="\n<bondArray>";
SET bondArray="";

OPEN cur_bondArray;
                
REPEAT
 FETCH cur_bondArray INTO atomId1, atomId2, bondOrder;
 IF NOT done THEN
   SET bondArray=CONCAT(bondArray, '\n  <cml:bond atomRefs2="');
   SET bondArray=CONCAT(bondArray, atomId1);
   SET bondArray=CONCAT(bondArray, ' ');
   SET bondArray=CONCAT(bondArray, atomId2);
   SET bondArray=CONCAT(bondArray, '" id="');
   SET bondArray=CONCAT(bondArray, atomId1);
   SET bondArray=CONCAT(bondArray, '_');
   SET bondArray=CONCAT(bondArray, atomId2);
   SET bondArray=CONCAT(bondArray, '" order="');
   SET bondArray=CONCAT(bondArray, bondOrder);
   SET bondArray=CONCAT(bondArray, '"/>');
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_bondArray;

IF (bondArray!="") THEN
  SET bondArray=CONCAT('\n<cml:bondArray>', bondArray, '\n</cml:bondArray>\n');
END IF;

RETURN CONCAT(atomArray,bondArray);

END$$

DROP FUNCTION IF EXISTS `F_GetCML_xml`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetCML_xml`(eID Integer) RETURNS text CHARSET utf8
    READS SQL DATA
BEGIN
DECLARE mID INT;

DECLARE mFormalCharge VARCHAR(5);

DECLARE atomId VARCHAR(10);
DECLARE elementType VARCHAR(10);
DECLARE isotopeNumber INT;
DECLARE formalCharge VARCHAR(5);
DECLARE molId INTEGER;

DECLARE atomId1 VARCHAR(10);
DECLARE atomId2 VARCHAR(10);
DECLARE bondOrder VARCHAR(10);

DECLARE done INT DEFAULT 0;

DECLARE xmlVersion VARCHAR(38) DEFAULT '<?xml version="1.0" encoding="UTF-8"?>';
DECLARE atomArray VARCHAR(1000);
DECLARE bondArray VARCHAR(1000);
DECLARE moleculeArray VARCHAR(1000);

DECLARE cur_atomArray CURSOR FOR 
  SELECT AA_AtomId, AA_ElementType, AA_IsotopeNumber, AA_FormalCharge 
  FROM AtomArray
  WHERE AA_E_ID=eID;

DECLARE cur_bondArray CURSOR FOR
  SELECT BA_AtomId1, BA_AtomId2, BA_Order
  FROM BondArray
  WHERE BA_E_ID=eID;

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;

SELECT E_M_ID INTO mID FROM Entries WHERE E_ID=eID;

SELECT M_ID, M_FormalCharge INTO molId, mFormalCharge FROM Molecules WHERE M_ID=mID;
SET moleculeArray='\n<molecule id="';
SET moleculeArray=CONCAT(moleculeArray,molId);
IF mFormalCharge is NOT NULL THEN
  SET moleculeArray=CONCAT(moleculeArray,'" formalCharge="');
  SET moleculeArray=CONCAT(moleculeArray,mFormalCharge);
END IF;
SET moleculeArray=CONCAT(moleculeArray,'">');

SET atomArray="<atomArray>";

OPEN cur_atomArray;
                
REPEAT
 FETCH cur_atomArray INTO atomId, elementType, isotopeNumber, formalCharge;
 IF NOT done THEN
   SET atomArray=CONCAT(atomArray, '\n  <atom id="');
   SET atomArray=CONCAT(atomArray, atomId);
   SET atomArray=CONCAT(atomArray, '" elementType="');
   SET atomArray=CONCAT(atomArray, elementType);
   IF isotopeNumber is not null THEN
     SET atomArray=CONCAT(atomArray, '" isotopeNumber="');
     SET atomArray=CONCAT(atomArray, isotopeNumber);
   END IF;
   IF formalCharge is not null THEN
     SET atomArray=CONCAT(atomArray, '" formalCharge="');
     SET atomArray=CONCAT(atomArray, formalCharge);
   END IF;
   SET atomArray=CONCAT(atomArray, '"/>');
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_atomArray;
SET atomArray=CONCAT(atomArray, '\n</atomArray>');

SET done=0;


#SET bondArray="\n<bondArray>";
SET bondArray="";

OPEN cur_bondArray;
                
REPEAT
 FETCH cur_bondArray INTO atomId1, atomId2, bondOrder;
 IF NOT done THEN
   SET bondArray=CONCAT(bondArray, '\n  <bond atomRefs2="');
   SET bondArray=CONCAT(bondArray, atomId1);
   SET bondArray=CONCAT(bondArray, ' ');
   SET bondArray=CONCAT(bondArray, atomId2);
   SET bondArray=CONCAT(bondArray, '" id="');
   SET bondArray=CONCAT(bondArray, atomId1);
   SET bondArray=CONCAT(bondArray, '_');
   SET bondArray=CONCAT(bondArray, atomId2);
   SET bondArray=CONCAT(bondArray, '" order="');
   SET bondArray=CONCAT(bondArray, bondOrder);
   SET bondArray=CONCAT(bondArray, '"/>');
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_bondArray;

IF (bondArray!="") THEN
  SET bondArray=CONCAT('\n<bondArray>', bondArray, '\n</bondArray>');
END IF;

RETURN CONCAT(xmlVersion, '\n<cml>\n',moleculeArray,'\n',atomArray,bondArray,'\n</molecule>\n</cml>');

END$$

DROP FUNCTION IF EXISTS `F_GetEnergy`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetEnergy`(
eID INTEGER,
qnTag INTEGER, 
qn1 INTEGER,
qn2 INTEGER,
qn3 INTEGER,
qn4 INTEGER,
qn5 INTEGER,
qn6 INTEGER
) RETURNS int(11)
    READS SQL DATA
BEGIN
DECLARE egyID INTEGER;
DECLARE energy DOUBLE;
DECLARE eLow DOUBLE;
DECLARE freq DOUBLE;
DECLARE degeneracy INTEGER;
DECLARE unc DOUBLE;
DECLARE pmix DOUBLE;
DECLARE tag INTEGER;
SELECT EGY_ID INTO egyID  
FROM EnergiesTMP
WHERE EGY_E_ID=eID
AND EGY_QN_TAG = qnTag 
AND EGY_QN1 <=> qn1
AND EGY_QN2 <=> qn2
AND EGY_QN3 <=> qn3
AND EGY_QN4 <=> qn4
AND EGY_QN5 <=> qn5
AND EGY_QN6 <=> qn6;
IF (egyID is NULL) THEN
  SELECT EGY_E_TAG, EGY_Energy, EGY_Uncertainty, EGY_PMIX, EGY_IDGN INTO tag, energy, unc, pmix, degeneracy  
  FROM Energies
  WHERE EGY_E_ID=eID
  AND EGY_QN_TAG = qnTag 
  AND EGY_QN1 <=> qn1
  AND EGY_QN2 <=> qn2
  AND EGY_QN3 <=> qn3
  AND EGY_QN4 <=> qn4
  AND EGY_QN5 <=> qn5
  AND EGY_QN6 <=> qn6;
  IF energy IS NOT NULL THEN
    INSERT INTO EnergiesTMP 
    (EGY_E_ID, EGY_E_Tag, EGY_Energy, EGY_Uncertainty, EGY_PMIX, EGY_IDGN, EGY_QN_Tag, EGY_QN1, EGY_QN2, EGY_QN3, EGY_QN4, EGY_QN5, EGY_QN6, EGY_TIMESTAMP)
    VALUES
    (eID, tag, energy, unc, pmix, degeneracy, qnTag, qn1, qn2, qn3, qn4, qn5, qn6, now());
    SELECT LAST_INSERT_ID() INTO egyID;
    RETURN egyID;
  END IF;
ELSE
  RETURN egyID;
END IF;
SELECT DISTINCT P_E_Tag, P_Energy_Lower INTO tag, energy  
FROM Predictions 
WHERE P_E_ID=eID
AND P_QN_TAG = qnTag 
AND P_QN_Low_1 <=> qn1
AND P_QN_Low_2 <=> qn2
AND P_QN_Low_3 <=> qn3
AND P_QN_Low_4 <=> qn4
AND P_QN_Low_5 <=> qn5
AND P_QN_Low_6 <=> qn6
AND P_Archive=0
limit 1;
SELECT DISTINCT P_Upper_State_Degeneracy, P_Energy_Lower, P_Frequency INTO degeneracy, eLow, freq  
FROM Predictions 
WHERE P_E_ID=eID
AND P_QN_TAG = qnTag 
AND P_QN_Up_1 <=> qn1
AND P_QN_Up_2 <=> qn2
AND P_QN_Up_3 <=> qn3
AND P_QN_Up_4 <=> qn4
AND P_QN_Up_5 <=> qn5
AND P_QN_Up_6 <=> qn6
AND P_Archive=0
limit 1;
IF (energy IS NULL) AND (freq is not NULL) THEN
  set energy=ROUND(eLow + (freq/29979.2458),4);
END IF;
IF energy IS NOT NULL THEN
  INSERT INTO EnergiesTMP 
  (EGY_E_ID, EGY_E_Tag, EGY_Energy, EGY_IDGN, EGY_QN_Tag, EGY_QN1, EGY_QN2, EGY_QN3, EGY_QN4, EGY_QN5, EGY_QN6, EGY_TIMESTAMP)
  VALUES
  (eID, tag, energy, degeneracy, qnTag, qn1, qn2, qn3, qn4, qn5, qn6, now());
  SELECT LAST_INSERT_ID() INTO egyID;
  RETURN egyID;
ELSE
  return(0);
END IF;
END$$

DROP FUNCTION IF EXISTS `F_GetEnergy2`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetEnergy2`(
eID INTEGER,
qnTag INTEGER, 
qn1 INTEGER,
qn2 INTEGER,
qn3 INTEGER,
qn4 INTEGER,
qn5 INTEGER,
qn6 INTEGER
) RETURNS int(11)
    READS SQL DATA
BEGIN

DECLARE egyID INTEGER;
DECLARE energy DOUBLE;
DECLARE eLow DOUBLE;
DECLARE freq DOUBLE;
DECLARE degeneracy INTEGER;
DECLARE unc DOUBLE;
DECLARE pmix DOUBLE;
DECLARE tag INTEGER;

SELECT EGY_ID INTO egyID  
FROM EnergiesTMP
WHERE EGY_E_ID=eID
AND EGY_QN_TAG = qnTag 
AND EGY_QN1 <=> qn1
AND EGY_QN2 <=> qn2
AND EGY_QN3 <=> qn3
AND EGY_QN4 <=> qn4
AND EGY_QN5 <=> qn5
AND EGY_QN6 <=> qn6;

Return egyID;

END$$

DROP FUNCTION IF EXISTS `F_GetIntensity`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetIntensity`(frequency double, lgint double, Q300 double, Qrs double, energyLow double, temperature double) RETURNS double
    NO SQL
    DETERMINISTIC
BEGIN
  Declare kB double;       
  Declare energyUp double; 
  Declare retValue double; 
  set kB=0.69506; 
  
  set energyUp=energyLow + 0.00003335640952 * frequency;
  set retValue = log10 ( pow(10,lgint) * (Q300 / Qrs) *(exp(-energyLow / (kB * temperature)) - exp(-energyUp / (kB * temperature))) / (exp(-energyLow / (kB * 300)) - exp(-energyUp / (kB *
 300))));
  
  return retValue;
END$$

DROP FUNCTION IF EXISTS `F_GetLine`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetLine`(str LONGTEXT, linenum INTEGER) RETURNS varchar(255) CHARSET utf8
    DETERMINISTIC
BEGIN

DECLARE strTo, strBefore LONGTEXT;

SET strTo = substring_index(str,'\n',linenum);

IF linenum = 1 THEN
  RETURN strTo;
END IF;

IF linenum > 1 THEN
  SET strBefore = substring_index(str,'\n',linenum-1);
  RETURN substr(strTo,length(strBefore)+2);
END IF;

RETURN "";

END$$

DROP FUNCTION IF EXISTS `F_GetMoleculeStoichiometricFormula`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetMoleculeStoichiometricFormula`(eID Integer) RETURNS text CHARSET utf8
    READS SQL DATA
BEGIN

DECLARE stoichiometricFormula VARCHAR(100);
DECLARE elementType VARCHAR(100);
DECLARE isotopeNumber INT;
DECLARE occurances INT;
DECLARE charge VARCHAR(10);

DECLARE done INT DEFAULT 0;


DECLARE cur_atomArray CURSOR FOR 
  SELECT AA_ElementType, Count(AA_ID) 
  FROM AtomArray
  WHERE AA_E_ID=eID
  GROUP BY AA_ElementType
  ORDER BY min(AA_IsotopeNumber);
  

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;


SET stoichiometricFormula = "";

OPEN cur_atomArray;
                
REPEAT
 FETCH cur_atomArray INTO elementType, occurances;
 IF NOT done THEN
   SET stoichiometricFormula = CONCAT(stoichiometricFormula, elementType);
   IF (occurances > 1) THEN
      SET stoichiometricFormula = CONCAT(stoichiometricFormula, occurances );
   END IF;
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_atomArray;

SELECT M_FormalCharge INTO charge FROM Molecules join Entries on M_ID=E_M_ID WHERE E_ID=eId;

IF (charge IS NOT NULL) THEN
	SET stoichiometricFormula = CONCAT(stoichiometricFormula,charge);
END IF;

RETURN stoichiometricFormula;

END$$

DROP FUNCTION IF EXISTS `F_GetReferences`$$
CREATE DEFINER=`root`@`%` FUNCTION `F_GetReferences`(fId INTEGER) RETURNS varchar(100) CHARSET utf8
    READS SQL DATA
BEGIN

DECLARE done INT DEFAULT 0;
DECLARE refId INT;
DECLARE retValue VARCHAR(100) DEFAULT "";

DECLARE cur_refs CURSOR FOR
 SELECT RL_R_ID 
  FROM  ReferenceList
  WHERE RL_F_ID=fId;

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;

OPEN cur_refs;
REPEAT
 FETCH cur_refs INTO refId;
 IF NOT done THEN
    SET retValue=CONCAT(retValue,',',refId);
 END IF;
UNTIL done END REPEAT;
CLOSE cur_refs;  

RETURN substr(retValue,2);

END$$

DROP FUNCTION IF EXISTS `F_GetStateQNS_String`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetStateQNS_String`(
eId Integer, 
qnTag Integer,
qn1 Integer,
qn2 Integer,
qn3 Integer,
qn4 Integer,
qn5 Integer,
qn6 Integer) RETURNS varchar(500) CHARSET utf8
    READS SQL DATA
BEGIN
DECLARE done INT DEFAULT 0;
DECLARE retValue VARCHAR(500) DEFAULT "";
DECLARE sid integer;
DECLARE xcase VARCHAR(50);
DECLARE label VARCHAR(50);
DECLARE value VARCHAR(100);
DECLARE spinref VARCHAR(50);
DECLARE attribute VARCHAR(50);
DECLARE cur_qns CURSOR FOR select SQN_ID as Id, SQN_Case as 'Case', SQN_Label as Label, IFNULL(SQN_ValueFloat, IFNULL(SQN_ValueString,IFNULL(F_ReturnQNColumnValue(qn1,qn2,qn3,qn4,qn5,qn6,SQN_ColumnValue,SQN_ColumnValueFunction),NULL))) AS Value, SQN_SpinRef as SpinRef, SQN_Attribute as Attribute
from StateQNXsams 
where SQN_E_ID=eId
and SQN_QN_Tag=qnTag 
and (qn1<=>IFNULL(SQN_QN1,qn1))
and (qn2<=>IFNULL(SQN_QN2,qn2))
and (qn3<=>IFNULL(SQN_QN3,qn3))
and (qn4<=>IFNULL(SQN_QN4,qn4))
and (qn5<=>IFNULL(SQN_QN5,qn5))
and (qn6<=>IFNULL(SQN_QN6,qn6));
DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;
Open cur_qns;
REPEAT
 FETCH cur_qns INTO sid, xcase, label, value, spinref, attribute;
 
 IF NOT done THEN
    SET retValue=CONCAT(retValue, label);
    SET retValue=CONCAT(retValue, ":");
    SET retValue=CONCAT(retValue, value);
    SET retValue=CONCAT(retValue, "\t");
 END IF;
UNTIL done END REPEAT;
                                                                            
CLOSE cur_qns;
RETURN retValue;
END$$

DROP FUNCTION IF EXISTS `F_GetStoichiometricFormula`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_GetStoichiometricFormula`(eID Integer) RETURNS text CHARSET utf8
    READS SQL DATA
BEGIN

DECLARE stoichiometricFormula VARCHAR(100);
DECLARE elementType VARCHAR(100);
DECLARE isotopeNumber INT;
DECLARE occurances INT;
DECLARE charge VARCHAR(10);

DECLARE done INT DEFAULT 0;


DECLARE cur_atomArray CURSOR FOR 
  SELECT AA_ElementType, AA_IsotopeNumber, Count(AA_ID) 
  FROM AtomArray
  WHERE AA_E_ID=eID
  GROUP BY AA_ElementType, AA_IsotopeNumber
  ORDER BY AA_IsotopeNumber;
  

DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;


SET stoichiometricFormula = "";

OPEN cur_atomArray;
                
REPEAT
 FETCH cur_atomArray INTO elementType, isotopeNumber, occurances;
 IF NOT done THEN
   SET stoichiometricFormula = CONCAT(stoichiometricFormula, "(");
   SET stoichiometricFormula = CONCAT(stoichiometricFormula, isotopeNumber);
   SET stoichiometricFormula = CONCAT(stoichiometricFormula, elementType);
   SET stoichiometricFormula = CONCAT(stoichiometricFormula, ")");
   IF (occurances > 1) THEN
      SET stoichiometricFormula = CONCAT(stoichiometricFormula, occurances );
   END IF;
 END IF;
 UNTIL done END REPEAT;
                                                                            
CLOSE cur_atomArray;


SELECT M_FormalCharge INTO charge FROM Molecules join Entries on M_ID=E_M_ID WHERE E_ID=eId;

IF (charge IS NOT NULL) THEN
	SET stoichiometricFormula = CONCAT(stoichiometricFormula,charge);
END IF;

RETURN stoichiometricFormula;

END$$

DROP FUNCTION IF EXISTS `F_Get_Egy_ID`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_Get_Egy_ID`(datID INTEGER,
qnTag INTEGER, 
qn1 INTEGER,
qn2 INTEGER,
qn3 INTEGER,
qn4 INTEGER,
qn5 INTEGER,
qn6 INTEGER
) RETURNS int(11)
    READS SQL DATA
BEGIN

DECLARE egyID INTEGER;


SELECT EGY_ID INTO egyID  
FROM Energies
WHERE EGY_DAT_ID=datID
AND EGY_QN_TAG = qnTag 
AND EGY_QN1 <=> qn1
AND EGY_QN2 <=> qn2
AND EGY_QN3 <=> qn3
AND EGY_QN4 <=> qn4
AND EGY_QN5 <=> qn5
AND EGY_QN6 <=> qn6
limit 1;

IF (egyID is NULL) THEN
    RETURN NULL;
ELSE
  RETURN egyID;
END IF;

END$$

DROP FUNCTION IF EXISTS `F_InsertMoleculeIfNotExists`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_InsertMoleculeIfNotExists`(
Name VARCHAR(200), 
Symbol VARCHAR(250), 
TrivialName VARCHAR(200), 
CAS INT, 
StFormula VARCHAR(200),
Comment LONGTEXT) RETURNS int(11)
    READS SQL DATA
BEGIN
DECLARE mID INT Default 0;
DECLARE notfound INTEGER Default 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET notfound=1;
SET mID=NULL;
SELECT M_ID INTO mID FROM Molecules WHERE M_Name=Name or M_TrivialName=TrivialName or (M_CAS!=0 and M_CAS=CAS) or M_Symbol=Symbol LIMIT 1;
IF notfound=0 THEN
  Return mID;
END IF;
IF Name is NULL THEN
  Return 0;
END IF;
INSERT INTO Molecules 
(M_Name, M_Symbol, M_CAS, M_StoichiometricFormula, M_TrivialName, M_Comment)
VALUES
(Name, Symbol, CAS, StFormula, TrivialName, Comment);
Select LAST_INSERT_ID() INTO mID;
Return mID;
END$$

DROP FUNCTION IF EXISTS `F_InsertParameterIfNotExists`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_InsertParameterIfNotExists`(
eID Integer,
Tag Integer,
Parameter VARCHAR(200),
Value VARCHAR(200)
) RETURNS int(11)
    READS SQL DATA
BEGIN
DECLARE pID INT Default 0;
DECLARE notfound INTEGER Default 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET notfound=1;
IF (Tag is NULL or eID is NULL) THEN
  Return 0;
END IF;
SET pID=NULL;
SELECT PAR_ID INTO pID FROM Parameter WHERE PAR_E_ID=eID and PAR_M_Tag=Tag and PAR_PARAMETER=Parameter;
IF notfound=0 THEN
  Return pID;
END IF;
INSERT INTO Parameter 
(PAR_E_ID, PAR_M_TAG, PAR_PARAMETER, PAR_VALUE)
VALUES
(eID, Tag, Parameter, Value);
Select LAST_INSERT_ID() INTO pID;
Return pID;
END$$

DROP FUNCTION IF EXISTS `F_Partitionfunction`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_Partitionfunction`(Temperature Double, eID int) RETURNS double
    DETERMINISTIC
BEGIN 
  DECLARE QR double DEFAULT 0.0; 
  DECLARE notfound INT DEFAULT 0;
  
  DECLARE pf_cursor CURSOR FOR 
  SELECT PF_Partitionfunction 
    FROM Partitionfunctions
   WHERE PF_E_ID=eID
     AND PF_Temperature=Temperature;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET notfound=1;
    
  OPEN pf_cursor;
  FETCH pf_cursor INTO QR;
  If notfound=1 THEN
     SELECT SUM(Exp(-1.43878*EGY_Energy/Temperature)*EGY_IDGN) INTO QR 
       FROM Energies 
       WHERE EGY_E_ID=eID;  
     If (QR>0) THEN
INSERT INTO Partitionfunctions
           (PF_E_ID, PF_Temperature, PF_Partitionfunction, PF_Comment)
        VALUES (eID, Temperature, QR, "autoinsert");
     
     End If;  
  End If;
    
  Return QR; 
      
END$$

DROP FUNCTION IF EXISTS `F_Partitionfunction2`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_Partitionfunction2`(Temperature Double, eID int) RETURNS double
    DETERMINISTIC
BEGIN 
  DECLARE QR double DEFAULT 0.0; 
  DECLARE notfound INT DEFAULT 0;
  
  DECLARE pf_cursor CURSOR FOR 
  SELECT PF_Partitionfunction 
    FROM Partitionfunctions
   WHERE PF_E_ID=eID
     AND PF_M_ID is not null
     AND PF_Temperature=Temperature;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET notfound=1;
    
  OPEN pf_cursor;
  FETCH pf_cursor INTO QR;
  If notfound=1 THEN
     SELECT SUM(Exp(-1.43878*EGY_Energy/Temperature)*EGY_IDGN) INTO QR 
       FROM Energies 
       WHERE EGY_E_ID=eID;  
     If (QR>0) THEN
INSERT INTO Partitionfunctions
           (PF_E_ID, PF_Temperature, PF_Partitionfunction, PF_Comment)
        VALUES (eID, Temperature, QR, "autoinsert");
     
     End If;  
  End If;
    
  Return QR; 
      
END$$

DROP FUNCTION IF EXISTS `F_ReturnQNColumnValue`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `F_ReturnQNColumnValue`(QN1 Integer,
QN2 Integer,
QN3 Integer,
QN4 Integer,
QN5 Integer,
QN6 Integer,
columnNum Integer,
columnFunc VARCHAR(10)) RETURNS double
    NO SQL
BEGIN
DECLARE RetValue Integer;
IF (columnNum=1) THEN
  SET RetValue=QN1;
ELSEIF (columnNum=1) THEN
  SET RetValue=QN1;
ELSEIF (columnNum=2) THEN
  SET RetValue=QN2;
ELSEIF (columnNum=3) THEN
  SET RetValue=QN3;
ELSEIF (columnNum=4) THEN
  SET RetValue=QN4;
ELSEIF (columnNum=5) THEN
  SET RetValue=QN5;
ELSEIF (columnNum=6) THEN
  SET RetValue=QN6;
ELSE 
  SET RetValue=NULL;
END IF;
IF (columnFunc="abs") THEN
  RETURN abs(RetValue);
ELSEIF (columnFunc="sign") THEN
  IF RetValue<0 THEN
    RETURN -1;
  ELSE
    RETURN +1;
  END IF;
ELSEIF (columnFunc="half") THEN
  RETURN RetValue-0.5;
ELSEIF (IsNumeric(columnFunc))=1 THEN
  RETURN RetValue+columnFunc;
ELSE
  RETURN RetValue;
END IF;
END$$

DROP FUNCTION IF EXISTS `getMolecID`$$
CREATE DEFINER=`root`@`%` FUNCTION `getMolecID`(isoID Integer) RETURNS int(11)
    READS SQL DATA
BEGIN

DECLARE molCount INTEGER;
DECLARE molecID INTEGER;
DECLARE inchikey VARCHAR(200);
DECLARE name VARCHAR(200);

SELECT InChIKey, iso_name INTO inchikey, name FROM Isotopologues WHERE id=isoID;

RETURN 0;
END$$

DROP FUNCTION IF EXISTS `IsNumeric`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `IsNumeric`(sIn varchar(1024)) RETURNS tinyint(4)
    DETERMINISTIC
RETURN sIn REGEXP '^(-|\\+){0,1}([0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+|[0-9]+)$'$$

DELIMITER ;
