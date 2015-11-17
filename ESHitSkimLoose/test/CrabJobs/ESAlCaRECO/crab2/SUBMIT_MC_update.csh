#!/bin/tcsh
##############################################################
#    This is the bprimeKit Production submit crab script     #
#    release:CMSSW_5_3_X                                     #
#    Please check the name of configure file and .cfg !!     #
##############################################################
if( $3 == "" ) then
    echo ">> [INFO] Please input configure file, crab.cfg and datacard"
    exit
endif
if( !( -e $1 ) ) then
    echo ">> [ERROR] There is no $1"
    exit
endif
if( !( -e $2 ) ) then
    echo ">> [ERROR] There is no $2"
    exit
endif
if( !( -e $3 ) ) then
    echo ">> [ERROR] There is no $3"
    exit
endif
set CFGPY=$1
set CRABCFG=$2
set DATACARD=$3

################## check the log forder ######################
if ( !( -e log_create_Forder )) then
        mkdir log_create_Forder
endif

################## create the log files ######################
rm -f log1 log2 log3 log4 log5 crab.cfg
set log=log_create_Forder/log_`date +%m_%d_%H%M`
echo `date` > $log
echo "\nAlready exited forder and $CFGPY :"             > log1
echo "\nAlready exited forder but Create new $CFGPY :" > log2
echo "\nCreate new forder and new $CFGPY :"            > log3
echo "\nAlready exited crab.cfg " > log4
echo "\nCreate new crab.cfg "          > log5

########### check oringin bprime.py and $CRABCFG ##########
if ( !( -e $CFGPY ) && !( -e $CRABCFG)) then
        echo 'Here is no $CFGPY  , please put it here!' >> $log 
        echo 'Here is no $CRABCFG  , please put it here!' >> $log 
        cat $log
        rm -f log1 log2 log3
        exit
else \
if ( !( -e $CFGPY ) &&  ( -e $CRABCFG)) then
        echo 'Here is no $CFGPY  , please put it here!' >> $log 
        cat $log
        rm -f log1 log2 log3
        exit

else \
if (  ( -e $CFGPY ) && !( -e $CRABCFG)) then
        echo 'Here is no $CRABCFG  , please put it here!' >> $log 
        cat $log
        rm -f log1 log2 log3
        exit
endif        

################ start to input the MC lists #################
################ start to submit the jobs Ya ################
#setenv SCRAM_ARCH slc5_amd64_gcc462                            ##CMSSW_5_3_X
cmsenv
source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh           ##crab
voms-proxy-init -voms cms -valid 192:0                         ##certificate

set production_FOLDER=SUBMIT_MC
set lists=`cat $DATACARD`
set EOS_folder=ESALCALRECO_CMSSW_7_4_15_patch4_v2

foreach li($lists)
        #set name=`echo $li_ | awk -F ";" '{print $2}'`
        ############# mkdir BHfolder and copy $CFGPY  #############
        #set dir=`echo $li | sed 's/\//_/g' | sed 's/^_//g' | sed 's/_$//g' `
        set dir=`echo $li | awk -F "/" '{print $2"_"$3}'`
        set dir_=./$production_FOLDER/$dir 
        echo "$dir"
        if (  ( -e $dir_) &&  ( -e $dir_/$CFGPY )) then
                echo "MC_FOLDER    : Done!"
                echo "$CFGPY  : Done!"
                echo "$dir" >> log1
        else \
        if (  ( -e $dir_) && !( -e $dir_/$CFGPY )) then
                cp $CFGPY  $dir_
                echo "MC_FOLDER    : Done!"
                echo "$CFGPY  : Create!"
                echo "$dir" >> log2
        else \
        if ( !( -e $dir_) && !( -e $dir_/$CFGPY  )) then
                mkdir -p ./$production_FOLDER/$dir
                cp $CFGPY  $dir_        
                echo "MC_FOLDER    : Create!"
                echo "$CFGPY  : Create!"
                echo "$dir" >> log3
        endif

        ################# built the crab.cfg to forder ################## 
        if (  ( -e $dir_/crab.cfg)) then
                echo "crab.cfg     : Done!"
                echo "$dir" >> log4
                continue
        else
                set lt_c=`echo $li | sed 's/\//\\\//g'`  #let / be \/
                sed "s/DATASETS/$lt_c/g" $CRABCFG \
                | sed "s/EOS_folder/$EOS_folder/g"   \
                | sed "s/MC_subFOLDER/$dir/g"        \
                | sed "s/CRAB_Project/$dir/g"        \
                >  crab.cfg
                mv crab.cfg $dir_
                echo "crab.cfg     : Create!"
                echo "$dir" >> log5
        endif
        ######################### Submit jobs ############################ 
        cd $dir_
        crab -create -cfg crab.cfg | tee -a log_$dir
        set JobNumber_=`grep "crab:  Total" log_$dir | grep "jobs created"| awk '{print $4}'| head -n 1`
        set checkJobNumber_=`grep "crab:  Total" log_$dir | grep "jobs created"| awk '{print $4}'| head -n 1 | wc | awk '{print $1}' `

        if ( $checkJobNumber_ != "0" ) then
                if ( $JobNumber_ < 500 ) then
                      crab -submit -c $dir
                else if ( $JobNumber_ <= 5000 ) then
                       set counter_=1
                       set counterEnd_=0
                       while ( $counter_ < $JobNumber_ )
                            @ counterEnd_=$counterEnd_ + 400
                            if ( $counterEnd_ > $JobNumber_ ) then
                                @ counterEnd_=$JobNumber_
                            endif
                                crab -submit ${counter_}-${counterEnd_} -c $dir
                                @ counter_=$counter_ + 400
                        end
                else 
                        echo ">> [ERROR] Too many jobs $JobNumber_ > 5000"
                        #set counter_=1
                        #set counterEnd_=0
                        #while ( $counter_ < 5000 )
                              #        @ counterEnd_=$counterEnd_ + 400
                              #        #crab -submit ${counter_}-${counterEnd_} -c $dir
                              #        @ counter_=$counter_ + 400
                        #end
                endif
        else
                echo ">> [WARNING] No matched site for $dir"
        endif
        cd -
end #finish
rm -f crab.cfg
cat log1 >> $log ; rm -f log1
cat log2 >> $log ; rm -f log2
cat log3 >> $log ; rm -f log3
cat log4 >> $log ; rm -f log4
cat log5 >> $log ; rm -f log5

