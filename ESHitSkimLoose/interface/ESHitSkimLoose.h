#ifndef AlignmentTool_ESHitSkimLoose_h
#define AlignmentTool_ESHitSkimLoose_h

// system include files
#include <memory>
#include <fstream>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "TROOT.h"

using namespace edm;
using namespace reco;   
using namespace std; 

class ESHitSkimLoose : public edm::EDFilter
{
public:
  explicit ESHitSkimLoose(const edm::ParameterSet&);
  virtual ~ESHitSkimLoose();

protected:
  virtual void beginJob() ;
  virtual bool filter(edm::Event &, const edm::EventSetup & );
  virtual void endJob() ;

  int _evt_run; 
  int _runNum, _evtNum, _restEvt;
  int Nesrh; 
  int Ntrack;

  edm::EDGetTokenT<TrackCollection> generalTracksLabel_;	 
  edm::EDGetTokenT<ESRecHitCollection> esRecHitLabel_;	 
};

#endif
