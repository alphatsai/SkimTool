from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'CRAB_JOB_NAME'
config.General.workArea = 'crab_ESALCARECO_v2'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PYTHONFILE'
config.JobType.outputFiles  = ['EcalESAlign.root']
config.JobType.disableAutomaticOutputCollection = True

config.Data.lumiMask = '/afs/cern.ch/work/j/jtsai/ESAlignment/CMSSW_8_0_7_patch3/src/SkimTool/ESHitSkimLoose/test/CrabJobs/ESAlCaRECO/crab3/ecal_good_runs_Bon_20160509.json'
config.Data.inputDataset = 'CRAB_DATA_SET1'
#config.Data.useParent = True
#config.Data.secondaryDataset = 'CRAB_DATA_SET2'

config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/dpg_ecal/alca_ecalcalib/ESAlignment/ESALCALRECO_CMSSW_8_0_7_patch3_v2' 
config.Data.publication = True

config.Site.storageSite = 'T2_CH_CERN'
