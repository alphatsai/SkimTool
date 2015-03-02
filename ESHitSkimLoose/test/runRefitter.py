import FWCore.ParameterSet.Config as cms

process = cms.Process("REFIT")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

###################### Modify following Global tag ################################
######################       This is example       ################################
#	https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
#process.GlobalTag.globaltag = 'POSTLS170_V5::All'
process.GlobalTag.globaltag = 'GR_R_74_V1A::All'  #for RECO data CMSSW_7_4_0_pre6 with condition=auto::run2_data
### Add or change spacial parameters from DB
#process.TrackerAlignment2009 = cms.ESSource("PoolDBESSource",
#                                          process.CondDBSetup,
#                                          connect = cms.string('frontier://PromptProd/CMS_COND_31X_ALIGNMENT'),
#                                          toGet= cms.VPSet(cms.PSet(record = cms.string("TrackerAlignmentRcd"),
#                                                                     tag = cms.string('TrackerAlignment_2009_v1_prompt'))
#                                                           )
#					 )
#process.es_prefer_TrackerAlignment2009 = cms.ESPrefer("PoolDBESSource", "TrackerAlignment2009")

#process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi") #NEW!! 
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.NavigationSchool = ""
process.TrackRefitter.src = "ESTracksReducer" # Default is generalTracks

################### Input file #############################
from inputFiles_cfi import * #FileNames
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(FileNames)
    #fileNames = cms.untracked.vstring(FileNames_PionGunTest)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

################### Define process #########################
process.out = cms.OutputModule("PoolOutputModule",
     outputCommands = cms.untracked.vstring('keep *'),
     fileName = cms.untracked.string('Refitter.root')
)

process.p = cms.EndPath(process.out)
process.p1 = cms.Path(process.TrackRefitter)
#process.p1 = cms.Path(process.MeasurementTrackerEvent #NEW!!
#                     *process.TrackRefitter)  
process.schedule = cms.Schedule( process.p1 , process.p)

