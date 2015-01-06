import FWCore.ParameterSet.Config as cms

process = cms.Process("REFIT")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

########## Change to new global tag ###############
#process.GlobalTag.globaltag = 'POSTLS170_V6::All'
process.GlobalTag.globaltag = 'POSTLS170_V5::All'

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.NavigationSchool = ""

################### Input file #############################
from inputFiles_cfi import * #FileNames
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(FileNames)
    #fileNames = cms.untracked.vstring(FileNames_SkimPionGun)
    #fileNames = cms.untracked.vstring(FileNames_PionGunTest)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5)
)

################### Define process #########################
process.out = cms.OutputModule("PoolOutputModule",
     outputCommands = cms.untracked.vstring('keep *'),
     fileName = cms.untracked.string('Refitter.root')
)

process.p = cms.EndPath(process.out)
process.p1 = cms.Path(process.TrackRefitter) 
process.schedule = cms.Schedule( process.p1 , process.p)

