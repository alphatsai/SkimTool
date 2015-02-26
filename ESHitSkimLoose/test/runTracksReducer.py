import FWCore.ParameterSet.Config as cms

process = cms.Process("ESSKIM")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.load("SkimTool.ESHitSkimLoose.ESTracksReducer_cfi")

################### global tag #############################
process.GlobalTag.globaltag = 'POSTLS170_V5::All'

################### Input file #############################
from inputFiles_cfi import * #FileNames
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring(FileNames)
    #fileNames = cms.untracked.vstring(FileNames_PionGunTest)
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/j/jtsai/generateSamples/CMSSW_7_4_0_pre6/src/DoubleElectron-Run2012D/reco_RAW2DIGI_RECO_100.root')
)
process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(3)
    #input = cms.untracked.int32(100)
    input = cms.untracked.int32(-1)
)

################### Define process #########################
#process.myFilter = cms.EDFilter('ESHitSkimLoose')
#process.myfilter = cms.Sequence(process.myFilter)
#process.myPath = cms.Path(process.ESTracksReducer, process.myfilter)
process.myPath = cms.Path(process.ESTracksReducer)
process.mySelection = cms.PSet(
 SelectEvents = cms.untracked.PSet(
       SelectEvents = cms.vstring('myPath')
 )
)
process.out = cms.OutputModule("PoolOutputModule",
     process.mySelection,
     outputCommands = cms.untracked.vstring('drop *',
       'keep *_ecalPreshowerRecHit_*_*',
       'keep *_ESTracksReducer_*_*',
       #'keep *_generalTracks_*_*',
       'keep *_offlineBeamSpot_*_*',
       'keep *_siPixelClusters_*_*',
       'keep *_siStripClusters_*_*',
       'keep *_siStripDigis_*_*', #NEW!!
      ),
     fileName = cms.untracked.string('ESRedSkim.root')
)
 
process.p = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.myPath,process.p)
