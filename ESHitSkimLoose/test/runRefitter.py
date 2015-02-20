import FWCore.ParameterSet.Config as cms

process = cms.Process("REFIT")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

########## Debug message ##############
#process.MessageLogger = cms.Service("MessageLogger",
#                     destinations =  cms.untracked.vstring('debugmessages'),
#                     #categories   = cms.untracked.vstring('interestingToMe'),
#                     categories   = cms.untracked.vstring('TrackRefitter'),
#                     debugModules = cms.untracked.vstring('*'),
#
#                     debugmessages = cms.untracked.PSet(
#                                      #threshold =  cms.untracked.vstring('DEBUG'),
#                                      #INFO      =  cms.untracked.int32(1),
#                                      #DEBUG   = cms.untracked.int32(0),
#                                      #interestingToMe = cms.untracked.int32(10000000)
#                    )
#)


###################### Modify following Global tag ################################
######################       This is example       ################################
#	https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
process.GlobalTag.globaltag = 'POSTLS170_V5::All'
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
process.TrackRefitter.src = "ESTracksReducer"

################### Input file #############################
from inputFiles_cfi import * #FileNames
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:ESRedSkim.root")
    #fileNames = cms.untracked.vstring(FileNames)
    #fileNames = cms.untracked.vstring(FileNames_SkimPionGun)
    #fileNames = cms.untracked.vstring(FileNames_PionGunTest)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
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

