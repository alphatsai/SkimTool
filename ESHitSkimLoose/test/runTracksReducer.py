import FWCore.ParameterSet.Config as cms

process = cms.Process("TRKRED")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.load("SkimTool.ESHitSkimLoose.ESTracksReducer_cfi")

################### global tag #############################
#process.GlobalTag.globaltag = 'POSTLS170_V5::All'
process.GlobalTag.globaltag = 'GR_R_74_V1A::All'  #for RECO data CMSSW_7_4_0_pre6 with condition=auto::run2_data
#process.GlobalTag.globaltag = 'MCRUN2_74_V1::All'  #for RECO MC CMSSW_7_4_0_pre6 with condition=auto::run2_mc

################### Input file #############################
from inputFiles_cfi import * #FileNames
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(FileNames)
    #fileNames = cms.untracked.vstring('file:ESHitsEvtSkim.root')
    #fileNames = cms.untracked.vstring(FileNames_PionGunTest)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

################### Define process #########################
process.esGeneralTracks = process.ESTracksReducer.clone()
process.myPath = cms.Path(process.esGeneralTracks)
process.mySelection = cms.PSet(
 SelectEvents = cms.untracked.PSet(
       SelectEvents = cms.vstring('myPath')
 )
)
process.out = cms.OutputModule("PoolOutputModule",
     process.mySelection,
     outputCommands = cms.untracked.vstring('drop *',
       'keep *_ecalPreshowerRecHit_*_*',
       'keep *_esGeneralTracks_*_*', # new collections from generalTracks
       #'keep *_ESTracksReducer_*_*',
       #'keep *_generalTracks_*_*',
       'keep *_offlineBeamSpot_*_*',
       'keep *_siPixelClusters_*_*',
       'keep *_siStripClusters_*_*',
       'keep *_siStripDigis_*_*', #NEW!!
      ),
     fileName = cms.untracked.string('ESTrkRed.root')
)
 
process.p = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.myPath,process.p)
