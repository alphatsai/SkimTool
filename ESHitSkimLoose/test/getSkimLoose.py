import FWCore.ParameterSet.Config as cms

process = cms.Process("ESSKIM")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

################### global tag #############################
process.GlobalTag.globaltag = 'GR_P_V14::All'
############################################################
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	'file:/data/chiyi/ESAlignment/CMSSW_4_1_2/src/DATAFiles/JetPD2011A_PromptReco-v1/DAACC74C-DF57-E011-A45D-001D09F2B30B.root'
  )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(3000)
)
process.myFilter = cms.EDFilter('ESHitSkimLoose')
process.myfilter = cms.Sequence(process.myFilter)
process.myPath = cms.Path(process.myfilter)
process.mySelection = cms.PSet(
 SelectEvents = cms.untracked.PSet(
       SelectEvents = cms.vstring('myPath')
 )
)

process.out = cms.OutputModule("PoolOutputModule",
     process.mySelection,
     outputCommands = cms.untracked.vstring('drop *',
       'keep *_ecalPreshowerRecHit_*_*',
       'keep *_generalTracks_*_*',
       'keep *_offlineBeamSpot_*_*',
       'keep *_siPixelClusters_*_*',
       'keep *_siStripClusters_*_*',
      ),
     fileName = cms.untracked.string('JET2011A_ESSkim_P1.root')
)
 
process.p = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.myPath,process.p)
