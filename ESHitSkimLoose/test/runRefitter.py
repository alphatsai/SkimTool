import FWCore.ParameterSet.Config as cms

process = cms.Process("REFIT")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

########## Change to new global tag ###############
process.GlobalTag.globaltag = 'POSTLS170_V6::All'
#process.newTKAlignment = cms.ESSource("PoolDBESSource",
#                                        process.CondDBSetup,
#                                        connect = cms.string('frontier://FrontierProd/CMS_COND_31X_ALIGNMENT'),
#                                        timetype = cms.string('runnumber'),
#                                        toGet = cms.VPSet(cms.PSet(
#                                                record = cms.string('TrackerAlignmentRcd'),
#                                                tag = cms.string('TrackerAlignment_GR10_v4_offline')
#                                                ))
#                                        )
#process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource", "newTKAlignment")
#
#process.newGlobalPosition = cms.ESSource("PoolDBESSource",
#                                          process.CondDBSetup,
#                                          connect = cms.string('frontier://FrontierProd/CMS_COND_31X_ALIGNMENT'),
#                                          toGet= cms.VPSet(cms.PSet(record = cms.string("GlobalPositionRcd"),
#                                                                     tag = cms.string('GlobalAlignment_TkRotMuonFromLastIovV2_offline'))
#                                                           )
#                                         )
#process.es_prefer_GlobalPositionDB = cms.ESPrefer("PoolDBESSource", "newGlobalPosition")

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
################### Input file #############################
from inputFiles_cfi import * #FileNames
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring(FileNames)
    #fileNames = cms.untracked.vstring(FileNames_SkimPionGun)
    fileNames = cms.untracked.vstring(FileNames_PionGunTest)
    #fileNames = cms.untracked.vstring('file:JET2011A_ESSkim_P1.root')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(2)
)

################### Define process #########################
#process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
#process.TrackRefitter.constraint = ""
#process.TrackRefitter.src = "doConstraint"
process.out = cms.OutputModule("PoolOutputModule",
     outputCommands = cms.untracked.vstring('keep *'),
     fileName = cms.untracked.string('Refitter.root')
)

process.p = cms.EndPath(process.out)
#process.p1 = cms.Path(process.doConstraint * process.TrackRefitter) 
process.p1 = cms.Path(process.TrackRefitter) 
process.schedule = cms.Schedule( process.p1 , process.p)

