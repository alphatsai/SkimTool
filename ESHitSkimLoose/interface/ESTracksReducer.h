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
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

class ESTracksReducer : public edm::EDProducer
{
public:
  explicit ESTracksReducer(const edm::ParameterSet&);
  virtual ~ESTracksReducer();

protected:
  virtual void beginJob();
  virtual void produce(edm::Event &, const edm::EventSetup & );
  virtual void endJob();
  bool TrackSelection( reco::Track track ); 

  edm::InputTag generalTracksLabel_;
  edm::InputTag generalTracksExtraLabel_;
  edm::InputTag trackingRecHitLabel_;
  std::string newGeneralTracksCollection_; 
  std::string newGeneralTracksExtraCollection_; 
  std::string newTrackingRecHitCollection_; 
 
  int evtRun_;
  int totalTracks_;
  int totalRedTracks_;

};

#endif
