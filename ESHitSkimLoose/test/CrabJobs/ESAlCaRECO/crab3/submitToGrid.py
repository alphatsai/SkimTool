#!/usr/bin/env python
import optparse
import os,sys
import commands
import time, datetime

CMSEOSECAL_ESAL='/store/group/dpg_ecal/alca_ecalcalib/ESAlignment'

"""
creates the crab cfg and submits the job
"""
def submitProduction( name, lfnDirBase, dataset, isData, cfg, workDir, lumiMask, submit=False):
    
    os.system("rm -rvf %s/*%s* "%( workDir, name))
    crabConfigFile=workDir+'/'+name+'_cfg.py'
    config_file=open(crabConfigFile,'w')
    config_file.write('from WMCore.Configuration import Configuration\n')
    config_file.write('import os\n')
    config_file.write('config = Configuration()\n')
    config_file.write('\n')
    config_file.write('config.section_("General")\n')
    config_file.write('config.General.requestName = "%s"\n' % name)
    config_file.write('config.General.workArea = "%s"\n' % workDir)
    config_file.write('config.General.transferOutputs=True\n')
    config_file.write('config.General.transferLogs=True\n')
    config_file.write('\n')
    config_file.write('config.section_("JobType")\n')
    config_file.write('config.JobType.pluginName = "Analysis"\n')
    config_file.write('config.JobType.psetName = "'+cfg+'"\n')
    config_file.write('config.JobType.disableAutomaticOutputCollection = True\n')
    config_file.write('config.JobType.outputFiles = [\'EcalESAlign.root\']\n')
    config_file.write('\n')
    config_file.write('config.section_("Data")\n')
    config_file.write('config.Data.inputDataset = "%s"\n' % dataset)
    config_file.write('config.Data.inputDBS = "global"\n')
    if isData : 
        config_file.write('config.Data.splitting = "LumiBased"\n')
        config_file.write('config.Data.unitsPerJob = 1\n')
        if lumiMask:
            config_file.write('config.Data.lumiMask = \'%s\'\n' %lumiMask)
    else : 
        config_file.write('config.Data.splitting = "FileBased"\n')
        config_file.write('config.Data.unitsPerJob = 10\n')
    config_file.write('config.Data.publication = True\n')
    config_file.write('config.Data.ignoreLocality = False\n')
    config_file.write('config.Data.outLFNDirBase = \'%s\'\n' % lfnDirBase)
    config_file.write('\n')
    config_file.write('config.section_("Site")\n')
    config_file.write('config.Site.storageSite = "T2_CH_CERN"\n')
    config_file.close()
    
    if submit : os.system('crab submit -c %s' % crabConfigFile )

"""
steer the script
"""
def main():
    
    # usage description
    usage = """Usage: ./submitToGrid.py [options]\n
    Example: ./submitToGrid.py -w myWorkDir -i inputSamplelist.txt -s /store/group/dpg_ecal/alca_ecalcalib/ESAlignment/storagePath -c myConfig_cfg.py -S \n
    For more help: ./submitToGrid.py --help
    """

    #configuration
    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--cfg',         dest='cfg'   ,      help='cfg to be sent to grid',         default=None,            type='string'      )
    parser.add_option('-i', '--inputList',   dest='inputList',   help='list of files',                  default=None,            type='string'      )
    parser.add_option('-j', '--jsonLumi',    dest='lumiMask',    help='json with list of good lumis',   default=None,            type='string'      )
    parser.add_option('-w', '--workDir',     dest='workDir',     help='working directory',              default=None,            type='string'      )
    parser.add_option('-s', '--lfn',         dest='lfn',         help='base lfn to store outputs',      default=CMSEOSECAL_ESAL, type='string'      )
    parser.add_option('-S', '--submit',      dest='submit',      help='submit jobs',                    default=False,           action='store_true')
    (opt, args) = parser.parse_args()

    if not opt.inputList or not opt.cfg:
        print usage
        sys.exit()

    #read list of samples
    samplesList = open(opt.inputList,'r')

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M')

    lfnDirBase = opt.lfn
    if lfnDirBase == CMSEOSECAL_ESAL:
        lfnDirBase =('%s/%s')%( opt.lfn, st )

    if not opt.workDir:
        opt.workDir = 'crab_%s'%st
        
            
    #submit jobs
    os.system("mkdir -p %s" % opt.workDir)
    for line in samplesList.readlines():
        info = line.strip().split() 
        if (len(info)==0 or info[0][0]=='#'): continue
        submitProduction( 
                          name       = info[0],
                          lfnDirBase = lfnDirBase,
                          dataset    = info[2],
                          isData     = info[1],
                          lumiMask   = os.path.realpath(opt.lumiMask),
                          cfg        = opt.cfg,
                          workDir    = opt.workDir,
                          submit     = opt.submit
                        )

    samplesList.close()
    print 'crab cfg files have been created under %s' % opt.workDir
    if opt.submit:
        print 'Jobs have been submitted'
        print 'Monitor jobs with http://dashb-cms-job.cern.ch/dashboard/templates/task-analysis/ or locally with crab'
        print 'Output will be found in %s' % lfnDirBase

"""
for execution from another script
"""
if __name__ == "__main__":
    sys.exit(main())
