// -*- C++ -*-
//
// Package:    ESHitSkimLoose
// Class:      ESHitSkimLoose
//
/**\class ESHitSkimLoose ESHitSkimLoose.cc SkimTool/ESHitSkimLoose/src/ESHitSkimLoose.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Kai-Yi KAO
//         Created:  Sat Jan 30 13:11:07 CET 2010
// $Id: ESHitSkimLoose.cc,v 1.2 2011/05/10 16:13:41 chiyi Exp $
//
//

#include "SkimTool/ESHitSkimLoose/interface/ESHitSkimLoose.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

//using namespace std;
//
// constructors and destructor
//
ESHitSkimLoose::ESHitSkimLoose(const edm::ParameterSet& iConfig)
{
	 std::cout<<"In ESHitSkimLoose Constructor\n";
	 generalTracksLabel_ = consumes<reco::TrackCollection>(iConfig.getParameter< edm::InputTag >("generalTracksLabel"));
	 esRecHitLabel_      = consumes<ESRecHitCollection>(iConfig.getParameter< edm::InputTag >("esRecHitLabel"));

	  _evt_run = 0;
	  _restEvt = 0;
}

ESHitSkimLoose::~ESHitSkimLoose()
{
 std::cout<<"In ESHitSkimLoose destructor\n";
}

// ------------ method called to for each event  ------------
bool ESHitSkimLoose::filter(edm::Event& evt, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace std;

    std::cout << "ESHitSkimLoose:: in analyze(), Event "<<_evt_run << std::endl;
  
  _runNum = evt.id().run();
  _evtNum = evt.id().event();
  _evt_run++;
  Ntrack = Nesrh = 0; 

  // Get ES rechits
  //edm::Handle<EcalRecHitCollection> PreshowerRecHits;
  edm::Handle<ESRecHitCollection> PreshowerRecHits;
  	evt.getByToken( esRecHitLabel_, PreshowerRecHits );

  Nesrh=PreshowerRecHits->size();
  cout << " number of ES Hits " << Nesrh << endl;

  // Get reco Tracks 
  edm::Handle<reco::TrackCollection>   TrackCol;
  	evt.getByToken( generalTracksLabel_, TrackCol );

  for(reco::TrackCollection::const_iterator itTrack = TrackCol->begin();
      itTrack != TrackCol->end(); ++itTrack)
  {
	/*cout<<endl;
	cout<<"charge !=0 "<<itTrack->charge()<<endl;
	cout<<"_TrackPt > 1. "<<itTrack->pt()<<endl;
	cout<<"fabs(itTrack->outerZ()) > 260 "<<fabs(itTrack->outerZ())<<endl;
	cout<<"fabs(itTrack->outerZ()) < 280 "<<fabs(itTrack->outerZ())<<endl;
	cout<<"fabs(_TrackEta[Ntrack]) > 1.7 "<<fabs(itTrack->eta())<<endl;
	cout<<"fabs(_TrackEta[Ntrack]) < 2.3 "<<fabs(itTrack->eta())<<endl;
	cout<<"_TrackNHit[Ntrack] >= 10 "<<itTrack->numberOfValidHits()<<endl;
	cout<<"((_TrackQuality[Ntrack])%8) >= 4 "<<(itTrack->qualityMask())%8<<endl;
	cout<<"quality "<<itTrack->quality(reco::TrackBase::qualityByName("highPurity"))<<endl;
	*/
    if ( itTrack->charge()!=0 )
    {
     if( itTrack->pt()>1.
        && fabs(itTrack->outerZ())>260&&fabs(itTrack->outerZ())<280
        && fabs(itTrack->eta())<2.3&&fabs(itTrack->eta())>1.7
        && itTrack->numberOfValidHits()>=10
        && itTrack->quality(reco::TrackBase::qualityByName("highPurity"))
        //&&((_TrackQuality[Ntrack])%8)>=4
       ){ Ntrack++; }//end if TrackPt>1
       //){ Ntrack++; break; }//end if TrackPt>1
    }//charge!=0
  }
  cout << " number of good tracks " << Ntrack << "/"<< TrackCol->size() << endl;

  if( Nesrh>0 && Ntrack>0 ){ 
	_restEvt++;  
  	return true;  
  }else{
	return false;
  }	
}

// ------------ method called once each job just before starting event loop  ------------
void
ESHitSkimLoose::beginJob()
{
 std::cout<<"In ESHitSkimLoose.beginJob\n";
}

// ------------ method called once each job just after ending the event loop  ------------
void
ESHitSkimLoose::endJob() {
  std::cout<<"In ESHitSkimLoose.endJob\n";
  cout << endl;
  cout << " --------------------------------------------- " << endl;
  cout << " number of events processed  " << _evt_run << endl; 
  cout << " Last Event number # " << _evtNum << endl; 
  cout << " Skimed Event number # " << _restEvt << endl; 
  cout << " --------------------------------------------- " << endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(ESHitSkimLoose);
