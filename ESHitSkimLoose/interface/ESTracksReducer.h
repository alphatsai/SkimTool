#ifndef AlignmentTool_ESTracksReducer_h
#define AlignmentTool_ESTracksReducer_h

// system include files
#include <memory>
#include <fstream>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class ESTracksReducer : public edm::EDProducer
{
public:
  explicit ESTracksReducer(const edm::ParameterSet&);
  virtual ~ESTracksReducer();

protected:
  virtual void beginJob() ;
  virtual void produce(edm::Event &, const edm::EventSetup & );
  virtual void endJob() ;

  edm::InputTag generalTracksLabel_;
  edm::InputTag generalTracksExtraLabel_;
  std::string redGeneralTrackCollection_; 
  std::string redGeneralTrackExtraCollection_; 
 
  int evtRun_;
  int restEvt_;

};

#endif
