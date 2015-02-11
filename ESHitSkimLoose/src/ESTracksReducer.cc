// -*- C++ -*-
//
// Package:    ESTracksReducer
// Class:      ESTracksReducer
//
/**\class ESTracksReducer ESTracksReducer.cc SkimTool/ESHitSkimLoose/src/ESTracksReducer.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Author: Jui-Fa 
//

#include "SkimTool/ESHitSkimLoose/interface/ESTracksReducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/TrackReco/interface/TrackExtraFwd.h"
#define GEN 0

using namespace std;
//
// constructors and destructor
//
ESTracksReducer::ESTracksReducer(const edm::ParameterSet& iConfig)
{
  std::cout<<"In ESTracksReducer Constructor\n";

  generalTracksLabel_      = iConfig.getParameter< edm::InputTag >("generalTracksLabel");
  generalTracksExtraLabel_ = iConfig.getParameter< edm::InputTag >("generalTracksExtraLabel");
  trackingHitsLabel_       = iConfig.getParameter< edm::InputTag >("trackingHitsLabel");
  redGeneralTrackCollection_      = iConfig.getParameter<std::string>("redGeneralTrackCollection");
  redGeneralTrackExtraCollection_ = iConfig.getParameter<std::string>("redGeneralTrackExtraCollection");
  redTrackingRecHitCollection_    = iConfig.getParameter<std::string>("redTrackingRecHitCollection");

  produces<reco::TrackCollection>(redGeneralTrackCollection_);
  produces<reco::TrackExtraCollection>(redGeneralTrackExtraCollection_); 
  produces<TrackingRecHitCollection>(redTrackingRecHitCollection_); 

  evtRun_ = 0;
  totalTracks_ = 0;
  totalRedTracks_ = 0;
}

ESTracksReducer::~ESTracksReducer()
{
 std::cout<<"In ESTracksReducer destructor\n";
}

// ------------ method called to for each event  ------------
void ESTracksReducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace std;

  std::cout << "ESTracksReducer:: in analyze()." << std::endl;
  
  int Ntrack = 0; 
  int NredTracks = 0; 
  evtRun_++;

  // Get Tracks' infomaiton 
  edm::Handle<reco::TrackCollection> TrackCol;
  	iEvent.getByLabel(generalTracksLabel_,TrackCol);
  edm::Handle<reco::TrackExtraCollection> TrackExtraCol;
   	iEvent.getByLabel(generalTracksExtraLabel_,TrackExtraCol);
  edm::Handle<TrackingRecHitCollection> TrackingRecHitCol;
   	iEvent.getByLabel(trackingHitsLabel_,TrackingRecHitCol);

  // Greate empty collection
  std::auto_ptr<reco::TrackCollection> 	    redGeneralTracksCollection(new reco::TrackCollection);
  std::auto_ptr<reco::TrackExtraCollection> redGeneralTracksExtraCollection(new reco::TrackExtraCollection);
  std::auto_ptr<TrackingRecHitCollection>   redTrackingRecHitCollection(new TrackingRecHitCollection);

  // this is needed to get the ProductId of the TrackExtra and TrackingRecHit collections
  reco::TrackExtraRefProd refTrackExtras    = const_cast<edm::Event&>( iEvent ).getRefBeforePut<reco::TrackExtraCollection>(redGeneralTrackExtraCollection_);
  TrackingRecHitRefProd   refTrackingRecHit = const_cast<edm::Event&>( iEvent ).getRefBeforePut<TrackingRecHitCollection>(redTrackingRecHitCollection_);
 
  // Select tracks in end cap direction
  if( TrackCol.isValid() ){
	  for( reco::TrackCollection::const_iterator itTrack = TrackCol->begin(); itTrack != TrackCol->end(); ++itTrack)
	  {
		  if( fabs(itTrack->eta())<3 && fabs(itTrack->eta())>1.5 ){
			  std::cout<<"No "<<Ntrack<<", Eta "<<itTrack->eta()<<", Keep!"<<endl;
	   		  //Fill track and trackExtras	
			  redGeneralTracksCollection->push_back(*itTrack);	
			  redGeneralTracksExtraCollection->push_back(*(itTrack->extra()));	
			  redGeneralTracksCollection->back().setExtra( reco::TrackExtraRef( refTrackExtras, redGeneralTracksExtraCollection->size()-1));
			  NredTracks++;
			  //Fill tracking rec hits, reference to trackExtras  
			  for( trackingRecHit_iterator iHit = itTrack->recHitsBegin(); iHit != itTrack->recHitsEnd(); ++iHit){
				redTrackingRecHitCollection->push_back(**iHit);
			        redGeneralTracksExtraCollection->back().add( TrackingRecHitRef( refTrackingRecHit, redTrackingRecHitCollection->size()-1));
			  }	
		  }else{
			  std::cout<<"No "<<Ntrack<<", Eta "<<itTrack->eta()<<", Drop!"<<endl;
		  }
		  Ntrack++;
	  }
  }
  totalTracks_+=Ntrack;
  totalRedTracks_+=NredTracks;
  cout << " number of EndCap tracks " << NredTracks << "/"<< Ntrack << endl;

  iEvent.put( redGeneralTracksCollection, 	redGeneralTrackCollection_ );
  iEvent.put( redGeneralTracksExtraCollection, 	redGeneralTrackExtraCollection_);
  iEvent.put( redTrackingRecHitCollection, 	redTrackingRecHitCollection_);
}

// ------------ method called once each job just before starting event loop  ------------
void
ESTracksReducer::beginJob()
{
 std::cout<<"In ESTracksReducer.beginJob\n";
}

// ------------ method called once each job just after ending the event loop  ------------
void
ESTracksReducer::endJob() {
  std::cout<<"In ESTracksReducer.endJob\n";
  cout << endl;
  cout << " ------------- ESTracksReducer ---------------- " << endl;
  cout << " --------------------------------------------- " << endl;
  cout << " number of events processed  " << evtRun_ << endl; 
  cout << " number of tracks " << totalTracks_ << endl; 
  cout << " number of reduced tracks " << totalRedTracks_ << endl; 
  cout << " --------------------------------------------- " << endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(ESTracksReducer);
