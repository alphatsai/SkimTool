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
  redGeneralTrackCollection_      = iConfig.getParameter<std::string>("redGeneralTrackCollection");
  redGeneralTrackExtraCollection_ = iConfig.getParameter<std::string>("redGeneralTrackExtraCollection");

  produces<reco::TrackCollection>(redGeneralTrackCollection_);
  produces<reco::TrackExtraCollection>(redGeneralTrackExtraCollection_); 

  evtRun_ = 0;
  restEvt_ = 0;
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
  int NECtrack = 0; 
  evtRun_++;

  // Get reco Tracks 
  edm::Handle<reco::TrackCollection> TrackCol;
  	iEvent.getByLabel(generalTracksLabel_,TrackCol);
  edm::Handle<reco::TrackExtraCollection> TrackExtraCol;
  	iEvent.getByLabel(generalTracksExtraLabel_,TrackExtraCol);

  // Greate empty collection
  std::auto_ptr<reco::TrackCollection> redGeneralTracksCollection(new reco::TrackCollection);
  std::auto_ptr<reco::TrackExtraCollection> redGeneralTracksExtraCollection(new reco::TrackExtraCollection);
 
  // Select tracks in end cap direction 
  for( reco::TrackCollection::const_iterator itTrack = TrackCol->begin(); itTrack != TrackCol->end(); ++itTrack)
  {
     if( fabs(itTrack->eta())<3 && fabs(itTrack->eta())>1.5 ){
	std::cout<<"No "<<Ntrack<<", Eta "<<itTrack->eta()<<", Keep!"<<endl;
        redGeneralTracksCollection->push_back(*itTrack);	
	//if(TrackExtraCol.isValid()){ 
	  // cout<<" TrackExtras is valided"<<endl;	
	   redGeneralTracksExtraCollection->push_back(*(itTrack->extra()));	
	//}
	NECtrack++;

     }else{
	std::cout<<"No "<<Ntrack<<", Eta "<<itTrack->eta()<<", Drop!"<<endl;
     }
     Ntrack++;
  }
  cout << " number of EndCap tracks " << NECtrack << "/"<< Ntrack << endl;

  iEvent.put( redGeneralTracksCollection, redGeneralTrackCollection_ );
  iEvent.put( redGeneralTracksExtraCollection, redGeneralTrackExtraCollection_);
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
  cout << " Skimed Event number # " << restEvt_ << endl; 
  cout << " --------------------------------------------- " << endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(ESTracksReducer);
