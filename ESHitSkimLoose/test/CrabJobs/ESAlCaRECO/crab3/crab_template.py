from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'CRAB_JOB_NAME'
config.General.workArea = 'crab_ESALCARECO'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PYTHONFILE'

config.Data.inputDataset = 'CRAB_DATA_SET1'
config.Data.useParent = True
#config.Data.secondaryDataset = 'CRAB_DATA_SET2'

#config.Data.useParent = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase = '/store/group/dpg_ecal/alca_ecalcalib/ESAlignment/ESALCALRECO_CMSSW_7_4_15_patch1_v2' 
#config.Data.publication = True

config.Site.storageSite = 'T2_CH_CERN'
