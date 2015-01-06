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

#include "TROOT.h"

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
  Double_t _TrackPt[10], _TrackEta[10], _TrackPhi[10]; 
  Double_t _TrackVx[10], _TrackVy[10], _TrackVz[10]; 
  Double_t _TrackOuterZ[10]; 
  Double_t _TrackOuterEta[10]; 
  Double_t _TrackOuterPhi[10]; 
  int _TrackNHit[10]; 
  Double_t _TrackNChi2[10];  
  int _TrackCharge[10]; 
  float _Trackd0[10];
  double _TrackPtError[10]; 
  int _TrackQuality[10]; 
};

#endif
