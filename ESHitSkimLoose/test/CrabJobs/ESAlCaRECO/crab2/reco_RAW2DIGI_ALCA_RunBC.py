# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: reco -s RAW2DIGI,ALCA:EcalESAlign -n 100 --filein=/store/data/Run2015B/SingleElectron/RECO/PromptReco-v1/000/251/252/00000/4E9031DF-9827-E511-8A01-02163E012BD2.root --secondfilein=/store/data/Run2015B/SingleElectron/RAW/v1/000/251/252/00000/1AAD09EE-F725-E511-88E0-02163E0119E4.root,/store/data/Run2015B/SingleElectron/RAW/v1/000/251/252/00000/98219A92-D025-E511-86ED-02163E011CF1.root --data --conditions=74X_dataRun2_Prompt_v2 --nThreads=4 --customise Configuration/DataProcessing/RecoTLR.customiseDataRun2Common --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('ALCA')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.AlCaRecoStreams_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2015B/SingleElectron/RECO/PromptReco-v1/000/251/252/00000/4E9031DF-9827-E511-8A01-02163E012BD2.root'),
    secondaryFileNames = cms.untracked.vstring('/store/data/Run2015B/SingleElectron/RAW/v1/000/251/252/00000/1AAD09EE-F725-E511-88E0-02163E0119E4.root', 
        '/store/data/Run2015B/SingleElectron/RAW/v1/000/251/252/00000/98219A92-D025-E511-86ED-02163E011CF1.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('reco nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('reco_RAW2DIGI_ALCA.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.ALCARECOStreamEcalESAlign = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pathALCARECOEcalESAlign')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('EcalESAlign')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('EcalESAlign.root'),
    outputCommands = cms.untracked.vstring('drop *', 
        'keep *_ecalPreshowerDigis_*_*', 
        'keep *_offlineBeamSpot_*_*', 
        'keep *_siPixelClusters_*_ALCA', 
        'keep *_siStripClusters_*_ALCA', 
        'keep *_ecalAlCaESAlignTrackReducer*_*_*')
)

# Other statements
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOEcalESAlign_noDrop.outputCommands)
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_dataRun2_Prompt_v4', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)
process.ALCARECOStreamEcalESAlignOutPath = cms.EndPath(process.ALCARECOStreamEcalESAlign)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.pathALCARECOEcalESAlign,process.endjob_step,process.RECOSIMoutput_step,process.ALCARECOStreamEcalESAlignOutPath)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.RecoTLR
from Configuration.DataProcessing.RecoTLR import customiseDataRun2Common 

#call to customisation function customiseDataRun2Common imported from Configuration.DataProcessing.RecoTLR
process = customiseDataRun2Common(process)

# End of customisation functions

