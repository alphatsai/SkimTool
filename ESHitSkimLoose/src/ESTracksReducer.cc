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

using namespace std;
//
// constructors and destructor
//
ESTracksReducer::ESTracksReducer(const edm::ParameterSet& iConfig)
{
	std::cout<<"In ESTracksReducer Constructor\n";

	generalTracksLabel_      = iConfig.getParameter< edm::InputTag >("generalTracksLabel");
	generalTracksExtraLabel_ = iConfig.getParameter< edm::InputTag >("generalTracksExtraLabel");
	trackingRecHitLabel_     = iConfig.getParameter< edm::InputTag >("trackingRecHitLabel");
	newGeneralTracksCollection_      = iConfig.getParameter<std::string>("newGeneralTracksCollection");
	newGeneralTracksExtraCollection_ = iConfig.getParameter<std::string>("newGeneralTracksExtraCollection");
	newTrackingRecHitCollection_     = iConfig.getParameter<std::string>("newTrackingRecHitCollection");

	produces<reco::TrackCollection>(newGeneralTracksCollection_);
	produces<reco::TrackExtraCollection>(newGeneralTracksExtraCollection_); 
	produces<TrackingRecHitCollection>(newTrackingRecHitCollection_); 

	evtRun_ = 0;
	totalTracks_ = 0;
	totalRedTracks_ = 0;
}

ESTracksReducer::~ESTracksReducer()
{
	std::cout<<"In ESTracksReducer destructor\n";
}

// ------------ additional functions  ------------
bool ESTracksReducer::TrackSelection( reco::Track track )
{
	if( fabs(track.eta())<3 && fabs(track.eta())>1.5 ) return true;
	else return false;
}

// ------------ method called to for each event  ------------
void ESTracksReducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;
	using namespace std;

	std::cout << "ESTracksReducer:: in analyze(), Event: " <<evtRun_<<std::endl;

	int Ntrack = 0; 
	int NnewTracks = 0; 
	evtRun_++;

	//* Get Tracks' infomaiton 
	edm::Handle<reco::TrackCollection> TrackCol;
		iEvent.getByLabel(generalTracksLabel_,TrackCol);
	edm::Handle<reco::TrackExtraCollection> TrackExtraCol;
		iEvent.getByLabel(generalTracksExtraLabel_,TrackExtraCol);
	edm::Handle<TrackingRecHitCollection> TrackingRecHitCol;
		iEvent.getByLabel(trackingRecHitLabel_,TrackingRecHitCol);

	//* Greate empty collection
	std::auto_ptr<reco::TrackCollection> 	  newGeneralTracksCollection(new reco::TrackCollection);
	std::auto_ptr<reco::TrackExtraCollection> newGeneralTracksExtraCollection(new reco::TrackExtraCollection);
	std::auto_ptr<TrackingRecHitCollection>   newTrackingRecHitCollection(new TrackingRecHitCollection);

	// Select tracks in end cap direction
	Ntrack = TrackCol->size();
	if( TrackCol.isValid() ){ 
		//* Fill new hits and new tracks
		for( reco::TrackCollection::const_iterator itTrack = TrackCol->begin(); itTrack != TrackCol->end(); ++itTrack){
			if( TrackSelection(*itTrack) ){
				// It's not clear if it's necessity for resetting hit pattern before filling new tracks. 
				// However, the result is the same with filling tracks without resetting hit patten.
				// So it may not need to reset hit pattern
				// But here still keep the way doing resetting!
				reco::Track newTrack(*itTrack);
				newTrack.resetHitPattern();
				int iHit=0;
				for( trackingRecHit_iterator itHit = itTrack->recHitsBegin(); itHit != itTrack->recHitsEnd(); ++itHit){
					newTrack.appendHitPattern(**itHit);
					newTrackingRecHitCollection->push_back(**itHit);
					iHit++;
				}
				newGeneralTracksCollection->push_back(newTrack);
				//newGeneralTracksCollection->push_back(*itTrack);
				NnewTracks++;
			}	
		}
		edm::OrphanHandle <TrackingRecHitCollection> ohRH = iEvent.put( newTrackingRecHitCollection, newTrackingRecHitCollection_ );
		edm::RefProd<TrackingRecHitCollection> ohRHProd(ohRH);

		//* connect new hits with trackExtra, and fill new tracksExtra
		int iRefRecHit=0;
		for( int iNewTrack = 0; iNewTrack < NnewTracks; ++iNewTrack){
			reco::Track newTrack = newGeneralTracksCollection->at(iNewTrack);
			//* Only this way works to fill new trackExtra from new tracks
			newGeneralTracksExtraCollection->emplace_back(
					newTrack.outerPosition(),
					newTrack.outerMomentum(),
					newTrack.outerOk(),
					newTrack.innerPosition(),
					newTrack.innerMomentum(),
					newTrack.innerOk(),
					newTrack.outerStateCovariance(),
					newTrack.outerDetId(),
					newTrack.innerStateCovariance(),
					newTrack.innerDetId(),
					newTrack.seedDirection(),
					newTrack.seedRef()
					);
			//* fill the TrackExtra with TrackingRecHitRef
			// unsigned int nHits = tracks->at(k).numberOfValidHits();
			unsigned int nHits = newTrack.recHitsSize();
			newGeneralTracksExtraCollection->back().setHits( ohRHProd, iRefRecHit, nHits);
			iRefRecHit += nHits;
		}	 
		edm::OrphanHandle<reco::TrackExtraCollection> ohTE = iEvent.put(newGeneralTracksExtraCollection, newGeneralTracksExtraCollection_);

		//* connect tracksExtra and tracks
		for( int iNewTrack = 0; iNewTrack < NnewTracks; iNewTrack++){
			const reco::TrackExtraRef newTrackExtraRef(ohTE,iNewTrack);
			newGeneralTracksCollection->at(iNewTrack).setExtra(newTrackExtraRef);
		}
		iEvent.put( newGeneralTracksCollection, newGeneralTracksCollection_ );

	}else{
		iEvent.put( newGeneralTracksCollection, 	newGeneralTracksCollection_ );
		iEvent.put( newGeneralTracksExtraCollection, 	newGeneralTracksExtraCollection_);
		iEvent.put( newTrackingRecHitCollection, 	newTrackingRecHitCollection_);

	}

	totalTracks_+=Ntrack;
	totalRedTracks_+=NnewTracks;
	cout << " number of EndCap tracks " << NnewTracks << "/"<< Ntrack << endl;

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
