import FWCore.ParameterSet.Config as cms

ESTracksReducer = cms.EDProducer("ESTracksReducer",
                     generalTracksLabel      = cms.InputTag("generalTracks"),
                     generalTracksExtraLabel = cms.InputTag("generalTracks"),
		     trackingHitsLabel 	     = cms.InputTag("generalTracks"),
                     redGeneralTrackCollection 	    = cms.string(''), 	# be endcap GeneralTracks 
                     redGeneralTrackExtraCollection = cms.string(''), 	# be endcap GeneralTrackExtras
                     redTrackingRecHitCollection    = cms.string(''), 	# be endcap TrackingRecHit
                  )
